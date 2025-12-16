from functools import lru_cache

s = "small_input.txt"
s_2 = "small_input_2.txt"
s_3 = "small_input_3.txt"
l = "input.txt"


def read_lines(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def get_coordinates_with_char(file_name):
    list_of_tachyon_manifold = read_lines(file_name)
    all_coordinates_with_char = []
    for row in range(len(list_of_tachyon_manifold)):
        for column, char in enumerate(list_of_tachyon_manifold[row]):
            all_coordinates_with_char.append((column, row, char))
    return all_coordinates_with_char


def get_char_from_location(file_name, x, y):
    all_coordinates_with_char = get_coordinates_with_char(file_name)
    for column, row, char in all_coordinates_with_char:
        if column == x and row == y:
            return char
    return None


def part_1(file_name):
    all_locations = get_coordinates_with_char(file_name)
    starting_point_with_location = [(x, y, char) for x, y, char in all_locations if char == "S"][0]
    tachyon_manifold_height = max([y for x, y, char in all_locations])
    next_candidates = [starting_point_with_location]
    count_splitters = 0
    while next_candidates:
        previous_location = next_candidates.pop(0)
        x0, y0, char = previous_location
        next_move_y = y0 + 1

        next_move_char = get_char_from_location(file_name, x0, next_move_y)

        # add to new candidates beam if still in tachyon manifold
        if next_move_y <= tachyon_manifold_height:

            # new location "." all good just add new location except we are at the end of tachyon manifold
            if get_char_from_location(file_name, x0, next_move_y) == ".":
                if (x0, next_move_y, next_move_char) not in next_candidates:
                    next_candidates.append((x0, next_move_y, next_move_char))
            # need to split beam move it next to "^"
            else:
                # count split on "^"
                count_splitters += 1
                # left beam
                next_move_x_left = x0 - 1
                # right beam
                next_move_x_right = x0 + 1

                # add left beam if not in next move candidates yet
                if (next_move_x_left, next_move_y, next_move_char) not in next_candidates:
                    next_candidates.append((next_move_x_left, next_move_y, next_move_char))

                if (next_move_x_right, next_move_y, next_move_char) not in next_candidates:
                    next_candidates.append((next_move_x_right, next_move_y, next_move_char))
    return count_splitters


# location (x, y) where char is "^" exclude S
def get_all_splitters_and_start_coordinates(file_name):
    all_coordinates_with_char = get_coordinates_with_char(file_name)
    return [(x, y, char) for x, y, char in all_coordinates_with_char if char == "^"]


def get_location_of_next_spitters(file_name, x, y):
    all_splitters_and_start = get_all_splitters_and_start_coordinates(file_name)
    left_candidates = []
    right_candidates = []
    for x0, y0, char in all_splitters_and_start:
        # left candidates
        if x0 == x - 1 and y0 > y:
            left_candidates.append((x0, y0))

        # rights candidates
        if x0 == x + 1 and y0 > y:
            right_candidates.append((x0, y0))

    # filter minimum of y (high as possible) for particular column (x or y)
    collect_candidates = []
    if left_candidates:
        collect_candidates.append(min(left_candidates))
    if right_candidates:
        collect_candidates.append(min(right_candidates))

    return collect_candidates


# i may need to add lru cache to save locations which I already calculated how many beams leave tachyon manifold
@lru_cache(maxsize=None)
def part_2(file_name, x, y):
    next_locations = get_location_of_next_spitters(file_name, x, y)
    # if there is not next location than it is last splitter which add 2 possible ways (2 timelines)
    if len(next_locations) == 0:
        return 2
    
    # if 1 next location of splitter - one beam leave grid other go to next splitter
    elif len(next_locations) == 1:
        x0, y0 = next_locations[0]
        return 1 + part_2(file_name, x0, y0)

    else:
        # splitter goes into two new splitters, continue recursion
        x1, y1 = next_locations[0]
        x2, y2 = next_locations[1]

        # get new location left and right of splitter
        return part_2(file_name, x1, y1) + part_2(file_name, x2, y2)


def test_part_1():
    assert part_1(s) == 21


def test_part_2():
    assert part_2(s_2, 7, 0) == 8
    assert part_2(s_3, 7, 0) == 13
    assert part_2(s, 7, 0) == 40
    assert part_2(l, 70, 0) == 15118009521693


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))

# 4032 too low
# 6384 too low
# ni pravi: 44011029008
# ni pravi: 6656981666168
