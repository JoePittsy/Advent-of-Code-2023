def read_input(fileName: str = "input.txt") -> list[str]:
    games = []
    with open(fileName, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line = line.split(": ")[1]
            games.append(line.split("; "))

    return games

def part1(input, bag): 
    legalGames = []
    for index, game in enumerate(input):
        index += 1
        gameLegal = True
        for subGame in game:
            cubes = subGame.split(", ")
            for cube in cubes:
                split = cube.split(" ")
                number = int(split[0])
                colour = split[1]

                bagMax = bag[colour]
                if number > bagMax:
                    print(f"Game {index} is illegal, {colour} has {number} cubes, but only {bagMax} are available.")
                    gameLegal = False
                    break
            if not gameLegal:
                break

        if gameLegal:
            legalGames.append(index)
    print(sum(legalGames))


def part2(input): 
    cubePowers = []
    for index, game in enumerate(input):
        index += 1
        maxRed = 0
        maxGreen = 0
        maxBlue = 0

        for subGame in game:
            cubes = subGame.split(", ")
            for cube in cubes:
                split = cube.split(" ")
                number = int(split[0])
                colour = split[1]

                if colour == "red" and number > maxRed:
                    maxRed = number
                elif colour == "green" and number > maxGreen:
                    maxGreen = number
                elif colour == "blue" and number > maxBlue:
                    maxBlue = number
                    

              
        print(f"Game {index} could be played with {maxRed} red, {maxGreen} green and {maxBlue} blue cubes.")
        cubePowers.append(maxRed * maxGreen * maxBlue)

    print(sum(cubePowers))



if __name__ == "__main__":
    bag = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    input = read_input()
    part1(input, bag)   
    part2(input)

