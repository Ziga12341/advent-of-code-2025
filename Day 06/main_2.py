from cmath import polar
from sys import exc_info

s = "small_input.txt"
l = "input.txt"

# new version
def read_lines(file_name: str) -> tuple[list[str], list[int]]:
    with open(file_name, "r", encoding="utf-8") as file:
        lines_to_list = [line.rstrip("\n") for line in file]

        operations = [operation for operation in lines_to_list[-1].strip().split(" ") if operation != ""]
        numbers_in_columns = []
        for column in lines_to_list[:-1]:
            new_column_to_int = [number for number in column]
            numbers_in_columns.append(column)
        return operations, numbers_in_columns
print(read_lines(s))


def count_length_of_biggest_number_in_column(file_name: str):
    with open(file_name, "r", encoding="utf-8") as file:
        lines_to_list = [line for line in file]
        count_spaces = 1  # space on last number is missing (no next number) i will add it here 
        numbers_length_in_column = []
        # take only last line with operations and reverse it (because is easier to count spaces)
        for operation in reversed(lines_to_list[-1]):
            if operation == "*" or operation == "+":
                numbers_length_in_column.append(count_spaces)
                count_spaces = 0
            else:
                count_spaces += 1

        return numbers_length_in_column[::-1]


print(count_length_of_biggest_number_in_column(l))
print(count_length_of_biggest_number_in_column(s))


def cut_string_into_numbers_with_spaces(file_name):
    operations, numbers_in_columns = read_lines(file_name)
    cell_length = count_length_of_biggest_number_in_column(file_name)
    count_numbers_in_row = len(operations)
    rearranged_numbers = []
    for line in numbers_in_columns:
        new_column =  []
        main_index = 0
        # count also " " space between numbers
        # new_column.append(line[start_index:end_index])

        for i in range(count_numbers_in_row - 1):
            # print(length)
            length = cell_length[i]

            # index_to_add += 1
            # start_index += index_to_add
            # end_index += index_to_add
            new_column.append(line[main_index:main_index + length])
            main_index = main_index + length + 1
        
        # add last number in column
        new_column.append(line[main_index:main_index + cell_length[-1]])
        rearranged_numbers.append(new_column)
        new_column = []
        start_index = 0
    return rearranged_numbers
        
print(cut_string_into_numbers_with_spaces(l))

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

def index_of_spaces(file_name: str):
    with open(file_name, "r", encoding="utf-8") as file:
        lines_to_list = [line.strip() for line in file]
        numbers_in_row = len([operation for operation in lines_to_list[-1].strip().split(" ") if operation != ""])
        i = 0
        space_index = set()
        for column in lines_to_list[:-1]:
            for number in column.strip().split(" "):
                if number != "":
                    i += 1
                else:
                    space_index.add(i % numbers_in_row)
        return sorted(space_index)

   
    
def not_split(file_name: str):
    with open(file_name, "r", encoding="utf-8") as file:
        lines_to_list = [line for line in file]
        numbers_length_in_column = count_length_of_biggest_number_in_column(file_name)
        i = 0
        # print(lines_to_list[-1])
        for column in lines_to_list[:-1]:
            for colum_length in numbers_length_in_column:
                start_index = 0
                end_index = colum_length
                # print(column[:3])
                ...

def transform_rows_to_columns(list_of_one_column):
    list_max_number_size = len(max(list_of_one_column))
    new_transformed_list = []
    # how to detect on which side is " "
    for j in range(list_max_number_size):

        new_number = ""
        for i, number in enumerate(list_of_one_column):
            new_number += number[j]
        new_transformed_list.append(new_number)
        new_number = ""

    return new_transformed_list

print(transform_rows_to_columns(['123', ' 45', '  6']))
print(transform_rows_to_columns(['328', '64 ', '98 ']))
print(transform_rows_to_columns([' 51', '387', '215']))

def transform_string_numbers_to_int(list_of_column):
    int_column = []
    for string_number in list_of_column:
        string_number = string_number.replace(" ", "")
        number = int(string_number)
        int_column.append(number)
    return int_column

print(transform_string_numbers_to_int(['1  ', '24 ', '356']))
print(transform_string_numbers_to_int(transform_rows_to_columns(['123', ' 45', '  6'])))

def multiply_vertical_list(vertical_list: list[int]):
    multiplication = 1
    for number in vertical_list:
        multiplication *= number
    return multiplication

"""
64
23
314
----
read from right to left each digit is own column (read column from top to 
4 + 431 + 623 = 1058
"""

def part_2(file_name):
    grand_total = 0
    new_order_column_to_row = remap_numbers_in_right_list(file_name)
    operations, _ = read_lines(file_name)

    for i, column in enumerate(new_order_column_to_row):
        # multiplication or sum
        operation = operations[i]
        
        ints_in_column_in_right_order = transform_string_numbers_to_int(transform_rows_to_columns(column))

        if operation == "*":
            grand_total += multiply_vertical_list(ints_in_column_in_right_order)
        else:
            grand_total += sum(ints_in_column_in_right_order)

    return grand_total

print(part_2(s))



def test_part_2():
    assert part_2(s) == 3263827

# too high
# 9675710241167

if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print("Second part: ", part_2(l))
