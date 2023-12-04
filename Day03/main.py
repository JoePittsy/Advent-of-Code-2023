from collections import defaultdict
import math
import numpy as np
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def read_input(fileName: str = "input.txt"): 
    with open(fileName, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]
    

def part1(input: list[str]) -> int:

    adjacents = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),(1, -1), (1, 0), (1, 1)]

    def get_adjacents(x, y):
        return [(x + dx, y + dy) for dx, dy in adjacents if 0 <= x + dx < len(input) and 0 <= y + dy < len(input[0])]
    
    def get_adjacent_symbols(x, y):
        adjacents = get_adjacents(x, y)
        for x, y in adjacents:
            char = input[y][x]
            if char != "." and char.isdecimal() == False:
                return True
        return False    

    partNumbers = []

    for y, row in enumerate(input):
        numberTouching = False
        numberParts = []
        for x, col in enumerate(row):
            lastOnRow = x == len(row) - 1
            lastNumberOnRow = lastOnRow and col.isdecimal()
            if (not col.isdecimal() or lastOnRow):

                if (lastNumberOnRow):
                    numberParts.append(col)

                if (len(numberParts) > 0 and numberTouching):
                    partNumbers.append(int(''.join(numberParts)))
                    print(f"{bcolors.OKGREEN}{''.join(numberParts)}{bcolors.ENDC}", end="")
                    if (not lastNumberOnRow): print(col, end="")
                elif (len(numberParts) > 0):
                    print(f"{bcolors.FAIL}{''.join(numberParts)}{bcolors.ENDC}", end="")
                    if (not lastNumberOnRow): print(col, end="")
                else: 
                    print(col, end="")
        
                numberTouching = False
                numberParts = []

            else: 
                numberParts.append(col)
                touching = get_adjacent_symbols(x, y)
                if (touching ):
                    numberTouching = True
    return sum(partNumbers)

def part2(input: list[str]) -> int:

    adjacents = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),(1, -1), (1, 0), (1, 1)]

    def get_adjacents(x, y):
        return [(x + dx, y + dy) for dx, dy in adjacents if 0 <= x + dx < len(input) and 0 <= y + dy < len(input[0])]
    
    def get_adjacent_stars(x, y) -> list[(int, int)]:
        adjacents = get_adjacents(x, y)
        stars = []
        for x, y in adjacents:
            char = input[y][x]
            if char == "*":
                stars.append((x, y))
        return stars

    partNumbers = []
    gears = defaultdict(list)


    for y, row in enumerate(input):
        numberTouching = False
        numberParts = []
        stars = []
        for x, col in enumerate(row):
            lastOnRow = x == len(row) - 1
            lastNumberOnRow = lastOnRow and col.isdecimal()
            if (not col.isdecimal() or lastOnRow):

                if (lastNumberOnRow):
                    numberParts.append(col)
                if (len(numberParts) > 0 and numberTouching):
                    partNumber = int(''.join(numberParts))
                    partNumbers.append(int(''.join(numberParts)))
                    print(stars)
                    for starx, stary in set(stars):
                        print(f"{bcolors.OKGREEN}{''.join(numberParts)}{bcolors.ENDC}", end=" ")
                        key = f"{starx},{stary}"
                        gears[key].append(partNumber)
        
        
                numberTouching = False
                numberParts = []
                stars = []

            else: 
                numberParts.append(col)
                myStars = get_adjacent_stars(x, y)
                if (len(myStars) > 0 ):
                    numberTouching = True
                    stars.extend(myStars)

                
    
    print(gears)
    return sum([math.prod(gears[key]) for key in gears if len(gears[key]) >= 2]) 

if __name__ == "__main__":
    input = read_input()

    # print(input)
    # print(f"Part 1: {part1(input)}")    
    print(f"Part 2: {part2(input)}")