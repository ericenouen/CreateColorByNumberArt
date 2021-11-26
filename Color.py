import matplotlib.pyplot as plt
from skimage import io, feature
from skimage.segmentation import slic, mark_boundaries
import numpy as np
from skimage.color import rgb2hsv
from scipy import signal, ndimage
import cv2 as cv

# Run the superpixel algorithm on a target image
def detectColors(imgPath):
    # https://scikit-image.org/docs/dev/api/skimage.segmentation.html?highlight=slic#skimage.segmentation.slic
    # https://github.com/scikit-image/scikit-image/blob/main/skimage/segmentation/slic_superpixels.py#L110-L384
    img = np.array(io.imread(imgPath).astype(float) / 255.)
    segments_slic = slic(img,
                        n_segments = 5000, # The number of labels in the output 5000
                        compactness = 1, # How much weight to give to space proximity
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
    ax.imshow(mark_boundaries(img, segments_slic, color=(0,0,0)))
    plt.show()
    uniqueListColors = getNcolors(img, listColors, segments_slic, 5)
    row, col = np.shape(segments_slic)
    for i in range(row):
        for j in range(col):
            img[i][j] = listColors[segments_slic[i][j]]
            for k in range(len(uniqueListColors)):
                if all(uniqueListColors[k] == listColors[segments_slic[i][j]]):
                    segments_slic[i][j] = k

    plt.imshow(img)
    plt.show()
    img = mark_boundaries(img, segments_slic, color= (0,0,0), outline_color=(0,0,0)) # np.ones(np.shape(img))
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
def getNcolors(img, listColors, segments_slic, n):
    for i in range(len(listColors)):
        for j in range(len(listColors)):
            if euclideanColorDist(listColors[i], listColors[j]) < .2:
                # boolIndex = segments_slic == j # np.take?
                # segments_slic[boolIndex] = i # This takes a very long time
                listColors[j] = listColors[i]
    return np.unique(listColors, axis=0)
    # for i in range(len(listColors)):
    #     segments_slic[]
    # # listUniqueColors = []
    # # for i in range(len(listUniqueColors)):
    # #     segments_slic[]
    # uniqueListColor = np.unique(listColors)


# Compute the euclidean distance between two colors
def euclideanColorDist(color1, color2):
    return np.sqrt(np.power(color1[0] - color2[0], 2) + 
           np.power(color1[1] - color2[1], 2) + 
           np.power(color1[2] - color2[2], 2))
           