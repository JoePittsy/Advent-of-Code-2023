from collections import defaultdict
from functools import cache, reduce
import re

def read_input(filename: str = "input.txt"):
    with open (filename) as f:
        return f.read().split(",")

@cache
def hash(str: str) -> int:
    return reduce(lambda acc, char: (acc * 17 + ord(char)) % 256, str, 0)

def part1(initSeq: [str]):
    return sum(hash(seq) for seq in initSeq)

def part2(initSeq: [str]):
    def get_index_of_lens(lens: str, box: list[str]) -> int:
        return next((i for i, seq in enumerate(box) if lens in seq), -1)

    boxes: dict[int, list[tuple[str, int]]] = defaultdict(list)
    for seq in initSeq:
        label, focal = re.split(r"[-=]", seq)
        box = hash(label)
        index = get_index_of_lens(label, boxes[box])
        operation = "replace" if index != -1 and focal != "" else "add" if focal != "" else "remove" if index != -1 else "none"

        match operation:
            case "replace": boxes[box][index] = f"{label} {focal}"
            case "add": boxes[box].append(f"{label} {focal}")
            case "remove": boxes[box].pop(index)

    return sum([(box+1) * i * int(lens.split(" ")[1]) for box in boxes for i, lens in enumerate(boxes[box], 1)])

if __name__ == "__main__":
    initSeq = read_input()
    print("Part 1: ", part1(initSeq))
    print("Part 2: ", part2(initSeq))
