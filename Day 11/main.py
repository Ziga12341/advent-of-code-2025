from collections import defaultdict
from functools import lru_cache

s = "small_input.txt"
s2 = "small_input_part_2.txt"
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


# 
# def svr_to_out_path(file_name, start: str = "svr"):
#     print(start)
#     devices_dictionary = read_lines(file_name)
#     # check if key "out" in set() (return one)
#     
#     if devices_dictionary[start].__contains__("out"):
#         return [start]
#     else:
#         return [start] + [svr_to_out_path(file_name, one_path) for one_path in devices_dictionary[start]]

# def svr_to_out_path(file_name, path: list = ["svr"]):
#     print(path)
#     devices_dictionary = read_lines(file_name)
#     # check if key "out" in set() (return one)
#     
#     if path[-1] == "out":
#         return path
#     else: 
#         return path + [svr_to_out_path(file_name, devices_dictionary[path[-1][0]])]
# 
# print(svr_to_out_path(s2))

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

# i want to add cashing for path already known from one point...
@lru_cache(maxsize=None)
def part_2(file_name, start: str = "svr", fft_in=False, dac_in=False):
    devices_dictionary = read_lines(file_name)
    print("start", start)
    print("dict start: ", devices_dictionary[start])
    # check if key "out" in set() (return one)
    if devices_dictionary[start].__contains__("out") and fft_in and dac_in:
        return 1
    else:
        sumaraza = 0
        for one_path in range(len(devices_dictionary[start])):
            new_step = devices_dictionary[start].pop()
            # could be that it work only for first time once true always true
            if new_step == "fft":
                fft_in = True
            if new_step == "dac":
                dac_in = True
            if new_step == "out":
                
                print("next step is out!!!!!")

            sumaraza += part_2(file_name, new_step, fft_in, dac_in)
            print((sumaraza, one_path, devices_dictionary[start]))

        return sumaraza

# second try... caching worked

@lru_cache(maxsize=None)
def part_2(file_name, start: str = "svr", fft_in=False, dac_in=False):
    devices_dictionary = read_lines(file_name)
    print("start", start)
    print("dict start: ", devices_dictionary[start])
    # check if key "out" in set() (return one)
    if devices_dictionary[start].__contains__("out") and fft_in and dac_in:
        return 1
    else:
        sumaraza = 0
        for one_path in devices_dictionary[start]:
            new_step = one_path
            # could be that it work only for first time once true always true
            if new_step == "fft":
                fft_in = True
            if new_step == "dac":
                dac_in = True
            if new_step == "out":
                
                print("next step is out!!!!!")

            sumaraza += part_2(file_name, new_step, fft_in, dac_in)
            print((sumaraza, one_path, devices_dictionary[start]))

        return sumaraza


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



# this is too high part 2 l
# 1833812855518320

# each time different result?? how is this possible?
# 1401654963133080
# 1065343787514900
# 805766464795500
# 1393810306014600