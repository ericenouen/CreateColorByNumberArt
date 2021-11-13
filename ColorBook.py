# Eric Enouen | Grant Zimpfer
# CSE 5524 - Final Project
# 11/13/2021

# Import statements
import Edge
import Color
# import numpy as np

"""
The goal of this project is to be able to create a printable color by number image based on any input image.
1. Detect the edges in the image
2. Detect a specified amount of superpixels in the image
3. Use an aggregation technique to reduce the amount of superpixels in the image by combining similar colors next to eachother
so that there are N-different colors where N can be selected by the user
4. Draw an image using the superpixel borders to draw out edges between different colors
5. Overlay the emboldened edges detected earlier as black
"""

# Edge.detectEdges("Images/smileyface.jpg")
# Edge.detectEdges("Images/banana.jpg")
Color.detectColors("Images/smileyface.jpg")
Color.detectColors("Images/banana.jpg")