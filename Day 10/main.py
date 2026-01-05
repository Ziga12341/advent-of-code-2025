s = "small_input.txt"
l = "input.txt"


# put this into true false list from string: #.#.###.
def indicator_lights_diagram_mapper(str_indicator_light_diagram: str) -> list[bool]:
    # if indicator light is ON change with true
    return [char == "#" for char in str_indicator_light_diagram]


# put button wiring into tuples
# example:  (4,6,7) (1,5) (1,2,3,5) (0,1,3,4,6,7) (0,4,6) (2,4) (1,3,4) (2,3,4,5,6,7) (0,3) 
def button_wiring_into_list_of_tuples(str_button_wiring_schematics: str):
    # first remove additional " " at beginning and end
    # remove ( and ) form button
    # put ints into tuple
    return [tuple(int(button_lights) for button_lights in single_button[1:-1].split(',')) for single_button in
            str_button_wiring_schematics.split(" ")[1:-1]]


def read_lines(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        factory_machines_manual = []
        for line in file:
            light_diagram, button_and_joltage = line.strip().split("]")
            light_diagram = (light_diagram.split('[')[1])
            light_diagram = indicator_lights_diagram_mapper(light_diagram)
            button_wiring, joltage_requirements = button_and_joltage.split('{')
            button_wiring = button_wiring_into_list_of_tuples(button_wiring)
            joltage_requirements = [int(str_number) for str_number in joltage_requirements[:-1].split(",")]
            factory_machines_manual.append((light_diagram, button_wiring, joltage_requirements))
    return factory_machines_manual


# loop O(n * 2^n)
# each combination
# get each combination from single button
def create_all_combination_of_button_wiring_schematics(button_wiring_schematics: list[tuple[int]]) -> list[list[tuple[int]]]:
    all_wiring_combination = [[]]
    for single_button in button_wiring_schematics:
        one_combination_of_button_shema = []
        for combo in all_wiring_combination:
            one_combination_of_button_shema.append(combo + [single_button])
        all_wiring_combination.extend(one_combination_of_button_shema)
    # remove first empty element end sort all combination by length of buttons in one combination (smaller first)
    return sorted(all_wiring_combination[1:], key=len)


# from one combination get what indicator lights would turn on in true / false format [false, true, true, false]
# compare this to initial indicator light diagram
def compare_initial_indication_lights_with_turn_on_from_shema_combination(initial_indicator_lights: list[bool],
                                                                          one_combination_of_button_shema: list[tuple[int]]):
    dynamic_shema_indicator_lights = [0] * len(initial_indicator_lights)
    for button in one_combination_of_button_shema:
        for lights_on in button:
            dynamic_shema_indicator_lights[lights_on] += 1
    # if odd number on particular light return False if even make this light True (turn on)
    return [light_number % 2 != 0 for light_number in dynamic_shema_indicator_lights] == initial_indicator_lights


# for each line get all possible wiring combinations with all buttons (sorted by number of buttons) add len of buttons to sum and break inner loop
def part_1(file_name):
    count_button_presses = 0
    for light_diagram, button_wiring, joltage_requirements in read_lines(file_name):
        all_wiring_combination = create_all_combination_of_button_wiring_schematics(button_wiring)
        for wiring_combination in all_wiring_combination:
            if compare_initial_indication_lights_with_turn_on_from_shema_combination(light_diagram, wiring_combination):
                count_button_presses += len(wiring_combination)
                break
    return count_button_presses


def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 7
    assert part_1(l) == 390


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
