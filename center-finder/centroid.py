import sys
import numpy
import cv2

image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
M = cv2.moments(image)
center = (M["m01"] / M["m00"], M["m10"] / M["m00"])
print(center)

if (len(sys.argv) >= 3) and (sys.argv[2] == "debug"):
    x = int(center[0])
    y = int(center[1])

    for i in range(0, image.shape[0]):
        image[i, y] = 0
    for i in range(0, image.shape[1]):
        image[x, i] = 0
    
    '''
    image[x, y] = 0
    image[x + 1, y] = 0
    image[x - 1, y] = 0
    image[x, y + 1] = 0
    image[x, y - 1] = 0
    '''
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
