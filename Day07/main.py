from collections import Counter
from functools import cmp_to_key

def read_input(filename: str = "input.txt") -> list:
    with open(filename) as file:
        return [line.strip().split(" ") for line in file.readlines()]
    

def identify_hand(hand: str, part2: bool = False) -> list:
    split_hand = list(hand)
    counts = Counter(split_hand)

    if part2 and "J" in counts:
        joker_count = counts["J"]
        del counts["J"]
        if (len(counts) == 0): # All of the cards were jokers
            return 7 # So it's a full house babbbyy
        # Otherwise let's find the most common card and add the jokers to it
        most_common = counts.most_common(1)[0][0]
        counts[most_common] += joker_count

    if (len(counts) == 1):
        return 7
    if (len(counts) == 2 and (counts.most_common(1)[0][1]) == 4):
        return 6
    if (len(counts) == 2 and (counts.most_common(1)[0][1]) == 3):
        return 5
    if (len(counts) == 3 and (counts.most_common(1)[0][1]) == 3):
        return 4
    if (len(counts) == 3 and (counts.most_common(1)[0][1]) == 2):
        return 3
    if (len(counts) == 4 and (counts.most_common(1)[0][1]) == 2):
        return 2
    if (len(counts) == 5):
        return 1


def compare_hands(game1: list, game2: list, value_map, part2: bool) -> int:
    hand1 = game1[0]
    hand2 = game2[0]

    hand1Type = identify_hand(hand1,part2)
    hand2Type = identify_hand(hand2,part2)
    if hand1Type == hand2Type:
        for card1, card2 in zip(hand1, hand2):
            if value_map[card1] > value_map[card2]:
                return 1
            elif value_map[card1] < value_map[card2]:
                return -1
        
    if hand1Type > hand2Type:
        return 1
    elif hand1Type < hand2Type:
        return -1
    return 0


def compare_hands2(game1: list, game2: list) -> int:
    value_map = {'A': 14, 'K': 13, 'Q': 12, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1,}
    return compare_hands(game1, game2, value_map, True)

def compare_hands1(game1: list, game2: list) -> int:
    value_map = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
    return compare_hands(game1, game2, value_map, False)



def calculate_winnings(games: list, part2: bool = False) -> int:
    if part2: 
        in_order = sorted(games, key=cmp_to_key(compare_hands2))
        return sum([int(game[1]) * rank for rank,game in enumerate(in_order, 1)])
    else:
        in_order = sorted(games, key=cmp_to_key(compare_hands1))
        return sum([int(game[1]) * rank for rank,game in enumerate(in_order, 1)])

if __name__ == "__main__":
    input = read_input()

    assert identify_hand("JJJJJ", part2=True) == 7
    assert identify_hand("AAJAA", part2=True) == 7
    assert identify_hand("AAAAA") == 7
    assert identify_hand("AA8AA") == 6
    assert identify_hand("23332") == 5
    assert identify_hand("TTT98") == 4
    assert identify_hand("23432") == 3
    assert identify_hand("A23A4") == 2
    assert identify_hand("23456") == 1

    print("Part 1:", calculate_winnings(input))
    print("Part 2:", calculate_winnings(input, part2=True))