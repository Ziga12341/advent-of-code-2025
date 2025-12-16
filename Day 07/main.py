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


print(get_coordinates_with_char(s))


def get_char_from_location(file_name, x, y):
    all_coordinates_with_char = get_coordinates_with_char(file_name)
    for column, row, char in all_coordinates_with_char:
        if column == x and row == y:
            return char
    return None


print(get_char_from_location(s, 7, 2))
print(max([y for x, y, char in get_coordinates_with_char(s)]))


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


def part_2(file_name):
    all_locations = get_coordinates_with_char(file_name)
    tachyon_manifold_height = max([y for x, y, char in all_locations])

    starting_point_with_location = [(x, y, char) for x, y, char in all_locations if char == "S"][0]
    x0, y0, _ = starting_point_with_location
    # remove starting position from quantum
    quantum_time_splitter_candidates = []
    all_splitters_and_start = get_all_splitters_and_start_coordinates(file_name)

    while all_splitters_and_start:
        x, y, char = all_splitters_and_start.pop(0)
        # print(x,y,char)
        # left first!
        # go down for i from each splitter to check if there we hit another splitter
        left = x - 1
        for left_index in range(tachyon_manifold_height - y):
            # check if we hit next splitter from left side
            new_left_x, new_left_y = left, y + left_index
            # get new char for each location 
            new_char_left = get_char_from_location(file_name, new_left_x, new_left_y)
            if (new_left_x, new_left_y, new_char_left) in all_splitters_and_start:
                if (new_left_x, new_left_y) not in quantum_time_splitter_candidates:
                    quantum_time_splitter_candidates.append((new_left_x, new_left_y))

            # need to check symbol/char in new location is "^" then we should not continue to move Y
            if new_char_left == "^":
                # break adding one to y because we hit splitter
                break

                # Then right side
        # split left and right side on each loop
        right = x + 1
        for right_index in range(tachyon_manifold_height - y):
            new_right_x, new_right_y = right, y + right_index
            # get new char for each location 
            new_char_right = get_char_from_location(file_name, new_right_x, new_right_y)
            if (new_right_x, new_right_y, new_char_right) in all_splitters_and_start:
                if (new_right_x, new_right_y) not in quantum_time_splitter_candidates:
                    quantum_time_splitter_candidates.append((new_right_x, new_right_y))
            if new_char_right == "^":
                # break adding one to y because we hit splitter
                break

        # print(quantum_time_splitter_candidates)
    return len(quantum_time_splitter_candidates) * 2


def beam_escape_tachyon_manifolds(file_name, x, y):
    tachyon_manifold_height = len(read_lines(file_name))
    new_y = y
    for i in range(1, tachyon_manifold_height - y):
        new_y = y + i
        # get new char for each location 
        new_char = get_char_from_location(file_name, x, new_y)
        # need to check symbol/char in new location is "^" then we should not continue to move Y
        if new_char == "^":
            # break adding one to y because we hit splitter
            return False, new_y
    return True, new_y


print(beam_escape_tachyon_manifolds(s, 7, 0))
print(beam_escape_tachyon_manifolds(s, 7, 14))


def get_location_of_next_spitters(file_name, x, y):
    tachyon_manifold_height = len(read_lines(file_name))
    new_y = y
    left_x = x - 1
    right_x = x + 1
    next_splitters_locations = []
    for i in range(1, tachyon_manifold_height - y):
        # case where we do not want to go lower on grid because we already have one or two in
        if len(next_splitters_locations) >= 1:
            break
        new_y = y + i
        # get new char for each location 
        new_char_left = get_char_from_location(file_name, left_x, new_y)
        new_char_right = get_char_from_location(file_name, right_x, new_y)
        # need to check symbol/char in new location is "^" then we should not continue to move Y
        if new_char_left == "^":
            next_splitters_locations.append((left_x, new_y))
        if new_char_right == "^":
            next_splitters_locations.append((right_x, new_y))

    return next_splitters_locations


print(get_location_of_next_spitters(s, 7, 0))
print(get_location_of_next_spitters(s, 7, 14))
print(get_location_of_next_spitters(s, 9, 10))
print(get_location_of_next_spitters(s, 11, 10))
print(get_location_of_next_spitters(s, 6, 12))
print(get_location_of_next_spitters(s, 9, 6))


# i may need to add lru cache to save locations which I already calculated how many beams leave tachyon manifold
# ali pa bi moral to napisati bolj optimizirano v smislu da tisti spodnji samo doda zgornjemu kolikor je donu
def part_2(file_name, x, y):
    # all_locations = get_coordinates_with_char(file_name)
    # tachyon_manifold_height = max([y for x, y, char in all_locations])
    # 
    # starting_point_with_location = [(x, y, char) for x, y, char in all_locations if char == "S"][0]
    # x0, y0, _ = starting_point_with_location
    # 
    counter = 0
    count_different_timelines = []
    next_locations = get_location_of_next_spitters(file_name, x, y)
    # escape condition
    print(next_locations)
    print(counter)
    if len(next_locations) == 0:
        return 2
        # return count_different_timelines
        # return count_different_timelines

    else:
        if len(next_locations) == 1:
            x1, y1 = next_locations[0]
            counter += part_2(file_name, x1, y1)
            # return 1
        else:
            x1, y1 = next_locations[0]
            x2, y2 = next_locations[1]
    
            # get new location left of splitter
            counter += part_2(file_name, x1, y1)
            counter += part_2(file_name, x2, y2)
            # return count_different_timelines
    return counter

@lru_cache(maxsize=None)
def part_2(file_name, x, y):
    counter = 0
    next_locations = get_location_of_next_spitters(file_name, x, y)
    if len(next_locations) != 2:
        if len(next_locations) == 1:
            x0, y0 = next_locations[0]
            return len(next_locations) +  part_2(file_name, x0, y0)
            # return 1
        else:
            return 2

    else:
        x1, y1 = next_locations[0]
        x2, y2 = next_locations[1]

        # get new location left of splitter
        return part_2(file_name, x1, y1) + part_2(file_name, x2, y2)
        # return count_different_timelines


# print(part_2(s_2, 7, 0)) # 8
# print(part_2(s_3, 7, 0)) # 13
print(part_2(s, 7, 0))  # 40


# print(part_2(l, 70, 0))


def test_part_1():
    assert part_1(s) == 21


def test_part_2():
    assert part_2(s, 7, 0) == 40
    assert part_2(s_2) == 8
    assert part_2(s_3) == 13


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    # print("First part: ", part_1(l))
    # print("Second part: ", part_2(l))

# 4032 too low
# 6384 too low
# ni pravi: 44011029008