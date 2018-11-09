import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

np.set_printoptions(suppress=True)


def transform(x, x0, y0, a, b, c, d):
    x = ([[a, b], [c, d]] @ (x.T - [[x0], [y0]])).T
    return np.sqrt(np.sum(x * x, 1))


def circle_equation_transformed(x, x0, y0, z0, sz, a, b, c, d):
    y = transform(x, x0, y0, a, b, c, d)
    return np.clip((sz * -y) + z0, 0, 255)


image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
Y = image.flatten()

X = np.empty([Y.size, 2])
for i in range(Y.size):
    X[i, 0] = i % image.shape[1]
    X[i, 1] = int(i / image.shape[1])

kernel = circle_equation_transformed
popt, pcov = curve_fit(kernel, X, Y, p0=(image.shape[0] / 2, image.shape[1] / 2, 255, 1, 1, 0, 0, 1), bounds=(
    [0, 0, 0, 1, 0.1, 0, 0, 0.1], [image.shape[0] - 1, image.shape[1] - 1, np.inf, np.inf, 1, 1, 1, 1]))

print(popt)
result = kernel(X, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7]).reshape(image.shape)

plt.subplot(1, 3, 1)
img2 = plt.imshow(image)

plt.subplot(1, 3, 2)
img2 = plt.imshow(result)

plt.subplot(1, 3, 3)
x = int(round(popt[0]))
y = int(round(popt[1]))
result[y, x] = 0
result[y - 1, x] = 0
result[y + 1, x] = 0
result[y, x - 1] = 0
result[y, x + 1] = 0
plt.imshow(image)
plt.imshow(result, cmap=plt.cm.gray, alpha=0.5)

plt.tight_layout()
plt.show()
