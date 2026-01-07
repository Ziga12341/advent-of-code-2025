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


print(create_all_combination_of_button_wiring_schematics(['a', 'b', 'c']))
print(create_all_combination_of_button_wiring_schematics([(3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)]))


# from one combination get what indicator lights would turn on in true / false format [false, true, true, false]
# compare this to initial indicator light diagram
def compare_initial_indication_lights_with_turn_on_from_shema_combination(initial_indicator_lights: list[bool],
                                                                          one_combination_of_button_shema: list[tuple[int]]):
    dynamic_shema_indicator_lights = [0] * len(initial_indicator_lights)
    for button in one_combination_of_button_shema:
        for lights_on in button:
            dynamic_shema_indicator_lights[lights_on] += 1
    # if odd number on particular light return True if even make this light False (turn on)
    # if we get the same as initial indicator return True
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

def lights_on_from_shema_combination(joltage_levels: list[int],
                                                                          one_combination_of_button_shema: list[tuple[int]]):
    dynamic_shema_indicator_lights = [0] * len(joltage_levels)
    for button in one_combination_of_button_shema:
        for lights_on in button:
            dynamic_shema_indicator_lights[lights_on] += 1
    return dynamic_shema_indicator_lights
print(lights_on_from_shema_combination([3,5,4,7], [(3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)]))

def new_shema_and_joltage_levels_the_same(joltage_levels: list[int],
                                                                          one_combination_of_button_shema: list[tuple[int]]):
    return lights_on_from_shema_combination(joltage_levels, one_combination_of_button_shema) == joltage_levels

def all_joltage_level_in_range(joltage_levels: list[int], suggested_light_shema_combination: list[tuple[int]]):
    new_shema_lights_on = lights_on_from_shema_combination(joltage_levels, suggested_light_shema_combination)
    return all(new_shema_lights_on[i] <= joltage_level for i, joltage_level in enumerate(joltage_levels))

print(all_joltage_level_in_range([3, 5, 4, 7], [(3,), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (2,), (2, 3), (0, 2), (0, 1)]))
from collections import defaultdict
def get_buttons_dictionary_by_lights(new_button_shema: list[tuple[int]]):
    dict_of_buttons_by_lights = defaultdict(set)
    for button in new_button_shema:
        for light in button:
            dict_of_buttons_by_lights[light].add(button)
    return dict_of_buttons_by_lights

print(get_buttons_dictionary_by_lights([(3,), (3,), (3,), (3,), (3,), (1, 3), (2,), (0, 2), (0, 1)]))

def valid_combination_by_joltage_index(joltage_levels: list[int], button_wiring_schematics: list[tuple[int]]) -> bool:
    lights_by_index = get_buttons_dictionary_by_lights(button_wiring_schematics)
    for i, joltage_level in enumerate(joltage_levels):
        count_buttons_for_one_joltage_level = 0
        for button in lights_by_index[i]:
            count_buttons_for_one_joltage_level += button_wiring_schematics.count(button)
        if count_buttons_for_one_joltage_level > joltage_level:
            return False
    return True

print(valid_combination_by_joltage_index([3, 5, 4, 7], [(3,), (1, 3), (1, 3), (1, 3), (1, 3), (2,), (2, 3), (0, 2), (0, 1)]))
    
def create_joltage_requirements_all_combination_candidates(joltage_levels: list[int], button_wiring_schematics: list[tuple[int]]) -> list[list[tuple[int]]]:
    all_wiring_combination = [[]]
    for single_button in button_wiring_schematics:
        multi_combination_of_button_shema = []
        for combo in all_wiring_combination:
            new_combination = combo + [single_button]
            # figure out how to skip more new combinations
            # something in logic... 
            if all_joltage_level_in_range(joltage_levels, new_combination) and valid_combination_by_joltage_index(joltage_levels, new_combination):
                multi_combination_of_button_shema.append(new_combination)
        for combination in multi_combination_of_button_shema:
            # TODO: this 1.5 is problem... fix this logically
            if combination not in all_wiring_combination and len(combination) < max(joltage_levels) * 1.5:
                all_wiring_combination.append(combination)
    # remove first empty element end sort all combination by length of buttons in one combination (smaller first)
    return sorted(all_wiring_combination[1:], key=len)


print(create_joltage_requirements_all_combination_candidates([3, 5, 4, 7], [(3,), (3,), (3,), (3,), (3,), (3,), (1, 3), (1, 3), (1, 3), (1, 3), (2,), (2,), (2,), (2,), (2, 3), (2, 3), (2, 3), (2, 3), (0, 2), (0, 2), (0, 2), (0, 1), (0, 1), (0, 1), (0, 1)]))
print(len(create_joltage_requirements_all_combination_candidates([3, 5, 4, 7],
                                                                 [(3,), (3,), (3,), (3,), (3,), (3,), (1, 3), (1, 3), (1, 3),
                                                                  (1, 3), (2,), (2,), (2,), (2,), (2, 3), (2, 3), (2, 3), (2, 3),
                                                                  (0, 2), (0, 2), (0, 2), (0, 1), (0, 1), (0, 1), (0, 1)])))
first_original_shema = [(3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)]
new_shema = [(3,), (3,), (3,), (3,), (3,), (3,), (1, 3), (1, 3), (1, 3), (1, 3), (2,), (2,), (2,), (2,), (2, 3), (2, 3), (2, 3), (2, 3), (0, 2), (0, 2), (0, 2), (0, 1), (0, 1), (0, 1), (0, 1)]
first_joltage_levels = [3, 5, 4, 7]

new_shema = [(3,), (3,), (3,), (3,), (3,), (3,), (1, 3), (1, 3), (1, 3), (1, 3), (2,), (2,), (2,), (2,), (2, 3), (2, 3), (2, 3), (2, 3), (0, 2), (0, 2), (0, 2), (0, 1), (0, 1), (0, 1), (0, 1)]
first_joltage_levels = [3, 5, 4, 7]

def create_max_combination_of_new_wiring_buttons_for_joltage_levels(joltage_levels: list[int],
                                                                          original_button_wiring_schema: list[tuple[int]]):
    all_possible_buttons = []
    for button in original_button_wiring_schema:
        smallest_possible_in_button = float('inf') # infinity in python
        for indicator_light in button:
            current_joltage_level = joltage_levels[indicator_light]
            if current_joltage_level < smallest_possible_in_button:
                smallest_possible_in_button = current_joltage_level
        for i in range(smallest_possible_in_button):
            all_possible_buttons.append(button)
    return all_possible_buttons

print(create_max_combination_of_new_wiring_buttons_for_joltage_levels(first_joltage_levels, first_original_shema))
big_input_first_shema = read_lines(l)[119][1]
big_input_first_joltage = read_lines(l)[119][2]
big_input_shema_all_combinations = create_max_combination_of_new_wiring_buttons_for_joltage_levels(big_input_first_joltage, big_input_first_shema)
print(big_input_first_shema)
print(big_input_first_joltage)
print(big_input_shema_all_combinations)
print("new_shema_and_joltage_levels_the_same()", new_shema_and_joltage_levels_the_same(first_joltage_levels, [(3,), (1, 3), (1, 3), (1, 3), (2, 3), (2, 3), (2, 3), (0, 2), (0, 1), (0, 1)]))
# for candidate in create_joltage_requirements_all_combination_candidates(big_input_first_joltage, big_input_shema_all_combinations):
#     if new_shema_and_joltage_levels_the_same(big_input_first_joltage, candidate):
#         print(candidate)

def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == 7
    assert part_1(l) == 390


def test_part_2():
    assert part_2(s) == 33


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
