
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

def read_input(filename: str = "input.txt") -> list:
    with open (filename, "r") as f: 
        return [list(line.strip()) for line in f.readlines()]
    
def pprint(input: list, energised_tiles) -> None:
    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if (row, col) in energised_tiles:
                print("#", end="")
            else:
                print(char, end="")
        print()

@dataclass
class Laser:
    row: int
    col: int
    direction: Direction
    alive: bool = True

    def __str__(self) -> str:
        return f"({self.row}, {self.col}) {self.direction.name}"

def solve_maze(maze, start_laser: Laser):
    lasers: [Laser] = [start_laser]
    energised_tiles = set()
    seen_lasers = set()

    while any(laser.alive for laser in lasers): 
        for laser in lasers:
            if not laser.alive:
                continue

            # Move the laser based on its direction
            match laser.direction:
                case Direction.RIGHT:
                    laser.col += 1
                case Direction.LEFT:
                    laser.col -= 1
                case Direction.UP:
                    laser.row -= 1
                case Direction.DOWN:
                    laser.row += 1

            # Check if laser is out of bounds
            if laser.row < 0 or laser.row >= len(maze) or laser.col < 0 or laser.col >= len(maze[0]):
                laser.alive = False
                continue

            # Check if the laser's state has been seen before
            laser_state = (laser.row, laser.col, laser.direction)
            if laser_state in seen_lasers:
                laser.alive = False
                continue
            else:
                seen_lasers.add(laser_state)

            # Energize the tile
            energised_tiles.add((laser.row, laser.col))

            # Handle the reflection and direction changes
            new_tile = maze[laser.row][laser.col]
            match new_tile:
                case "|":
                    if laser.direction == Direction.LEFT or laser.direction == Direction.RIGHT:
                        #print("Laser is going up, a new laser will be created going down")
                        laser.direction = Direction.UP
                        lasers.append(Laser(laser.row, laser.col, Direction.DOWN))
                case "-":
                    if laser.direction == Direction.UP or laser.direction == Direction.DOWN:
                        #print("Laser is going left, a new laser will be created going right")
                        laser.direction = Direction.LEFT
                        lasers.append(Laser(laser.row, laser.col, Direction.RIGHT))
                case "\\":
                    match laser.direction:
                        case Direction.RIGHT:
                            #print("Laser has been reflected, it will now go down")
                            laser.direction = Direction.DOWN
                        case Direction.LEFT:
                            #print("Laser has been reflected, it will now go up")
                            laser.direction = Direction.UP
                        case Direction.UP:
                            #print("Laser has been reflected, it will now go left")
                            laser.direction = Direction.LEFT
                        case Direction.DOWN:
                            #print("Laser has been reflected, it will now go right")
                            laser.direction = Direction.RIGHT
                case "/":
                    match laser.direction:
                        case Direction.RIGHT:
                            #print("Laser has been reflected, it will now go up")
                            laser.direction = Direction.UP
                        case Direction.LEFT:
                            #print("Laser has been reflected, it will now go down")
                            laser.direction = Direction.DOWN
                        case Direction.UP:
                            #print("Laser has been reflected, it will now go right")
                            laser.direction = Direction.RIGHT
                        case Direction.DOWN:
                            #print("Laser has been reflected, it will now go left")
                            laser.direction = Direction.LEFT

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