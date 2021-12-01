# Create Color By Number Art

By Eric Enouen and Grant Zimpfer

## Goal
When we first began discussing ideas for the project, something involving turning an image into a coloring book style black and white outline was immediately the focus of what our end goal should be. The first approach that came to mind was using a 2D gaussian derivative filter on the image to perform edge detection and outline where major objects were in the image.

After thinking about more of our previous work and algorithms from class, we realized the superpixeling process from the image segmentation homework would allow us to recognize like-sections by color. This in turn, we decided, would be useful to turn the normal coloring book outline into a color by numbers style image, derived from any image that we could perform those two algorithms on. Below is an example of our target output.

<img src="https://github.com/ericenouen/CreateColorByNumberArt/blob/master/ReadmeImages/color.png" width="300" height="auto" />

## Color Detection
To start we began tinkering with the scikit slic superpixel function, and its various parameters. The compactness would have to be low as color segments could take any variety of shape within an image, and to keep the runtime at a reasonable low, we limited the K-means iterations to 100. Once the parameters were established to find quality segments with strong distinctions in color, the small variations within those segments needed to be removed. 

To do this, we found the average RBG color value within a segment, and then proceeded to assign that color to every pixel within that segment. Now that every segment had one color assigned to it, small variations in colors (two close shades of red or blue) needed to be equalized, to reduce the final amount of colors needed for the image. To do this, we checked if the euclidean distance between RGB values of two segment colors was within a threshold, and if so they were assigned to be the same color. The segments were then merged into the same segment to avoid drawing extraneous borders in the image between segments of the same color. Once the boundaries of the segments are finalized, they are highlighted onto the color filled image and an empty image of all white, the latter is then printed with numbers correlating to colors in the segment and their key label. The list of colors is used to create a key, by printing the colors/numbers in order on a new image.

<img src="https://github.com/ericenouen/CreateColorByNumberArt/blob/master/ReadmeImages/display.png" width="500" height="auto" />

## Edge Detection
The edge detection task was primarily used to improve the final image by adding some more visual information about the object. This can be seen in the image below, where the actual color segments don’t have super well defined shapes to them, but the edges displayed help make it clear that the image is of Spiderman even when the image is black and white.
 
Edge detection was performed by applying a 2D gaussian filter in both the x and y directions, calculating the magnitude using both of these computed images, and then thresholding the result to get a binary image of whether or not an edge was detected at that point. These detected edges could then be overlaid on top of the final computed Color By Number Image using OpenCV’s findContours method.

<img src="https://github.com/ericenouen/CreateColorByNumberArt/blob/master/ReadmeImages/spiderman_output5.jpg" width="700" height="auto" />

## Results

After these two processes have been run on the image, the output provides the necessary information for a user to recreate a general sketch of the input image. The user has a mostly white image with black borders around where the objects in that image originally were, numbers printed all over the image corresponding to which color to draw in at that position in the image, and a key to let the user know which color should be drawn for each number. Here is one example of a banana.

<img src="https://github.com/ericenouen/CreateColorByNumberArt/blob/master/ReadmeImages/banana_key9.jpg" width="700" height="auto" />
<img src="https://github.com/ericenouen/CreateColorByNumberArt/blob/master/ReadmeImages/banana_output9.jpg" width="350" height="auto" />
<img src="https://github.com/ericenouen/CreateColorByNumberArt/blob/master/ReadmeImages/banana_filled9.jpg" width="350" height="auto" />

## Bokeh

The tool Bokeh was used to create a Graphical User Interface that the user could interact with to produce images. This helped create a more user friendly environment that could be used to create multiple different color by number pages in a simple way. 

The user interface provided variations to the algorithm that the user could control, such as thresholds for how prominent an edge has to be to be drawn onto the output, the number of pixels/segments for the starting superpixel function to create, and a threshold for how close two different segments’ colors must be to merge into one common color. This addition allowed for the user to create more complex images if they’d like, or to keep it simple if they were wanting a cartoon-ish look. 

[Here](http://docs.bokeh.org/en/latest/index.html) is a link to its documentation

## Limitations/Future Work

There were a few things that we were not able to accomplish in the time frame given that we would improve if we had more time. The most important aspect we would want to fix is the placement of numbers onto the image. The current method simply places a number on the image every X steps. This method struggles with smaller segments or segments near edges where the color of the segment is ambiguous because a number was not placed inside of it. One way to fix this is by separating out all of the segments and performing a center of mass calculation, placing a number at the center of mass of each different color segment.

In the future we might also make the GUI more user-friendly, by resizing properly no matter the size of the image so the user didn’t have to zoom out unnecessarily.

The last thing we would want to work on is speeding up the computation of the algorithm so that images could be produced faster and different thresholds could be tested more easily.
