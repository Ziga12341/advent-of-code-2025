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


def part_1(file_name):
    ...


def part_2(file_name):
    ...


def test_part_1():
    assert part_1(s) == None


def test_part_2():
    assert part_2(s) == None


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
