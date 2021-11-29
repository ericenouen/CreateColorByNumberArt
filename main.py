# To use bokeh, first install bokeh into your python environment.
# Then use the command prompt to locate the directory ABOVE the CreateColorByNumberArt directory
# Type the following command: bokeh serve --show CreateColorByNumberArt
# This will open up the local page running the 

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Slider, Button, TextInput, Div

from ColorBook import generateColorByNumberArt

versionNumber = 0

file_input = TextInput(title="File Name:")

edge_slider = Slider(start=0, end=255, value=50, step=.1, title="Edge detection threshold (Low = More Edges)")
pixel_slider = Slider(start=1, end=10000, value=1000, step=1, title="Number of superpixels (Low = Less Detail)")
color_slider = Slider(start=0, end=2, value=.2, step=.01, title="Color merging threshold (Low = More Colors)")

button = Button(label="Compute", button_type="success")
clear = Button(label="Clear")
div_image = Div(text="", width=1000, height=1000, sizing_mode="scale_both")
div_key = Div(text="", width=1000, height=1000, sizing_mode="scale_both")

def computeImage():
    global versionNumber
    generateColorByNumberArt("CreateColorByNumberArt\\static\\Input\\" + file_input.value, "CreateColorByNumberArt\\static\\" + file_input.value, edge_slider.value, pixel_slider.value, color_slider.value, versionNumber)
    div_image.text = "<img src='" + "CreateColorByNumberArt\\static\\" + file_input.value.split('.')[0] + "_output" + str(versionNumber) + ".jpg' alt=\"div_image\">"
    div_key.text = "<img src='" + "CreateColorByNumberArt\\static\\" + file_input.value.split('.')[0] + "_key" + str(versionNumber) + ".jpg' alt=\"div_image\">"
    versionNumber += 1

def clearImage():
    div_image.text = ""
    div_key.text = ""

button.on_click(computeImage)
clear.on_click(clearImage)

layout = row(
    column(file_input, edge_slider, pixel_slider, color_slider, div_image),
    column(button, clear, div_key),
)

curdoc().title = "Create Color By Number Art"
curdoc().add_root(layout)