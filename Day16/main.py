
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

def part1(maze):
    lasers: [Laser] = [Laser(0, -1, Direction.RIGHT)]
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



if __name__ == "__main__":
    maze = read_input()
    p1 = part1(maze)
    print(f"Part1 One: {p1}")