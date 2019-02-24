import tkinter as tk
import cv2
import numpy as np
import PIL
from PIL import Image, ImageTk
from tkinter import filedialog
from time import sleep

class Entry:
    def __init__(self, name, frame_object, widget_object_list, widget_variable_list):
        self.name = name
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
#
#
# class CallBacks:
#     @staticmethod
#     def print_hello(n, m, x):
#         print("Hello")
#
#     @staticmethod
#     def print_goodbye(n, m, x):
#         print("Goodbye")
#
#     @staticmethod
#     def add_recipe_line(obj):
#         instance = obj.clone_entry(custom_recipe_details_frame)
#         custom_recipe_sequence.append(instance)
#         instance.frame_object.grid(row=1, column=2)

class Shared:
    def __init__(self):
        self.input_image_filename = "C:/Users/v_sam/Documents/PxlRT/PhotoImages/wheelie.jpg"
        self.output_image_filename = None
        self.image_display_width = 300
        self.input_img = cv2.imread(self.input_image_filename)
        self.input_imgtk = self.convert_image(self.input_img)
        self.output_img = self.input_img
        self.output_imgtk = self.input_imgtk
        self.generic_recipes = [["Blur", self.print_hello, ["kernel", 1, 7, 1]],
                                ["Crop", self.print_goodbye, ["X", 0, 1, 0.01], ["Y", 0, 1, 0.01],
                                 ["width", 0, 1, 0.01], ["height", 0, 1, 0.01]],
                                ["Blqw", self.print_hello, ["matrix", 1, 7, 1]]]

    def convert_image(self, img):
        height, width, depth = img.shape
        imgScale = self.image_display_width / width
        newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
        newimg = cv2.resize(img, (int(newX), int(newY)))
        im = Image.fromarray(newimg)
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk

    def update_shared(self, shared):
        self.input_image_filename = shared.input_image_filename
        self.input_img = shared.input_img
        self.input_imgtk = shared.input_imgtk
        self.output_img = shared.output_img
        self.output_imgtk = shared.output_imgtk

    # @staticmethod
    def print_hello(self, n, m, x):
        print("Hello", n,m, x)
        self.output_img = self.input_img * 1

    @staticmethod
    def print_goodbye(n, m, x):
        print("Goodbye", n)

    # @staticmethod
    # def add_recipe_line(obj):
    #     instance = obj.clone_entry(custom_recipe_details_frame)
    #     custom_recipe_sequence.append(instance)
    #     instance.frame_object.grid(row=1, column=2)


class MainWindow:
    def __init__(self, root, shared):
        self.output_frame = OutputFrame(root, shared)
        self.input_frame = InputFrame(root, self.output_frame, shared)
        self.filter_frame = FilterFrame(root, self.output_frame, shared)
        # self.recipe_frame = RecipeFrame(root)
        # self.input_frame.grid(row=0, column=0)
        # self.output_frame.grid(row=0, column=1)
        # self.filter_frame.grid(row=1, column=0, columnspan=2)
        # self.recipe_frame.grid(row=0, column=2, rowspan=2)


class InputFrame():
    def __init__(self, root, output_frame, shared):
        self.input_frame = tk.Frame(root)
        self.input_frame.grid(row=0, column=0)
        self.output_frame = output_frame
        self.shared = shared
        self.image_label = None
        self.load_button = None
        self.populate_input_frame()

    def populate_input_frame(self):
        self.image_label = tk.Label(self.input_frame, image=self.shared.input_imgtk)
        self.image_label.grid(row=0, column=0)
        self.load_button = tk.Button(self.input_frame, text="LOAD", command=self.openfile_callback)
        self.load_button.grid(row=1, column=0)

    def openfile_callback(self):
        self.shared.input_image_filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.shared.input_img = cv2.imread(self.shared.input_image_filename)
        self.shared.input_imgtk = self.shared.convert_image(self.shared.input_img)
        self.image_label.config(image=self.shared.input_imgtk)
        self.output_frame.image_label.config(image=self.shared.input_imgtk)
        self.shared.update_shared(shared)


class OutputFrame:
    def __init__(self, root, shared):
        self.output_frame = tk.Frame(root)
        self.output_frame.grid(row=0, column=1)
        self.shared = shared
        self.image_label = None
        self.save_button = None
        self.populate_output_frame()

    def populate_output_frame(self):
        self.image_label = tk.Label(self.output_frame, image=self.shared.output_imgtk)
        self.image_label.grid(row=0, column=0)
        self.save_button = tk.Button(self.output_frame, text="SAVE", command=self.savefile_callback)
        self.save_button.grid(row=1, column=0)

    def savefile_callback(self):
        self.shared.output_image_filename = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",
                                                     filetypes = (("jpeg files","*.jpg"),("all files","*.*")))


class FilterFrame:
    def __init__(self, root, output_frame, shared):
        self.filter_frame = tk.Frame(root, width=shared.image_display_width*2, height=300, bg="green")
        self.filter_frame.grid(row=1, column=0, columnspan=2)
        self.filter_frame.columnconfigure(1, minsize=400)
        self.filter_frame.grid_propagate(0)
        self.shared = shared
        self.output_frame = output_frame
        self.recipe_frames = list()
        self.generate_generic_recipe_frames()
        self.recipe_listbox = tk.Listbox(self.filter_frame, height=10)
        self.create_listbox_frame()
        self.current_active_recipe_frame = 1
        self.recipe_frames[self.current_active_recipe_frame].frame_object.grid(row=0, column=1, sticky="NE")
        self.recipe_listbox.grid(row=0, column=0, sticky="NW")

    def generate_generic_recipe_frames(self):
        for recipe_line in self.shared.generic_recipes:
            new_entry = self.create_recipe_frame(recipe_line)
            self.recipe_frames.append(new_entry)

    def create_recipe_frame(self, recipe_line):
        frame = tk.Frame(self.filter_frame)
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
            widget.grid(row=row_, column=0)
            widget_list.append(widget)
            variable_list.append(widget_variable)
        recipe_entry = Entry(recipe_line[0], frame, widget_list, variable_list)
        return recipe_entry

    def create_listbox_frame(self):
        for entry in self.recipe_frames:
            print(entry.name)
            self.recipe_listbox.insert(tk.END, entry.name)
        self.recipe_listbox.bind('<<ListboxSelect>>', self.onselect)

    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        self.recipe_frames[self.current_active_recipe_frame].frame_object.grid_remove()
        self.recipe_frames[index].frame_object.grid(row=0, column=1, sticky="N")
        self.current_active_recipe_frame = index


# def generate_generic_recipe_frames():
#     recipe_frames = list()
#     for recipe_line in generic_recipes:
#         new_entry = create_recipe_frame(filters_frame, recipe_line)
#         recipe_frames.append(new_entry)
#     return recipe_frames
# def create_recipe_frame(master_, recipe_line):
#     frame = tk.Frame(master_)
#     widget_list = list()
#     variable_list = list()
#     for row_, slider_definition in enumerate(recipe_line[2:]):
#         widget_variable = tk.DoubleVar()
#         widget_variable.trace("w", recipe_line[1])
#         widget = tk.Scale(master=frame,
#                           label=slider_definition[0],
#                           from_=slider_definition[1],
#                           to=slider_definition[2],
#                           resolution=slider_definition[3],
#                           orient=tk.HORIZONTAL,
#                           variable=widget_variable,
#                           bg="yellow",
#                           length=300)
#         widget.grid(row=row_, column=0, sticky="E")
#         widget_list.append(widget)
#         variable_list.append(widget_variable)
#     recipe_entry = Entry(frame, widget_list, variable_list)
#     return recipe_entry
#
#
# def generate_generic_recipe_frames():
#     recipe_frames = list()
#     for recipe_line in generic_recipes:
#         new_entry = create_recipe_frame(filters_frame, recipe_line)
#         recipe_frames.append(new_entry)
#     return recipe_frames
#
#
# def import_image(path, target_width):
#     img = cv2.imread(path)
#     height, width, depth = img.shape
#     imgScale = target_width / width
#     newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
#     newimg = cv2.resize(img, (int(newX), int(newY)))
#     im = Image.fromarray(newimg)
#     imgtk = ImageTk.PhotoImage(image=im)
#     return imgtk
#
#
# def create_input_image_panel(frame):
#     img = import_image(default_image_path, 200)
#     image_label = tk.Label(frame, image=img)
#     image_label.grid(row=0, column=0)
#     return frame
#
# def openfile_callback():
#     filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
#     return filename

root = tk.Tk()
root.geometry("800x500")
shared = Shared()
main_window = MainWindow(root, shared)
# custom_recipe_sequence = list()
#
# input_image_frame = tk.Frame(root, width=200, height=200, bg="grey90")
# input_image_frame.grid(row=0,column=0)
# output_image_frame = tk.Frame(root, width=200, height=200, bg="grey50")
# output_image_frame.grid(row=0, column=1)
# filters_frame = tk.Frame(root, width=200, height=200, bg="grey30")
# filters_frame.grid(row=1, column=0, columnspan=2, sticky="E")
# custom_recipe_sequence_frame = tk.Frame(root, width=200, height=200, bg="grey70")
# custom_recipe_sequence_frame.grid(row=0, column=2)
# custom_recipe_details_frame = tk.Frame(root, width=200, height=200, bg="grey40")
# custom_recipe_details_frame.grid(row=1, column=2)
# controls_frame = tk.Frame(root, width=200, height=200, bg="grey50")
# controls_frame.grid(row=0, column=3)
#
#
# # f = tk.Frame(root) q
# # f2 = tk.Frame(root)
#
# generic_recipes = [["Blur", CallBacks.print_hello, ["kernel", 1, 7, 1]],
#                    ["Crop", CallBacks.print_goodbye, ["X", 0, 1, 0.01], ["Y", 0, 1, 0.01], ["width", 0, 1, 0.01],
#                     ["height", 0, 1, 0.01]],
#                    ["Blqw", CallBacks.print_hello, ["matrix", 1, 7, 1]]]
#
# recipe_frames = generate_generic_recipe_frames()
#
# recipe_frames[1].frame_object.grid(row=0, column=0, sticky="E")
# add_button = tk.Button(controls_frame, text="add", command=lambda: CallBacks.add_recipe_line(recipe_frames[1]))
# add_button.grid(row=0,column=0)
#
# default_image_path="C:\\Users\\v_sam\\Documents\\PxlRT\\PhotoImages\\wheelie.jpg"
# img = import_image(default_image_path, 200)
# image_label = tk.Label(input_image_frame, image=img)
# image_label.grid(row=0, column=0)
# open_button = tk.Button(input_image_frame, text="Open File", command=openfile_callback)
# open_button.grid(row=1, column=0)
#
#
#
#
#
# # f2.pack()
root.mainloop()
