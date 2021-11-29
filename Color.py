import matplotlib.pyplot as plt
from skimage import io
from skimage.segmentation import slic, mark_boundaries
import numpy as np
# from skimage.color import rgb2hsv
# from scipy import signal, ndimage
import cv2 as cv

# Run the superpixel algorithm on a target image
def detectColors(imgPath, pixelNum, colorThresh):
    # https://scikit-image.org/docs/dev/api/skimage.segmentation.html?highlight=slic#skimage.segmentation.slic
    # https://github.com/scikit-image/scikit-image/blob/main/skimage/segmentation/slic_superpixels.py#L110-L384
    img = np.array(io.imread(imgPath).astype(float) / 255.)
    segments_slic = slic(img,
                        n_segments = pixelNum, # The number of labels in the output
                        compactness = .1, # How much weight to give to space proximity
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
    # fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1])
    # ax.imshow(mark_boundaries(img, segments_slic))
    # plt.show()

    uniqueListColors, listColors = getColors(listColors, colorThresh)
    intUnique = (uniqueListColors * 255).astype(int)
    intColor = (listColors*255).astype(int)
    row, col = np.shape(segments_slic)
    for i in range(row):
        for j in range(col):
            compareValue = intColor[segments_slic[i][j]]
            k = np.argmax(compareValue == intUnique, axis = 0)[0]
            segments_slic[i][j] = k
            img[i][j] = uniqueListColors[k]

    # plt.imshow(img)
    # plt.show()
    img = mark_boundaries(np.ones(np.shape(img)), segments_slic, color=(0,0,0))
    # img = mark_boundaries(img, segments_slic, color=(0,0,0))

    # Super botched fix for labeling regions
    i, j = 25, 25
    while i < row:
        while j < col:
            cv.putText(img, str(segments_slic[i][j] + 1), (j-5, i+5), cv.FONT_HERSHEY_SIMPLEX, .5, (.5,.5,.5))
            # cv.circle(img, (i,j), radius=0, color=(0, 0, 1), thickness=-1) # Used to determine center of text
            j += 24
        j = 0
        i += 24

    # Need to display numbers on each region which will be pretty difficult
    # Can try https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.center_of_mass.html
    # to find the center of each region?

    # Could loop through and draw a number every time the value changes?
    
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

# Combine colors and regions based off euclidean color distance
def getColors(listColors, colorThresh):
    for i in range(len(listColors)):
        for j in range(len(listColors)):
            if euclideanColorDist(listColors[i], listColors[j]) < colorThresh: # Default .2
                listColors[j] = listColors[i]
    return np.unique(listColors, axis=0), listColors

# Compute the euclidean distance between two colors
def euclideanColorDist(color1, color2):
    return np.sqrt(np.power(color1[0] - color2[0], 2) + 
           np.power(color1[1] - color2[1], 2) + 
           np.power(color1[2] - color2[2], 2))
