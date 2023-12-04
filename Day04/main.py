def read_input(filename: str = "input.txt"):
    with open(filename, 'r') as f:
        games = [line.strip().split(": ")[1].split(" | ") for line in f.readlines()]
        intGames = []
        for game in games:
            numbers1 = list(map(int, game[0].split()))
            numbers2 = list(map(int, game[1].split()))
            intGames.append((numbers1, numbers2))

        return intGames
    
def part1(games: list[tuple[list[int], list[int]]]) -> int:
    total_score = 0

    for winning_numbers, my_numbers in games:
        intersection = set(winning_numbers) & set(my_numbers)
        if intersection:
            total_score += 2 ** (len(intersection) - 1)

    return total_score


def part2(games: list[tuple[list[int], list[int]]]) -> int:

    winnings = {}
    extra_cards = []

    for i, (winning_numbers, my_numbers) in enumerate(games, 1):
        if set(winning_numbers) & set(my_numbers):
            won_cards = [c + i for c, _ in enumerate(set(winning_numbers) & set(my_numbers), 1)]
            winnings[i] = won_cards
            extra_cards.extend(won_cards)
        else :
            winnings[i] = []
    
    def expand_winnings(card, winnings, simplified):
        if card in simplified:
            return simplified[card]
        
        total_winnings = winnings[card].copy()
        for won_card in winnings[card]:
            total_winnings.extend(expand_winnings(won_card, winnings, simplified))

        simplified[card] = total_winnings
        return total_winnings

    # It's way way more efficent to flatten the winnings recursivley once then it is to recursively procsess every extra!
    def simplify_winnings(winnings):
        simplified = {}
        for key in sorted(winnings.keys(), reverse=True):
            expand_winnings(key, winnings, simplified)
        return simplified

    simplified_winnings = simplify_winnings(winnings)

    return sum(len(cards) for cards in simplified_winnings.values()) + len(simplified_winnings.keys())

if __name__ == "__main__": 
    input = read_input()
    print(f"Part 1: {part1(input)}")
    print(f"Part 2: {part2(input)}")