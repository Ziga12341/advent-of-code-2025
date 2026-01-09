s = "small_input.txt"
l = "input.txt"

present_shapes_quantity_large = {
    0: 5,
    1: 7,
    2: 6,
    3: 7,
    4: 7,
    5: 7
}

present_shapes_quantity_small = {
    0: 7,
    1: 7,
    2: 7,
    3: 7,
    4: 7,
    5: 7
}


# I read only the second part of input (the first part is represented above in dict)
# i did not precess whole input! removed first part and manually solved
def read_lines_without_persent_shapes(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        region_and_presents = []
        for line in file:
            grid, presents_quantity = line.strip().split(": ")
            column, row = grid.split("x")
            presents_quantity = [int(present) for present in presents_quantity.split()]
            region_and_presents.append(((int(column), int(row)), presents_quantity))
    return region_and_presents


# to solve this puzzle it was enough just to check how many units cover one present
# this works on bigger area (grid) because in the middle section all units (grid places) would be full
def part_1(file_name: str, present_shapes_quantity: dict = present_shapes_quantity_large):
    count_present_fit_grid = 0
    for grid, presents_quantity in read_lines_without_persent_shapes(file_name):
        column, row = grid
        whole_grid_area = column * row
        present_space_calculation = 0
        # list of presents with quantity by index - get quantity from dict above
        for i, present in enumerate(presents_quantity):
            present_space_calculation += present_shapes_quantity[i] * present

        # calculate the percentage of covered units (places in grid) with present_space_calculation / whole_grid_area
        # this is just good enough approach to finish lagre input (this approach does not solve small input)
        count_present_fit_grid += present_space_calculation / whole_grid_area < 1

    return count_present_fit_grid


def test_part_1():
    assert part_1(l) == 499


if __name__ == "__main__":
    small_input = read_lines_without_persent_shapes(s)
    large_input = read_lines_without_persent_shapes(l)
    print(small_input)
    print("First part: ", part_1(l))
