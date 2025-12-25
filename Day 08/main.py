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


@lru_cache(maxsize=None)
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
                collect_all_junction_box_pair_with_distance.add((distance, first_junction_box, second_junction_box))
    return collect_all_junction_box_pair_with_distance


print(calculate_euclidean_distance_for_junction_boxes(s))


def sort_boxes_based_on_shortest_distance(file_name: str, number_of_pairs: int = 1000) -> list[
    tuple[float, tuple[int, int, int], tuple[int, int, int]]]:
    if file_name == s:
        number_of_pairs = 10
    pairs_with_distance = calculate_euclidean_distance_for_junction_boxes(file_name)
    return sorted(pairs_with_distance)[:number_of_pairs]


print("=========")
print(sort_boxes_based_on_shortest_distance(s))


def merge_circuits(circuits: list[set[tuple[int, int, int]]],
                   junction_box_pair: tuple[float, tuple[int, int, int], tuple[int, int, int]]):
    _, first_junction_box, second_junction_box = junction_box_pair
    new_circuits = circuits
    first_circuit_to_merge = set()
    second_circuit_to_merge = set()

    for first_circuit in new_circuits:
        if first_junction_box in first_circuit:
            first_circuit_to_merge = first_circuit_to_merge | first_circuit
            # i think i can break loop after finding first circuit where first jb in
            # break

    for second_circuit in new_circuits:
        if first_circuit_to_merge != second_circuit:
            if second_junction_box in second_circuit:
                second_circuit_to_merge = second_circuit_to_merge | second_circuit
                # break

    # the first and second circuit should not be the same
    if first_circuit_to_merge and second_circuit_to_merge and first_circuit_to_merge != second_circuit_to_merge:
        # append union of first and second circuit, which were removed
        new_circuits.append(first_circuit_to_merge | second_circuit_to_merge)
        new_circuits.remove(first_circuit_to_merge)
        new_circuits.remove(second_circuit_to_merge)

        return new_circuits
    return circuits


def merge_circuits(circuits: list[set[tuple[int, int, int]]],
                   junction_box_pair: tuple[float, tuple[int, int, int], tuple[int, int, int]]):
    _, first_junction_box, second_junction_box = junction_box_pair
    new_circuits = []
    merged_circuits = set()
    for circuit in circuits:
        if first_junction_box in circuit or second_junction_box in circuit:
            # case where need union (merging circuits)
            # how to do it what do it what to do it???
            merged_circuits = merged_circuits | circuit
        else:
            # just add current circuit to new circuits
            new_circuits.append(circuit)
    new_circuits.append(merged_circuits)
    return new_circuits


print(merge_circuits([
    {(346, 949, 466), (162, 817, 812), (425, 690, 689), (431, 825, 988)},
    {(739, 650, 466), (906, 360, 560), (805, 96, 715)},
    {(862, 61, 35), (984, 92, 344)},
    {(52, 470, 668), (117, 168, 530)},
    {(941, 993, 340), (819, 987, 18)}
], (352.936254867646, (906, 360, 560), (984, 92, 344))
))
print(merge_circuits([
    {(346, 949, 466), (162, 817, 812), (425, 690, 689), (431, 825, 988)},
    {(739, 650, 466), (906, 360, 560), (805, 96, 715)},
    {(862, 61, 35), (984, 92, 344)},
    {(52, 470, 668), (117, 168, 530)},
    {(941, 993, 340), (819, 987, 18)}
], (316.90219311326956, (162, 817, 812), (425, 690, 689))
))

"""
[
{(346, 949, 466), (162, 817, 812), (425, 690, 689), (431, 825, 988)},
{(739, 650, 466), (906, 360, 560), (805, 96, 715)},
{(862, 61, 35), (984, 92, 344)},
{(52, 470, 668), (117, 168, 530)},
{(941, 993, 340), (819, 987, 18)}
]
"""


def get_circuits_candidates(file_name):
    sorted_junction_boxes = sort_boxes_based_on_shortest_distance(file_name)
    st_distance, st_first_junction_box, st_second_junction_box = sorted_junction_boxes[0]
    already_in_circuits = {st_first_junction_box, st_second_junction_box}
    collect_circuits = [{st_first_junction_box, st_second_junction_box}]
    for distance, first_junction_box, second_junction_box in sorted_junction_boxes[1:]:
        # this last one should connect two bigger circuits: (352.936254867646, (906, 360, 560), (984, 92, 344))
        for i in range(len(collect_circuits)):
            if first_junction_box in collect_circuits[i] or second_junction_box in collect_circuits[i]:
                if first_junction_box not in already_in_circuits:
                    collect_circuits[i].add(first_junction_box)
                if second_junction_box not in already_in_circuits:
                    collect_circuits[i].add(second_junction_box)

                already_in_circuits.add(first_junction_box)
                already_in_circuits.add(second_junction_box)

        # if there is junction box not already in any circuits than ?? add it to new one (bat should i add bouth??
        else:
            if first_junction_box not in already_in_circuits and second_junction_box not in already_in_circuits:
                collect_circuits.append({first_junction_box, second_junction_box})
            elif first_junction_box not in already_in_circuits:
                collect_circuits.append({second_junction_box})
            elif second_junction_box not in already_in_circuits:
                collect_circuits.append({first_junction_box})
            else:
                # print("in else")
                pass

            # collect_circuits.append({second_junction_box})
            already_in_circuits.add(first_junction_box)
            already_in_circuits.add(second_junction_box)
    return collect_circuits


def part_1(file_name):
    sorted_junction_boxes = sort_boxes_based_on_shortest_distance(file_name)
    circuits_candidates = get_circuits_candidates(file_name)
    # in order to know if i understand excercise correctly i would like to check this
    # i need to merge set-s if there is one element in others
    # this last one should connect two bigger circuits: (352.936254867646, (906, 360, 560), (984, 92, 344))
    circuits = []
    for junction_box in sorted_junction_boxes:
        if merge_circuits(circuits_candidates, junction_box):
            circuits_candidates = merge_circuits(circuits_candidates, junction_box)

    print(math.prod((sorted([len(circuit) for circuit in circuits_candidates])[::-1][:3])))

    # take 3 biggest circuits and multiply them together
    return math.prod((sorted([len(circuit) for circuit in circuits_candidates])[::-1][:3]))


print("test--- shortest distance")
print(sort_boxes_based_on_shortest_distance(s))
print(sort_boxes_based_on_shortest_distance(l))


def part_1(file_name):
    sorted_junction_boxes = sort_boxes_based_on_shortest_distance(file_name)
    circuits = [{first_junction_box, second_junction_box} for _, first_junction_box, second_junction_box in sorted_junction_boxes]
    for junction_box_pair in sorted_junction_boxes:
        circuits = merge_circuits(circuits, junction_box_pair)
    # take 3 biggest circuits and multiply them together
    return math.prod((sorted([len(circuit) for circuit in circuits])[::-1][:3]))


# need to figure out how to merge two bigger circuits when already created
print(part_1(s))
print(part_1(l))


def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 40


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    # print(small_input)
    print("First part: ", part_1(l))
    # print("Second part: ", part_2(l))

# Too low:
# 1080
