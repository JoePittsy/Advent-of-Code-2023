import math

def read_input(filename: str = "input.txt"):
    with open(filename, 'r') as f:
        data = f.readlines()
        instructions = data[0]
        maps = {m.strip().split(" = ")[0]: m.strip().split(" = ")[1][1:-1].split(", ") for m in data[2:]}
        return (instructions, maps)

def walk_to_xxZ(start: str, instructions: str, maps: dict) -> int:
    location = start
    steps = 0   
    while not location.endswith("Z"):
        left_or_right = 0 if instructions[steps % (len(instructions)-1)] == "L" else 1
        location = maps[location][left_or_right]
        steps += 1
    return steps

def part2(instructions, maps):   
    startLocations = [k for k in maps.keys() if k[-1] == "A"]
    cycles = [walk_to_xxZ(start, instructions, maps) for start in startLocations]
    return math.lcm(*cycles)

if __name__ == "__main__":
    instructions, maps = read_input()

    print(walk_to_xxZ("AAA", instructions, maps))
    print(part2(instructions, maps))