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


# find invalid id form - first part
def is_invalid_id(id_from_range: int) -> bool | None:
    id_from_range = str(id_from_range)
    how_many_decimals = len(id_from_range)
    if how_many_decimals % 2 == 0:
        where_to_split = how_many_decimals // 2
        return id_from_range[:where_to_split] == id_from_range[where_to_split:]
    return None


def part_1(file_name):
    sum_invalid_ids = 0
    for first_id, second_id in read_lines(file_name):
        for id_number in range(first_id, second_id + 1):
            if is_invalid_id(id_number):
                sum_invalid_ids += id_number
    return sum_invalid_ids


# how to break string just need to break string into smaller units?

# calculate common devisor for each number length
# example 100 000 has 6 digits which mean len(number) is 6
# you can brake this number into 2 or 3 or 6 smaller pieces
def common_devisor(number):
    all_devisors = []
    for step in range(1, number + 1):
        if number % step == 0:
            # remove all divided by 1 because I do not need it (buggy with devisor 1)
            if step != 1:
                all_devisors.append(step)
    return all_devisors


# iterative approach
def is_invalid_id_part_2(number: int):
    for devisor in common_devisor(len(str(number))):
        collection_of_devisor_chunks = set()
        new_number = str(number)
        for i in range(devisor):
            # I take the first element from initial number (set by devisor) and add in set()
            # then update new number without a chunk which is already in set (continue until empty)
            collection_of_devisor_chunks.add(new_number[:len(str(number)) // devisor])
            new_number = new_number[len(str(number)) // devisor:]
        # if lists saved in a set collection all the same, then we have invalid id
        if len(collection_of_devisor_chunks) == 1:
            return True
        # if not, set a collection to an empty list and continue with another devisor
        else:
            collection_of_devisor_chunks = set()
    return None


# the same code as in part 2 but changed check for invalid id
def part_2(file_name):
    actual_numbers = []
    sum_invalid_ids = 0
    for first_id, second_id in read_lines(file_name):
        for id_number in range(first_id, second_id + 1):
            if is_invalid_id_part_2(id_number):
                sum_invalid_ids += id_number
                actual_numbers.append(id_number)
    return sum_invalid_ids


def test_part_1():
    assert part_1(s) == 1227775554
    assert is_invalid_id(22)
    assert is_invalid_id(11)


def test_invalid_id_part_2():
    assert is_invalid_id_part_2(11)
    assert is_invalid_id_part_2(1010)
    assert is_invalid_id_part_2(1188511885)
    assert is_invalid_id_part_2(565656)
    assert is_invalid_id_part_2(2121212121)
    assert not is_invalid_id_part_2(12)


def test_part_2():
    assert part_2(s) == 4174379265
    assert part_2(l) == 27469417404


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
