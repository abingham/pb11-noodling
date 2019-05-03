import numpy
import _zivid

Application = _zivid.Application


class Camera(_zivid.Camera):
    def data(self):
        mv = super().data()
        arr = numpy.frombuffer(mv, dtype=numpy.uint8)
        return arr.reshape((10, 10))
