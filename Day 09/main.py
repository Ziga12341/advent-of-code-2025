s = "small_input.txt"
l = "input.txt"


def read_lines(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        return [(int(line.strip().split(",")[0]), int(line.strip().split(",")[1])) for line in file]


def calculate_rectangle_area(x_1: int, y_1: int, x_2: int, y_2: int):
    return (abs(x_1 - x_2) + 1) * (abs(y_1 - y_2) + 1)


def compare_each_corner(file_name):
    collect_all_corner_combinations = set()
    all_red_tile_locations = read_lines(file_name)
    for first_corner in all_red_tile_locations[:-1]:
        x_1, y_1 = first_corner
        for second_corner in all_red_tile_locations[1:]:
            x_2, y_2 = second_corner
            if first_corner != second_corner:
                area_result = calculate_rectangle_area(x_1, y_1, x_2, y_2)
                if (area_result, second_corner, first_corner) not in collect_all_corner_combinations:
                    collect_all_corner_combinations.add((area_result, first_corner, second_corner))
    return collect_all_corner_combinations

print(sorted(compare_each_corner(s)))
def part_1(file_name):
    return sorted(compare_each_corner(file_name))[-1][0]


def part_2(file_name):
    ...


def test_part_1():
    assert calculate_rectangle_area(2, 5, 11, 1) == 50
    assert calculate_rectangle_area(7, 3, 2, 3) == 6
    assert calculate_rectangle_area(2, 5, 9, 7) == 24
    assert part_1(s) == 50
    assert part_1(l) == 4748985168


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
