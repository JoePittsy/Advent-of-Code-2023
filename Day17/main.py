from dataclasses import dataclass
import heapq
from typing import Any, Tuple


def read_input(filename: str = "input.txt") -> list:
    with open (filename, "r") as f: 
        graph = {}
        for i, r in enumerate(f):
            for j, c in enumerate(r.strip()):
                graph[i,j] = int(c)
        return graph


@dataclass
class Move:
    total_heat : int
    x: int
    y: int
    last_x: int
    last_y: int

    last_Move: Any

    @property
    def pos(self):
        return (self.x, self.y)
    
    @property
    def last_location(self):
        return (self.x - self.last_x, self.y - self.last_y)

    @property
    def last_move(self):
        return (self.last_x, self.last_y)

    @property
    def negative_last_move(self):
        return (-self.last_x, -self.last_y)
    
    def __lt__(self, other):
        return self.total_heat < other.total_heat


def minimal_heat(start: Tuple[int, int], end: Tuple[int, int], least: int, most: int, board: dict[(int,int):int]):
    queue: [Move] = [Move(0, *start, 0, 0, None)]
    seen: set[tuple(int, int, int, int)] = set()

    while queue:
        move = heapq.heappop(queue)

        if move.pos == end:
            current_move = move
            path = []
            while current_move:
                path.append(current_move.pos)
                current_move = current_move.last_Move
            return path[::-1], move.total_heat
        
        if (*move.pos, *move.last_move) in seen:
            continue

        seen.add((*move.pos, *move.last_move))

        directions = {(1, 0), (0, 1), (-1, 0), (0, -1)}
        # Exclude last move and its opposite to avoid backtracking
        valid_directions = directions - {move.last_move, move.negative_last_move}

        for dx, dy in valid_directions:
            current_x, current_y = move.x, move.y
            current_heat = move.total_heat

            for step in range(1, most + 1):
                # Update position
                current_x += dx
                current_y += dy

                # Check if the new position is on the board
                if (current_x, current_y) in board:
                    current_heat += board[current_x, current_y]
                    if step >= least:
                        newMove = Move(current_heat, current_x, current_y, dx, dy, move)
                        heapq.heappush(queue, newMove)




def pprint(terrain: dict[(int,int):int], path):

    expanded_path = []
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i+1]
        if start[0] == end[0]:
            for j in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                expanded_path.append((start[0], j))
        else:
            for j in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                expanded_path.append((j, start[1]))

    for row in range(min(terrain, key=lambda x: x[0])[0], max(terrain, key=lambda x: x[0])[0] + 1):
        for col in range(min(terrain, key=lambda x: x[1])[1], max(terrain, key=lambda x: x[1])[1] + 1):
            if (row, col) in terrain:
                if (row, col) in expanded_path:
                    index = expanded_path.index((row, col)) -1 
                    if index >= 0:
                        previous_position = expanded_path[index]
                        if previous_position[0] == row:
                            if previous_position[1] < col:
                                print(">", end="")
                            else:
                                print("<", end="")
                        else:
                            if previous_position[0] < row:
                                print("v", end="")
                            else:
                                print("^", end="")
                    else:
                        print("S", end="")
                else:
                    print(terrain[(row, col)], end="")
            else:
                print(".", end="")
        print()
    

   
def part1(terrain):
    path, heat = minimal_heat((0,0), max(terrain), 1, 3, terrain)
    return heat

   
def part2(terrain):
    path, heat = minimal_heat((0,0), max(terrain), 4, 10, terrain)
    return heat

if __name__ == "__main__":
    terrain = read_input()
    p1 = part1(terrain)
    print("Part 1:", p1)
    p2 = part2(terrain)
    print("Part 2:", p2)


