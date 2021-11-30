from skimage import io
import numpy as np
import math
from scipy import ndimage
import cv2 as cv

# Compute the gaussian derivative in the x and y directions for the given sigma value.
def gaussDeriv2D(sigma):
    Gx = []
    Gy = []
    xrange = np.array([*range(int(-np.ceil(3*sigma)), int(np.ceil(3*sigma))+1)])
    yrange = np.array([*range(int(-np.ceil(3*sigma)), int(np.ceil(3*sigma))+1)])
    for y in yrange:
        constantX = (xrange / (2. * math.pi * np.power(sigma, 4)))
        constantY = (y / (2. * math.pi * np.power(sigma, 4)))
        exponent = np.exp(-(np.power(xrange, 2) + np.power(y, 2)) / (2 * np.power(sigma, 2)))
        Gx.append(constantX * exponent)
        Gy.append(constantY * exponent)
    return Gx, Gy

def calculateContours(imgPath, edgeThresh):
    # Calculate Gaussian masks
    sigma1 = 1.
    Gx, Gy = gaussDeriv2D(sigma1)

    # Apply masks to image to get magnitude of change
    origImg = io.imread(imgPath, as_gray=True)
    gxIm = np.float64(ndimage.correlate(origImg, Gx, mode='nearest'))
    gyIm = np.float64(ndimage.correlate(origImg, Gy, mode='nearest'))
    magIm = np.hypot(gxIm, gyIm)
    magIm *= 255.0 / np.max(magIm)

    # Threshold detections
    tIm = magIm > edgeThresh # 50 is default
    tIm = tIm.astype(np.uint8)

    # Use border following to calculate edges from the binary image
    contours, hierarchy = cv.findContours(tIm,
                                cv.RETR_LIST,
                                cv.CHAIN_APPROX_NONE)
    return contours

# Draw edges on the image
def drawContour(img, contours):
    img = cv.drawContours(img, contours, -1, (0,0,0), thickness = 2)
    return img