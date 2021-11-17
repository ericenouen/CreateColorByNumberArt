import matplotlib.pyplot as plt
from skimage import io, feature
import numpy as np
import math
from scipy import signal, ndimage
import Color
import cv2 as cv
# Detect the edges in a target image
def detectEdges(imgPath):
    origImg = io.imread(imgPath, as_gray=True)
    fIm = feature.canny(origImg)
    plt.imshow(fIm, cmap='gray')
    plt.show()

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

# # Calculate Gaussian masks
# sigma1 = 1.
# Gx, Gy = gaussDeriv2D(sigma1)
# # plt.imshow(np.array(Gx), cmap='gray')
# # plt.show()
# # plt.imshow(np.array(Gy), cmap='gray')
# # plt.show()

# # Apply masks to image to get magnitude of change
# origImg = io.imread("Images/banana.jpg", as_gray=True)
# gxIm = np.float64(ndimage.correlate(origImg, Gx, mode='nearest'))
# gyIm = np.float64(ndimage.correlate(origImg, Gy, mode='nearest'))
# magIm = np.hypot(gxIm, gyIm)
# magIm *= 255.0 / np.max(magIm)
# # plt.imshow(gxIm, cmap='gray')
# # plt.show()
# # plt.imshow(gyIm, cmap='gray')
# # plt.show()
# # plt.imshow(magIm, cmap='gray')
# # plt.show()

# # Threshold detections
# tIm = magIm > 25
# tIm = tIm.astype(np.uint8)
# plt.imshow(tIm, cmap='gray')
# plt.show()

# # Compute the superpixel colors and apply the detected edges on to the image.
# img = Color.detectColors("Images/banana.jpg")
# contours, hierarchy = cv.findContours(tIm,
#                             cv.RETR_LIST,
#                             cv.CHAIN_APPROX_NONE)
# cv.drawContours(img, contours, -1, (0,0,0), thickness = 2)

# plt.imshow(img)
# plt.show()