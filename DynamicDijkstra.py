from queue import PriorityQueue

STRAIGHT_COST = 1
TURN_COST = 2

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
                pq.put((cur_dist + weight, neighbor, node))
        else:
            while not pq.empty():
                pq.get(False)
    return distList, retList

def returnPath(retList, start, end):
    nodes = []
    cur_node = end
    while cur_node != start:
        nodes.append(cur_node)
        cur_node = retList[cur_node]
    nodes.append(start)
    nodes.reverse()
    return nodes

def displayDict(dictionary):
    for node, neighbors in dictionary.items():
        print(f"node: {node},   neighbors: {neighbors}")

def addEdge(graph, u, v, weight):
    if u not in graph:
        graph[u] = {}
    if v not in graph:
        graph[v] = {}
    graph[u][v] = weight
    graph[v][u] = weight

def updateGraph(maze, r, c, graph, maze_dim):
    if r % 2 == 0: # vertical edges
        if c > 0:
            if maze[r][c - 1] == 0:
                addEdge(graph, (r, c), (r, c - 1), STRAIGHT_COST)
        if r > 0:
            if maze[r - 1][c] == 0:
                addEdge(graph, (r, c), (r - 1, c), TURN_COST)
        if r < (maze_dim[1] * 2 - 2):
            if maze[r + 1][c] == 0:
                addEdge(graph, (r, c), (r + 1, c), TURN_COST)
    else: # horizontal edges
        if r > 1:
            if maze[r - 2][c] == 0:
                addEdge(graph, (r, c), (r - 2, c), STRAIGHT_COST)
        if c > 0:
            if maze[r - 1][c - 1] == 0:
                addEdge(graph, (r, c), (r - 1, c - 1), TURN_COST)
            if maze[r + 1][c - 1] == 0:
                addEdge(graph, (r, c), (r + 1, c - 1), TURN_COST)



"""
# nodes: "A" = (0, 0), "B" = (0, 1), "C" = (1, 0), "D" = (1, 1)
adj = {(0, 0): {(0, 1): 3, (1, 0): 1, (1, 1): 5},
       (0, 1): {(0, 0): 3, (1, 0): 1, (1, 1): 1},
       (1, 0): {(0, 0): 1, (0, 1): 1, (1, 1): 4},
       (1, 1): {(0, 0): 5, (0, 1): 1, (1, 0): 4}}

dist, ret = dijkstra(adj, (0, 0), (1, 1))
return_nodes = returnPath(ret, (0, 0), (1, 1))

print(dist)
print(return_nodes)
# print(adj)
"""

START = (69, 69)
END = (420, 420)

mazeWalls = [[0, 1, 0, 0],
             [1, 0, 0, 0, 0],
             [0, 0, 1, 1],
             [0, 1, 1, 0, 0],
             [0, 1, 1, 0],
             [1, 0, 0, 1, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0, 0],
             [0, 0, 0, 1]]

nodes = {}

for row in range(9):
    for col in range(4 + (row % 2)):
        if mazeWalls[row][col] == 0:
            updateGraph(mazeWalls, row, col, nodes, (5, 5))

addEdge(nodes, START, (0, 0), 1)
addEdge(nodes, END, (5, 2), 1)

# displayDict(nodes)

dist, ret = dijkstra(nodes, START, END)
return_nodes = returnPath(ret, START, END)

print(return_nodes)


