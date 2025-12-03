s = "small_input.txt"
l = "input.txt"


def read_lines(file_name: str) -> list[list[int]]:
    with open(file_name, "r", encoding="utf-8") as file:
        banks = []
        for line in file:
            bank = []
            line = line.strip()
            for digit in line:
                bank.append(int(digit))
            banks.append(bank)
            bank = []
        return banks


# find the biggest first digit in a bank with sorted and index
# cat last mean how many digits you do not have in collection for picking biggest int,
# because you need those digits for next iteration (next digits)
# if we looking for first digit of 12 we need to leave at least 11 digits untouched
def find_biggest_first_digit_in_bank(bank: list[int], cut_last_n=1) -> tuple[int, list[int]]:
    # the last one can be the first digit because we need two (cut it)
    bank_without_last_digit = bank[:-cut_last_n]
    biggest_digit_in_bank = sorted(bank_without_last_digit)[-1]
    biggest_digit_index = bank_without_last_digit.index(biggest_digit_in_bank)
    # get the first digit and list with candidates for the last digit
    return bank[biggest_digit_index], bank[biggest_digit_index + 1:]

# deprecated (used in part 1 initial version)
# def find_biggest_second_digit_in_remaining_bank(remaining_bank: list[int]) -> int:
#     biggest_digit_in_remaining_bank = sorted(remaining_bank)[-1]
#     biggest_digit_index = remaining_bank.index(biggest_digit_in_remaining_bank)
#     return remaining_bank[biggest_digit_index]


# add each bank first and second digit to joltage total
# def part_1(file_name):
#     total_output_joltage = 0
#     for bank in read_lines(file_name):
#         biggest_first_digit, remaining_bank = find_biggest_first_digit_in_bank(bank)
#         biggest_second_digit = find_biggest_second_digit_in_remaining_bank(remaining_bank)
#         # need to change to string that I can join digits in a list
#         total_output_joltage += int("".join([str(biggest_first_digit), str(biggest_second_digit)]))
#     return total_output_joltage

# -------------------------------------
# solved the same way as part 2... reusable code up is old way
def part_1(file_name):
    return sum_all_batteries(file_name, 2)


# return list of n digits that is the biggest number from the following battery bank
# n_batteries tells how many batteries we want to get from bank (how many digits)
# it works for n batteries but n needs to be smaller as it is length of initial bank
def collect_n_batteries(bank, n_batteries=12):
    batteries = []
    for i in range(n_batteries):
        if len(bank) == n_batteries - i:
            # if we need to fill just all numbers that are in bank, extend batteries and fill them
            batteries.extend(bank)
            return batteries
        if i == n_batteries - 1:
            # append the biggest what is left from an initial battery bank
            batteries.append(sorted(bank)[-1])
            return batteries
        # update a bank to meet and save the biggest digit from current position to a new battery bank
        biggest_current_digit, bank = find_biggest_first_digit_in_bank(bank, cut_last_n=n_batteries - 1 - i)
        batteries.append(biggest_current_digit)
    return batteries


# just merge list of digits in single number and sum all batteries output
def sum_all_batteries(file_name, n_batteries_digits=12):
    total_output_joltage = 0
    for bank in read_lines(file_name):
        digits_in_int = collect_n_batteries(bank, n_batteries_digits)
        battery_joltage_in_string = ""
        for digit in digits_in_int:
            battery_joltage_in_string += str(digit)
        total_output_joltage += int(battery_joltage_in_string)
    return total_output_joltage


def part_2(file_name):
    return sum_all_batteries(file_name, 12)


def test_first_biggest():
    assert find_biggest_first_digit_in_bank([8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1]) == (9,
                                                                                               [1, 1, 1, 1, 2, 1, 1, 1])


# deprecated
# def test_second_biggest():
#     assert find_biggest_second_digit_in_remaining_bank([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9]) == 9


def test_part_1():
    assert part_1(s) == 357
    assert part_1(l) == 16854


def test_collect_twelve_batteries():
    assert collect_n_batteries([9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1]) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1]
    assert collect_n_batteries([8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9]) == [8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9]
    assert collect_n_batteries([2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8]) == [4, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8]
    assert collect_n_batteries([8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1]) == [8, 8, 8, 9, 1, 1, 1, 1, 2, 1, 1, 1]


def test_part_2():
    assert part_2(s) == 3121910778619
    assert part_2(l) == 167526011932478


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
