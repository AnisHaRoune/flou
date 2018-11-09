import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import hyp0f1

np.set_printoptions(suppress=True)


def diffraction2D(X, x0, y0, z0, sz, a, b, c, d):
    T = np.array([[x0], [y0]])
    M = np.array([[a, b], [c, d]])
    D = np.empty(X.shape[0])
    for i, xy in enumerate(X):
        x, y = xy
        P = np.array([[x], [y]])
        Y = M @ (P - T)
        x = Y[0, 0]
        y = Y[1, 0]
        h = -1 / 4 * ((x ** 2) + (y ** 2))
        D[i] = min(255, (sz * (hyp0f1(2, h) ** 2)) + z0)
    return D


image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
Y = image.flatten()

X = np.empty(Y.shape[0], dtype='2i')
for j in range(0, image.shape[1]):
    for i in range(0, image.shape[0]):
        X[i + (j * image.shape[0])] = (j, i)

popt, pcov = curve_fit(diffraction2D, X, Y, p0=(image.shape[0] / 2, image.shape[1] / 2, 0, 511, 1, 0, 0, 1), bounds=(
    [0, 0, 0, 255, 0.1, 0, 0, 0.1], [image.shape[0] - 1, image.shape[1] - 1, 255, np.inf, 1, 1, 1, 1]))

print(popt)
diffraction = diffraction2D(X, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7]).reshape(
    image.shape)

plt.subplot(1, 3, 1)
img2 = plt.imshow(image)

plt.subplot(1, 3, 2)
img2 = plt.imshow(diffraction)

plt.subplot(1, 3, 3)
x = int(round(popt[0]))
y = int(round(popt[1]))
diffraction[x, y] = 0
diffraction[x - 1, y] = 0
diffraction[x + 1, y] = 0
diffraction[x, y - 1] = 0
diffraction[x, y + 1] = 0
plt.imshow(image)
plt.imshow(diffraction, cmap=plt.cm.gray, alpha=0.5)

plt.tight_layout()
plt.show()
