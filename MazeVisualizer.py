import numpy as np
import tkinter as tk

canvas_width = 720
canvas_height = 720
offset = 40
cell_size = 40

# double this value to add and subtract
border_size = 2

def canvas_setup(canvas_width, canvas_height, offset, cell_size, border_size):
    # Four Horsemen of the corners
    canvas.create_rectangle(offset - border_size, offset - border_size,
                            offset + border_size, offset + border_size,
                            fill="red", outline="red")
    canvas.create_rectangle((canvas_width - offset - border_size), offset - border_size,
                            (canvas_width - offset + border_size), offset + border_size,
                            fill="red", outline="red")
    canvas.create_rectangle(offset - border_size, (canvas_width - offset - border_size),
                            offset + border_size, (canvas_width - offset + border_size),
                            fill="red", outline="red")
    canvas.create_rectangle((canvas_width - offset - border_size), (canvas_width - offset - border_size),
                            (canvas_width - offset + border_size), (canvas_width - offset + border_size),
                            fill="red", outline="red")

    # Four edges
    canvas.create_rectangle((offset + border_size), (offset - border_size),
                            (canvas_width - offset - border_size), (offset + border_size),
                            fill="red", outline="red")
    canvas.create_rectangle((offset + border_size), (canvas_height - offset - border_size),
                            (canvas_width - offset - border_size), (canvas_height - offset + border_size),
                            fill="red", outline="red")
    canvas.create_rectangle((offset - border_size), (offset + border_size),
                            (offset + border_size), (canvas_height - offset - border_size),
                            fill="red", outline="red")
    canvas.create_rectangle((canvas_width - offset - border_size), (offset + border_size),
                            (canvas_width - offset + border_size), (canvas_height - offset - border_size),
                            fill="red", outline="red")

    # Corners of each cell
    for i in range(offset + cell_size, canvas_width - offset, cell_size):
        for j in range(offset + cell_size, canvas_width - offset, cell_size):
            canvas.create_rectangle((j - border_size), (i - border_size),
                                    (j + border_size), (i + border_size),
                                    fill="red", outline="red")

def display_grid(canvas_width, canvas_height, offset, cell_size, border_size):
    # Accessibility
    """for i in range(16):
        for j in range(16):
            if accessible_array[i][j] == 1:
                canvas.create_rectangle((cell_size * j) + offset + border_size,
                                        canvas_height - (cell_size * i) - (2 * offset) + border_size,
                                        (cell_size * j) + offset + 15,
                                        canvas_height - (cell_size * i) - (2 * offset) + 15,
                                        fill="green", outline="green")
            else:
                canvas.create_rectangle((cell_size * j) + offset + border_size,
                                        canvas_height - (cell_size * i) - (2 * offset) - border_size,
                                        (cell_size * j) + offset + 15,
                                        canvas_height - (cell_size * i) - (2 * offset) + 15,
                                        fill="red", outline="red")"""

    # Garbage
    for i in range(15):
        for j in range(16):
            if horiz_data[i][j] == 1:
                canvas.create_rectangle((cell_size * j) + offset + border_size,
                                        canvas_height - (cell_size * i) - (2 * offset) - border_size,
                                        (cell_size * (j + 1)) + offset - border_size,
                                        canvas_height - (cell_size * i) - (2 * offset) + border_size,
                                        fill="red", outline="red")

    # Also garbage
    for i in range(16):
        for j in range(15):
            if vert_data[i][j] == 1:
                canvas.create_rectangle((cell_size * j) + (2 * offset) - border_size,
                                        canvas_height - (cell_size * i) - offset - border_size,
                                        (cell_size * j) + (2 * offset) + border_size,
                                        canvas_height - (cell_size * (i + 1)) - offset + border_size,
                                        fill="red", outline="red")



filename = input("Enter filename: ")

if not (".txt" in filename):
    print("Bad filename")
    exit()

filename = "saved_mazes/" + filename

print(filename)

with open(filename, "rb") as file:
    data = np.frombuffer(file.read(), dtype=np.bool)

horiz_data = data[0:240]
vert_data = data[240:480]

horiz_data = horiz_data.reshape(15, 16)
vert_data = vert_data.reshape(16, 15)



# The stuff that actually shows up
root = tk.Tk()
root.title("Maze Thingy")

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

canvas_setup(canvas_width, canvas_height, offset, cell_size, border_size)

display_grid(canvas_width, canvas_height, offset, cell_size, border_size)

root.mainloop()
