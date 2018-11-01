import sys
import numpy
import cv2

image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

if len(sys.argv) >= 3:
    t = int(sys.argv[2])
else:
    t = 0

if (len(sys.argv) >= 4):
    debug = sys.argv[3] == "debug"
else:
    debug = False

X = numpy.array([0, 0])
Y = 0
for (x, y), value in numpy.ndenumerate(image):
    pixel = max(image[x, y] - t, 0)
    X += numpy.array([x, y]) * pixel
    Y += pixel

center = X/Y
print(center)

if debug:
    x = int(center[0])
    y = int(center[1])
    image[x, y] = 0
    image[x + 1, y] = 0
    image[x - 1, y] = 0
    image[x, y + 1] = 0
    image[x, y - 1] = 0
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
