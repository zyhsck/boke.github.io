import tkinter as tk

class ColorPicker:
    def __init__(self, master):
        self.master = master
        self.color = (0, 0, 0)
        self.create_widgets()
        # 在 ColorPicker 类中添加一个输入框，用于输入 RGB 值
        self.rgb_entry = tk.Entry(self.master)
        self.rgb_entry.pack()
        self.rgb_button = tk.Button(self.master, text="Set Color by RGB", command=self.set_color_by_rgb)
        self.rgb_button.pack()
    def create_widgets(self):
        self.r_slider = tk.Scale(self.master, from_=0, to=255, orient="horizontal", label="Red", command=self.update_color)
        self.r_slider.set(0)
        self.r_slider.pack()

        self.g_slider = tk.Scale(self.master, from_=0, to=255, orient="horizontal", label="Green", command=self.update_color)
        self.g_slider.set(0)
        self.g_slider.pack()

        self.b_slider = tk.Scale(self.master, from_=0, to=255, orient="horizontal", label="Blue", command=self.update_color)
        self.b_slider.set(0)
        self.b_slider.pack()

        self.color_label = tk.Label(self.master, text="Selected Color", font=("Arial", 12))
        self.color_label.pack()

    def update_color(self, event=None):
        r = self.r_slider.get()
        g = self.g_slider.get()
        b = self.b_slider.get()
        self.color = (r, g, b)
        self.color_label.config(bg="#%02x%02x%02x" % self.color, text="Selected Color: R=%d, G=%d, B=%d" % self.color)
    
    # 添加设置颜色的方法
    def set_color_by_rgb(self):
        rgb_str = self.rgb_entry.get()
        try:
            r, g, b = rgb_str.split(",")
            r,g,b = int(r),int(g),int(b)
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                self.color = (r, g, b)
                self.color_label.config(bg="#%02x%02x%02x" % self.color, text="Selected Color: R=%d, G=%d, B=%d" % self.color)#self.update_color()
                print(self.color,rgb_str)
            else:
                print("Invalid RGB values.")
        except ValueError:
            print("Invalid input format. Please use 'R,G,B' format.")

class PixelArtApp:
    def __init__(self, root):
        self.root = root
        self.pixel_size = 20
        self.rows = 20
        self.cols = 20
        self.pixels = [[(255, 255, 255) for _ in range(self.cols)] for _ in range(self.rows)]
        self.color = (0, 0, 0)  # Default color is black
        self.create_widgets()
        self.save_button = tk.Button(self.root, text="Save", command=self.save_pixels)
        self.save_button.grid(row=9, column=0, columnspan=2)

    def create_widgets(self):
        self.row_label = tk.Label(self.root, text="Rows:")
        self.row_label.grid(row=0, column=0)
        self.row_entry = tk.Entry(self.root)
        self.row_entry.grid(row=0, column=1)

        self.col_label = tk.Label(self.root, text="Columns:")
        self.col_label.grid(row=1, column=0)
        self.col_entry = tk.Entry(self.root)
        self.col_entry.grid(row=1, column=1)

        self.create_button = tk.Button(self.root, text="Create Canvas", command=self.create_canvas)
        self.create_button.grid(row=2, column=0, columnspan=2)

        self.color_button = tk.Button(self.root, text="Set Color", command=self.set_color)
        self.color_button.grid(row=3, column=0, columnspan=2)

        self.clear_button = tk.Button(self.root, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.grid(row=6, column=0, columnspan=2)

        self.color_frame = tk.Frame(self.root, width=200, height=50)
        self.color_frame.grid(row=7, column=0, columnspan=2)
        '''
        colors = [
            (255, 255, 255),  # White
            (0, 0, 0),  # Black
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255)  # Blue
        ]

        for i, color in enumerate(colors):
            btn = tk.Button(self.color_frame, bg="#%02x%02x%02x" % color, command=lambda c=color: self.set_quick_color(c))
            btn.grid(row=0, column=i, padx=5, pady=5)
        '''
        
    def clear_canvas(self):
        if self.canvas:
            self.canvas.delete("all")  # Clear the canvas
            self.pixels = [[(255, 255, 255) for _ in range(self.cols)] for _ in range(self.rows)]  # Reset pixel values
        for i in range(0, self.rows * self.pixel_size, self.pixel_size):
            self.canvas.create_line(0, i, self.cols * self.pixel_size, i, fill="gray")
        for i in range(0, self.cols * self.pixel_size, self.pixel_size):
            self.canvas.create_line(i, 0, i, self.rows * self.pixel_size, fill="gray")

    def create_canvas(self):
        self.rows = int(self.row_entry.get())
        self.cols = int(self.col_entry.get())
        self.pixels = [[(255, 255, 255) for _ in range(self.cols)] for _ in range(self.rows)]
        self.canvas = tk.Canvas(self.root, width=self.cols*self.pixel_size, height=self.rows*self.pixel_size, bg="white")
        self.canvas.bind("<B1-Motion>", self.draw_pixel)
        for i in range(0, self.rows * self.pixel_size, self.pixel_size):
            self.canvas.create_line(0, i, self.cols * self.pixel_size, i, fill="gray")
        for i in range(0, self.cols * self.pixel_size, self.pixel_size):
            self.canvas.create_line(i, 0, i, self.rows * self.pixel_size, fill="gray")
        self.canvas.grid(row=8, column=0, columnspan=2)

    def set_color(self):
        color_picker = tk.Toplevel(self.root)
        color_picker.title("Color Picker")
        cp = ColorPicker(color_picker)

        def set_custom_color(color):
            self.color = color
            color_picker.destroy()

        # 创建颜色选择按钮
        custom_color_button = tk.Button(color_picker, text="Select Custom Color", command=lambda: set_custom_color(cp.color))
        custom_color_button.pack(side="top", padx=5, pady=5)

        # 添加快捷颜色选择按钮
        colors = [
            (255, 255, 255),  # White
            (0, 0, 0),  # Black
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255)  # Blue
        ]

        for color in colors:
            btn = tk.Button(color_picker, bg="#%02x%02x%02x" % color, command=lambda c=color: set_custom_color(c))
            btn.pack(side="left", padx=5, pady=5)

    def draw_pixel(self, event):
        col = event.x // self.pixel_size
        row = event.y // self.pixel_size
        self.pixels[row][col] = self.color
        x0, y0 = col * self.pixel_size, row * self.pixel_size
        x1, y1 = x0 + self.pixel_size, y0 + self.pixel_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="#%02x%02x%02x" % self.color, outline="")

    def set_quick_color(self, color):
        self.color = color
    def save_pixels(self):
        pixel_values = [list(value) for row in self.pixels for value in row]
        
        print(f"{pixel_values},\n")

root = tk.Tk()
app = PixelArtApp(root)
root.mainloop()
    