import tkinter as tk
from tkinter import filedialog
import multiprocessing
import threading

class FileSelection:
    def __init__(self):
        self.selected_file_label = " "
        self.file_path = ""
        self.tk_thread = None
        self.root = None
        self.queue = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a file", initialdir=".")
        print(f"Selected file: {self.file_path}")
        self.queue.put(self.file_path)
        # if self.file_path:
        #     self.selected_file_label.config(text="Selected File: " + self.file_pathfile_path)
        # else:
        #     self.selected_file_label.config(text="No file selected")
        self.root.destroy()

    def my_thread(self):
        #print(f"Hello tkinter_thread {val}")
        self.root = tk.Tk()
        root = self.root
        #root.withdraw()  # Hide the root window

        select_button = tk.Button(root, text="Select File", command=self.select_file)
        selected_file_label = tk.Label(root, text="No file selected")

        select_button.pack()
        selected_file_label.pack()

        root.mainloop()
        print(f"File is: {self.file_path}")

    def start(self):
        print("File selection start")
        if self.tk_thread:
            print("tk_thread start")
            self.tk_thread.start()
    def join(self):
        if self.tk_thread:
            self.tk_thread.join()
            self.tk_thread = None
    def run(self):
        if self.tk_thread:
            return
        # Create the main window
        print("Hello file selection")
        val = 123
        self.queue = multiprocessing.Queue()
        self.tk_thread = multiprocessing.Process(target=self.my_thread, args=())
        self.tk_thread.start()
        self.tk_thread.join()
        selected_file = self.queue.get()
        print(f"Does the data available here: {selected_file}")
        
        # self.tk_thread = threading.Thread(target=self.my_thread, args=(val, ))
