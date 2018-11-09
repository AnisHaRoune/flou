import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import hyp0f1
from argparse import ArgumentParser

np.set_printoptions(suppress=True)


def center_finder_curve_fitting(image, args):
    x0, y0, z0, sz, a, b, c, d = args_initial_values(image, args)

    Y = image.flatten()
    X = np.empty([Y.size, 2])
    for i in range(Y.size):
        X[i, 0] = i % image.shape[1]
        X[i, 1] = int(i / image.shape[1])

    equation = args_method(args)

    popt, pcov = curve_fit(equation, X, Y, p0=(x0, y0, z0, sz, a, b, c, d), bounds=(
        [0, 0, 0, 1, 0.01, 0, 0, 0.01], [image.shape[0] - 1, image.shape[1] - 1, np.inf, np.inf, 1, 1, 1, 1]))
    print(popt[0], popt[1])

    if args.debug:
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


def center_finder_mean(image, args):
    x0, y0, z0, sz, a, b, c, d = args_initial_values(image, args)

    X = np.array([0, 0], dtype=np.float)
    Y = 0
    for (x, y), value in np.ndenumerate(image):
        pixel = max(image[x, y] - z0, 0)
        X += np.array([x, y]) * pixel
        Y += pixel
    center = X / Y
    print(center[0], center[1])

    if args.debug:
        x = int(round(center[0]))
        y = int(round(center[1]))
        image[x, y] = 0
        image[x - 1, y] = 0
        image[x + 1, y] = 0
        image[x, y - 1] = 0
        image[x, y + 1] = 0

        plt.imshow(image)
        plt.show()


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


def args_initial_values(image, args):
    if args.x0 is not None:
        x0 = args.x0
    else:
        x0 = image.shape[1] / 2

    if args.y0 is not None:
        y0 = args.y0
    else:
        y0 = image.shape[0] / 2

    if args.threshold_method == 'min':
        z0 = min_threshold(image)
    elif args.threshold_method == 'mean':
        z0 = mean_threshold(image)
    elif args.threshold_method == 'square':
        z0 = square_threshold(image)
    elif args.threshold_method == 'abs':
        z0 = abs_threshold(image)
    elif args.threshold_method == 'log':
        z0 = log_threshold(image)
    elif args.z0 is not None:
        z0 = args.z0
    else:
        z0 = 0

    if args.sz is not None:
        sz = args.sz
    else:
        sz = 1

    if args.a is not None:
        a = args.a
    else:
        a = 1

    if args.b is not None:
        b = args.b
    else:
        b = 0

    if args.c is not None:
        c = args.c
    else:
        c = 0

    if args.d is not None:
        d = args.d
    else:
        d = 1

    return x0, y0, z0, sz, a, b, c, d


def args_method(args):
    if args.method == 'circle':
        kernel = circle_equation_transformed
    elif args.method == 'diffraction':
        kernel = diffraction_equation_transformed
    return kernel


def main():
    parser = ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('method')
    parser.add_argument('-threshold_method')
    parser.add_argument('-x0', type=float)
    parser.add_argument('-y0', type=float)
    parser.add_argument('-z0', type=float)
    parser.add_argument('-sz', type=float)
    parser.add_argument('-a', type=float)
    parser.add_argument('-b', type=float)
    parser.add_argument('-c', type=float)
    parser.add_argument('-d', type=float)
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()

    image_path = args.filepath
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if args.method == 'mean':
        center_finder_mean(image, args)
    else:
        center_finder_curve_fitting(image, args)


if __name__ == "__main__":
    main()
