from itertools import islice
import zivid

app = zivid.Application()
camera = zivid.Camera(app)

# iteration
for datum in islice(app, 10):
    print(datum)

# We delete the app to give Python a chance to garbage collect it. When that
# happens, setting camera data should cause a segfault...unless we establish the
# correct lifetime relationship between the app and the camera.
del app

print(camera.data())
camera.data()[3] = 42