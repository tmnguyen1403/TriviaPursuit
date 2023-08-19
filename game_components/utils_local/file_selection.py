import tkinter as tk
from tkinter import filedialog, ttk
import multiprocessing
import pygame
class FileSelection:
    def __init__(self, default_sound_dir:'str'):
        self.selected_file_label = " "
        self.file_path = ""
        self.tk_thread = None
        self.root = None
        self.queue = None
        self.default_sound_dir = default_sound_dir

    def select_file(self):
        # mouse_x, mouse_y = self.root.winfo_pointerxy()
        # print(f"Mouse x -y {mouse_x}, {mouse_y}")
        print(f"Default sound dir: {self.default_sound_dir}")
        self.file_path = filedialog.askopenfilename(
            title="Select A Music File",
            initialdir=self.default_sound_dir,  # You can change this to a specific directory if needed,
            parent=self.root,
            filetypes=(("Music files", "*.mp3"), ("All files", "*.*")),
        )
        if self.file_path == "":
            #Allow user to use cancel button to close the file selection
            return
        self.queue.put(self.file_path)
        self.root.destroy()

    def cancel(self):
        self.root.destroy()
        self.queue.put("")
        

    def my_thread(self):
        #print(f"Hello tkinter_thread {val}")
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        x,y = self.window_pos
        geometry = f"500x400+{x}+{y}"
        self.root.geometry(geometry)

        select_button = tk.Button(self.root, text="Select Music File", command=self.select_file)

        select_button.pack(side= 'left')

        cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel, background="red")
        cancel_button.pack(side= 'right')
        self.root.mainloop()
        print(f"File mythread is: {self.file_path} - User probably press x to close")
        self.queue.put(self.file_path)
        # How to check if destroyed?>
        # if tk.Tk.winfo_exists(self.root):
        #     print("Destroying Tk window")
        #     self.root.destroy()
        # else:
        #     print("Tk window is already destroyed")

    def start(self):
        print("File selection start")
        if self.tk_thread:
            print("tk_thread start")
            self.tk_thread.start()

    def join(self):
        if self.tk_thread:
            self.tk_thread.join()
            self.tk_thread = None

    def run(self, window_pos):
        self.window_pos = window_pos
        if self.tk_thread:
            return
        # Create the main window
        print("Hello file selection")
        self.queue = multiprocessing.Queue()
        self.tk_thread = multiprocessing.Process(target=self.my_thread, args=())
        self.tk_thread.start()
        self.tk_thread.join()
        selected_file = self.queue.get()
        print(f"Selected run file: {selected_file}")
        return selected_file

if __name__ == "__main__":
    pygame.init()
    # Set screen size
    screen_width = 1200
    screen_height = 1000
    display_index = 0
    screen = pygame.display.set_mode(size=(screen_width, screen_height), display=display_index)
    desktop_size = pygame.display.get_desktop_sizes()
    display_width, display_height = desktop_size[display_index]
    x = (display_width - screen_width)//2
    y = (display_height - screen_height)//2
    print(f"position x-y: {x} - {y}")
    
    screen.fill()
    
    '''
    Get the top_left coordinate of the screen
    Assume the screen is drawn from the center
    Then top_left cooridnate
    x = (display_width - screen_width)//2
    y = (display_height - screen_height)//2
    '''
    '''
    mouse_pos is relative to the screen
    screen is relative to desktop
    translate mouse_pos to desktop coordinate
    screen_x + 
    '''
    window_size = pygame.display.get_window_size()
    parent = screen.get_abs_parent()
    # print(f"Child Window position: {window_position}")
    # print(f"Child Window size: {window_size}")
    # print(f"Child num displays: {pygame.display.get_num_displays()}")
    # print(f"Child num displays: {pygame.display.get_num_displays()}")
    
    # Get display information

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    fl = FileSelection(default_sound_dir="/")
                    music_file = fl.run((x,y))
                    print(f"Handle mouse click: {music_file}")
        screen.fill(color=(255,255,255))

        pygame.display.flip()
       
    # root = tk.Tk()
    # root.title("Test open dialog")
    # root.geometry("500x400+3000+300")
    # root.attributes("-topmost", True)
    # root.mainloop()
    # root.destroy()