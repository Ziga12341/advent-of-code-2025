s = "small_input.txt"
l = "input.txt"
s_2 = "small_input_2.txt"
s_3 = "small_input_3.txt"
s_4 = "small_input_4.txt"

def read_lines(file_name: str) -> tuple[list[int], list[int]]:
    with open(file_name, "r", encoding="utf-8") as file:
        is_new_line = False
        fresh_ranges = []
        ingredients = []
        for line in file:
            line = line.strip()
            if line == "":
                is_new_line = True
            elif is_new_line:
                # where we have ingredients ids
                ingredients.append(int(line))

            else:
                # case where ranges
                low_range, high_range = line.split("-")
                low_range = int(low_range)
                high_range = int(high_range)
                fresh_ranges.append((low_range, high_range))

        return ingredients, fresh_ranges


def is_fresh_in_range(ingredient_id: int, range_min: int, range_max: int):
    return range_min <= ingredient_id <= range_max


def is_ingredient_fresh(ingredient_id: int, fresh_ranges: list[tuple[int, int]]):
    return any(is_fresh_in_range(ingredient_id, range_min, range_max) for range_min, range_max in fresh_ranges)


def part_1(file_name):
    ingredients, fresh_ranges = read_lines(file_name)
    return sum(is_ingredient_fresh(ingredient, fresh_ranges) for ingredient in ingredients)
    # return sum(ingredient for ingredient in ingredients if is_ingredient_fresh(ingredient, fresh_ranges))


def count_range(range_min: int, range_max: int):
    return range_max + 1 - range_min


# merge two ranges if goes one over another (make new range out of two)
def compare_two_ranges(range_min_1: int, range_max_1: int, range_min_2: int, range_max_2: int):
    new_range_min = None
    new_range_max = None
    # if first min range is in between second range
    if range_min_2 <= range_min_1 <= range_max_2:

        # we need to change max range in merged ranges
        # max range of first range is bigger than max from second
        if range_max_2 < range_max_1:
            new_range_min = range_min_2
            new_range_max = range_max_1
        # else: we do not need to change anything because first range is in between

    # if first max range is in between second range
    if range_min_2 <= range_max_1 <= range_max_2:
        # case where first range caver lower values than range 2 and need to adjust lower values
        if range_min_1 < range_min_2:
            new_range_min = range_min_1
            new_range_max = range_max_2

        # else: we do not need to change anything because first range is in between and do not cover lower values
    # case where first range extend second range in both directions
    if range_min_1 <= range_min_2 and range_max_1 >= range_max_2:
        new_range_min = range_min_1
        new_range_max = range_max_1

    # case where second range extend first one in both direction
    if range_min_1 >= range_min_2 and range_max_1 <= range_max_2:
        new_range_min = range_min_2
        new_range_max = range_max_2
    # if range is not overlapping just return False oder wise return new range
    if new_range_min is None and new_range_max is None:
        return False
    return new_range_min, new_range_max


def part_2(file_name):
    count_valid = 0
    ingredients, fresh_ranges = read_lines(file_name)
    # continue until list empty (because of pop-ing and counting the ones who do not overlap
    while len(fresh_ranges) > 0:
        # pop first from list
        range_min_1, range_max_1 = fresh_ranges.pop(0)
        # in this case i just count valid once and because is pop leave removed it
        if not any(compare_two_ranges(range_min_1, range_max_1, range_min_2, range_max_2) for range_min_2, range_max_2 in
                   fresh_ranges):
            # add if no range covers this one
            count_valid += count_range(range_min_1, range_max_1)
        # if two ranges cover each other (case when from two ranges generate one new) than do this:
        else:
            for range_min_2, range_max_2 in fresh_ranges:
                # for each new pair check if ranges overlap
                new_range = compare_two_ranges(range_min_1, range_max_1, range_min_2, range_max_2)
                # if we get new range out of two than append new range for next iteration and remove also second range (first removed when pop-ed)
                if new_range:
                    fresh_ranges.append(new_range)
                    fresh_ranges.remove((range_min_2, range_max_2))


    return count_valid


def test_part_1():
    assert part_1(s) == 3
    assert part_1(l) == 756


def test_part_2():
    assert part_2(s) == 14
    assert part_2(s_2) == 6
    assert part_2(s_3) == 8
    assert part_2(s_4) == 8
    assert part_2(l) != 397240914128925
    assert part_2(l) != 319721886174838
    assert part_2(l) != 327242267786143
    assert part_2(l) == 355555479253787


# too high:
# 397240914128925

# too low:
# 319721886174838
# 327242267786143

if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
