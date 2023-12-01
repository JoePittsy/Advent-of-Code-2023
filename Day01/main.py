import re


def read_input(fileName: str = "input.txt") -> list[str]:
    with open(fileName, 'r') as f:
        return [line.strip() for line in f.readlines()]


def part1(input: list[str]):
    print("Part 1")
    sum = 0 

    numbers = ["".join(re.findall("\d+", line)) for line in input]
    for number in numbers:
        sum += int(number[0] + number[-1])


    print(sum)

def part2(input: list[str]):
    print("Part 2")

    sum = 0

    toReplace = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    numbersAndStrings = [re.findall("(?=(one|two|three|four|five|six|seven|eight|nine|1|2|3|4|5|6|7|8|9))", line) for line in input]


    for line in numbersAndStrings:
        first = line[0]
        last = line[-1]
        if first in toReplace:
            first = toReplace[first]
        if last in toReplace:
            last = toReplace[last]
        calibration = int(first + last)
        sum += calibration

    print(sum)



if __name__ == '__main__':
    input = read_input()
    part1(input)
    part2(input)