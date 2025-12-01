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
    point_at_zero = 0
    current_direction = 50
    for direction, distance in read_lines(file_name):

        # if goes multi circles goes multiple times over 0
        how_many_cycles = distance // 100
        point_at_zero += how_many_cycles
        distance = distance - how_many_cycles * 100

        if direction == "L":
            distance = - distance

        # figure out how if in the same cycle cross 0
        # if goes over 100 or over 0

        # two cases:
        # first: when distance is positive, we go clockwise; if we go from the current direction, and we finish on lower value than we cross zero
        # clockwise only count if current position and distance is over 100

        # i need to check not to start from 0 in order this logic to works
        if current_direction != 0:
            if distance > 0:
                if current_direction + distance > 100:
                    point_at_zero += 1
            # second: negative we go contra clockwise
            # current position is smaller than current position + distance
            else:
                if current_direction + distance < 0:
                    point_at_zero += 1

        # need to update "location" to new directions
        current_direction = (current_direction + distance) % 100
        # add how many times cross 0


        # check if after updating dial is pointing to zero:
        if current_direction == 0:
            point_at_zero += 1

    return point_at_zero



# def part_2(file_name):
#     point_at_zero = 0
#     current_direction = 50
#     for direction, distance in read_lines(file_name):
#
#         if direction == "L":
#             distance = - distance
#         new_distance = (current_direction + distance)
#         if current_direction != 0:
#             if new_distance > 100 or new_distance < 0:
#                 point_at_zero += abs(new_distance // 100)
#
#         current_direction = new_distance % 100
#         if current_direction == 0:
#             point_at_zero += 1
#
#     return point_at_zero

def test_part_1():
    assert part_1(s) == 3


def test_part_2():
    assert part_2(s) == 6


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
