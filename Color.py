import matplotlib.pyplot as plt
from skimage import io, feature
from skimage.segmentation import slic, mark_boundaries
import numpy as np
from skimage.color import rgb2hsv
import Edge
from scipy import signal, ndimage
import cv2 as cv

# Run the superpixel algorithm on a target image
def detectColors(imgPath):
    # https://scikit-image.org/docs/dev/api/skimage.segmentation.html?highlight=slic#skimage.segmentation.slic
    # https://github.com/scikit-image/scikit-image/blob/main/skimage/segmentation/slic_superpixels.py#L110-L384
    img = io.imread(imgPath).astype(float) / 255.
    segments_slic = slic(img,
                        n_segments = 1000, # The number of labels in the output
                        compactness = .01, # How much weight to give to space proximity
                        max_iter = 100, # Max number of k-means iterations
                        sigma = .5, # Amount of gaussian smoothing
                        spacing = None, # Voxel spacing along each dimension
                        multichannel = True, # Treat as multiple channels
                        convert2lab = False, # Convert to Lab colorspace before
                        enforce_connectivity = True, # Connect generated segments
                        min_size_factor = 0.5, # Min. segment size to remove
                        max_size_factor = 3, # Max segment size
                        slic_zero = False, # Zero parameter version
                        start_label = 0, # First index
                        mask = None) # Where to compute superpixels
    listColors = matchColors(img, segments_slic)
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(mark_boundaries(img, segments_slic))
    plt.show()
    getNcolors(img, listColors, 5)
    row, col = np.shape(segments_slic)
    for i in range(row):
        for j in range(col):
            img[i][j] = listColors[segments_slic[i][j]]

    plt.imshow(img)
    plt.show()
    # Calculate Gaussian masks
    sigma1 = 1.
    Gx, Gy = Edge.gaussDeriv2D(sigma1)

    # Apply masks to image to get magnitude of change
    origImg = io.imread(imgPath, as_gray=True)
    gxIm = np.float64(ndimage.correlate(origImg, Gx, mode='nearest'))
    gyIm = np.float64(ndimage.correlate(origImg, Gy, mode='nearest'))
    magIm = np.hypot(gxIm, gyIm)
    magIm *= 255.0 / np.max(magIm)

    # Threshold detections
    tIm = magIm > 25
    tIm = tIm.astype(np.uint8)
    contours, hierarchy = cv.findContours(tIm,
                                cv.RETR_LIST,
                                cv.CHAIN_APPROX_NONE)
    cv.drawContours(img, contours, -1, (0,0,0), thickness = 2)
    plt.imshow(img)
    plt.show()
    return img

# Set the color of each pixel to the average of its segment
def matchColors(img, segments_slic):
    listColors = np.zeros([np.amax(segments_slic)+1, 3]) # The average RGB value in each segment
    numPixels = np.zeros([np.amax(segments_slic)+1, 1]) # The number of pixels in each segment
    row, col = np.shape(segments_slic)

    # Calculate average RGB values
    for i in range(row):
        for j in range(col):
            listColors[segments_slic[i][j]] += img[i][j]
            numPixels[segments_slic[i][j]] += 1
    listColors /= numPixels

    # Apply the average values to each pixel in the target image
    for i in range(row):
        for j in range(col):
            img[i][j] = listColors[segments_slic[i][j]]
    return listColors

def getNcolors(img, listColors, n):
    # Use connected components ideas applied to color images?
    # Use a flood fill algorithm somehow?
    # Measure the distances between all of the pixels and iteratively merge
    # the closest ones until the select number is acquired?
    for i in range(len(listColors)):
        for j in range(len(listColors)):
            if euclideanColorDist(listColors[i], listColors[j]) < .2:
                listColors[j] = listColors[i]

    # Could probably have a conversation with Dr. Barker about this

def euclideanColorDist(color1, color2):
    return np.sqrt(np.power(color1[0] - color2[0], 2) + 
           np.power(color1[1] - color2[1], 2) + 
           np.power(color1[2] - color2[2], 2))
           