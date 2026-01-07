from collections import defaultdict

s = "small_input.txt"
l = "input.txt"


def read_lines(file_name: str):
    with open(file_name, "r", encoding="utf-8") as file:
        devices = defaultdict(set)
        for line in file:
            split_line = (line.strip().split(": "))
            from_device = split_line[0]
            to_device = split_line[1].split(" ")
            # put into a dictionary key from where it comes to set of all possible path form particular one
            devices[from_device] = set(to_device)
    return devices


def part_1(file_name, start: str = "you"):
    devices_dictionary = read_lines(file_name)
    # check if key "out" in set() (return one)
    if devices_dictionary[start].__contains__("out"):
        return 1
    else:
        return sum([part_1(file_name, one_path) for one_path in devices_dictionary[start]])


def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 5
    assert part_1(l) == 690


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    # large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
