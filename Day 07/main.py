from idlelib.debugobj_r import remote_object_tree_item

s = "small_input.txt"
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


def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 21


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
