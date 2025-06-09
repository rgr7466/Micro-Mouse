import numpy as np
import tkinter as tk
import random

CANVAS_WIDTH = 720
CANVAS_HEIGHT = 720
OFFSET = 40
CELL_SIZE = 40
SOL_OFFSET = 60

# double this value to add and subtract
BORDER_SIZE = 2

DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3

toggle_fast = False

def fast_solution_button():
    global toggle_fast
    canvas.delete("line")
    if toggle_fast:
        displaySolution(path_since_fork, "green")
        toggle_fast = False
    else:
        displaySolution(path_chosen, "blue")
        toggle_fast = True

def canvas_setup(CANVAS_WIDTH, CANVAS_HEIGHT, OFFSET, CELL_SIZE, BORDER_SIZE):
    # Four Horsemen of the corners
    canvas.create_rectangle(OFFSET - BORDER_SIZE, OFFSET - BORDER_SIZE,
                            OFFSET + BORDER_SIZE, OFFSET + BORDER_SIZE,
                            fill="red", outline="red")
    canvas.create_rectangle((CANVAS_WIDTH - OFFSET - BORDER_SIZE), OFFSET - BORDER_SIZE,
                            (CANVAS_WIDTH - OFFSET + BORDER_SIZE), OFFSET + BORDER_SIZE,
                            fill="red", outline="red")
    canvas.create_rectangle(OFFSET - BORDER_SIZE, (CANVAS_WIDTH - OFFSET - BORDER_SIZE),
                            OFFSET + BORDER_SIZE, (CANVAS_WIDTH - OFFSET + BORDER_SIZE),
                            fill="red", outline="red")
    canvas.create_rectangle((CANVAS_WIDTH - OFFSET - BORDER_SIZE), (CANVAS_WIDTH - OFFSET - BORDER_SIZE),
                            (CANVAS_WIDTH - OFFSET + BORDER_SIZE), (CANVAS_WIDTH - OFFSET + BORDER_SIZE),
                            fill="red", outline="red")

    # Four edges
    canvas.create_rectangle((OFFSET + BORDER_SIZE), (OFFSET - BORDER_SIZE),
                            (CANVAS_WIDTH - OFFSET - BORDER_SIZE), (OFFSET + BORDER_SIZE),
                            fill="red", outline="red")
    canvas.create_rectangle((OFFSET + BORDER_SIZE), (CANVAS_HEIGHT - OFFSET - BORDER_SIZE),
                            (CANVAS_WIDTH - OFFSET - BORDER_SIZE), (CANVAS_HEIGHT - OFFSET + BORDER_SIZE),
                            fill="red", outline="red")
    canvas.create_rectangle((OFFSET - BORDER_SIZE), (OFFSET + BORDER_SIZE),
                            (OFFSET + BORDER_SIZE), (CANVAS_HEIGHT - OFFSET - BORDER_SIZE),
                            fill="red", outline="red")
    canvas.create_rectangle((CANVAS_WIDTH - OFFSET - BORDER_SIZE), (OFFSET + BORDER_SIZE),
                            (CANVAS_WIDTH - OFFSET + BORDER_SIZE), (CANVAS_HEIGHT - OFFSET - BORDER_SIZE),
                            fill="red", outline="red")

    # Corners of each cell
    for i in range(OFFSET + CELL_SIZE, CANVAS_WIDTH - OFFSET, CELL_SIZE):
        for j in range(OFFSET + CELL_SIZE, CANVAS_WIDTH - OFFSET, CELL_SIZE):
            canvas.create_rectangle((j - BORDER_SIZE), (i - BORDER_SIZE),
                                    (j + BORDER_SIZE), (i + BORDER_SIZE),
                                    fill="red", outline="red")

def display_grid(CANVAS_WIDTH, CANVAS_HEIGHT, OFFSET, CELL_SIZE, BORDER_SIZE):
    # Garbage
    for i in range(15):
        for j in range(16):
            if horiz_data[i][j] == 1:
                canvas.create_rectangle((CELL_SIZE * j) + OFFSET + BORDER_SIZE,
                                        CANVAS_HEIGHT - (CELL_SIZE * i) - (2 * OFFSET) - BORDER_SIZE,
                                        (CELL_SIZE * (j + 1)) + OFFSET - BORDER_SIZE,
                                        CANVAS_HEIGHT - (CELL_SIZE * i) - (2 * OFFSET) + BORDER_SIZE,
                                        fill="red", outline="red")

    # Also garbage
    for i in range(16):
        for j in range(15):
            if vert_data[i][j] == 1:
                canvas.create_rectangle((CELL_SIZE * j) + (2 * OFFSET) - BORDER_SIZE,
                                        CANVAS_HEIGHT - (CELL_SIZE * i) - OFFSET - BORDER_SIZE,
                                        (CELL_SIZE * j) + (2 * OFFSET) + BORDER_SIZE,
                                        CANVAS_HEIGHT - (CELL_SIZE * (i + 1)) - OFFSET + BORDER_SIZE,
                                        fill="red", outline="red")

def displaySolution(sol_array, color):
    cur_index_x = 0
    cur_index_y = 0
    next_index_x = 0
    next_index_y = 0
    for val in sol_array:
        if val == 0:
            next_index_y -= 1
        elif val == 1:
            next_index_x += 1
        elif val == 2:
            next_index_y += 1
        elif val == 3:
            next_index_x -= 1
        canvas.create_line((40 * cur_index_x) + SOL_OFFSET,
                           CANVAS_HEIGHT - (40 * cur_index_y) - SOL_OFFSET,
                           (40 * next_index_x) + SOL_OFFSET,
                           CANVAS_HEIGHT - (40 * next_index_y) - SOL_OFFSET,
                           fill=color, width=4, tags="line")
        cur_index_x = next_index_x
        cur_index_y = next_index_y

def displayGridDist(dist_array):
    for i in range(16):
        for j in range(16):
            canvas.create_text((40 * j) + SOL_OFFSET, CANVAS_HEIGHT - (40 * i) - SOL_OFFSET, text=dist_array[i][j], font=("Helvetica", 16))

def validDirections():
    global cur_mouse_y, cur_mouse_x
    dir_array = np.zeros(4, dtype=int)
    if cur_mouse_y != 0:
        if horiz_data[cur_mouse_y - 1][cur_mouse_x] == 0:
            dir_array[DOWN] = 1
    if cur_mouse_x != 15:
        if vert_data[cur_mouse_y][cur_mouse_x] == 0:
            dir_array[RIGHT] = 1
    if cur_mouse_y != 15:
        if horiz_data[cur_mouse_y][cur_mouse_x] == 0:
            dir_array[UP] = 1
    if cur_mouse_x != 0:
        if vert_data[cur_mouse_y][cur_mouse_x - 1] == 0:
            dir_array[LEFT] = 1
    # print("valid: ", dir_array)
    return dir_array

def idealDirections():
    ideal = np.zeros(4, dtype=int)
    global has_been, cur_mouse_y, cur_mouse_x
    val_dir = validDirections()
    if cur_mouse_y != 0:
        if (has_been[cur_mouse_y - 1][cur_mouse_x] == 0) and (val_dir[DOWN] == 1):
            ideal[DOWN] = 1
    if cur_mouse_x != 15:
        if (has_been[cur_mouse_y][cur_mouse_x + 1] == 0) and (val_dir[RIGHT] == 1):
            ideal[RIGHT] = 1
    if cur_mouse_y != 15:
        if (has_been[cur_mouse_y + 1][cur_mouse_x] == 0) and (val_dir[UP] == 1):
            ideal[UP] = 1
    if cur_mouse_x != 0:
        if (has_been[cur_mouse_y][cur_mouse_x - 1] == 0) and (val_dir[LEFT] == 1):
            ideal[LEFT] = 1
    # print("ideal: ", ideal)
    return ideal

def directionChoice(ideal_dir):
    dir_choice_num = random.randint(1, np.sum(ideal_dir))
    count = 0
    actual_direction = 0
    for i in range(4):
        if ideal_dir[i] == 1:
            count += 1
        if count == dir_choice_num:
            actual_direction = i
            break
    return actual_direction

def chooseDirection():
    global cur_mouse_y, cur_mouse_x, last_fork_y, last_fork_x
    ideal_dir = idealDirections()
    if np.sum(ideal_dir) > 1:
        last_fork_y.append(cur_mouse_y)
        last_fork_x.append(cur_mouse_x)
    return directionChoice(ideal_dir)



def reachedEnd():
    global cur_mouse_y, cur_mouse_x
    if (cur_mouse_y == 7 or cur_mouse_y == 8) and (cur_mouse_x == 7 or cur_mouse_x == 8):
        return True
    return False

def move(direction):
    global has_been, cur_mouse_y, cur_mouse_x
    if direction == DOWN:
        cur_mouse_y -= 1
    if direction == RIGHT:
        cur_mouse_x += 1
    if direction == UP:
        cur_mouse_y += 1
    if direction == LEFT:
        cur_mouse_x -= 1
    has_been[cur_mouse_y][cur_mouse_x] = 1


filename = input("Enter a file name: ")
filename = "saved_mazes/" + filename
print("File: ", filename)

try:
    with open(filename, "rb") as file:
        data = np.frombuffer(file.read(), dtype=np.bool)
except FileNotFoundError:
    print("File not found")
    exit()

horiz_data = data[0:240]
vert_data = data[240:480]
horiz_data = horiz_data.reshape(15, 16)
vert_data = vert_data.reshape(16, 15)

"""-------------------------------------------------------------------------"""

path_chosen = []
path_since_fork = []
has_been = np.zeros((16, 16), dtype=int)
has_been[0][0] = 1

cur_mouse_y = 0
cur_mouse_x = 0

last_fork_y = [0]
last_fork_x = [0]

return_to_fork = False

while not reachedEnd():
#for i in range(100):
    if np.sum(idealDirections()) == 0:
        return_to_fork = True
    if return_to_fork:
        direction = (path_since_fork.pop() + 2) % 4
    else:
        direction = chooseDirection()
        path_since_fork.append(direction)
    path_chosen.append(direction)
    move(direction)
    if (cur_mouse_y == last_fork_y[-1]) and (cur_mouse_x == last_fork_x[-1]):
        return_to_fork = False
        last_fork_y.pop()
        last_fork_x.pop()

"""print("fork? ", return_to_fork)
print("y x: ", cur_mouse_y, cur_mouse_x)
print("last fork: ", last_fork_y, last_fork_x)
print("path: ", path_chosen)
print("path since fork: ", path_since_fork)"""






# The stuff that actually shows up
root = tk.Tk()
root.title("Maze Thingy")

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack()

canvas_setup(CANVAS_WIDTH, CANVAS_HEIGHT, OFFSET, CELL_SIZE, BORDER_SIZE)

display_grid(CANVAS_WIDTH, CANVAS_HEIGHT, OFFSET, CELL_SIZE, BORDER_SIZE)

button = tk.Button(root, text="Toggle Solution", command=fast_solution_button)
button.pack(pady=10)

# displayGridDist(dist_array)

root.mainloop()
