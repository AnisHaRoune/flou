import cv2
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from scipy.optimize import curve_fit
from scipy.special import hyp0f1
from argparse import ArgumentParser

np.set_printoptions(suppress=True)


class METHODS(Enum):
    CENTROID = 'centroid'
    CIRCLE = 'circle'
    DIFFRACTION = 'diffraction'
    SINC = 'sinc'
    INVERTED_SQUARE = 'isquare'
    EULER = 'euler'


class ThresholdMethods(Enum):
    MIN = 'min'
    MEAN = 'mean'
    MEDIAN = 'median'
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
        draw_crosshair(image, popt[0], popt[1])
        plt.imshow(image)
        plt.imshow(result, cmap=plt.cm.gray, alpha=0.5)

        plt.tight_layout()
        plt.show()

    return popt[0], popt[1]


def center_finder_diffraction(image, debug=False):
    x0, y0 = center_finder_centroid(image, False)
    p0 = (x0, y0, 0, 2 ** 10, 0.5, 0, 0, 0.5)
    bounds = ([0, 0, 0, 1, 0.45, 0, 0, 0.45], [image.shape[0] - 1, image.shape[1] - 1, np.inf, np.inf, 1, 0.5, 0.5, 1])
    return center_finder_curve_fitting(image, diffraction_equation_transformed, p0, bounds, debug)


def center_finder_circle(image, debug=False):
    x0, y0 = center_finder_centroid(image, False)
    p0 = (x0, y0, image.max(), 1, 0.5, 0, 0, 0.5)
    bounds = ([0, 0, 0, 1, 0.45, 0, 0, 0.45], [image.shape[0] - 1, image.shape[1] - 1, np.inf, np.inf, 1, 0.5, 0.5, 1])
    return center_finder_curve_fitting(image, circle_equation_transformed, p0, bounds, debug)


def center_finder_inverted_square(image, debug=False):
    x0, y0 = center_finder_centroid(image, False)
    p0 = (x0, y0, 0, 1, 0.5, 0, 0, 0.5)
    bounds = ([0, 0, 0, 1, 0.45, 0, 0, 0.45], [image.shape[0] - 1, image.shape[1] - 1, np.inf, np.inf, 1, 0.1, 0.1, 1])
    return center_finder_curve_fitting(image, inverted_square_equation_transformed, p0, bounds, debug)


def center_finder_euler(image, debug=False):
    x0, y0 = center_finder_centroid(image, False)
    p0 = (x0, y0, 0, image.max(), 1, 0, 0, 1)
    bounds = ([0, 0, 0, 1, 0.01, 0, 0, 0.01], [image.shape[0] - 1, image.shape[1] - 1, np.inf, np.inf, 1, 0.1, 0.1, 1])
    return center_finder_curve_fitting(image, euler_equation_transformed, p0, bounds, debug)


def center_finder_centroid(image, debug=False):
    M = cv2.moments(image)

    if M['m00'] == 0:
        x = image.shape[1] / 2
        y = image.shape[0] / 2
    else:
        x = M['m10'] / M['m00']
        y = M['m01'] / M['m00']

    if debug:
        draw_crosshair(image, x, y)
        plt.imshow(image)
        plt.show()

    return x, y


def threshold(image, args):
    if args.threshold_method == ThresholdMethods.MIN.value:
        return min_threshold(image)
    elif args.threshold_method == ThresholdMethods.MEAN.value:
        return mean_threshold(image)
    elif args.threshold_method == ThresholdMethods.MEDIAN.value:
        return median_threshold(image)
    elif args.threshold_method == ThresholdMethods.LOG.value:
        return log_threshold(image)
    elif args.z0 is not None:
        return args.z0
    else:
        return 0


def min_threshold(x):
    return np.min(x)


def mean_threshold(x):
    return np.mean(x)


def median_threshold(x):
    return np.median(x)


def log_threshold(x):
    x = x.astype(np.float64)
    values = np.empty(64)
    for i in range(values.size):
        values[i] = np.sum(np.log(((x - i) ** 2) + 1)) / x.size
    return np.argmin(values)


def transform(x, x0, y0, a, b, c, d):
    x = ([[a, b], [c, d]] @ (x.T - [[x0], [y0]])).T
    return np.sqrt(np.sum(x * x, 1))


def circle_equation_transformed(x, x0, y0, z0, sz, a, b, c, d):
    y = transform(x, x0, y0, a, b, c, d)
    return np.clip((sz * -y) + z0, 0, 255)


def diffraction_equation_transformed(x, x0, y0, z0, sz, a, b, c, d):
    y = transform(x, x0, y0, a, b, c, d)
    y = hyp0f1(2, -1 / 4 * (y ** 2)) ** 2
    return np.clip((sz * y) + z0, 0, 255)


def inverted_square_equation_transformed(x, x0, y0, z0, sz, a, b, c, d):
    y = transform(x, x0, y0, a, b, c, d)
    y = 1 / ((y ** 2) + 1)
    return np.clip((sz * y) + z0, 0, 255)


def euler_equation_transformed(x, x0, y0, z0, sz, a, b, c, d):
    y = transform(x, x0, y0, a, b, c, d)
    y = np.exp(-np.exp(1) * (y ** 2))
    return np.clip((sz * y) + z0, 0, 255)


def clean_image(args, image):
    z0 = threshold(image, args)
    x, y = center_finder_centroid(np.clip(image.astype(np.int16) - z0, 0, 255).astype(np.uint8), False)
    x = int(x)
    y = int(y)
    c = 64
    x0 = max(x - c, 0)
    x1 = min(x + c, image.shape[1])
    y0 = max(y - c, 0)
    y1 = min(y + c, image.shape[0])

    image = image[y0:y1, x0:x1]
    z0 = threshold(image, args)
    image = np.clip(image.astype(np.int16) - z0, 0, 255).astype(np.uint8)

    if args.debug:
        print(z0)

    return image, x0, y0, x1, y1


def draw_crosshair(image, x, y):
    cx = int(round(x))
    cy = int(round(y))
    for i in range(image.shape[1]):
        image[cy, i] = 127
    for i in range(image.shape[0]):
        image[i, cx] = 127


def main():
    parser = ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('method',
                        choices=[METHODS.CENTROID.value, METHODS.CIRCLE.value, METHODS.DIFFRACTION.value,
                                 METHODS.INVERTED_SQUARE.value, METHODS.EULER.value])
    parser.add_argument('--threshold_method', '-t',
                        choices=[ThresholdMethods.MIN.value, ThresholdMethods.MEAN.value, ThresholdMethods.MEDIAN.value,
                                 ThresholdMethods.LOG.value])
    parser.add_argument('--debug', '-d', action="store_true")
    args = parser.parse_args()

    image_path = args.filepath
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    cropped_image, x0, y0, x1, y1 = clean_image(args, image)

    if args.method == METHODS.CENTROID.value:
        x, y = center_finder_centroid(cropped_image, args.debug)
    elif args.method == METHODS.DIFFRACTION.value:
        x, y = center_finder_diffraction(cropped_image, args.debug)
    elif args.method == METHODS.CIRCLE.value:
        x, y = center_finder_circle(cropped_image, args.debug)
    elif args.method == METHODS.INVERTED_SQUARE.value:
        x, y = center_finder_inverted_square(cropped_image, args.debug)
    elif args.method == METHODS.EULER.value:
        x, y = center_finder_euler(cropped_image, args.debug)

    x += x0
    y += y0

    print("{},{}".format(x, y))

    if args.debug:
        draw_crosshair(image, x, y)
        plt.imshow(image)
        plt.show()


if __name__ == "__main__":
    main()
