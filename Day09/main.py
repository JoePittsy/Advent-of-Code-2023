def read_input(filename: str = "input.txt"):
    with open(filename, "r") as f: 
        return [list(map(int, l.split(" "))) for l in f.readlines()]
    

def difference_at_step(reading: list[int]):
    # 0 3 6 9 12 15 -> 3 3 3 3 3
    # 3 3 3 3 3 -> 0 0 0 0

    difference = [ reading[i+1] - reading[i] for i in range(len(reading) - 1) ]
    return difference

def extrapolate(difference: int, lastInSeq: int):
    return lastInSeq + difference

def extrapolate2(difference: int, firstInSeq: int):
    return firstInSeq - difference


def part1(oasis: list[str]):
    extrapolatedSum = 0
    for reading in oasis:
        print()
        differences = [reading]
        last_difference = difference_at_step(reading)
        differences.append(last_difference)
        while [a for a in last_difference if a != 0]:
            last_difference = difference_at_step(last_difference)
            differences.append(last_difference)
            
        differenceToMatch = 0
        for diff in differences[::-1]:
            oldDifferenceToMatch = differenceToMatch
            differenceToMatch = extrapolate(differenceToMatch, diff[-1])
            print(diff, oldDifferenceToMatch, differenceToMatch)
        extrapolatedSum += differenceToMatch
    return extrapolatedSum

def part2(oasis: list[str]):
    extrapolatedSum = 0
    for reading in oasis:
        differences = [reading]
        last_difference = difference_at_step(reading)
        differences.append(last_difference)
        while [a for a in last_difference if a != 0]:
            last_difference = difference_at_step(last_difference)
            differences.append(last_difference)
            
        differenceToMatch = 0
        for diff in differences[::-1]:
            differenceToMatch = extrapolate2(differenceToMatch, diff[0])
        extrapolatedSum += differenceToMatch
    return extrapolatedSum



if __name__ == "__main__":
    readings = read_input()
    # print(part1(readings))
    print()
    print(part2(readings))

