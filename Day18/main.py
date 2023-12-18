
from dataclasses import dataclass
from typing import Literal

@dataclass
class Instruction:
    direction: Literal["U", "D", "L", "R"]
    distance: int
    direction2: Literal["U", "D", "L", "R"]
    distance2: int

@dataclass 
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def to_tuple(self):
        return (self.x, self.y)

def read_input(filename: str = "input.txt"):
    instructions = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split(" ")
            direction = parts[0]
            distance = int(parts[1])
            part2 = parts[2].strip()[2:-1]
            part2Direction = {"0": "R", "1": "D", "2": "L", "3": "U"}[part2[-1]]
            part2Distance = int(part2[:-1], 16)
            instructions.append(Instruction(direction, distance, part2Direction, part2Distance))
    return instructions



def solve(instructions, part2 = False):
    direction_map = {'U': Point(0, 1), 'D': Point(0, -1), 'L': Point(-1, 0), 'R': Point(1, 0)}


    def rearanged_picks(area, perimerer):

        return area - (perimerer/2) + 1

    def get_perimeter(dug):
        # The point's are dot to dot 
        count = 0 

        for i, point in enumerate(dug):
            last_point = dug[i - 1]
            if i == 0:
                last_point = dug[-1]
            
            if point.x == last_point.x:
                count += abs(point.y - last_point.y)
            else:
                count += abs(point.x - last_point.x)
        
        return count
    
    def shoelace_formula(vertices: list[Point]):
        n = len(vertices)
        area = 0
        for i, point in enumerate(vertices):
            next_real_point = vertices[(i + 1) % n]
            
            # Determine whether to move horizontally or vertically to the next point
            if point.x != next_real_point.x:
                # Horizontal movement
                directionString = "R" if point.x < next_real_point.x else "L"
            else:
                # Vertical movement
                directionString = "U" if point.y < next_real_point.y else "D"

            direction = direction_map[directionString]
            current_point = point

            # Traverse from current_point to next_real_point, filling in the gaps
            while current_point != next_real_point:
                next_imaginary_point = current_point + direction
                area += current_point.x * next_imaginary_point.y
                area -= next_imaginary_point.x * current_point.y
                current_point = next_imaginary_point

        # Closing the last vertex with the first
        area += vertices[-1].x * vertices[0].y
        area -= vertices[0].x * vertices[-1].y

        return abs(area) / 2



    current_position = Point(0, 0)
    dot_to_dot = list()


    for instruction in instructions:
        distance = instruction.distance if not part2 else instruction.distance2
        direction = direction_map[instruction.direction] if not part2 else direction_map[instruction.direction2]
        new_position = Point(current_position.x + direction.x * distance, 
                             current_position.y + direction.y * distance)
        
        current_position = new_position
        dot_to_dot.append(current_position)


    # I tired using the same approach as day 10 but the size of the grid was way too big
    

    area = shoelace_formula(dot_to_dot) # Use the shoelace formula to calculate the area
    perimiter = get_perimeter(dot_to_dot) # Fill in the gaps between the points to get the perimiter
    inside = rearanged_picks(area, perimiter) # Rearange the picks theorm to get the inside point count

    # We then now the total lava capacity is the perimiter count + the inside count
    return int(perimiter + inside)

if __name__ == "__main__":
    instructions = read_input()
    print(f"Part One: {solve(instructions)}")
    print(f"Part Two: {solve(instructions, True)}")

    