import numpy as np 

def read_input(filename: str = "input.txt"):
    with open(filename, "r") as f:
        grid = f.read()
        grid = [np.array(list(a)) for a in grid.replace("-","─").replace("|","│").replace("F","┌").replace("L","└").replace("7","┐").replace("J","┘").replace("."," ").split("\n")]
        np_grid = np.array(grid)
        return np_grid


def check_neighbors(grid, my, mx):
    my_location = grid[my][mx] # Y and X are flipped :) 
    def get_adjacents(grid, x, y):
        adjacents = [(-1, 0), (0, -1), (0, 1), (1, 0)]  # Up, Left, Right, Down
        return [(x + dx, y + dy) for dx, dy in adjacents if 0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0])]

    # Define connections based on direction

    connections = {
        "┌": {
            "up": [],
            "down": ["│", "└", "┘"],
            "left": [],
            "right": ["─", "┐", "┘"]
        },
        "└": {
            "up": ["│", "┌", "┐"],
            "down": [],
            "left": [],
            "right": ["─", "┘", "┐"]
        },
        "┐": {
            "up": [],
            "down": ["│", "┘", "└"],
            "left": ["─", "└", "┌"],
            "right": []
        },
        "┘": {
            "up": ["│", "┌", "┐"],
            "down": [],
            "left": ["─", "└", "┌"],
            "right": []
        },
        "─": {
            "up": [],
            "down": [],
            "left": ["┌", "┘", "└", "┐", "─"],
            "right": ["┌", "┘", "└", "┐", "─"]
        },
        "│": {
            "up": ["┌", "│", "┐"],
            "down": ["┘", "└", "│"],
            "left": [],
            "right": []
        }
    }

    my_connections = connections[my_location]

    adjacents = get_adjacents(grid, mx, my)
    neighbors = []
    for x, y in adjacents:
        direction = ""
        if y > my:
            direction = "down"
        elif y < my:
            direction = "up"
        elif x > mx:
            direction = "right"
        elif x < mx:
            direction = "left"
        
        neighbor = grid[y][x]


        if neighbor in my_connections[direction]:
            neighbors.append((y, x))

    return neighbors

def fix_s_pipe(G, r, c):

    up_valid = (G[r-1][c] in ['│','┐','┌'])
    right_valid = (G[r][c+1] in ['─','┐','┘'])
    down_valid = (G[r+1][c] in ['│','└','┘'])
    left_valid = (G[r][c-1] in ['─','L','┌'])
    if up_valid and down_valid:
        G[r][c]='│'
    elif up_valid and right_valid:
        G[r][c]='└'
    elif up_valid and left_valid:
        G[r][c]='┘'
    elif down_valid and right_valid:
        G[r][c]='┌'
    elif down_valid and left_valid:
        G[r][c]='┐'
    elif left_valid and right_valid:
        G[r][c]='─'

def part1(grid):
    s_location = np.argwhere(grid == "S")
    fix_s_pipe(grid, s_location[0][0], s_location[0][1])

    start_neighbors = check_neighbors(grid, s_location[0][0], s_location[0][1])
    visited = [start_neighbors[0]]
    my_location = (s_location[0][0], s_location[0][1])

    steps = 1
    while True:
        steps += 1
        visited.append(my_location)

        my_neighbours = check_neighbors(grid, my_location[0], my_location[1])
        my_unvisited_neighbors = [n for n in my_neighbours if n not in visited]
        if len(my_unvisited_neighbors) == 0:
            break
        my_location = my_unvisited_neighbors[0]
        # Remove visited



    print(steps)
    return (steps / 2), visited

def part2(grid, loop):
    from matplotlib.path import Path

    path = Path(loop)
    ans = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (x, y) in loop:
                continue
            if path.contains_point((x, y)):
                ans += 1
    print(ans)


if __name__ == "__main__":  
    data = read_input()
    p1, loop = part1(data)
    print(f"Part 1: {p1}")
    part2(data, loop)