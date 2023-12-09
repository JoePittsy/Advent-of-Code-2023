import time

def read_input(filename: str = "input.txt"): 
    with open(filename, 'r') as f:
        almanac = f.read()
        seeds = list(map(int, almanac.split("\n")[0].split(": ")[1].split(" ")))
        maps = {m.split("\n")[0].split("-")[-1].split(" ")[0]: [list(map(int, seeds.split(" "))) for seeds in m.split("\n")[1:]] for m in almanac.split("\n\n")[1:]}
        return (seeds, maps)


def map_lookup(item, map):
    for dest_range_start, source_range_start, range_length in map:
        if source_range_start <= item < source_range_start + range_length:
            return item - source_range_start + dest_range_start
    return item

def part1(seeds, maps, length):
    min_location = float('inf')
    start_time = time.time()

    for i, value in enumerate(seeds):
        for m_key in maps:
            value = map_lookup(value, maps[m_key])

        if (i % 100000) == 0 and i > 0:
            elapsed_time = time.time() - start_time
            avg_time_per_iteration = elapsed_time / i
            estimated_time_remaining = avg_time_per_iteration * (length - i)

            # Convert to minutes and seconds
            minutes = int(estimated_time_remaining // 60)
            seconds = int(estimated_time_remaining % 60)
            print(f"Percentage done: {i/length*100}%, Estimated time remaining: {minutes} min {seconds} sec")

        if value < min_location:
            min_location = value

    return min_location

def part2(seeds, maps):
    transformed_seeds = [(start, start + length) for start, length in zip(seeds[::2], seeds[1::2])]
    total_length = sum(end - start for start, end in transformed_seeds)
    all_seeds = (item for start, end in transformed_seeds for item in range(start, end))
    return part1(all_seeds, maps, total_length)
    

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

if __name__ == "__main__": 
    seeds, maps = read_input()

    print(part1(seeds, maps, len(seeds)))
    # This is a not the way to do it, but it works after 30 minutes or so :)
    print(part2(seeds, maps))


