from copy import deepcopy
import numpy as np

def read_input(filename: str = "input.txt") -> list:
    with open(filename) as file:
        return [ np.array(g) for g in [ [ list(l) for l in m.split("\n") ] for m in file.read().strip("\n").split("\n\n") ] ] 


def pprint(l: list[str]):
    print("".join(l))

def find_horitzontal_reflection(surface, ignore_reflection=None):
    
    def drop_unreflected_rows(top, bottom):
        if len(top)<len(bottom):
            bottom = bottom[:len(top)]
        elif len(bottom)<len(top):
            top = top[len(top)-len(bottom):]
        return top, bottom
        
    for i in range(len(surface)-1):
        top_one = surface[i]
        one_below = surface[i+1]
        if np.array_equal(top_one, one_below):
            # Now we need to check if the rest of the surface is the same
            top = surface[:i+1]
            bottom = surface[i+1:]
            # Need to ensure these are the same size. If not drop the last row.
            top, bottom = drop_unreflected_rows(top, bottom)
            # Now let's flip the bottom
            bottom = np.flip(bottom, axis=0)   

            if np.array_equal(top, bottom):
                if ignore_reflection == (i+1): 
                    continue
                return i+1
    return 0

def find_vertical_reflection(surface, ignore_reflection=None):
    rotated = np.rot90(surface, k=3)
    return find_horitzontal_reflection(rotated, ignore_reflection)


def part1(surfaces):
    horizontal_reflections = sum([find_horitzontal_reflection(s) for s in surfaces])
    vertical_reflections = sum([find_vertical_reflection(s) for s in surfaces])
    return vertical_reflections + 100 * horizontal_reflections


# Brute force babbbyyyyyy
def part2(surf):

    def fix_smudge(surf):
        oldH = find_horitzontal_reflection(surf)
        oldV = find_vertical_reflection(surf)     
        old = (oldH, oldV)

        for y, line in enumerate(surf):
            for x, item in enumerate(line):
                coppiedSurface = deepcopy(surf)
                # Swap every item and see if it's a reflection
                newItem = "#" if item == "." else "."
                coppiedSurface[y,x] = newItem
                # Ignore the old line of reflection
                newH = find_horitzontal_reflection(coppiedSurface, ignore_reflection=oldH)
                newV = find_vertical_reflection(coppiedSurface, ignore_reflection=oldV)
                new = (newH, newV)

                if new != (0,0) and new != old:
                    return new
    
    fixed_reflections = [fix_smudge(s) for s in surf]
    horizontal_reflections = sum([h for h, v in fixed_reflections])
    vertical_reflections = sum([v for h, v in fixed_reflections])
    return vertical_reflections + 100 * horizontal_reflections

if __name__ == "__main__":
    surfaces = read_input()
    part1Answer = part1(surfaces)
    print(f"Part 1: {part1Answer}")
    part2Answer = part2(surfaces)
    print(f"P2: {part2Answer}")
