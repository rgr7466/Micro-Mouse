import tkinter as tk
from queue import PriorityQueue

STRAIGHT_COST = 1
DIAGONAL_COST = 0.7
TURN_COST = 0.4

TOP = 1
MIDDLE = 0
BOTTOM = -1

maze_rows = 3
maze_cols = 10

"""-------------------------------------------------------------------------"""

CANVAS_WIDTH = 720
CANVAS_HEIGHT = 720
OFFSET = 40
CELL_SIZE = 40
HALF = 20

# double this value to add and subtract
BORDER = 2
RAD = 3

def mazeDisplay(maze, maze_rows, maze_cols):

    START_X = (CELL_SIZE * maze_cols) + OFFSET
    START_Y = (CELL_SIZE * maze_rows) + OFFSET
    # Corners
    canvas.create_rectangle(OFFSET - BORDER, OFFSET - BORDER,
                            OFFSET + BORDER, OFFSET + BORDER,
                            fill="red", outline="red")
    canvas.create_rectangle(START_X - BORDER, OFFSET - BORDER,
                            START_X + BORDER, OFFSET + BORDER,
                            fill="red", outline="red")
    canvas.create_rectangle(OFFSET - BORDER, START_Y - BORDER,
                            OFFSET + BORDER, START_Y + BORDER,
                            fill="red", outline="red")
    canvas.create_rectangle(START_X - BORDER, START_Y - BORDER,
                            START_X + BORDER, START_Y + BORDER,
                            fill="red", outline="red")
    # Maze edges
    canvas.create_rectangle(OFFSET - BORDER, OFFSET + BORDER,
                            OFFSET + BORDER, START_Y - BORDER,
                            fill="red", outline="red")
    canvas.create_rectangle(OFFSET + BORDER, OFFSET - BORDER,
                            START_X + BORDER, OFFSET + BORDER,
                            fill="red", outline="red")
    canvas.create_rectangle(START_X - BORDER, OFFSET + BORDER,
                            START_X + BORDER, START_Y - BORDER,
                            fill="red", outline="red")
    canvas.create_rectangle(OFFSET + BORDER, START_Y - BORDER,
                            START_X + BORDER, START_Y + BORDER,
                            fill="red", outline="red")
    for row in range(1, maze_rows):
        for col in range(1, maze_cols):
            canvas.create_rectangle((CELL_SIZE * col) + OFFSET - BORDER, (CELL_SIZE * row) + OFFSET - BORDER,
                                    (CELL_SIZE * col) + OFFSET + BORDER, (CELL_SIZE * row) + OFFSET + BORDER,
                                    fill="red", outline="red")
    for row in range(2 * maze_rows - 1):
        for col in range(maze_cols - 1 + (row % 2)):
            if maze[row][col] == 1:
                if row % 2 == 0:
                    canvas.create_rectangle((CELL_SIZE * col) + (2 * OFFSET) - BORDER, START_Y - (HALF * row) - BORDER,
                                            (CELL_SIZE * col) + (2 * OFFSET) + BORDER, START_Y - (HALF * (2 + row)) + BORDER,
                                            fill="red", outline="red")
                else:
                    canvas.create_rectangle((CELL_SIZE * col) + OFFSET + BORDER, START_Y - (HALF * row) - HALF - BORDER,
                                            (CELL_SIZE * (1 + col)) + OFFSET - BORDER, START_Y - (HALF * row) - HALF + BORDER,
                                            fill="red", outline="red")

def nodeVisualizer(graph, maze_rows, maze_cols, end_y, end_x):
    START_Y = (CELL_SIZE * maze_rows) + OFFSET
    for row in range(2 * maze_rows - 1):
        for col in range(maze_cols - 1 + (row % 2)):
            if (row, col, MIDDLE) in graph:
                if row % 2 == 0:
                    node_x = (CELL_SIZE * col) + (2 * OFFSET)
                    node_y = START_Y - (HALF * row) - HALF
                    canvas.create_oval(node_x - RAD, node_y - RAD,
                                       node_x + RAD, node_y + RAD,
                                       outline="black")
                else:
                    node_x = (CELL_SIZE * col) + OFFSET + HALF
                    node_y = START_Y - (HALF * row) - HALF
                    canvas.create_oval(node_x - RAD, node_y - RAD,
                                       node_x + RAD, node_y + RAD,
                                       outline="black")
    # start and end nodes
    canvas.create_oval(OFFSET + HALF - RAD - RAD, START_Y - HALF - RAD - RAD,
                       OFFSET + HALF + RAD + RAD, START_Y - HALF + RAD + RAD,
                       outline="green")
    canvas.create_oval((CELL_SIZE * end_x) + HALF - RAD - RAD, START_Y - (CELL_SIZE * end_y) + HALF - RAD - RAD,
                       (CELL_SIZE * end_x) + HALF + RAD + RAD, START_Y - (CELL_SIZE * end_y) + HALF + RAD + RAD,
                       outline="green")

def solutionVisualizer(graph, start, end, maze_rows, maze_cols, end_y, end_x):
    START_Y = (CELL_SIZE * maze_rows) + OFFSET
    tail = start
    head = start
    while head != end:
        tail = head
        head = graph[head]
        # print(f"tail: {tail},    head: {head}")
        x0 = 0
        y0 = 0
        x1 = 0
        y1 = 0
        if tail == start:
            x0 = OFFSET + HALF
            y0 = (CELL_SIZE * maze_rows) + HALF
        else:
            x0 = (CELL_SIZE * tail[1]) + (2 * OFFSET) - (HALF * (tail[0] % 2))
            y0 = START_Y - (HALF * tail[0]) - HALF

        if head == end:
            x1 = (CELL_SIZE * end_x) + HALF
            y1 = START_Y - (CELL_SIZE * end_y) + HALF
        else:
            x1 = (CELL_SIZE * head[1]) + (2 * OFFSET) - (HALF * (head[0] % 2))
            y1 = START_Y - (HALF * head[0]) - HALF
        canvas.create_line(x0, y0, x1, y1)

"""-------------------------------------------------------------------------"""

def dijkstra(adjList, start, end):
    pq = PriorityQueue()
    pq.put((0, start, 0))
    distList = {}
    retList = {}
    while not pq.empty():
        cur_dist, node, prev = pq.get()
        if node in distList:
            continue
        distList[node] = cur_dist
        retList[node] = prev
        if node != end:
            for neighbor, weight in adjList[node].items():
                if neighbor not in distList:
                    pq.put((cur_dist + weight, neighbor, node))
        else:
            while not pq.empty():
                pq.get(False)
    return distList, retList

def addEdge(graph, u, v, weight):
    if u not in graph:
        graph[u] = {}
    if v not in graph:
        graph[v] = {}
    graph[u][v] = weight
    graph[v][u] = weight

def returnPath(retList, start, end):
    nodeList = {}
    cur_node = end
    while cur_node != start:
        nodeList[retList[cur_node]] = cur_node
        cur_node = retList[cur_node]
    return nodeList

def displayDict(dictionary):
    for node, neighbors in dictionary.items():
        print(f"node: {node},   neighbors: {neighbors}")

def connectLayerNodes(graph, row, col, maze):
    if maze[r][c] == 0:
        addEdge(graph, (row, col, TOP), (row, col, MIDDLE), TURN_COST)
        addEdge(graph, (row, col, MIDDLE), (row, col, BOTTOM), TURN_COST)

def connectTopDiagonal(graph, row, col, maze):
    global maze_rows, maze_cols
    if maze[row][col] == 0:
        if (row + 1) < 2 * maze_rows - 1 and (col + 1) < maze_cols:
            row2 = row + 1
            col2 = col + 1 - (row % 2)
            if maze[row2][col2] == 0:
                addEdge(graph, (row, col, TOP), (row2, col2, TOP), DIAGONAL_COST)

def connectBottomDiagonal(graph, row, col, maze):
    global maze_rows, maze_cols
    if maze[row][col] == 0:
        if (row - 1) > -1 and (col + 1) < maze_cols:
            row2 = row - 1
            col2 = col + 1 - (row % 2)
            if maze[row2][col2] == 0:
                addEdge(graph, (row, col, BOTTOM), (row2, col2, BOTTOM), DIAGONAL_COST)

def connectStraights(graph, row, col, maze):
    global maze_rows, maze_cols
    if maze[row][col] == 0:
        if row % 2 == 0:
            if col + 1 < maze_cols - 1:
                if maze[row][col + 1] == 0:
                    addEdge(graph, (row, col, MIDDLE), (row, col + 1, MIDDLE), STRAIGHT_COST)
        else:
            if row + 2 < 2 * maze_rows - 1:
                if maze[row + 2][col] == 0:
                    addEdge(graph, (row, col, MIDDLE), (row + 2, col, MIDDLE), STRAIGHT_COST)

def connectSurroundingNodes(graph, row, col, maze):
    connectTopDiagonal(graph, row, col, maze)
    connectBottomDiagonal(graph, row, col, maze)
    connectStraights(graph, row, col, maze)



START = (69, 69, 0)
END = (420, 420, 0)

mazeWalls = [[1, 0, 1, 0, 1, 0, 1, 0, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 1, 0, 1, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 1, 0, 1, 0, 1, 0, 1]]

nodes = {}

# each vertex need three different pieces of info for the key:
# The x and y coords (not 1 to 1 from maze cells) and the layer level (1, 0, -1)

for r in range(2 * maze_rows - 1):
    for c in range(maze_cols - 1 + (r % 2)):
        # print(f"{row}, {col}")
        connectLayerNodes(nodes, r, c, mazeWalls)
        connectSurroundingNodes(nodes, r, c, mazeWalls)

addEdge(nodes, START, (1, 0, 0), STRAIGHT_COST)
addEdge(nodes, END, (3, 9, 0), STRAIGHT_COST)

# displayDict(nodes)

dist, ret = dijkstra(nodes, START, END)

retSolved = returnPath(ret, START, END)

# print(dist)

# print(retSolved)

root = tk.Tk()
root.title("Dijkstra Maze Visualizer")
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack()

mazeDisplay(mazeWalls, maze_rows, maze_cols)
nodeVisualizer(nodes, maze_rows, maze_cols, 3, 10)
solutionVisualizer(retSolved, START, END, maze_rows, maze_cols, 3, 10)

root.mainloop()
