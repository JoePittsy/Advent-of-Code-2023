import math

def read_input(filename: str = "input.txt"):
    with open(filename) as f: 
        data = f.readlines()
        times = list(map(int, data[0].strip().split("Time:")[1].lstrip().split()))
        distance = list(map(int, data[1].strip().split("Distance:")[1].lstrip().split()))
        return times, distance
    
def part1(times, distance): 
    return math.prod([number_of_winners_for_time(time, dist) for (time, dist) in zip(times, distance)])
       
def number_of_winners_for_time(time, dist): 
    winners = 0
    had_a_win = False
    for hold in range(time+1):
        winner = ((time - hold) * hold) > dist
        if winner:
            had_a_win = True
            winners += 1
        if had_a_win and not winner:
            break
    return winners

if __name__ == "__main__":
    times, distance = read_input()

    def combine(int_array):
        return int("".join(map(str, int_array)))

    print("Part 1: ", part1(times, distance))
    print("Part 2: ", number_of_winners_for_time(combine(times), combine(distance)))
