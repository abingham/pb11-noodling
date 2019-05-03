class BMP:
    """A proxy around the student-developed `Bitmap` class.

    This is intended to be somewhat robust against the various APIs that
    `Bitmap` will expose. For example, in some phases of the workshop
    `Bitmap.height` will be a method; in others, it'll be a property. These
    proxy provides a uniform API for using both APIs transparently.

    DON'T ABUSE THIS PROXY! In some cases we very much want to verify that the
    student has implemented a particular API. In that case, access the `bmp`
    attribute of the proxy and use it directly.

    """
    def __init__(self, bmp):
        self.bmp = bmp

    @property
    def h(self):
        try:
            return self.bmp.height()
        except TypeError:
            return self.bmp.height

    @h.setter
    def h(self, x):
        try:
            self.bmp.set_height(x)
        except AttributeError:
            self.bmp.height = x

    @property
    def w(self):
        try:
            return self.bmp.width()
        except TypeError:
            return self.bmp.width

    @w.setter
    def w(self, x):
        try:
            self.bmp.set_width(x)
        except AttributeError:
            self.bmp.width = x

    @property
    def bpp(self):
        try:
            return self.bmp.bytes_per_pixel()
        except TypeError:
            return self.bmp.bytes_per_pixel

    def __getitem__(self, idx):
        return self.bmp[idx]

    def __setitem__(self, idx, val):
        self.bmp[idx] = val

    def save_image(self, f):
        return self.bmp.save_image(f)

    @property
    def data(self):
        return self.bmp.data
