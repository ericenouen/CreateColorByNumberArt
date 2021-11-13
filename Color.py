import matplotlib.pyplot as plt
from skimage import io, feature
from skimage.segmentation import slic, mark_boundaries

# Run the superpixel algorithm on a target image
def detectColors(imgPath):
    # https://scikit-image.org/docs/dev/api/skimage.segmentation.html?highlight=slic#skimage.segmentation.slic
    img = io.imread(imgPath)
    segments_slic = slic(img, n_segments=1000, compactness=1, start_label=1, sigma=1)
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(mark_boundaries(img, segments_slic))
    plt.show()