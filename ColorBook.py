# Eric Enouen | Grant Zimpfer
# CSE 5524 - Final Project
# 11/13/2021

# Import statements
import Edge
import Color
from skimage import io
import numpy as np

"""
The goal of this project is to be able to create a printable color by number image based on any input image.
1. Detect the edges in the image using gaussian derivative masks and a threshold.
2. Detect a specified amount of superpixels in the image using skimage's superpixel detection algorithm.
3. Use an aggregation technique to reduce the amount of superpixels in the image by combining similar colors into the same color
4. Draw an image using the superpixel borders to draw out edges between different colors.
5. Label each superpixel segment with its corresponding index and add a key at the bottom of the paper.
6. Overlay the emboldened edges detected earlier as black edges to give the image more detail.
7. Possibly add tunable thresholds to control how strong the edges are and how strong the colors are?
"""

def generateColorByNumberArt(imgPath, outputPath, edgeThresh, pixelNum, colorThresh, versionNumber):
    contours = Edge.calculateContours(imgPath, edgeThresh)
    img, keyIm, filled = Color.detectColors(imgPath, pixelNum, colorThresh)

    img = Edge.drawContour(img, contours)
    filled = Edge.drawContour(filled, contours)

    io.imsave(outputPath.split('.')[0] + "_output" + str(versionNumber) + ".jpg", (255 * img).astype(np.uint8))
    io.imsave(outputPath.split('.')[0] + "_key" + str(versionNumber) + ".jpg", keyIm.astype(np.uint8))
    io.imsave(outputPath.split('.')[0] + "_filled" + str(versionNumber) + ".jpg", (255 * filled).astype(np.uint8))
# Car takes like two minutes, use smaller images

# Printing out a key for each color
# Try to implement visualization dashboard with Bokeh to add sliders for edges, # superpixels, # colors
# Add some method to save/print the image and key

# Try to fix the numbers to print in a more visually appealing way
# Gather more test images and then run the algorithm to get examples

# Look into issues, things we would want to improve

# Finish Presentation Slides
# Finish Project Report