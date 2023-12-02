
from collections import defaultdict
from itertools import groupby
from typing import Dict, List
import math


def read_input(fileName: str = "input.txt") -> list[str]:
    with open(fileName, 'r') as f:
        return [line.strip().split(": ")[1].split("; ") for line in f]


def get_largest_cubes_for_game(game: List[str]) -> Dict[str, int]:
    # ["1 red, 2 green, 3 blue", "4 red, 5 green, 6 blue"] -> [(1, "red"), (2, "green"), (3, "blue"), (4, "red"), (5, "green"), (6, "blue")]
    cubes = [(int(number), colour) for subGame in game for cube in subGame.split(", ") for number, colour in [cube.split(" ")]]
    cubes.sort(key=lambda x: x[1]) # Sort the list of tuples by color (group by requires the list to be sorted 🙄)        
    max_cubes = {color: max(group, key=lambda x: x[0])[0] for color, group in groupby(cubes, key=lambda x: x[1])} # Group by color and find the max number for each color

    return max_cubes


def part1(games: List[List[str]]) -> int:

    bag = { "red": 12, "green": 13, "blue": 14 }

    def is_game_legal(game: List[str], bag: Dict[str, int]) -> bool:
        for color, number in get_largest_cubes_for_game(game).items():
            if number > bag.get(color, 0):
                return False
        return True

    return sum(index for index, game in enumerate(games, start=1) if is_game_legal(game, bag))


def part2(games: List[List[str]]) -> int: 
    return sum(math.prod(get_largest_cubes_for_game(game).values()) for game in games)

if __name__ == "__main__":
    games = read_input()
    print(f"Part 1: {part1(games)}")    
    print(f"Part 2: {part2(games)}")

