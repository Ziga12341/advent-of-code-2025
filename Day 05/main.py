s = "small_input.txt"
l = "input.txt"


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


def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 3
    assert part_1(l) == 756


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
