s = "small_input.txt"
l = "input.txt"


def read_lines(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        all_id_ranges_in_int = []
        list_of_ranges = file.readline().strip().split(",")
        for id_range in list_of_ranges:
            first_id, second_id = id_range.strip().split("-")
            all_id_ranges_in_int.append((int(first_id), int(second_id)))
        return all_id_ranges_in_int


# find invalid id form
def is_invalid_id(id_from_range: int) -> bool:
    id_from_range = str(id_from_range)
    how_many_decimals = len(id_from_range)
    if how_many_decimals % 2 == 0:
        where_to_split = how_many_decimals // 2
        return id_from_range[:where_to_split] == id_from_range[where_to_split:]


def part_1(file_name):
    sum_invalid_ids = 0
    for first_id, second_id in read_lines(file_name):
        for id_number in range(first_id, second_id + 1):
            if is_invalid_id(id_number):
                sum_invalid_ids += id_number
    return sum_invalid_ids

def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 1227775554
    assert is_invalid_id(22)
    assert is_invalid_id(11)

def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
