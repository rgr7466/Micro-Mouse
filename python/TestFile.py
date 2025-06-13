import numpy as np
import tkinter as tk
import random

canvas_width = 720
canvas_height = 720
offset = 40
cell_size = 40

# double this value to add and subtract
border_size = 2

DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3

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
            if test_array_horiz[i][j] == 1:
                canvas.create_rectangle((cell_size * j) + offset + border_size,
                                        canvas_height - (cell_size * i) - (2 * offset) - border_size,
                                        (cell_size * (j + 1)) + offset - border_size,
                                        canvas_height - (cell_size * i) - (2 * offset) + border_size,
                                        fill="red", outline="red")

    # Also garbage
    for i in range(16):
        for j in range(15):
            if test_array_vert[i][j] == 1:
                canvas.create_rectangle((cell_size * j) + (2 * offset) - border_size,
                                        canvas_height - (cell_size * i) - offset - border_size,
                                        (cell_size * j) + (2 * offset) + border_size,
                                        canvas_height - (cell_size * (i + 1)) - offset + border_size,
                                        fill="red", outline="red")

def valid_directions(acc_array, x, y):
    dir = np.zeros(4)
    if acc_array[y][x] == 0:
        return dir
    if y != 0:
        if acc_array[y - 1][x] == 0:
            dir[0] = 1
    if x != 15:
        if acc_array[y][x + 1] == 0:
            dir[1] = 1
    if y != 15:
        if acc_array[y + 1][x] == 0:
            dir[2] = 1
    if x != 0:
        if acc_array[y][x - 1] == 0:
            dir[3] = 1
    return dir

def direction(possible_directions):
    dir_choice_num = random.randint(1, np.sum(possible_directions))
    count = 0
    actual_direction = 0
    for i in range(4):
        if possible_directions[i] == 1:
            count += 1
        if count == dir_choice_num:
            actual_direction = i
            break
    return actual_direction

def jump_to(acc_array):
    cur_guess_x = 0
    cur_guess_y = 0
    num_attempts = 0
    total_accessible = np.sum(acc_array)
    found_valid_coord = False
    while (found_valid_coord == False):
        count = 0
        found = False
        acc_choice = random.randint(1, total_accessible)
        for i in range(16):
            for j in range(16):
                if acc_array[i][j] == 1:
                    count += 1
                if count == acc_choice:
                    cur_guess_y = i
                    cur_guess_x = j
                    num_attempts += 1
                    found = True
                    break
            if found == True:
                break
        if np.sum(valid_directions(acc_array, cur_guess_x, cur_guess_y)) != 0:
            if np.sum(acc_array) == 4: # starting value
                found_valid_coord = True
            if not ((cur_guess_y == 7 or cur_guess_y == 8) and (cur_guess_x == 7 or cur_guess_x == 8)):
                found_valid_coord = True
    return cur_guess_y, cur_guess_x, num_attempts

"""---------------------------------------------------------"""

test_array_horiz = np.ones((15, 16), dtype=bool)
test_array_vert = np.ones((16, 15), dtype=bool)

accessible_array = np.zeros((16, 16), dtype=bool)

# Starting place
accessible_array[7][7] = 1
accessible_array[7][8] = 1
accessible_array[8][7] = 1
accessible_array[8][8] = 1

# Removing middle walls
test_array_horiz[7][7] = 0
test_array_horiz[7][8] = 0
test_array_vert[7][7] = 0
test_array_vert[8][7] = 0

index_x = 0
index_y = 0

done = False

jump_count = 0
attempt_count = 0
num_attempts = 0

while (done == False):
    possible_directions = valid_directions(accessible_array, index_x, index_y)
    if np.sum(possible_directions) == 0:
        # jump to new start point
        index_y, index_x, num_attempts = jump_to(accessible_array)
        jump_count += 1
        attempt_count += num_attempts

    else:
        actual_direction = direction(possible_directions)
        if actual_direction == DOWN:
            test_array_horiz[index_y - 1][index_x] = 0
            index_y -= 1
        elif actual_direction == RIGHT:
            test_array_vert[index_y][index_x] = 0
            index_x += 1
        elif actual_direction == UP:
            test_array_horiz[index_y][index_x] = 0
            index_y += 1
        elif actual_direction == LEFT:
            test_array_vert[index_y][index_x - 1] = 0
            index_x -= 1
        accessible_array[index_y][index_x] = 1

    if np.sum(accessible_array) == 256:
        done = True

print("jump_count:", jump_count)
print("jump attempt count:", attempt_count)



# The stuff that actually shows up
root = tk.Tk()
root.title("Maze Thingy")

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

canvas_setup(canvas_width, canvas_height, offset, cell_size, border_size)

display_grid(canvas_width, canvas_height, offset, cell_size, border_size)

root.mainloop()



user_save_prompt = input("Save maze? (y/n): ")

if user_save_prompt != "y":
    exit()

filename = input("Enter a file name (default - test.txt): ")

if not (".txt" in filename):
    filename = "test.txt"
    print("Changed name to test.txt")

filename = "saved_mazes/" + filename
print(filename)
file = open(filename, "wb")

file.write(test_array_horiz)
file.write(test_array_vert)

# each bool value is taking up a whole byte not sure how to change that
# Technically speaking it's fine as long as the data can be read the same way

file.close()
