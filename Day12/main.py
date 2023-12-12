from functools import cache


def read_input(filename: str = "input.txt") -> list:
    with open(filename) as file:
        springs = [c.strip().split() for c in file.readlines()]
        springsAndNumbers = [[c[0],tuple(int(d) for d in c[1].split(','))] for c in springs]
        return springsAndNumbers
    
@cache
def number_of_legal_permutations(springs: str, nums: tuple[int] ) -> int:

    without_leading = springs.lstrip(".")

    if len(without_leading) == 0:
        return len(nums) == 0
    
    # ???. ()
    # In a case where we have some question marks but we know there are no more working springs 
    # We know it's legal as those "?" must be "."
    if len(nums) == 0:
        return without_leading.count("#") == 0

    num_to_check = nums[0]    

    # print(without_leading, nums, num_to_check)
    if without_leading[0] == "#":
        start_to_check = without_leading[:num_to_check]
        # If ?? < 3 then we know it's illegal
        # ?.?? to check is 3 so start to check is ?.? we know this is illegal as it has a . in it and we want 3 #
        if (len(without_leading) < num_to_check) or start_to_check.count(".") >= 1:
            return False
        # ??? to check is 3 so we could convert them all to # and it would be legal
        if (len(without_leading) == num_to_check):
            return int(len(nums) == 1) #single spring, right size
        # ???#?? to check is 3 Let's check the 3rd one is a # so this must be illegal because if we converted the first 3 to # it would be four # in a row which is 4 not 4
        if without_leading[num_to_check] == "#":
            return False
        
        # Right let's move on by to_check and check the rest of the springs
        return number_of_legal_permutations(without_leading[num_to_check+1:], nums[1:])
    return number_of_legal_permutations('#'+without_leading[1:], nums) + number_of_legal_permutations(without_leading[1:], nums)



if __name__ == "__main__":
    data = read_input()

    print("Part 1 total:", sum(number_of_legal_permutations(s,c) for [s,c] in data))

    part2Data = read_input()
    p2Sum = 0
    for [s,c] in part2Data:
        newS = ("?".join([s for _ in range(5)]))
        newC = (c*5)
        p2Sum+= (number_of_legal_permutations(newS,newC))
    print("Part 2 total:", p2Sum)
    