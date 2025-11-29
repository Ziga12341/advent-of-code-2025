import os

# Define the code to write into each main.py file as a string
code_to_write = '''s = "small_input.txt"
l = "input.txt"


def read_lines(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


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
'''

# Create folders for 12 days (Advent of Code 2025 is only 12 days)
for day in range(1, 13):
    day_str = f"Day {day:02d}"  # Zero-pad the day number to two digits
    new_path = os.path.join(os.getcwd(), day_str)

    # Create the directory if it doesn't exist
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    # Create empty input files in the directory
    input_path = os.path.join(new_path, "input.txt")
    small_input_path = os.path.join(new_path, "small_input.txt")

    if not os.path.exists(input_path):
        with open(input_path, 'w', encoding='utf-8') as f:
            pass  # Create empty file

    if not os.path.exists(small_input_path):
        with open(small_input_path, 'w', encoding='utf-8') as f:
            pass  # Create empty file

    # Write the specified code into main.py only if it doesn't already exist
    main_py_path = os.path.join(new_path, "main.py")
    if not os.path.exists(main_py_path):
        with open(main_py_path, 'w', encoding='utf-8') as f:
            f.write(code_to_write)

print("Created folders for Day 01 through Day 12!")
print("\nTo use:")
print("  cd 'Day 01'")
print("  uv run main.py          # Run the solution")
print("  uv run pytest main.py   # Run tests")
