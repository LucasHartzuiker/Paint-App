import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageDraw, ImageTk

class SimplePaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint Application")
        self.root.geometry("800x600")

        # Default settings
        self.brush_color = "black"
        self.brush_size = 10  # Increased default brush size
        self.mode = "brush"  # Can be 'brush', 'eraser', 'rectangle', 'circle', or 'line'

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize image for saving and drawing
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # Create mode buttons
        self.create_mode_buttons()

        # Create menu
        self.create_menu()

        # Variables to store coordinates
        self.start_x = None
        self.start_y = None
        self.current_shape = None  # Stores current shape object on canvas

    def create_mode_buttons(self):
        # Frame for mode buttons
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(side=tk.TOP, fill=tk.X)

        # Button for Brush Mode
        brush_button = tk.Button(mode_frame, text='🖌️', command=self.use_brush, width=8, height=4, font=("Arial", 20))
        brush_button.pack(side=tk.LEFT)

        # Button for Eraser Mode
        eraser_button = tk.Button(mode_frame, text='🧹', command=self.use_eraser, width=8, height=4, font=("Arial", 20))
        eraser_button.pack(side=tk.LEFT)

        # Button for Rectangle Mode
        rectangle_button = tk.Button(mode_frame, text='⬜', command=self.use_rectangle, width=8, height=4, font=("Arial", 20))
        rectangle_button.pack(side=tk.LEFT)

        # Button for Circle Mode
        circle_button = tk.Button(mode_frame, text='⚪', command=self.use_circle, width=8, height=4, font=("Arial", 20))
        circle_button.pack(side=tk.LEFT)

        # Button for Line Mode
        line_button = tk.Button(mode_frame, text='➖', command=self.use_line, width=8, height=4, font=("Arial", 20))
        line_button.pack(side=tk.LEFT)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        # Brush size menu
        size_menu = tk.Menu(menu_bar, tearoff=0)
        size_menu.add_command(label="Small Brush (5px)", command=lambda: self.change_brush_size(5))
        size_menu.add_command(label="Medium Brush (10px)", command=lambda: self.change_brush_size(10))
        size_menu.add_command(label="Large Brush (15px)", command=lambda: self.change_brush_size(15))
        menu_bar.add_cascade(label="Brush Size", menu=size_menu)

        # Color menu
        color_menu = tk.Menu(menu_bar, tearoff=0)
        color_menu.add_command(label="Choose Color", command=self.choose_color)
        menu_bar.add_cascade(label="Color", menu=color_menu)

        # File menu for saving and opening images
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Open", command=self.open_image)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Clear canvas
        menu_bar.add_command(label="Clear Canvas", command=self.clear_canvas)

        # Exit
        menu_bar.add_command(label="Exit", command=self.root.quit)

        self.root.config(menu=menu_bar)

    def paint(self, event):
        # Check the current mode and call drawing functions accordingly
        if self.mode == "brush":
            self.draw_line(event, self.brush_color)
        elif self.mode == "eraser":
            self.draw_line(event, "white")  # Erase by drawing in white

    def draw_line(self, event, color):
        # Draw line segment based on start and current coordinates
        if self.start_x and self.start_y:
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                    fill=color, width=self.brush_size,
                                    capstyle=tk.ROUND, smooth=True)
            # Draw line on image for saving
            self.draw.line([(self.start_x, self.start_y), (event.x, event.y)],
                           fill=color, width=self.brush_size)
        self.start_x = event.x
        self.start_y = event.y

    def start_draw(self, event):
        # Initialize start coordinates when the user clicks the mouse
        self.start_x = event.x
        self.start_y = event.y
               
        # Reset current shape for rectangle, circle, or line modes
        if self.mode in ["rectangle", "circle", "line"]:
            self.current_shape = None

    def reset(self, event):
        # Finalize shape drawing when mouse is released
        if self.mode == "rectangle":
            self.draw_rectangle(event)
        elif self.mode == "circle":
            self.draw_circle(event)
        elif self.mode == "line":
            self.draw_line_shape(event)

        self.start_x, self.start_y = None, None
        self.current_shape = None

    def draw_rectangle(self, event):
        # Draws a rectangle on the canvas and image
        if self.current_shape:
            self.canvas.delete(self.current_shape)
        self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                                          outline=self.brush_color, width=self.brush_size)
        # Draw on image for saving
        self.draw.rectangle([self.start_x, self.start_y, event.x, event.y],
                            outline=self.brush_color, width=self.brush_size)

    def draw_circle(self, event):
        # Draws a circle based on the radius from the start point to the current point
        if self.current_shape:
            self.canvas.delete(self.current_shape)
        x0, y0 = self.start_x, self.start_y
        x1, y1 = event.x, event.y
        radius = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        self.current_shape = self.canvas.create_oval(x0 - radius, y0 - radius, x0 + radius, y0 + radius,
                                                     outline=self.brush_color, width=self.brush_size)
        # Draw on image for saving
        self.draw.ellipse([x0 - radius, y0 - radius, x0 + radius, y0 + radius],
                          outline=self.brush_color, width=self.brush_size)

    def draw_line_shape(self, event):
        # Draws a straight line from start to current coordinates
        if self.current_shape:
            self.canvas.delete(self.current_shape)
        self.current_shape = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                                     fill=self.brush_color, width=self.brush_size)
        # Draw on image for saving
        self.draw.line([self.start_x, self.start_y, event.x, event.y],
                       fill=self.brush_color, width=self.brush_size)

    def choose_color(self):
        # Opens color picker dialog to select brush color
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color = color

    def change_brush_size(self, size):
        self.brush_size = size

    def use_brush(self):
        self.mode = "brush"

    def use_eraser(self):
        self.mode = "eraser"

    def use_rectangle(self):
        self.mode = "rectangle"

    def use_circle(self):
        self.mode = "circle"

    def use_line(self):
        self.mode = "line"

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        # Saves the current image to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.image.save(file_path)

    def open_image(self):
        # Opens an image file and pastes it onto the canvas and PILLOW image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")])
        if file_path:
            opened_image = Image.open(file_path)
            self.image.paste(opened_image.resize((800, 600)))
            self.draw = ImageDraw.Draw(self.image)
            # Update the canvas with the opened image
            self.update_canvas_image()

    def update_canvas_image(self):
        # Convert the PILLOW image to a format tkinter can display and update the canvas
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplePaintApp(root)
    root.mainloop()