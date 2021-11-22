# Eric Enouen | Grant Zimpfer
# CSE 5524 - Final Project
# 11/13/2021

# Import statements
import Edge
import Color

"""
The goal of this project is to be able to create a printable color by number image based on any input image.
1. Detect the edges in the image using gaussian derivative masks and a threshold.
2. Detect a specified amount of superpixels in the image using skimage's superpixel detection algorithm.
3. Use an aggregation technique to reduce the amount of superpixels in the image by combining similar colors next to eachother
so that there are N-different colors where N can be selected by the user. Hard, not sure how to do.
4. Draw an image using the superpixel borders to draw out edges between different colors.
5. Label each superpixel segment with its corresponding index and add a key at the bottom of the paper.
6. Overlay the emboldened edges detected earlier as black edges to give the image more detail.
7. Possibly add tunable thresholds to control how strong the edges are and how strong the colors are?
"""

def generateColorByNumberArt(imgPath):
    contours = Edge.calculateContours(imgPath)
    img = Color.detectColors(imgPath)
    Edge.drawContour(img, contours)

generateColorByNumberArt("Images/spiderman.jpg")