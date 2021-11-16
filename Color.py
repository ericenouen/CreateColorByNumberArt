import matplotlib.pyplot as plt
from skimage import io, feature
from skimage.segmentation import slic, mark_boundaries
import numpy as np

# Run the superpixel algorithm on a target image
def detectColors(imgPath):
    # https://scikit-image.org/docs/dev/api/skimage.segmentation.html?highlight=slic#skimage.segmentation.slic
    # https://github.com/scikit-image/scikit-image/blob/main/skimage/segmentation/slic_superpixels.py#L110-L384
    img = io.imread(imgPath).astype(float) / 255.
    n_segments = 100 # The number of labels in the output
    segments_slic = slic(img,
                        n_segments = n_segments,
                        compactness = .001, # How much weight to give to space proximity
                        max_iter = 50, # Max number of k-means iterations
                        sigma = 0,
                        spacing = None,
                        multichannel = True,
                        convert2lab = False,
                        enforce_connectivity = True,
                        min_size_factor = 0.5,
                        max_size_factor = 3,
                        slic_zero = False,
                        start_label = 1,
                        mask = None
                        )
    matchColors(img, segments_slic, n_segments)
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(mark_boundaries(img, segments_slic))
    plt.show()

def matchColors(img, segments_slic, maxNum):
    listColors = np.zeros([maxNum, 3])
    numPixels = np.zeros([maxNum, 1])
    row, col = np.shape(segments_slic)
    for i in range(row):
        for j in range(col):
            listColors[segments_slic[i][j] - 1] += img[i][j]
            numPixels[segments_slic[i][j] - 1] += 1
    listColors /= numPixels
    for i in range(row):
        for j in range(col):
            img[i][j] = listColors[segments_slic[i][j]-1]