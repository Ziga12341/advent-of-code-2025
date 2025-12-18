import math
from math import sqrt

s = "small_input.txt"
l = "input.txt"


def read_lines(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        data = []
        for line in file:
            x, y, z = line.strip().split(",")
            x = int(x)
            y = int(y)
            z = int(z)
            data.append((x, y, z))
        return data


def calculate_euclidean_distance(x_1: int, y_1: int, z_1: int, x_2: int, y_2: int, z_2: int) -> float:
    return math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2 + (z_1 - z_2) ** 2)


def calculate_euclidean_distance_for_junction_boxes(file_name: str) -> list[tuple[float, int, int]]:
    all_junction_boxes_locations: list = read_lines(file_name)
    collect_all_junction_box_pair_with_distance = []
    for first_junction_box in all_junction_boxes_locations[:-1]:
        x_1, y_1, z_1 = first_junction_box
        for second_junction_box in all_junction_boxes_locations[1:]:
            x_2, y_2, z_2 = second_junction_box
            distance = calculate_euclidean_distance(x_1, y_1, z_1, x_2, y_2, z_2)
            # exclude the same pair
            if first_junction_box != second_junction_box:
                # check if par in but in another order
                if (distance, second_junction_box, first_junction_box) not in collect_all_junction_box_pair_with_distance:
                    collect_all_junction_box_pair_with_distance.append((distance, first_junction_box, second_junction_box))
    return collect_all_junction_box_pair_with_distance


print(calculate_euclidean_distance_for_junction_boxes(s))


def sort_boxes_based_on_shortest_distance(file_name: str, number_of_pairs: int = 1000) -> list[tuple[float, int, int]]:
    if file_name == s:
        number_of_pairs = 10
    pairs_with_distance = calculate_euclidean_distance_for_junction_boxes(file_name)
    return sorted(pairs_with_distance)[:number_of_pairs]


print(sort_boxes_based_on_shortest_distance(s))


def part_1(file_name):
    sorted_junction_boxes = sort_boxes_based_on_shortest_distance(file_name)
    st_distance, st_first_junction_box, st_second_junction_box = sorted_junction_boxes[0]
    collect_circuits = [{st_first_junction_box, st_second_junction_box}]
    for distance, first_junction_box, second_junction_box in sorted_junction_boxes[1:]:
        for i in range(len(collect_circuits)):
            if first_junction_box in collect_circuits[i] or second_junction_box in collect_circuits[i]:
                collect_circuits[i].add(first_junction_box)
                collect_circuits[i].add(second_junction_box)
        # if there is junction box not already in any circuits than ?? add it to new one (bat should i add bouth??
        else:
            collect_circuits.append({first_junction_box, second_junction_box})
            # collect_circuits.append({second_junction_box})
    return collect_circuits


print(part_1(s))


def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 40


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    # print("First part: ", part_1(l))
    # print("Second part: ", part_2(l))
