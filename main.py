import tkinter as tk
import cv2
import numpy as np
import PIL
from PIL import Image, ImageTk
from tkinter import filedialog

class Entry:
    def __init__(self, frame_object, widget_object_list, widget_variable_list):
        self.frame_object = frame_object
        self.widget_objects = widget_object_list
        self.widget_variable_list = widget_variable_list

    def clone_entry(self, frame):
        new_widget_objects = list()
        clone_frame=tk.Frame(frame)
        for i, widget in enumerate(self.widget_objects):
            new_widget_objects.append(self.clone_scale_widget(i, widget, clone_frame))
        return Entry(clone_frame, new_widget_objects, None)

    def clone_scale_widget(self, i, widget, new_parent):
        parent = widget.nametowidget(widget.winfo_parent())

        cls = widget.__class__
        print(cls, parent)

        clone = cls(new_parent)
        for key in widget.configure():
            if key != "variable":
                clone.configure({key: widget.cget(key)})
        clone.set(widget.get())
        clone.grid(row=i, column=0)
        return clone


class CallBacks:
    @staticmethod
    def print_hello(n, m, x):
        print("Hello")

    @staticmethod
    def print_goodbye(n, m, x):
        print("Goodbye")

    @staticmethod
    def add_recipe_line(obj):
        instance = obj.clone_entry(custom_recipe_details_frame)
        custom_recipe_sequence.append(instance)
        instance.frame_object.grid(row=1, column=2)


def create_recipe_frame(master_, recipe_line):
    frame = tk.Frame(master_)
    widget_list = list()
    variable_list = list()
    for row_, slider_definition in enumerate(recipe_line[2:]):
        widget_variable = tk.DoubleVar()
        widget_variable.trace("w", recipe_line[1])
        widget = tk.Scale(master=frame,
                          label=slider_definition[0],
                          from_=slider_definition[1],
                          to=slider_definition[2],
                          resolution=slider_definition[3],
                          orient=tk.HORIZONTAL,
                          variable=widget_variable,
                          bg="yellow",
                          length=300)
        widget.grid(row=row_, column=0, sticky="E")
        widget_list.append(widget)
        variable_list.append(widget_variable)
    recipe_entry = Entry(frame, widget_list, variable_list)
    return recipe_entry


def generate_generic_recipe_frames():
    recipe_frames = list()
    for recipe_line in generic_recipes:
        new_entry = create_recipe_frame(filters_frame, recipe_line)
        recipe_frames.append(new_entry)
    return recipe_frames


def import_image(path, target_width):
    img = cv2.imread(path)
    height, width, depth = img.shape
    imgScale = target_width / width
    newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
    newimg = cv2.resize(img, (int(newX), int(newY)))
    im = Image.fromarray(newimg)
    imgtk = ImageTk.PhotoImage(image=im)
    return imgtk


def create_input_image_panel(frame):
    img = import_image(default_image_path, 200)
    image_label = tk.Label(frame, image=img)
    image_label.grid(row=0, column=0)
    return frame

def openfile_callback():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    return filename

root = tk.Tk()
custom_recipe_sequence = list()

input_image_frame = tk.Frame(root, width=200, height=200, bg="grey90")
input_image_frame.grid(row=0,column=0)
output_image_frame = tk.Frame(root, width=200, height=200, bg="grey50")
output_image_frame.grid(row=0, column=1)
filters_frame = tk.Frame(root, width=200, height=200, bg="grey30")
filters_frame.grid(row=1, column=0, columnspan=2, sticky="E")
custom_recipe_sequence_frame = tk.Frame(root, width=200, height=200, bg="grey70")
custom_recipe_sequence_frame.grid(row=0, column=2)
custom_recipe_details_frame = tk.Frame(root, width=200, height=200, bg="grey40")
custom_recipe_details_frame.grid(row=1, column=2)
controls_frame = tk.Frame(root, width=200, height=200, bg="grey50")
controls_frame.grid(row=0, column=3)


# f = tk.Frame(root) q
# f2 = tk.Frame(root)

generic_recipes = [["Blur", CallBacks.print_hello, ["kernel", 1, 7, 1]],
                   ["Crop", CallBacks.print_goodbye, ["X", 0, 1, 0.01], ["Y", 0, 1, 0.01], ["width", 0, 1, 0.01],
                    ["height", 0, 1, 0.01]],
                   ["Blqw", CallBacks.print_hello, ["matrix", 1, 7, 1]]]

recipe_frames = generate_generic_recipe_frames()

recipe_frames[1].frame_object.grid(row=0, column=0, sticky="E")
add_button = tk.Button(controls_frame, text="add", command=lambda: CallBacks.add_recipe_line(recipe_frames[1]))
add_button.grid(row=0,column=0)

default_image_path="C:\\Users\\v_sam\\Documents\\PxlRT\\PhotoImages\\wheelie.jpg"
img = import_image(default_image_path, 200)
image_label = tk.Label(input_image_frame, image=img)
image_label.grid(row=0, column=0)
open_button = tk.Button(input_image_frame, text="Open File", command=openfile_callback)
open_button.grid(row=1, column=0)





# f2.pack()
root.mainloop()
