from itertools import count, combinations
import numpy as np

def read_input(filename: str = "input.txt"):
    with open(filename, "r") as f:
        return np.array([list(l.strip()) for l in f.readlines()], dtype=object)

def pprint(observations):
    print('\n'.join([''.join([str(cell) for cell in row]) for row in observations]))


def manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) + abs(y2 - y1)


def expand_data_and_return_pairings(observations, factor=2):
    columnToExpand = [i for i, column in enumerate(observations.T) if '#' not in column]
    rowToExpand = [i for i, row in enumerate(observations) if '#' not in row]

    # Replace '#' with numbers
    counter = count(1)
    for i, row in enumerate(observations):
        for j, col in enumerate(row):
            if col == '#':
                observations[i, j] = str(next(counter))
    
    # Calculate the unique values and their coordinates
    unique_values = np.unique(observations)
    filtered_unique_values = [val for val in unique_values if val != '.']
    coordinates = {val: np.argwhere(observations == val) for val in filtered_unique_values}

    # Expand the coordinates, we are replacing every col in the columnToExpand with factor columns. Same for rows.
    # So if columnToExpand = [ 2] and factor = 2, a coord of (2, 2) will be expanded to (3, 2) 
    expanded_coordinates = {}
    for val, coords in coordinates.items():
        new_coords = []
        for coord in coords:
            x, y = coord
            x += sum(1 for i in rowToExpand if i <= x) * (factor - 1)
            y += sum(1 for i in columnToExpand if i <= y) * (factor - 1)
            new_coords.append((x, y))
        expanded_coordinates[val] = new_coords

    numbers = list(range(1, next(counter)))
    print(numbers)
    return list(combinations(numbers, 2)), expanded_coordinates



def solve(observations, factor):
    pairings, coordinates = expand_data_and_return_pairings(observations, factor)

    pairings_array = np.array(pairings)
    p1_coords = np.array([coordinates[str(pair[0])][0] for pair in pairings_array])
    p2_coords = np.array([coordinates[str(pair[1])][0] for pair in pairings_array])
    all_dists = np.sum(np.abs(p1_coords - p2_coords), axis=1)
    total_distance = np.sum(all_dists)
    return total_distance

if __name__ == "__main__":
    observations = read_input()

    p1 = solve(observations, 2)
    print(f"Part 1: {p1}")
    observations = read_input()
    p2 = solve(observations, 1000000)
    print(f"Part 2: {p2}")
