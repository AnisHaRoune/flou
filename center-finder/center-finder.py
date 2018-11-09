import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import hyp0f1
from argparse import ArgumentParser

np.set_printoptions(suppress=True)


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
    if args.x0 is None:
        x0 = image.shape[1] / 2
    else:
        x0 = args.x0
    if args.y0 is None:
        y0 = image.shape[0] / 2
    else:
        y0 = args.y0
    if args.z0 is None:
        z0 = 0
    else:
        z0 = args.z0
    if args.sz is None:
        sz = 1
    else:
        sz = args.sz
    if args.a is None:
        a = 1
    else:
        a = args.a
    if args.b is None:
        b = 0
    else:
        b = args.b
    if args.c is None:
        c = 0
    else:
        c = args.c
    if args.d is None:
        d = 1
    else:
        d = args.d
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
    image_path = 'laser4.bmp'
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Y = image.flatten()

    X = np.empty([Y.size, 2])
    for i in range(Y.size):
        X[i, 0] = i % image.shape[1]
        X[i, 1] = int(i / image.shape[1])

    x0, y0, z0, sz, a, b, c, d = args_initial_values(image, args)
    equation = args_method(args)

    popt, pcov = curve_fit(equation, X, Y, p0=(x0, y0, z0, sz, a, b, c, d), bounds=(
        [0, 0, 0, 1, 0.01, 0, 0, 0.01], [image.shape[0] - 1, image.shape[1] - 1, np.inf, np.inf, 1, 1, 1, 1]))

    print(popt[0], popt[1])

    if args.debug:
        print(popt)
        result = equation(X, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7]).reshape(image.shape)

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


if __name__ == "__main__":
    main()
