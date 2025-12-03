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
def find_biggest_first_digit_in_bank(bank: list[int]) -> tuple[int, list[int]]:
    # the last one can be the first digit because we need two (cut it)
    bank_without_last_digit = bank[:-1]
    biggest_digit_in_bank = sorted(bank_without_last_digit)[-1]
    biggest_digit_index = bank_without_last_digit.index(biggest_digit_in_bank)
    # get the first digit and list with candidates for the last digit
    return bank[biggest_digit_index], bank[biggest_digit_index + 1:]


def find_biggest_second_digit_in_remaining_bank(remaining_bank: list[int]) -> int:
    biggest_digit_in_remaining_bank = sorted(remaining_bank)[-1]
    biggest_digit_index = remaining_bank.index(biggest_digit_in_remaining_bank)
    return remaining_bank[biggest_digit_index]


# add each bank first and second digit to joltage total
def part_1(file_name):
    total_output_joltage = 0
    for bank in read_lines(file_name):
        biggest_first_digit, remaining_bank = find_biggest_first_digit_in_bank(bank)
        biggest_second_digit = find_biggest_second_digit_in_remaining_bank(remaining_bank)
        # need to change to string that I can join digits in a list
        total_output_joltage += int("".join([str(biggest_first_digit), str(biggest_second_digit)]))
    return total_output_joltage


def part_2(file_name):
    ...


def test_first_biggest():
    assert find_biggest_first_digit_in_bank([8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1]) == (9,
                                                                                               [1, 1, 1, 1, 2, 1, 1, 1])


def test_second_biggest():
    assert find_biggest_second_digit_in_remaining_bank([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9]) == 9


def test_part_1():
    assert part_1(s) == 357
    assert part_1(l) == 16854


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
