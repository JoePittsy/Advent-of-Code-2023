
def read_input(filename: str = "input.txt"):
    with open(filename, 'r') as f:
        #games = [['41 48 83 86 17', '83 86  6 31 17  9 48 53'], ['13 32 20 16 61', '61 30 68 82 17 32 24 19'], [' 1 21 53 59 44', '69 82 63 72 16 21 14  1'], ['41 92 73 84 69', '59 84 76 51 58  5 54 83'], ['87 83 26 28 32', '88 30 70 12 93 22 82 36'], ['31 18 13 56 72', '74 77 10 23 35 67 36 11']]
        games = [line.strip().split(": ")[1].split(" | ") for line in f.readlines()]
        intGames = []
        for game in games:
            numbers1 = list(map(int, game[0].split()))
            numbers2 = list(map(int, game[1].split()))
            intGames.append((numbers1, numbers2))

        return intGames
    

def part1(input: list[tuple[list[int], list[int]]]) -> int:
    totalScore = 0

    def double_n_times(a, n):
        return a * 2 ** n

    for game in input:
        winningNumbers = game[0]
        myNumbers = game[1]
        intersection = list(set(winningNumbers) & set(myNumbers))
        if (len(intersection) > 0):
            totalScore += double_n_times(1, len(intersection)-1)
    return totalScore

def part2(input: list[tuple[list[int], list[int]]]) -> int:

    winnings = dict()
    extraCards: list[int] = []
    global totalScratchCards
    totalScratchCards = len(input)

    # Process original cards
    for i, game in enumerate(input):
        winningNumbers = game[0]
        myNumbers = game[1]

        intersection = list(set(winningNumbers) & set(myNumbers))
        if (len(intersection) > 0):
            # We know that card i equals c+i cards
            wonCards = [c + i for c, _ in enumerate(intersection, 1)]
            winnings[i] = wonCards
            extraCards.extend(wonCards)
    
    # Now we can process the extra cards
    totalScratchCards += len(extraCards)
    print(f"Extra cards: {extraCards}")
    print(f"Total cards before processing extras: {totalScratchCards}, to process: {len(extraCards)}")

    def process_extras_recursively(cards, winnings):
        totalExtraCards = 0
        for card in cards:
            wonCards = winnings.get(card)
            if wonCards is not None:
                # Add the number of won cards
                totalExtraCards += len(wonCards)

                # Recursively process won cards and add to the total
                totalExtraCards += process_extras_recursively(wonCards, winnings)
        return totalExtraCards

    extras = process_extras_recursively(extraCards, winnings)
    

    return totalScratchCards + extras



if __name__ == "__main__": 
    input = read_input()
    print(f"Part 1: {part1(input)}")
    print(f"Part 2: {part2(input)}")