import numpy as np
import tkinter as tk
import queue

CELL_LENGTH = 16

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

display_grid_dist = True
display_forward = True
display_return = True
display_solution = True

def toggleDisplayGridDist():
    global display_grid_dist, dist_array
    if display_grid_dist:
        displayGridDist(dist_array)
        display_grid_dist = False
    else:
        canvas.delete("dstgrd")
        display_grid_dist = True

def toggleForward():
    global display_forward, mouse_moves
    if display_forward:
        displaySolution(mouse_moves, "blue", "forward", 0, 0)
        display_forward = False
    else:
        canvas.delete("forward")
        display_forward = True

def toggleReturn():
    global display_return, mouse_return_path, mouse_goal_y, mouse_goal_x
    if display_return:
        displaySolution(mouse_return_path, "green", "return", mouse_goal_y, mouse_goal_x)
        display_return = False
    else:
        canvas.delete("return")
        display_return = True

def toggleSolution():
    global display_solution, mouse_best_solution
    if display_solution:
        displaySolution(mouse_best_solution, "orange", "sol", 0, 0)
        display_solution = False
    else:
        canvas.delete("sol")
        display_solution = True

def canvas_setup():
    global CANVAS_WIDTH, CANVAS_HEIGHT, OFFSET, CELL_SIZE, BORDER_SIZE
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

def display_grid(cur_data_horiz, cur_data_vert):
    global CANVAS_WIDTH, CANVAS_HEIGHT, OFFSET, CELL_SIZE, BORDER_SIZE
    # Garbage
    for i in range(15):
        for j in range(16):
            if cur_data_horiz[i][j] == 1:
                canvas.create_rectangle((CELL_SIZE * j) + OFFSET + BORDER_SIZE,
                                        CANVAS_HEIGHT - (CELL_SIZE * i) - (2 * OFFSET) - BORDER_SIZE,
                                        (CELL_SIZE * (j + 1)) + OFFSET - BORDER_SIZE,
                                        CANVAS_HEIGHT - (CELL_SIZE * i) - (2 * OFFSET) + BORDER_SIZE,
                                        fill="red", outline="red")

    # Also garbage
    for i in range(16):
        for j in range(15):
            if cur_data_vert[i][j] == 1:
                canvas.create_rectangle((CELL_SIZE * j) + (2 * OFFSET) - BORDER_SIZE,
                                        CANVAS_HEIGHT - (CELL_SIZE * i) - OFFSET - BORDER_SIZE,
                                        (CELL_SIZE * j) + (2 * OFFSET) + BORDER_SIZE,
                                        CANVAS_HEIGHT - (CELL_SIZE * (i + 1)) - OFFSET + BORDER_SIZE,
                                        fill="red", outline="red")

def displayGridDist(dist_array):
    for i in range(16):
        for j in range(16):
            canvas.create_text((40 * j) + SOL_OFFSET, CANVAS_HEIGHT - (40 * i) - SOL_OFFSET, text=dist_array[i][j], font=("Helvetica", 16), tags="dstgrd")

def displaySolution(sol_array, color, tag, off_y, off_x):
    cur_index_y = off_y
    cur_index_x = off_x
    next_index_y = off_y
    next_index_x = off_x
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
                           fill=color, width=4, tags=tag)
        cur_index_x = next_index_x
        cur_index_y = next_index_y

def validCells(y, x, horiz_data, vert_data, acc_array):
    valid_array = np.zeros(4, dtype=int)
    if y != 0:
        if (acc_array[y - 1][x] == 0) and (horiz_data[y - 1][x] == 0):
            valid_array[DOWN] = 1
    if x != 15:
        if (acc_array[y][x + 1] == 0) and (vert_data[y][x] == 0):
            valid_array[RIGHT] = 1
    if y != 15:
        if (acc_array[y + 1][x] == 0) and (horiz_data[y][x] == 0):
            valid_array[UP] = 1
    if x != 0:
        if (acc_array[y][x - 1] == 0) and (vert_data[y][x - 1] == 0):
            valid_array[LEFT] = 1
    return valid_array

def fillAvailableCells(y, x, valid, num, dist_array, acc_array, coords_q):
    if valid[DOWN] == 1:
        dist_array[y - 1][x] = num
        acc_array[y - 1][x] = 1
        coords_q.put((y - 1, x, num))
    if valid[RIGHT] == 1:
        dist_array[y][x + 1] = num
        acc_array[y][x + 1] = 1
        coords_q.put((y, x + 1, num))
    if valid[UP] == 1:
        dist_array[y + 1][x] = num
        acc_array[y + 1][x] = 1
        coords_q.put((y + 1, x, num))
    if valid[LEFT] == 1:
        dist_array[y][x - 1] = num
        acc_array[y][x - 1] = 1
        coords_q.put((y, x - 1, num))

def calcDistArray(horiz_data, vert_data, return_path):
    dist_array = np.zeros((16, 16), dtype=int)
    acc_array = np.zeros((16, 16), dtype=np.bool)
    coords_q = queue.Queue()
    if return_path:
        acc_array[0][0] = 1
        coords_q.put((0, 0, 0))
    else:
        acc_array[7][7] = 1
        acc_array[7][8] = 1
        acc_array[8][7] = 1
        acc_array[8][8] = 1
        coords_q.put((7, 7, 0))
        coords_q.put((7, 8, 0))
        coords_q.put((8, 7, 0))
        coords_q.put((8, 8, 0))

    while coords_q.qsize() != 0:
        coords = coords_q.get()
        y = coords[0]
        x = coords[1]
        value = coords[2]
        valid_cells = validCells(y, x, horiz_data, vert_data, acc_array)
        fillAvailableCells(y, x, valid_cells, value + 1, dist_array, acc_array, coords_q)
    return dist_array

def validDirection(y, x, horiz_data, vert_data):
    valid_array = np.zeros(4, dtype=int)
    if y != 0:
        if horiz_data[y - 1][x] == 0:
            valid_array[DOWN] = 1
    if x != 15:
        if vert_data[y][x] == 0:
            valid_array[RIGHT] = 1
    if y != 15:
        if horiz_data[y][x] == 0:
            valid_array[UP] = 1
    if x != 0:
        if vert_data[y][x - 1] == 0:
            valid_array[LEFT] = 1
    return valid_array

def reachedEnd(y, x, iterations, return_path):
    if return_path:
        if (y == 0) and (x == 0):
            return True
    else:
        if (y == 7 or y == 8) and (x == 7 or x == 8):
            return True
    if (iterations > 256):
        print("No Solution/Failed to find solution")
        return True
    return False

def calculateSolution(dist_array, horiz_array, vert_array):
    global solution
    local_y, local_x = 0, 0
    iter_count = 0
    while not reachedEnd(local_y, local_x, iter_count, False):
        temp_dist = dist_array[local_y][local_x]
        valid_directions = validDirection(local_y, local_x, horiz_array, vert_array)
        if (valid_directions[DOWN] == 1) and (dist_array[local_y - 1][local_x] < temp_dist):
            solution.append(DOWN)
            local_y -= 1
        elif (valid_directions[RIGHT] == 1) and (dist_array[local_y][local_x + 1] < temp_dist):
            solution.append(RIGHT)
            local_x += 1
        elif (valid_directions[UP] == 1) and (dist_array[local_y + 1][local_x] < temp_dist):
            solution.append(UP)
            local_y += 1
        elif (valid_directions[LEFT] == 1) and (dist_array[local_y][local_x - 1] < temp_dist):
            solution.append(LEFT)
            local_x -= 1
        iter_count += 1

def gatherData(y, x, cur_horiz_data, cur_vert_data):
    global complete_horiz_data, complete_vert_data
    if y != 0:
        cur_horiz_data[y - 1][x] = complete_horiz_data[y - 1][x]
    if x != 15:
        cur_vert_data[y][x] = complete_vert_data[y][x]
    if y != 15:
        cur_horiz_data[y][x] = complete_horiz_data[y][x]
    if x != 0:
        cur_vert_data[y][x - 1] = complete_vert_data[y][x - 1]

def mouseDirection(y, x, dist_array, horiz_data, vert_data):
    global mouse_y, mouse_x
    valid_directions = validDirection(y, x, horiz_data, vert_data)
    temp_dist = dist_array[y][x]
    if (valid_directions[DOWN] == 1) and (dist_array[y - 1][x] < temp_dist):
        mouse_y -= 1
        return DOWN
    elif (valid_directions[RIGHT] == 1) and (dist_array[y][x + 1] < temp_dist):
        mouse_x += 1
        return RIGHT
    elif (valid_directions[UP] == 1) and (dist_array[y + 1][x] < temp_dist):
        mouse_y += 1
        return UP
    elif (valid_directions[LEFT] == 1) and (dist_array[y][x - 1] < temp_dist):
        mouse_x -= 1
        return LEFT
    return -1



filename = "saved_mazes/qwerty.txt"
print("File: ", filename)

try:
    with open(filename, "rb") as file:
        data = np.frombuffer(file.read(), dtype=np.bool)
except:
    print("File not Found")

complete_horiz_data = data[0:240]
complete_vert_data = data[240:480]
complete_horiz_data = complete_horiz_data.reshape(15, 16)
complete_vert_data = complete_vert_data.reshape(16, 15)

current_horiz_data = np.zeros((15, 16), dtype=np.bool)
current_vert_data = np.zeros((16, 15), dtype=np.bool)



mouse_moves = []
mouse_y, mouse_x = 0, 0
iter_count = 0

while not reachedEnd(mouse_y, mouse_x, iter_count, False):
    gatherData(mouse_y, mouse_x, current_horiz_data, current_vert_data)
    dist_array = calcDistArray(current_horiz_data, current_vert_data, False)
    mouse_moves.append(mouseDirection(mouse_y, mouse_x, dist_array, current_horiz_data, current_vert_data))
    iter_count += 1

mouse_goal_y = mouse_y
mouse_goal_x = mouse_x

# To see if there are more entrances to the goal
gatherData(7, 7, current_horiz_data, current_vert_data)
gatherData(7, 8, current_horiz_data, current_vert_data)
gatherData(8, 7, current_horiz_data, current_vert_data)
gatherData(8, 8, current_horiz_data, current_vert_data)
dist_array = calcDistArray(current_horiz_data, current_vert_data, False)

# Return path needs to check for any shortcuts (any time numbers count down instead of up on the return path)
# maybe just flood fill from (0, 0) to return there



mouse_return_path = []
iter_count = 0

while not reachedEnd(mouse_y, mouse_x, iter_count, True):
    gatherData(mouse_y, mouse_x, current_horiz_data, current_vert_data)
    dist_array = calcDistArray(current_horiz_data, current_vert_data, True)
    mouse_return_path.append(mouseDirection(mouse_y, mouse_x, dist_array, current_horiz_data, current_vert_data))
    iter_count += 1



mouse_best_solution = []
mouse_y, mouse_x = 0, 0
iter_count = 0

dist_array = calcDistArray(current_horiz_data, current_vert_data, False)

while not reachedEnd(mouse_y, mouse_x, iter_count, False):
    mouse_best_solution.append(mouseDirection(mouse_y, mouse_x, dist_array, current_horiz_data, current_vert_data))
    iter_count += 1








# The stuff that actually shows up
root = tk.Tk()
root.title("Maze Thingy")
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack()
canvas_setup()
# display_grid(complete_horiz_data, complete_vert_data)
display_grid(current_horiz_data, current_vert_data)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

grid_dist_button = tk.Button(button_frame, text="Toggle Dist Grid", command=toggleDisplayGridDist)
grid_dist_button.pack(side="left", padx=10)
forward_path_button = tk.Button(button_frame, text="Toggle Forward", command=toggleForward)
forward_path_button.pack(side="left", padx=10)
return_path_button = tk.Button(button_frame, text="Toggle Return", command=toggleReturn)
return_path_button.pack(side="left", padx=10)
best_solution_button = tk.Button(button_frame, text="Toggle Best Solution", command=toggleSolution)
best_solution_button.pack(side="left", padx=10)

root.mainloop()
