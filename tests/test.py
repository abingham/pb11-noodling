import bitmap
from functools import partial
from operator import eq, gt, le
import pathlib
import pytest
import tempfile

from bmp_proxy import BMP


@pytest.fixture
def bmp():
    return BMP(bitmap.Bitmap('../data/mandel.bmp'))


@pytest.fixture
def tmpdir():
    with tempfile.TemporaryDirectory() as name:
        yield pathlib.Path(name)


@pytest.mark.for_exercise(partial(eq, (1, 'a')))
def test_bitmap_is_importable():
    import bitmap


@pytest.mark.for_exercise(partial(le, (1, 'b')))
def test_print_metadata_exists():
    assert hasattr(bitmap, 'print_metadata')


@pytest.mark.for_exercise(partial(le, (2, 'a')))
class Test02a:
    def test_bitmap_class_exists(self):
        assert hasattr(bitmap, 'Bitmap')

    def test_bitmap_is_instantiable(self):
        bitmap.Bitmap('../data/mandel.bmp')


@pytest.mark.for_exercise(partial(le, (2, 'b')))
@pytest.mark.for_exercise(partial(gt, (6, 'a')))
class Test02b:
    def test_height(self, bmp):
        assert bmp.bmp.height() == 800

    def test_width(self, bmp):
        assert bmp.bmp.width() == 1200

    def test_bytes_per_pixel(self, bmp):
        assert bmp.bmp.bytes_per_pixel() == 3


@pytest.mark.for_exercise(partial(le,  (3, 'a')))
def test_no_argument_constructor():
    bitmap.Bitmap()


@pytest.mark.for_exercise(partial(le,  (3, 'b')))
@pytest.mark.for_exercise(partial(gt, (6, 'b')))
class Test03b:
    def test_set_height(self, bmp):
        h = bmp.h
        h += 1
        bmp.bmp.set_height(h)
        assert bmp.h == h

    def test_set_width(self, bmp):
        w = bmp.w
        w += 1
        bmp.bmp.set_width(w)
        assert bmp.w == w


@pytest.mark.for_exercise(partial(le, (3, 'c')))
def test_save_file(bmp, tmpdir):
    fname = tmpdir / "test.bmp"
    assert not fname.exists()
    bmp.save_image(str(fname))
    assert fname.exists()
    assert fname.is_file()


@pytest.mark.for_exercise(partial(eq, (4, 'a')))
def test_get_pixel(bmp):
    bmp = bmp.bmp
    assert bmp.get_pixel((100, 100)) == (210, 255, 0)
    assert bmp.get_pixel((200, 200)) == (76, 255, 0)
    assert bmp.get_pixel((420, 799)) == (137, 255, 0)


@pytest.mark.for_exercise(partial(eq, (4, 'b')))
def test_set_pixel(bmp):
    bmp = bmp.bmp
    r, g, b = bmp.get_pixel((690, 203))
    pixel = (r + 1, g + 1, b + 1)
    bmp.set_pixel((690, 203), pixel)
    assert bmp.get_pixel((690, 203)) == pixel


@pytest.mark.for_exercise(partial(le, (4, 'c')))
class TestPixelIndexOperators:
    def test_get_pixel(self, bmp):
        assert bmp[100, 100] == (210, 255, 0)
        assert bmp[200, 200] == (76, 255, 0)
        assert bmp[420, 799] == (137, 255, 0)

    def test_set_pixel(self, bmp):
        r, g, b = bmp[690, 203]
        pixel = (r + 1, g + 1, b + 1)
        bmp[690, 203] = pixel
        assert bmp[690, 203] == pixel

    def test_negative_indexing_for_get_pixel(self, bmp):
        for x in range(1, bmp.w, 10):
            for y in range(1, bmp.h, 10):
                val = bmp[x, y]
                assert bmp[x - bmp.w, y] == val
                assert bmp[x, y - bmp.h] == val
                assert bmp[x - bmp.w, y - bmp.h] == val

    def test_negative_indexing_for_set_pixel(self, bmp):
        for x in range(1, bmp.w, 10):
            for y in range(1, bmp.h, 10):
                r, g, b = bmp[x, y]
                pixel = ((r + 1) % 255, (g + 1) % 255, (b + 1) % 255)

                bmp[x - bmp.w, y] = pixel
                assert bmp[x, y] == pixel

                pixel = ((r + 2) % 255, (g + 2) % 255, (b + 2) % 255)
                bmp[x, y - bmp.h] = pixel
                assert bmp[x, y] == pixel

                pixel = ((r + 3) % 255, (g + 3) % 255, (b + 3) % 255)
                bmp[x - bmp.w, y - bmp.h] = pixel
                assert bmp[x, y] == pixel


@pytest.mark.for_exercise(partial(le, (5, 'a')))
class Test5a:
    def test_getitem_throws_index_error_for_large_x(self, bmp):
        with pytest.raises(IndexError):
            bmp[bmp.w + 1, 0]

    def test_getitem_throws_index_error_for_large_y(self, bmp):
        with pytest.raises(IndexError):
            bmp[0, bmp.h + 1]

    def test_getitem_throws_index_error_for_large_negative_x(self, bmp):
        with pytest.raises(IndexError):
            bmp[bmp.w + 1, 0]

    def test_getitem_throws_index_error_for_large_negative_y(self, bmp):
        with pytest.raises(IndexError):
            bmp[0, bmp.h + 1]


@pytest.mark.for_exercise(partial(le, (5, 'b')))
class Test5b:
    def test_setitem_throws_index_error_for_large_x(self, bmp):
        with pytest.raises(IndexError):
            bmp[bmp.w + 1, 0] = (0, 0, 0)

    def test_setitem_throws_index_error_for_large_y(self, bmp):
        with pytest.raises(IndexError):
            bmp[0, bmp.h + 1] = (0, 0, 0)

    def test_setitem_throws_index_error_for_large_negative_x(self, bmp):
        with pytest.raises(IndexError):
            bmp[bmp.w + 1, 0] = (0, 0, 0)

    def test_setitem_throws_index_error_for_large_negative_y(self, bmp):
        with pytest.raises(IndexError):
            bmp[0, bmp.h + 1] = (0, 0, 0)


@pytest.mark.for_exercise(partial(le, (5, 'c')))
class Test5c:
    def test_set_height_throws_value_error_on_negative(self, bmp):
        with pytest.raises(ValueError):
            bmp.h = -1

    def test_set_width_throws_value_error_on_negative(self, bmp):
        with pytest.raises(ValueError):
            bmp.w = -1


@pytest.mark.for_exercise(partial(le, (6, 'a')))
def test_bytes_per_pixel_property(bmp):
    assert bmp.bmp.bytes_per_pixel == 3


@pytest.mark.for_exercise(partial(le, (6, 'b')))
class Test6b:
    def test_read_height_property(self, bmp):
        assert bmp.bmp.height == 800

    def test_set_height_property(self, bmp):
        bmp.bmp.height = 900
        assert bmp.h == 900


@pytest.mark.for_exercise(partial(le, (6, 'c')))
class Test6c:
    def test_read_width_property(self, bmp):
        assert bmp.bmp.width == 1200

    def test_set_width_property(self, bmp):
        bmp.bmp.width = 1300
        assert bmp.w == 1300


@pytest.mark.for_exercise(partial(le, (7, 'a')))
class Test7a:
    def test_raw_data_size(self, bmp):
        assert len(bmp.data) == bmp.h * bmp.w * bmp.bpp

    def test_raw_data_read(self, bmp):
        assert bmp.data[123] == 0
        assert bmp.data[112358] == 221
        assert bmp.data[314159] == 126

    def test_raw_data_write(self, bmp):
        val = bmp.data[1337]
        bmp.data[1337] = val + 1
        assert bmp.data[1337] == val + 1


@pytest.mark.for_exercise(partial(le, (9, 'a')))
class Test9a:
    def test_raw_data_size(self):
        bmp = bitmap.random_bitmap(100, 100)
        assert bmp.height == 100
        assert bmp.width == 100

        # Ensure that the data looks random...that it's no all zeros
        assert any(bmp[x, y] != (0, 0, 0)
                   for x in range(0, bmp.width, 10)
                   for y in range(0, bmp.height, 10))


class Test10:
    @pytest.mark.for_exercise(partial(le, (10, 'a')))
    def test_module_docstring(self):
        assert bitmap.__doc__ is not None

    @pytest.mark.for_exercise(partial(le, (10, 'b')))
    def test_class_docstring(self):
        assert bitmap.Bitmap.__doc__ is not None

    @pytest.mark.for_exercise(partial(le, (10, 'c')))
    def test_function_docstring(self):
        assert len(bitmap.print_metadata.__doc__.split('\n')) > 2

    @pytest.mark.for_exercise(partial(le, (10, 'd')))
    def test_method_docstring(self):
        assert bitmap.Bitmap.bytes_per_pixel.__doc__ != ''


@pytest.mark.for_exercise(partial(le, (11, 'b')))
class Test11b:
    def test_row_vector_is_correct(self, bmp):
        for x in range(bmp.bmp.width):
            bmp[x, 0] = (0, 0, 0)
        row = bmp.bmp.row(0)
        assert len(row) == bmp.w
        assert all(pixel == (0, 0, 0) for pixel in row)

    def test_row_raises_IndexError_for_large_indices(self, bmp):
        with pytest.raises(IndexError):
            bmp.bmp.row(bmp.h)

    def test_row_raises_IndexError_for_small_indices(self, bmp):
        with pytest.raises(IndexError):
            bmp.bmp.row(-1 * (bmp.h + 1))


@pytest.mark.for_exercise(partial(le, (11, 'c')))
def test_row_type_is_correct(bmp):
    r = bmp.bmp.row(0)
    assert type(r) is bitmap.Row
