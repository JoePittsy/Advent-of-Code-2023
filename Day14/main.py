from collections import OrderedDict
import numpy.typing as npt
import numpy as np 
import itertools
import pickle

def read_input(filename: str = "input.txt"):
    with open (filename) as f:
        return np.array([np.array(list(line.strip())) for line in f.readlines()])

def slide_column2(col, n: int = 1, direction: str = "up"):
    stringCol = "".join(col)
    if direction == "up":
        s = stringCol
        for _ in range(n):
            s = s.replace('.O', 'O.')

        return np.array(list(s))
    else:
        s = stringCol
        for _ in range(n):
            s = s.replace('O.', '.O')
        return np.array(list(s))


def slide_column(col, n: int = 1, direction: str = "up"):
    modified_col = np.copy(col)

    o_indices = np.where(modified_col == 'O')[0]
    permanent_barriers = set(np.where(modified_col == '#')[0])
    temp_barriers = set(o_indices)  # Temporary barriers for already moved rocks

    for idx in sorted(o_indices, reverse=(direction == "down")):
        temp_barriers.discard(idx)
        if direction == "up":
            target_pos = max(idx - n, 0)
            barriers = [i for i in permanent_barriers.union(temp_barriers) if i < idx]
        elif direction == "down":
            target_pos = min(idx + n, len(col) - 1)
            barriers = [i for i in permanent_barriers.union(temp_barriers) if i > idx]

        if barriers:
            closest_barrier = max(barriers) if direction == "up" else min(barriers)
            target_pos = max(target_pos, closest_barrier + 1) if direction == "up" else min(target_pos, closest_barrier - 1)

        if target_pos != idx:
            modified_col[target_pos] = 'O'  
            modified_col[idx] = '.'        
        temp_barriers.add(target_pos) 

    return modified_col

def calculate_load(data):
    max_load = len(data)
    overall_load = 0
    for i, row in enumerate(data):
        load = max_load - i
        overall_load += np.sum(row == 'O') * load
    return overall_load

def pprint(data, end="\n"):
    for row in data:
        print("".join(row))
    print(end)

def cycle(data):    
    north = np.apply_along_axis(slide_column2, 0, data, len(data) - 1, "up")
    west = np.apply_along_axis(slide_column2, 1, north, len(north[0]) - 1, "up")
    south = np.apply_along_axis(slide_column2, 0, west, len(west) - 1, "down")
    east = np.apply_along_axis(slide_column2, 1, south, len(south[0]) - 1, "down")
    return east


def find_cycle(data: npt.NDArray):
    cache = OrderedDict()
    cache[pickle.dumps(data)] =  0
    toCycle = data
    for i in itertools.count(1):
        toCycle = cycle(toCycle)
        s = pickle.dumps(toCycle)
        if s in cache:
            return cache[s], i - cache[s], cache
        cache[s] = i
    assert False

def part1(data):
    north = np.apply_along_axis(slide_column2, 0, data, len(data) - 1, "up")
    load = calculate_load(north)
    return load

def part2(data):
    start, period, memory  = find_cycle(data)
    endGrid = list(memory.items())[(start + (1000000000 - start) % period)][0]
    return calculate_load(pickle.loads(endGrid))

if __name__ == "__main__":
    data = read_input()   
    print("Part 1: ", part1(data))
    print("Part 2: ", part2(data))

