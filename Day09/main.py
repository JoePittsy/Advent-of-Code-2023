from functools import reduce

def read_input(filename: str = "input.txt"):
    with open(filename, "r") as f: 
        return [list(map(int, l.split(" "))) for l in f.readlines()]
    
def solve(oasis: list[str]):
    def difference_at_step(reading: list[int]) -> list[int]:
        return [b-a for a,b in zip(reading, reading[1:])]    
    
    part1, part2 = 0, 0
    for reading in oasis:
        differences = [reading, difference_at_step(reading)]
        while not all(a == 0 for a in differences[-1]):
            differences.append(difference_at_step(differences[-1]))
        part1 += reduce(lambda acc, lst: lst[-1] + acc, reversed(differences), 0)
        part2 += reduce(lambda acc, lst: lst[0] - acc , reversed(differences), 0)

    return part1, part2

if __name__ == "__main__":
    readings = read_input()
    part1, part2 = solve(readings)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")