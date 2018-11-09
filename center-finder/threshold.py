import sys
import math
import numpy as np
import cv2

np.set_printoptions(suppress=True)

def abs_threshold(X, l):
    return np.sum(abs(X - l)) / X.size

def square_threshold(X, l):
    return np.sum((X - l) ** 2) / X.size

def log_threshold(X, l):
    X = (X - l)
    X = X ** 2
    X = X + 1
    X = np.log(X)
    s = X.sum(dtype=np.float64)
    return s / X.size
    

image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

if sys.argv[2] == 'min':
    print(image.min())
elif sys.argv[2] == 'mean':
    print(image.mean())
elif sys.argv[2] == 'abs':
    values = np.empty(256)
    for i in range(0, values.size):
        values[i] = abs_threshold(image, i)
    print(min(values))
elif sys.argv[2] == 'square':
    values = np.empty(256)
    for i in range(0, values.size):
        values[i] = square_threshold(image, i)
    print(min(values))
elif sys.argv[2] == 'log':
    values = np.empty(256)
    for i in range(0, values.size):
        values[i] = log_threshold(image, i)
    print(min(values))

