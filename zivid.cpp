#include <Python.h>

#include <iostream>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


namespace py=pybind11;

class Application {
public:
    Application() : data_(100, 3) {}

    unsigned char* data() {
        return data_.data();
    }   

    unsigned char const* begin() const {
        return data_.data();
    }

    unsigned char const* end() const {
        return data_.data() + data_.size();
    }

private:
    std::vector<unsigned char> data_;
};

class Camera {
public:
    Camera(Application& app) :
        app_ (app)
    {}

    unsigned char* data() {
        return app_.data();
    }

private:
    Application& app_;
};

py::object data(Camera& camera) {
    PyObject* mview = PyMemoryView_FromMemory(
        reinterpret_cast<char*>(camera.data()),
        100,
        PyBUF_WRITE);

    return py::reinterpret_steal<py::object>(mview);
}

PYBIND11_MODULE(_zivid, m) {
    m.doc() = "An attempt to duplicate Zivid's binding crash.";

    py::class_<Application>(
        m, "Application",
        "An application...")
        .def(py::init<>())

        // Keep Application alive as long as Iterator is alive
        .def("__iter__", [](const Application& a) { return py::make_iterator(a.begin(), a.end()); },
                         py::keep_alive<0, 1>())
        ;

    py::class_<Camera>(
        m, "Camera",
        "A camera...")

        // Keep Application alive as long as Camera is alive.
        .def(py::init<Application&>(),  py::keep_alive<1, 2>())
        .def("data", &data)
        ;
        // .def_property("height", &bitmap_image::height, &set_height)
        // .def_property("width", &bitmap_image::width, &set_width)
        // .def_property_readonly("bytes_per_pixel",
        //                      &bitmap_image::bytes_per_pixel,
        //                      "The number of bytes used for each pixel.")
        // .def("save_image", &bitmap_image::save_image)
        // .def("__getitem__", &get_pixel)
        // .def("__setitem__", &set_pixel)
        // .def_property_readonly("data", &data)
        // .def("row", &row)
        // ;
}