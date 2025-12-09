s = "small_input.txt"
l = "input.txt"


def read_lines(file_name: str) -> tuple[list[str], list[int]]:
    with open(file_name, "r", encoding="utf-8") as file:
        lines_to_list = [line.strip() for line in file]

        operations = [operation for operation in lines_to_list[-1].strip().split(" ") if operation != ""]
        numbers_in_columns = []
        for column in lines_to_list[:-1]:
            new_column_to_int = [int(number) for number in column.strip().split(" ") if number != ""]
            numbers_in_columns.append(new_column_to_int)
        return operations, numbers_in_columns


def multiply_vertical_list(vertical_list: list[int]):
    multiplication = 1
    for number in vertical_list:
        multiplication *= number
    return multiplication

# put columns into one list
def part_1(file_name):
    grand_total = 0
    operations, numbers_in_columns = read_lines(file_name)
    for i, operation in enumerate(operations):
        new_list = []
        for j in range(len(numbers_in_columns)):
            # this is main part to put numbers in right list...
            new_list.append(numbers_in_columns[j][i])
        if operation == "*":
            grand_total += multiply_vertical_list(new_list)
        else:
            grand_total += sum(new_list)
        new_list = []
    return grand_total


def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 4277556
    assert part_1(l) == 4719804927602


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print(large_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
