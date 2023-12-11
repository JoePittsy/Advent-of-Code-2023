import numpy as np 
from matplotlib.path import Path

def read_input(filename: str = "input.txt"):
    with open(filename, "r") as f:
        grid = f.read()
        grid = [np.array(list(a)) for a in grid.replace("-","─").replace("|","│").replace("F","┌").replace("L","└").replace("7","┐").replace("J","┘").replace("."," ").split("\n")]
        np_grid = np.array(grid)
        return np_grid


def check_neighbors(grid, my, mx):
    my_location = grid[my][mx] # Y and X are flipped :) 
    def get_adjacents(grid, x, y):
        directions = {
            (-1, 0): "left",
            (0, -1): "up",
            (0, 1): "down",
            (1, 0): "right"
        }
        return [((x + dx, y + dy), directions[(dx, dy)]) for dx, dy in directions if 0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0])]

    connections = {
        "┌": { "up": [], "down": ["│", "└", "┘"], "left": [], "right": ["─", "┐", "┘"] },
        "└": { "up": ["│", "┌", "┐"], "down": [], "left": [], "right": ["─", "┘", "┐"] },
        "┐": { "up": [], "down": ["│", "┘", "└"], "left": ["─", "└", "┌"], "right": [] },
        "┘": { "up": ["│", "┌", "┐"], "down": [], "left": ["─", "└", "┌"], "right": [] },
        "─": { "up": [], "down": [], "left": ["┌", "┘", "└", "┐", "─"], "right": ["┌", "┘", "└", "┐", "─"] },
        "│": { "up": ["┌", "│", "┐"], "down": ["┘", "└", "│"], "left": [], "right": [] }
    }

    return {(y, x) for (x, y), direction in get_adjacents(grid, mx, my) if grid[y][x] in connections[my_location][direction]}

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
    (start_y,), (start_x,) = np.where(grid == "S")

    # Initial setup
    fix_s_pipe(grid, start_y, start_x)
    my_location = (start_y, start_x)

    # Set for visited coordinates
    visited = {my_location}

    while True:
        my_neighbours = check_neighbors(grid, *my_location)
        my_unvisited_neighbors = my_neighbours - visited
        if not my_unvisited_neighbors:
            break  # No unvisited neighbors left, exit the loop
        my_location = my_unvisited_neighbors.pop()
        visited.add(my_location)

    steps = len(visited) // 2
    return steps, list(visited)




def part2(loop):
    path = Path(loop)

    min_x, min_y, max_x, max_y = path.get_extents().bounds

    # Create a grid of points within the bounding box of the loop, does not matter the pipe there so we don't even need the grid
    y_indices, x_indices = np.mgrid[int(min_y):int(max_y) + 1, int(min_x):int(max_x) + 1]
    all_points_within_bbox = np.vstack([x_indices.ravel(), y_indices.ravel()]).T

    # Filter out the points that are part of the loop
    loop_set = set(map(tuple, loop))  # Convert loop to a set for faster lookup
    bounded_points_not_part_of_loop = np.array([pt for pt in all_points_within_bbox if tuple(pt) not in loop_set])

    # Maybe it's a bit of a cheat to use the contains_points method, but it's fast and it works :)
    # I did implement a ray casting algorithm myself, but it was pretty damn slow. 
    # interesting how it works, if the ray intersects an odd number of times, the point is inside the loop 
    points_inside_loop = path.contains_points(bounded_points_not_part_of_loop)
    ans = np.sum(points_inside_loop)

    return ans

if __name__ == "__main__":  
    data = read_input()
    p1, loop = part1(data)
    print(f"Part 1: {p1}")
    print(f"Part 2: {part2(loop)}")
