#include <Python.h>
#include <sstream>
#include <tuple>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include <bitmap_image.hpp>

#include <string>

namespace py=pybind11;

typedef std::tuple<int, int> Index;
typedef std::tuple<unsigned char, unsigned char, unsigned char> Pixel;
typedef std::vector<Pixel> Row;

PYBIND11_MAKE_OPAQUE(Row);

void print_metadata(const std::string& filename)
{
    bitmap_image bmp(filename);
    std::cout
        << bmp.height() << "\n"
        << bmp.width() << "\n"
        << bmp.bytes_per_pixel() << std::endl;
}


void set_width(bitmap_image& bmp, const int width) {
    if (width < 0) {
        throw py::value_error(
            "Width cannot be negative");
    }

    bmp.setwidth_height(width, bmp.height());
}

void set_height(bitmap_image& bmp, const int height) {
    if (height < 0) {
        throw py::value_error(
            "Height cannot be negative");
    }

    bmp.setwidth_height(bmp.width(), height);
}

Index normalize_index(const bitmap_image& bmp, const Index& idx) {
    auto sx = std::get<0>(idx);
    auto sy = std::get<1>(idx);

    auto x = (sx < 0) ? bmp.width() + sx : sx;
    auto y = (sy < 0) ? bmp.height() + sy : sy;

    if (x >= bmp.width()) {
        std::stringstream ss;
        ss << "x coordinate (" << sx << ") is out of bounds (" << bmp.width() << ")";
        throw py::index_error(ss.str());
    }

    if (y >= bmp.height()) {
        std::stringstream ss;
        ss << "y coordinate (" << sy << ") is out of bounds (" << bmp.height() << ")";
        throw py::index_error(ss.str());
    }
    return {x, y};
}

Pixel get_pixel(const bitmap_image& bmp, const Index& idx) {
    auto normalized = normalize_index(bmp, idx);

    Pixel pixel;
    bmp.get_pixel(
        std::get<0>(normalized),
        std::get<1>(normalized),
        std::get<0>(pixel),
        std::get<1>(pixel),
        std::get<2>(pixel));
    return pixel;
}

void check_rgb(const Pixel& rgb) {
    if ((std::get<0>(rgb) > 255)
        || (std::get<1>(rgb) > 255)
        || (std::get<2>(rgb) > 255)) {
        throw py::value_error(
            "RGB value must be between 0 and 255");
    }
}

void set_pixel(bitmap_image& bmp, const Index& idx, const Pixel& pixel) {
    auto normalized = normalize_index(bmp, idx);

    check_rgb(pixel);

    bmp.set_pixel(
        std::get<0>(normalized),
        std::get<1>(normalized),
        std::get<0>(pixel),
        std::get<1>(pixel),
        std::get<2>(pixel));
}

py::object data(bitmap_image& bmp) {
    PyObject* mview = PyMemoryView_FromMemory(
        reinterpret_cast<char*>(bmp.data()),
        bmp.height() * bmp.width() * bmp.bytes_per_pixel(),
        PyBUF_WRITE);

    return py::reinterpret_steal<py::object>(mview);
}

bitmap_image random_bitmap(int width, int height) {
    bitmap_image bmp;
    bmp.setwidth_height(width, height);

    py::object random = py::module::import("random");
    py::object randint = random.attr("randint");

    for (int x = 0; x < width; ++x) {
        for (int y = 0; y < height; ++y) {
            bmp.set_pixel(
                x, y,
                randint(0, 255).cast<unsigned char>(),
                randint(0, 255).cast<unsigned char>(),
                randint(0, 255).cast<unsigned char>());
        }
    }

    return bmp;
}

Row row(const bitmap_image& bmp, int row) {
    Row r;
    for (unsigned int x = 0; x < bmp.width(); ++x) {
        r.push_back(get_pixel(bmp, {x, row}));
    }
    return r;
}

PYBIND11_MODULE(bitmap, m) {
    py::bind_vector<Row>(m, "Row");

    m.doc() = "A module for working with bitmap images.";

    m.def("print_metadata", &print_metadata,
         "print a bitmap's metadata");
    m.def("random_bitmap", &random_bitmap);

    py::class_<bitmap_image>(
        m, "Bitmap",
        "A class to reate, inspect, modify, and save bitmap images.")
        .def(py::init<const std::string&>())
        .def(py::init<>())
        .def_property("height", &bitmap_image::height, &set_height)
        .def_property("width", &bitmap_image::width, &set_width)
        .def_property_readonly("bytes_per_pixel",
                             &bitmap_image::bytes_per_pixel,
                             "The number of bytes used for each pixel.")
        .def("save_image", &bitmap_image::save_image)
        .def("__getitem__", &get_pixel)
        .def("__setitem__", &set_pixel)
        .def_property_readonly("data", &data)
        .def("row", &row)
        ;
}
