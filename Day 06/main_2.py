from cmath import polar
from sys import exc_info

s = "small_input.txt"
l = "input.txt"


# new version -  get just raw strings of numbers and operations separately
def read_lines(file_name: str) -> tuple[list[str], list[int]]:
    with open(file_name, "r", encoding="utf-8") as file:
        lines_to_list = [line.rstrip("\n") for line in file]
        operations = [operation for operation in lines_to_list[-1].strip().split(" ") if operation != ""]
        numbers_in_columns = []
        for column in lines_to_list[:-1]:
            numbers_in_columns.append(column)
        return operations, numbers_in_columns


print(read_lines(s))


# for each column we need to know how big is particular number (how many places (char) it takes)
def count_length_of_biggest_number_in_column(file_name: str):
    with open(file_name, "r", encoding="utf-8") as file:
        lines_to_list = [line for line in file]
        count_spaces = 1  # space on last number is missing (no next number) i will add it here 
        numbers_length_in_column = []
        # take only last line with operations and reverse it (because is easier to count spaces)
        for operation in reversed(lines_to_list[-1]):
            if operation == "*" or operation == "+":
                # detect on which index there is operator
                numbers_length_in_column.append(count_spaces)
                count_spaces = 0
            else:
                count_spaces += 1

        return numbers_length_in_column[::-1]


def cut_string_into_numbers_with_spaces(file_name):
    operations, numbers_in_columns = read_lines(file_name)
    cell_length = count_length_of_biggest_number_in_column(file_name)
    count_numbers_in_row = len(operations)
    rearranged_numbers = []
    for line in numbers_in_columns:
        new_column = []
        main_index = 0
        # count also " " space between numbers

        for i in range(count_numbers_in_row - 1):
            # get length of cell into for each index to know how much we need to move forward in slices
            length = cell_length[i]
            # slice line to get only number with relevant " " spaces
            new_column.append(line[main_index:main_index + length])
            # add one to skip inside spaces " " remove inside spaces
            main_index = main_index + length + 1

        # add last number in column (get last number length from cell_length function)
        new_column.append(line[main_index:main_index + cell_length[-1]])
        rearranged_numbers.append(new_column)
        new_column = []
    return rearranged_numbers


print(cut_string_into_numbers_with_spaces(l))


# put rows into columns, we need to get numbers from top to down in the same column nad in the same cell from top down
def remap_numbers_in_right_list(file_name):
    numbers_in_list = cut_string_into_numbers_with_spaces(file_name)
    new_order_list = []

    for i in range(len(numbers_in_list[0])):
        rearranged_list = []
        for j in range(len(numbers_in_list)):
            rearranged_list.append(numbers_in_list[j][i])
        new_order_list.append(rearranged_list)
        rearranged_list = []

    return new_order_list


print("this put rows to columns", remap_numbers_in_right_list(s))


# put rows into columns (change order in lists)
def transform_rows_to_columns(list_of_one_column):
    # get len of the biggest number
    list_max_number_size = len(max(list_of_one_column))
    new_transformed_list = []
    # j go over range of the biggest number
    for j in range(list_max_number_size):
        new_number = ""
        # in the second loop go over a list
        for number in list_of_one_column:
            new_number += number[j]
        new_transformed_list.append(new_number)
        new_number = ""

    return new_transformed_list


print(transform_rows_to_columns(['123', ' 45', '  6']))


# cut spaces from numbers and convert string into int and put in the same list (the same structure)
def transform_string_numbers_to_int(list_of_column):
    int_column = []
    for string_number in list_of_column:
        string_number = string_number.replace(" ", "")
        number = int(string_number)
        int_column.append(number)
    return int_column


print(transform_string_numbers_to_int(transform_rows_to_columns(['123', ' 45', '  6'])))


# helper function for multiplication in a list
def multiply_vertical_list(vertical_list: list[int]):
    multiplication = 1
    for number in vertical_list:
        multiplication *= number
    return multiplication


def part_2(file_name):
    grand_total = 0
    # transformed data already in 
    new_order_column_to_row = remap_numbers_in_right_list(file_name)
    operations, _ = read_lines(file_name)

    for i, column in enumerate(new_order_column_to_row):
        # multiplication or sum
        operation = operations[i]
        # transform and cut spaces
        ints_in_column_in_right_order = transform_string_numbers_to_int(transform_rows_to_columns(column))

        if operation == "*":
            grand_total += multiply_vertical_list(ints_in_column_in_right_order)
        else:
            grand_total += sum(ints_in_column_in_right_order)

    return grand_total


def test_part_2():
    assert part_2(s) == 3263827
    assert part_2(l) == 9608327000261


# too high
# 9675710241167

if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print("Second part: ", part_2(l))
