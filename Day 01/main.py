s = "small_input.txt"
l = "input.txt"


def read_lines(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        return [(line.strip()[0], int(line.strip()[1:])) for line in file]


def part_1(file_name):
    point_at_zero = 0
    current_direction = 50
    for direction, distance in read_lines(file_name):
        if direction == "L":
            distance = - distance
        current_direction = (current_direction + distance) % 100
        if current_direction == 0:
            point_at_zero += 1

    return point_at_zero


def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 3


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
