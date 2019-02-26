import tkinter as tk
import cv2
import numpy as np
import PIL
from PIL import Image, ImageTk
from tkinter import filedialog
from time import sleep
from settings import *


class Entry:
    def __init__(self, name, frame_object, widget_object_list, widget_variable_list):
        self.name = name
        self.frame_object = frame_object
        self.widget_objects = widget_object_list
        self.widget_variable_list = widget_variable_list

    def clone_entry(self, frame):
        new_widget_objects = list()
        clone_frame = tk.Frame(frame)
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


class Shared:
    def __init__(self):
        self.input_image_filename = "C:/Users/v_sam/Documents/PxlRT/PhotoImages/wheelie.jpg"
        self.output_image_filename = None
        self.image_display_width = (WIDTH_IMAGE_FRAME - 2 * PADX)
        self.input_img = cv2.imread(self.input_image_filename)
        self.input_imgtk = self.convert_image(self.input_img)
        self.output_img = self.input_img
        self.output_imgtk = self.input_imgtk
        self.generic_recipes = [["Normalise", self.normalise_image, ["Normalise", 0, 1, 1]],
                                ["Contrast", self.modify_contrast, ["Factor", 0, 5, 0.01]],
                                ["Blur", self.print_hello, ["kernel", 1, 7, 1]],
                                ["Crop", self.print_hello, ["X", 0, 1, 0.01], ["Y", 0, 1, 0.01],
                                 ["width", 0, 1, 0.01], ["height", 0, 1, 0.01]],
                                ["Blqw", self.print_hello, ["matrix", 1, 7, 1]]]
        self.sequence_listbox = None
        self.sequence_listbox_entries = list()

    def convert_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height, width = img.shape
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

    def refresh_output_image(self, output_frame):
        self.output_imgtk = self.convert_image(self.output_img)
        output_frame.image_label.config(image=self.output_imgtk)

    def normalise_image(self, n, m, x, var, output_frame):
        print("Normalising")
        if var.get()==1:
            min_value = np.amin(self.input_img)
            self.output_img -= min_value
            max_value = np.amax(self.output_img)
            scale = 255.0/max_value
            self.output_img = (self.output_img * scale).astype(np.uint8)
        else:
            self.output_img = self.input_img
        self.refresh_output_image(output_frame)

    def modify_contrast(self, n, m, x, var, output_frame):
        print("Modifying contrast")
        self.output_img = (self.input_img * var.get()).astype(np.uint8)
        self.refresh_output_image(output_frame)

    # @staticmethod
    def print_hello(self, n, m, x, var, output_frame):
        print("Hello", n, m, x)
        print(var.get())
        self.output_img = self.input_img * int(var.get())
        self.output_imgtk = self.convert_image(self.output_img)
        output_frame.image_label.config(image=self.output_imgtk)

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
        self.filter_frame = FilterFrame(root, self.input_frame, self.output_frame, shared)
        self.sequence_frame = SequenceFrame(root, self.output_frame, self.filter_frame, shared)


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
                                                                      filetypes=(
                                                                      ("jpeg files", "*.jpg"), ("all files", "*.*")))
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
        self.shared.output_image_filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                                         filetypes=(
                                                                         ("jpeg files", "*.jpg"), ("all files", "*.*")))
        cv2.imwrite(self.shared.output_image_filename, self.shared.output_img)


class FilterFrame:
    def __init__(self, root, input_frame, output_frame, shared):
        self.filter_frame = tk.Frame(root, width=WIDTH_FILTER_FRAME, height=HEIGHT_FILTER_FRAME, bg="green")
        self.filter_frame.grid(row=1, column=0, columnspan=2)
        self.filter_frame.columnconfigure(0, minsize=WIDTH_FILTER_LISTBOX)
        self.filter_frame.columnconfigure(1, minsize=WIDTH_FILTER_CONTROL_FRAME)
        self.filter_frame.columnconfigure(2, minsize=WIDTH_FILTER_SLIDER_FRAME)
        self.filter_frame.grid_propagate(0)
        self.shared = shared
        self.input_frame = input_frame
        self.output_frame = output_frame
        self.recipe_frames = list()
        self.generate_generic_recipe_frames()
        self.recipe_listbox = tk.Listbox(self.filter_frame, height=int(HEIGHT_FILTER_FRAME/FONT_POINTS_2_PIXELS))
        self.create_listbox_frame()
        self.current_active_recipe_frame = 1
        self.recipe_frames[self.current_active_recipe_frame].frame_object.grid(row=0, column=2, sticky="N")
        self.recipe_listbox.grid(row=0, column=0, sticky="NW", padx=PADX)
        self.filter_control_frame = tk.Frame(self.filter_frame)
        self.filter_control_frame.grid(row=0, column=1, sticky="NW")
        self.add_button = tk.Button(self.filter_control_frame, text="Add", command=self.add_to_sequence)
        self.output_as_input_button = tk.Button(self.filter_control_frame, text="Use Output as Input", command=self.output_as_input)
        self.mode_variable = tk.IntVar()
        self.mode_variable.set(1)
        self.single_filter_radiobutton = tk.Radiobutton(self.filter_control_frame, text="Single Filter", variable=self.mode_variable, value=1)
        self.sequence_filter_radiobutton = tk.Radiobutton(self.filter_control_frame, text="Sequence Filter", variable=self.mode_variable, value=2)
        self.add_button.pack(anchor="nw")
        self.output_as_input_button.pack(anchor="nw")
        self.single_filter_radiobutton.pack(anchor="nw")
        self.sequence_filter_radiobutton.pack(anchor="nw")

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
            # widget_variable.trace("w", recipe_line[1])
            widget_variable.trace("w", lambda a,b,c, var=widget_variable, output_frame=self.output_frame: recipe_line[1](a,b,c,var, output_frame))
            widget = tk.Scale(master=frame,
                              label=slider_definition[0],
                              from_=slider_definition[1],
                              to=slider_definition[2],
                              resolution=slider_definition[3],
                              orient=tk.HORIZONTAL,
                              variable=widget_variable,
                              bg="yellow",
                              length=WIDTH_FILTER_SLIDER_FRAME-2*PADX)
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
        self.recipe_frames[index].frame_object.grid(row=0, column=2, sticky="N")
        self.current_active_recipe_frame = index

    def add_to_sequence(self):
        self.shared.sequence_listbox_entries.append(self.recipe_frames[self.current_active_recipe_frame])
        self.shared.sequence_listbox.insert(tk.END, self.recipe_frames[self.current_active_recipe_frame].name)

    def output_as_input(self):
        self.shared.input_img = self.shared.output_img
        self.shared.input_imgtk = self.shared.output_imgtk
        self.input_frame.image_label.config(image=self.shared.output_imgtk)


class SequenceFrame:
    def __init__(self, root, output_frame, filter_frame, shared):
        self.sequence_frame = tk.Frame(root, width=WIDTH_SEQUENCE_FRAME, height=HEIGHT_MAIN_WINDOW, bg="blue")
        self.sequence_frame.grid(row=0, column=2, rowspan=2)
        self.sequence_frame.columnconfigure(0, minsize=WIDTH_SEQUENCE_FRAME)
        self.sequence_frame.grid_propagate(0)

        self.sequence_controls = tk.Frame(self.sequence_frame, width=WIDTH_SEQUENCE_FRAME, height=HEIGHT_MAIN_WINDOW, bg="orange")
        self.sequence_controls.grid(row=1, column=0)
        self.sequence_controls.columnconfigure(0, minsize=WIDTH_SEQUENCE_FRAME)
        self.sequence_controls.grid_propagate(0)

        self.shared = shared
        self.output_frame = output_frame
        self.filter_frame = filter_frame

        self.shared.sequence_listbox = tk.Listbox(self.sequence_frame, height=int((HEIGHT_MAIN_WINDOW/10*8)/FONT_POINTS_2_PIXELS))
        self.shared.sequence_listbox.grid(row=0, column=0, sticky="N", pady=PADY)

        self.delete_button = tk.Button(self.sequence_controls, text="DELETE").pack()
        self.move_up_button = tk.Button(self.sequence_controls, text="MOVE UP").pack()
        self.move_down_button = tk.Button(self.sequence_controls, text="MOVE_DOWN").pack()


def configure_root():
    root = tk.Tk()
    root.geometry(str(WIDTH_MAIN_WINDOW) + "x" + str(HEIGHT_MAIN_WINDOW))
    root.columnconfigure(0, minsize=WIDTH_IMAGE_FRAME)
    root.columnconfigure(1, minsize=WIDTH_IMAGE_FRAME)
    root.columnconfigure(2, minsize=WIDTH_SEQUENCE_FRAME)
    root.rowconfigure(0, minsize=HEIGHT_IMAGE_FRAME)
    root.rowconfigure(1, minsize=HEIGHT_FILTER_FRAME)
    return root


root = configure_root()
shared = Shared()
main_window = MainWindow(root, shared)
root.mainloop()
