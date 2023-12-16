
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
    last_len = 0
    lives = 90000000


    while True: 
        for laser in lasers:
            match laser.direction:
                case Direction.RIGHT:
                    laser.col += 1
                case Direction.LEFT:
                    laser.col -= 1
                case Direction.UP:
                    laser.row -= 1
                case Direction.DOWN:
                    laser.row += 1

            if laser.row < 0 or laser.row >= len(maze) or laser.col < 0 or laser.col >= len(maze[0]):
                laser.alive = False
                continue

            new_tile = maze[laser.row][laser.col]
            energised_tiles.add((laser.row, laser.col))
            if len(energised_tiles) == last_len:
                #print("Removing a life")
                lives -= 1
                #print(f"Lives remaining: {lives}")
            if lives <= 0:
                #print("All lives have been lost, the program will now exit")
                pprint(maze, energised_tiles)
                return len(energised_tiles) 
            last_len = len(energised_tiles)
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
                    




if __name__ == "__main__":
    maze = read_input()
    p1 = part1(maze)
    print(f"Part1 One: {p1}")