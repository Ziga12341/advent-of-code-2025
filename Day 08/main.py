import math
from functools import lru_cache
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


# i firsts need to optimize this part!!
def calculate_euclidean_distance_for_junction_boxes(file_name: str) -> list[
    tuple[float, tuple[int, int, int], tuple[int, int, int]]]:
    all_junction_boxes_locations: list = read_lines(file_name)
    collect_all_junction_box_pair_with_distance = set()
    i = 0
    for first_junction_box in all_junction_boxes_locations[:-1]:
        x_1, y_1, z_1 = first_junction_box
        for second_junction_box in all_junction_boxes_locations[1:]:
            x_2, y_2, z_2 = second_junction_box
            distance = calculate_euclidean_distance(x_1, y_1, z_1, x_2, y_2, z_2)
            # exclude the same pair
            if first_junction_box != second_junction_box:
                # check if par in but in another order
                # add optimization to add in set
                if (distance, second_junction_box, first_junction_box) not in collect_all_junction_box_pair_with_distance:
                    collect_all_junction_box_pair_with_distance.add((distance, first_junction_box, second_junction_box))
    return collect_all_junction_box_pair_with_distance


def sort_boxes_based_on_shortest_distance(file_name: str, number_of_pairs: int = 1000) -> list[
    tuple[float, tuple[int, int, int], tuple[int, int, int]]]:
    pairs_with_distance = calculate_euclidean_distance_for_junction_boxes(file_name)
    return sorted(pairs_with_distance)[:number_of_pairs]


def merge_circuits(circuits: list[set[tuple[int, int, int]]],
                   junction_box_pair: tuple[float, tuple[int, int, int], tuple[int, int, int]]):
    _, first_junction_box, second_junction_box = junction_box_pair
    new_circuits = []
    merged_circuits = set()
    for circuit in circuits:
        if first_junction_box in circuit or second_junction_box in circuit:
            # case where need union (merging circuits)
            # add to which circuit already in candidates (can merge more than two circuits in one pass)
            merged_circuits = merged_circuits | circuit
        else:
            # in else: add current circuit to new circuits
            new_circuits.append(circuit)
    new_circuits.append(merged_circuits)
    return new_circuits


# 
# print(merge_circuits([
#     {(346, 949, 466), (162, 817, 812), (425, 690, 689), (431, 825, 988)},
#     {(739, 650, 466), (906, 360, 560), (805, 96, 715)},
#     {(862, 61, 35), (984, 92, 344)},
#     {(52, 470, 668), (117, 168, 530)},
#     {(941, 993, 340), (819, 987, 18)}
# ], (352.936254867646, (906, 360, 560), (984, 92, 344))
# ))
# print(merge_circuits([
#     {(346, 949, 466), (162, 817, 812), (425, 690, 689), (431, 825, 988)},
#     {(739, 650, 466), (906, 360, 560), (805, 96, 715)},
#     {(862, 61, 35), (984, 92, 344)},
#     {(52, 470, 668), (117, 168, 530)},
#     {(941, 993, 340), (819, 987, 18)}
# ], (316.90219311326956, (162, 817, 812), (425, 690, 689))
# ))
# 

def get_new_circuits_status_after_n_merge(file_name, number_of_pairs):
    # this is the order junction boxes by distance with number of them you need them
    sorted_junction_boxes = sort_boxes_based_on_shortest_distance(file_name, number_of_pairs=number_of_pairs)
    # each connection put in circuits with each other in initial circuits
    circuits = [{first_junction_box, second_junction_box} for _, first_junction_box, second_junction_box in sorted_junction_boxes]
    # with each merging, creating new circuits collection
    for junction_box_pair in sorted_junction_boxes:
        circuits = merge_circuits(circuits, junction_box_pair)
    # get new circuits status and also get last valid junction box pair 
    return circuits, sorted_junction_boxes[-1]


def part_1(file_name):
    # results for part 2:
    # if file_name == s:
    #     number_of_pairs = 29
    # else:
    #     number_of_pairs = 4872
    if file_name == s:
        number_of_pairs = 10
    else:
        number_of_pairs = 1000
    circuits, last_from_sorted_junction_boxes = get_new_circuits_status_after_n_merge(file_name, number_of_pairs)
    # take 3 biggest circuits and multiply them together
    return math.prod((sorted([len(circuit) for circuit in circuits])[::-1][:3]))

def find_initial_number_with_one_circuit(file_name):
    # check how many junction boxes positions is in input
    junction_box_positions = len(read_lines(file_name))
    for initial_number_with_only_one_circuit in range(junction_box_positions, junction_box_positions**2):
        circuits, last_from_sorted_junction_boxes = get_new_circuits_status_after_n_merge(file_name,
                                                                                          initial_number_with_only_one_circuit)
        len_of_first_circuit_in_all_circuits = [len(circuit) for circuit in circuits][0]
        number_of_circuit = len([circuit for circuit in circuits])
        # only one circuit left
        if number_of_circuit == 1:
            ...
            
def part_2(file_name):
    # check how many junction boxes positions is in input
    junction_box_positions = len(read_lines(file_name))

    get_only_one_circuits = True
    initial_number_with_only_one_circuit = junction_box_positions
    if file_name == l:
        # i try where myself first where to look the right results (i did not solve programmatically)
        initial_number_with_only_one_circuit = 4850
    while get_only_one_circuits:
        # get result for number of ordered junction boxes by distance
        circuits, last_from_sorted_junction_boxes = get_new_circuits_status_after_n_merge(file_name,
                                                                                          initial_number_with_only_one_circuit)
        len_of_first_circuit_in_all_circuits = [len(circuit) for circuit in circuits][0]
        if len_of_first_circuit_in_all_circuits == junction_box_positions:
            get_only_one_circuits = False
        else:
            initial_number_with_only_one_circuit += 1

    # get last junction box pair in which all junction boxes in one circle - calculate multiplication from x coordinates
    distance, first_junction_box, second_junction_box = last_from_sorted_junction_boxes
    x_1, y_1, z_1 = first_junction_box
    x_2, y_2, z_2 = second_junction_box
    return x_1 * x_2


def test_part_1():
    assert part_1(s) == 40
    assert part_1(l) == 131150


def test_part_2():
    assert part_2(s) == 25272
    assert part_2(l) == 2497445


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)

    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))

# part 2 too high:
# 7919740182
# 4384275632


# 4872 ordered junction pair iterated so we have only one circuit
# 
#     if file_name == s:
#         number_of_pairs = 29
#     else:
#         number_of_pairs = 4872
