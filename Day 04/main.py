s = "small_input.txt"
l = "input.txt"

# how a direction x, y change for a different direction
directions = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, -1),
    "D": (0, 1),
    "LU": (-1, -1),
    "RU": (1, -1),
    "LD": (-1, 1),
    "RD": (1, 1),
}


def read_lines(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


# get position of a particular neighbour and check if it is in grid
def position_neighbour(initial_grid: list[str], x: int, y: int, direction: str) -> tuple[int, int] | None:
    grid = initial_grid
    x1, y1 = directions[direction]
    new_x = x + x1
    new_y = y + y1
    if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
        return new_x, new_y


def all_position_neighbours(initial_grid: list[str], x: int, y: int) -> list[tuple[int, int]]:
    # grid = read_lines(file_name)
    # if 0 < x < len(grid[0]) and 0 < y < len(grid)
    all_valid_neighbours = []
    for direction in directions:
        neighbour = position_neighbour(initial_grid, x, y, direction)
        if neighbour:
            all_valid_neighbours.append(neighbour)

    return all_valid_neighbours


grid = read_lines(s)


# collect positions of neighbours (do not need positions later in code)
def roll_papers_from_position(initial_grid: list[str], x: int, y: int) -> list[tuple[int, int]]:
    roll_paper_positions_from_initial_position = []
    for x0, y0 in all_position_neighbours(initial_grid, x, y):
        if initial_grid[y0][x0] == "@":
            roll_paper_positions_from_initial_position.append((x0, y0))
    return roll_paper_positions_from_initial_position


# check how many near roll papers has less than 3 roll papers and count them
def part_1(file_name):
    grid = read_lines(file_name)
    count_accessed_roll_papers = 0
    for y, row in enumerate(grid):
        for x, symbol in enumerate(row):
            if symbol == "@" and len(roll_papers_from_position(grid, x, y)) <= 3:
                count_accessed_roll_papers += 1
    return count_accessed_roll_papers


# here I get the current removed roll papers from grid and new state.
# I collect new grid without removed roll papers "@"
def new_state_with_removed_roll_papers(grid):
    count_accessed_roll_papers = 0
    new_state = []
    for y, row in enumerate(grid):
        collect_new_row = ""
        for x, symbol in enumerate(row):
            if symbol == "@" and len(roll_papers_from_position(grid, x, y)) <= 3:
                count_accessed_roll_papers += 1
                collect_new_row += "."
            else:
                collect_new_row += symbol
        new_state.append(collect_new_row)
    return count_accessed_roll_papers, new_state


def part_2(file_name):
    count_accessed_roll_papers = 0
    initial_state = read_lines(file_name)
    removed_roll_paper_changed = True
    while removed_roll_paper_changed:
        removed_roll_papers, initial_state = new_state_with_removed_roll_papers(initial_state)
        count_accessed_roll_papers += removed_roll_papers
        if removed_roll_papers == 0:
            return count_accessed_roll_papers
    return count_accessed_roll_papers


def test_part_1():
    assert part_1(s) == 13


def test_part_2():
    assert part_2(s) == 43
    assert part_2(l) == 8739


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part: ", part_2(l))
