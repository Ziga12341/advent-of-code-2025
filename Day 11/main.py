from collections import defaultdict
from functools import lru_cache

s = "small_input.txt"
s2 = "small_input_part_2.txt"
l = "input.txt"


def read_lines(file_name: str):
    with open(file_name, "r", encoding="utf-8") as file:
        devices = defaultdict(list)
        for line in file:
            split_line = (line.strip().split(": "))
            from_device = split_line[0]
            to_device = split_line[1].split(" ")
            # put into a dictionary key from where it comes to set of all possible path form particular one
            devices[from_device].extend(to_device)
    return devices


def part_1(file_name, start: str = "you"):
    devices_dictionary = read_lines(file_name)
    # check if key "out" in set() (return one)
    if "out" in devices_dictionary[start]:
        return 1
    else:
        # sum all paths / different paths which go to "out"
        # if a path finishes in out - count one and sum all of them together and return a result at the end
        return sum([part_1(file_name, one_path) for one_path in devices_dictionary[start]])


# caching is a necessary 
# function argument if fft and dac are in (in that way you can use lru cache not to create a whole path)
@lru_cache(maxsize=None)
def part_2(file_name, start: str = "svr", fft_in=False, dac_in=False):
    devices_dictionary = read_lines(file_name)
    # check if key "out" in a list and if ftt and dac meet in a way - (return one)
    if "out" in devices_dictionary[start] and fft_in and dac_in:
        return 1
    else:
        count_right_paths = 0
        for one_path in devices_dictionary[start]:
            # one path is only one option form a list of way where you can go from one device
            # check if now path is ftt or dac... set initial function argument to this two
            if one_path == "fft":
                fft_in = True
            if one_path == "dac":
                dac_in = True
            # recursive call with this new path (NEXT STEP) and fft and dac as it is
            count_right_paths += part_2(file_name, one_path, fft_in, dac_in)
        # at the end i want to know sum of all valid paths
        return count_right_paths


print(part_2(l))


def test_part_1():
    assert part_1(s) == 5
    assert part_1(l) == 690


def test_part_2():
    assert part_2(s2) == 2
    assert part_2(l) == 557332758684000


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
