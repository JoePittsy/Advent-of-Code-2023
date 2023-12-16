
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

@dataclass
class Laser:
    row: int
    col: int
    direction: Direction
    alive: bool = True

    @property
    def coords(self):
        return (self.row, self.col)


def read_input(filename: str = "input.txt") -> list:
    with open (filename, "r") as f: 
        return [list(line.strip()) for line in f.readlines()]


def solve_maze(maze, start_laser: Laser):
    def get_new_direction(current_direction, tile):
        direction_change_map = {
            (Direction.LEFT, '|'): (Direction.UP, Direction.DOWN),
            (Direction.RIGHT, '|'): (Direction.UP, Direction.DOWN),
            (Direction.UP, '-'): (Direction.LEFT, Direction.RIGHT),
            (Direction.DOWN, '-'): (Direction.LEFT, Direction.RIGHT),
            (Direction.RIGHT, '\\'): Direction.DOWN,
            (Direction.LEFT, '\\'): Direction.UP,
            (Direction.UP, '\\'): Direction.LEFT,
            (Direction.DOWN, '\\'): Direction.RIGHT,
            (Direction.RIGHT, '/'): Direction.UP,
            (Direction.LEFT, '/'): Direction.DOWN,
            (Direction.UP, '/'): Direction.RIGHT,
            (Direction.DOWN, '/'): Direction.LEFT,
        }
        return direction_change_map.get((current_direction, tile), current_direction)
    
    direction_deltas = {
        Direction.RIGHT: (0, 1),
        Direction.LEFT: (0, -1),
        Direction.UP: (-1, 0),
        Direction.DOWN: (1, 0)
    }

    lasers: [Laser] = [start_laser]
    energised_tiles = set()
    seen_lasers = set()

    while any(laser.alive for laser in lasers):
        for laser in lasers:
            if not laser.alive:
                continue

            delta_row, delta_col = direction_deltas[laser.direction]
            laser.row += delta_row
            laser.col += delta_col

            if not (0 <= laser.row < len(maze) and 0 <= laser.col < len(maze[0])):
                laser.alive = False
                continue

            laser_state = (laser.row, laser.col, laser.direction)
            if laser_state in seen_lasers:
                laser.alive = False
                continue

            seen_lasers.add(laser_state)
            energised_tiles.add(laser.coords) 

            new_tile = maze[laser.row][laser.col]
            directions = get_new_direction(laser.direction, new_tile)
            if isinstance(directions, tuple):
                lasers.append(Laser(laser.row, laser.col, directions[0]))
                lasers.append(Laser(laser.row, laser.col, directions[1]))
                laser.alive = False
            else:
                laser.direction = directions

    return len(energised_tiles)

def part1(maze):
    return solve_maze(maze, Laser(0, -1, Direction.RIGHT))


def part2(maze):
    c1, r1, c2, r2 = 0, 0, len(maze[0]), len(maze)
    left_edge = [Laser(c, r1-1, Direction.RIGHT) for c in range(c1, c2)]
    right_edge = [Laser(c, r2+1, Direction.LEFT) for c in range(c1, c2)]

    # Generate the left and right edges, excluding the corners
    top_edge = [Laser(c1-1, r, Direction.DOWN) for r in range(r1, r2)]
    bottom_edge = [Laser(c2+1, r, Direction.UP) for r in range(r1, r2)]

    corners = [
        Laser(c1-1, r1, Direction.RIGHT),
        Laser(c1, r1-1, Direction.DOWN),
        Laser(c2+1, r1, Direction.LEFT),
        Laser(c2, r1-1, Direction.DOWN),
        Laser(c1-1, r2, Direction.RIGHT),
        Laser(c1, r2+1, Direction.UP),
        Laser(c2+1, r2, Direction.LEFT),
        Laser(c2, r2+1, Direction.UP),
    ]

    # Combine all edges
    lasers = top_edge + bottom_edge + left_edge + right_edge + corners

    return max((solve_maze(maze, laser) for laser in lasers))


if __name__ == "__main__":
    maze = read_input()
    p1 = part1(maze)
    print(f"Part One: {p1}")
    p2 = part2(maze)
    print(f"Part Two: {p2}")