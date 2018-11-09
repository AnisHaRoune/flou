import cv2
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from scipy.optimize import curve_fit
from scipy.special import hyp0f1
from argparse import ArgumentParser

np.set_printoptions(suppress=True)


class METHODS(Enum):
    MEAN = 'mean'
    CIRCLE = 'circle'
    DIFFRACTION = 'diffraction'
    SINC = 'sinc'


class THRESHOLD_METHODS(Enum):
    MIN = 'min'
    MEAN = 'mean'
    ABS = 'abs'
    SQUARE = 'square'
    LOG = 'log'


def center_finder_curve_fitting(image, equation, p0, bounds, debug=False):
    Y = image.flatten()
    X = np.empty([Y.size, 2])
    for i in range(Y.size):
        X[i, 0] = i % image.shape[1]
        X[i, 1] = int(i / image.shape[1])

    popt, pcov = curve_fit(equation, X, Y, p0=p0, bounds=bounds)

    if debug:
        print(popt)
        result = equation(X, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7]).reshape(
            image.shape)

        plt.subplot(1, 3, 1)
        plt.imshow(image)

        plt.subplot(1, 3, 2)
        plt.imshow(result)

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

    return popt[0], popt[1]


def center_finder_diffraction(image, z0, debug=False):
    y0, x0 = center_finder_mean(image, z0, False)
    p0 = (x0, y0, z0, 2 ** 10, 0.5, 0, 0, 0.5)
    bounds = ([0, 0, 0, 1, 0.45, 0, 0, 0.45], [image.shape[0] - 1, image.shape[1] - 1, np.inf, np.inf, 1, 0.1, 0.1, 1])
    return center_finder_curve_fitting(image, diffraction_equation_transformed, p0, bounds, debug)


def center_finder_circle(image, z0, debug=False):
    y0, x0 = center_finder_mean(image, z0, False)
    p0 = (x0, y0, z0, 1, 0.5, 0, 0, 0.5)
    bounds = ([0, 0, 0, 1, 0.45, 0, 0, 0.45], [image.shape[0] - 1, image.shape[1] - 1, np.inf, np.inf, 1, 0.1, 0.1, 1])
    return center_finder_curve_fitting(image, circle_equation_transformed, p0, bounds, debug)


def center_finder_mean(image, z0, debug=False):
    X = np.array([0, 0], dtype=np.float)
    Y = 0
    for (x, y), value in np.ndenumerate(image):
        pixel = max(image[x, y] - z0, 0)
        X += np.array([x, y]) * pixel
        Y += pixel
    center = X / Y

    if debug:
        x = int(round(center[0]))
        y = int(round(center[1]))
        image[x, y] = 0
        image[x - 1, y] = 0
        image[x + 1, y] = 0
        image[x, y - 1] = 0
        image[x, y + 1] = 0

        plt.imshow(image)
        plt.show()

    return center[0], center[1]


def threshold(image, args):
    if args.threshold_method == THRESHOLD_METHODS.MIN.value:
        return min_threshold(image)
    elif args.threshold_method == THRESHOLD_METHODS.MEAN.value:
        return mean_threshold(image)
    elif args.threshold_method == THRESHOLD_METHODS.SQUARE.value:
        return square_threshold(image)
    elif args.threshold_method == THRESHOLD_METHODS.ABS.value:
        return abs_threshold(image)
    elif args.threshold_method == THRESHOLD_METHODS.LOG.value:
        return log_threshold(image)
    elif args.z0 is not None:
        return args.z0
    else:
        return 0


def min_threshold(x):
    return x.min()


def mean_threshold(x):
    return x.mean()


def abs_threshold(x):
    values = np.empty(256)
    for i in range(values.size):
        values[i] = np.sum(abs(x - i)) / x.size
    return np.min(values)


def square_threshold(x):
    values = np.empty(256)
    for i in range(values.size):
        values[i] = np.sum((x - i) ** 2) / x.size
    return np.min(values)


def log_threshold(x):
    values = np.empty(256)
    for i in range(values.size):
        values[i] = np.log(((x - i) ** 2) + 1).sum(dtype=np.float64) / x.size
    return np.min(values)


def transform(x, x0, y0, a, b, c, d):
    x = ([[a, b], [c, d]] @ (x.T - [[x0], [y0]])).T
    return np.sqrt(np.sum(x * x, 1))


def circle_equation_transformed(x, x0, y0, z0, sz, a, b, c, d):
    y = transform(x, x0, y0, a, b, c, d)
    return np.clip((sz * -y) + z0, 0, 255)


def diffraction_equation_transformed(x, x0, y0, z0, sz, a, b, c, d):
    y = transform(x, x0, y0, a, b, c, d)
    return np.clip((sz * (hyp0f1(2, -1 / 4 * (y ** 2)) ** 2)) + z0, 0, 255)


def sinc_equation_transformed(x, x0, y0, z0, sz, a, b, c, d):
    y = transform(x, x0, y0, a, b, c, d)
    return np.clip((sz * y) + z0, 0, 255)


def main():
    parser = ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('method',
                        choices=[METHODS.MEAN.value, METHODS.CIRCLE.value, METHODS.DIFFRACTION.value])
    parser.add_argument('-threshold_method',
                        choices=[THRESHOLD_METHODS.MIN.value, THRESHOLD_METHODS.MEAN.value, THRESHOLD_METHODS.ABS.value,
                                 THRESHOLD_METHODS.SQUARE.value, THRESHOLD_METHODS.LOG.value])
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()

    image_path = args.filepath
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    z0 = threshold(image, args)

    if args.method == METHODS.MEAN.value:
        x, y = center_finder_mean(image, z0, args.debug)
    elif args.method == METHODS.DIFFRACTION.value:
        x, y = center_finder_diffraction(image, z0, args.debug)
    elif args.method == METHODS.CIRCLE.value:
        x, y = center_finder_circle(image, z0, args.debug)
    elif args.method == METHODS.SINC.value:
        todo = 0

    print(x, y)


if __name__ == "__main__":
    main()
