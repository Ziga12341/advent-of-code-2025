s = "small_input.txt"
l = "input.txt"


def read_lines(file_name: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        return [(int(line.strip().split(",")[0]), int(line.strip().split(",")[1])) for line in file]


def calculate_rectangle_area(x_1: int, y_1: int, x_2: int, y_2: int):
    return (abs(x_1 - x_2) + 1) * (abs(y_1 - y_2) + 1)
# up zgorni predel
print("nice try part 2 up", calculate_rectangle_area(4837,34263,94901,48488))
# 4837,34263
# 94901,48488
# rezultat: 1281264690
# check down:
print("nice try part 2 down", calculate_rectangle_area(5921,67692,94901,50265))

# 5921,67692
# 94901,50265
#  rezultat: 1550760868
# vec na spodnjo!
def each_red_corner_with_corner_area_calculation(file_name):
    collect_all_corner_combinations = set()
    all_red_tile_locations = read_lines(file_name)
    for first_corner in all_red_tile_locations[:-1]:
        x_1, y_1 = first_corner
        for second_corner in all_red_tile_locations[1:]:
            x_2, y_2 = second_corner
            if first_corner != second_corner:
                area_result = calculate_rectangle_area(x_1, y_1, x_2, y_2)
                if (area_result, second_corner, first_corner) not in collect_all_corner_combinations:
                    # possible optimization to remove rectangles in one line
                    # if not rectangle_in_one_row(x_1, y_1, x_2, y_2):
                    collect_all_corner_combinations.add((area_result, first_corner, second_corner))
    return collect_all_corner_combinations


print(sorted(each_red_corner_with_corner_area_calculation(s)))
print((len(each_red_corner_with_corner_area_calculation(s))))
print((len(each_red_corner_with_corner_area_calculation(l))))


def part_1(file_name):
    return sorted(each_red_corner_with_corner_area_calculation(file_name))[-1][0]


# check it rectangle in one line
def rectangle_in_one_row(x_1: int, y_1: int, x_2: int, y_2: int):
    return x_1 == x_2 or y_1 == y_2


# check if any initial red tile more to the outside of particular point in 4 directions
# first any initial red tile in area right - top from point
def initial_red_tile_location_top_right(file_name: str, x: int, y: int):
    red_tile_locations = read_lines(file_name)
    # if any red tile location is more top and right from input x, y point
    return any(x_0 >= x and y_0 <= y for x_0, y_0 in red_tile_locations)


print('===')
print(initial_red_tile_location_top_right(s, 9, 5))


def initial_red_tile_location_bottom_right(file_name: str, x: int, y: int):
    red_tile_locations = read_lines(file_name)
    # if any red tile location is more bottom and right from input x, y point
    return any(x_0 >= x and y_0 >= y for x_0, y_0 in red_tile_locations)


def initial_red_tile_location_bottom_right(file_name: str, x: int, y: int):
    red_tile_locations = read_lines(file_name)
    # if any red tile location is more bottom and right from input x, y point
    for x_0, y_0 in red_tile_locations:
        if x_0 >= x and y_0 >= y:
            return True
    return False


print(initial_red_tile_location_bottom_right(s, 11, 5))


def initial_red_tile_location_bottom_left(file_name: str, x: int, y: int):
    red_tile_locations = read_lines(file_name)
    # if any red tile location is more bottom and left from input x, y point
    return any(x_0 <= x and y_0 >= y for x_0, y_0 in red_tile_locations)


print(initial_red_tile_location_bottom_left(s, 2, 7))
print(initial_red_tile_location_bottom_left(s, 2, 5))


def initial_red_tile_location_top_left(file_name: str, x: int, y: int):
    red_tile_locations = read_lines(file_name)
    # if any red tile location is more top and left from input x, y point
    return any(x_0 <= x and y_0 <= y for x_0, y_0 in red_tile_locations)


def initial_red_tile_location_top_left(file_name: str, x: int, y: int):
    red_tile_locations = read_lines(file_name)
    # if any red tile location is more top and left from input x, y point
    for x_0, y_0 in red_tile_locations:
        if x_0 <= x and y_0 <= y:
            return True
    return False


print(initial_red_tile_location_top_left(s, 2, 1))
print(initial_red_tile_location_top_left(s, 2, 3))
# (4618517036, (16587, 15444), (83238, 84736), 'FIRST TOP LEFT')
print("test first input top left on big input: ", initial_red_tile_location_top_left(l, 16587, 15444))
print("test second input bottom right on big input: ", initial_red_tile_location_bottom_right(l, 83238, 84736))


# from each rectangle point I will get the opposite points from other corners which do not have red tiles
# example: if currently i have top left point and bottom right, here i will calculate bottom left and top right location
# x1, y1 will become x1, y2 and x2, y2 will become x2, y1
# then i will check if this new points are still in area of red and green tiles (valid area)
def mirror_all_rectangle_points(file_name):
    all_red_corners = each_red_corner_with_corner_area_calculation(file_name)
    mirror_locations = set()
    for area, first_corner_location, second_corner_location in all_red_corners:
        x_1, y_1 = first_corner_location
        x_2, y_2 = second_corner_location
        mirror_locations.add((area, (x_1, y_2), (x_2, y_1)))
    return mirror_locations


print(sorted(mirror_all_rectangle_points(s)))

# ----- new implementation -----
print("new implementation")
def get_three_points_for_each_step(file_name):
    all_points = read_lines(file_name)
    three_points_for_each_step = []
    for i in range(len(all_points) - 2):
        three_points_for_each_step.append((all_points[i],all_points[i + 1], all_points[i + 2]))
    return three_points_for_each_step

print(get_three_points_for_each_step(s))

# buggy implementation
def get_x_and_y_length_and_direction(file_name):
    three_points_for_step = get_three_points_for_each_step(file_name)
    length_and_direction = []
    for first_point, second_point, third_point in three_points_for_step:
        x1, y1 = first_point
        x2, y2 = second_point
        x3, y3 = third_point
        
        # get reference for second point
        
        # horizontal line "|"
        if x1 == x2:
            length = abs(y1 - y2)
            # if y2 is bigger the directions between point 1 and point 2 is from top to down
            if y2 > y1:
                point_1_point_2_direction = "down"
            else:
                point_1_point_2_direction = "up"
            # if x3 bigger than x2 from point 2 to point 3 goes right
            if x3 > x2:
                point_2_point_3_direction = "right"
            else:
                point_2_point_3_direction = "left"
        # horizontal line between second and third_point
        elif x2 == x3:
            length = abs(x1 - x2)
            # if y3 is bigger the directions between point 1 and point 2 is from top to down
            if y3 > y2:
                point_2_point_3_direction = "down"
            else:
                point_2_point_3_direction = "up"
            if x2 > x1:
                point_1_point_2_direction = "right"
            else:
                point_1_point_2_direction = "left"
        # vertical line "-" (between first and second point)
        elif y1 == y2:
            length = abs(x1 - x2)
            if x2 > x1:
                point_1_point_2_direction = "right"
            else:
                point_1_point_2_direction = "left"
            
            # case where line between paint 2 and point 3 goes down
            if y3 > y2:
                point_2_point_3_direction = "down"
            else:
                point_2_point_3_direction = "up"
        
        # vertical line between second and third_point ("-")
        elif y2 == y3:
            length = abs(y1 - y2)
            # if y3 is bigger, the directions between point 1 and point 2 is from top to down
            if x3 > x2:
                point_2_point_3_direction = "right"
            else:
                point_2_point_3_direction = "left"
            if y2 > y1:
                point_1_point_2_direction = "down"
            else:
                point_1_point_2_direction = "up"
        
        length_and_direction.append((length, second_point, point_1_point_2_direction, point_2_point_3_direction, (first_point, second_point, third_point)))
    
    return length_and_direction
print(get_x_and_y_length_and_direction(s))

def find_top_five_length(file_name):
    return sorted(get_x_and_y_length_and_direction(file_name))[-5:][::-1]
print(find_top_five_length(s))

print(find_top_five_length(l))
for line in find_top_five_length(l):
    print(line)

# part 2 solution explained for large input - not programmatically solved

# from find_top_five_length() you get candidates for biggest x or y difference between two points
# in my case there small and lagre input has biggest difference in x direction "-"
# in both cases there is clockwise "path" of red tiles
# from get_x_and_y_length_and_direction() you see point 1 and 2 direction n and point 2 and 3 direction
# now you know that from which two points you need to look for biggest area
# first ypu check from middle point if you need ot look up or down
# middle point with point difference: 92536 is (94901, 50265)
# check first how much room you need to go down : take only points that are more to right form this point and down
# the more far point in y is (94907, 68050)
# this give us room 17785
# find point on the other sice with smaller y (4837, 34263)
# now you calculate area between those points... and you get the right result

print("end of new implementation")
# ----- new implementation -----


# check if any red tiles is in area more to outside (left and up) of current opposite / mirror point
def part_2(file_name):
    # first need to figure out which point is on right or on left side
    mirror_locations = mirror_all_rectangle_points(file_name)
    new_valid_locations = set()
    for area, first_mirror_location, second_mirror_location in mirror_locations:
        x_1, y_1 = first_mirror_location
        x_2, y_2 = second_mirror_location
        if rectangle_in_one_row(x_1, y_1, x_2, y_2):
            # print("this is rectangle in one row - valid")
            # valid because this is in one row (the end and beginning of row is red tile
            new_valid_locations.add((area, first_mirror_location, second_mirror_location, "ONE ROW ONLY"))
        # first location (x_1) is bigger than x_2 that means first (x_1) is on right side of grid
        # this can't be in the same row because of check above
        elif x_1 > x_2:
            # first is on the right side
            if y_1 > y_2:
                # first is right and down (bottom right)
                # check first for this location and also second for opposite (diagonal) location
                if initial_red_tile_location_bottom_right(file_name, x_1, y_1) and initial_red_tile_location_top_left(file_name,
                                                                                                                      x_2, y_2):
                    # add this location as also valid in new area (inside red and green tiles)
                    new_valid_locations.add((area, first_mirror_location, second_mirror_location, "FIRST BOTTOM RIGHT"))
            else:
                # first right and up (top right)
                if initial_red_tile_location_top_right(file_name, x_1, y_1) and initial_red_tile_location_bottom_left(file_name,
                                                                                                                      x_2, y_2):
                    new_valid_locations.add((area, first_mirror_location, second_mirror_location, "FIRST TOP RIGHT"))

        elif x_1 < x_2:
            # first is on the left side
            if y_1 > y_2:
                # first is left and down (bottom left)
                # second in opposite diagonal site top left
                if initial_red_tile_location_bottom_left(file_name, x_1, y_1) and initial_red_tile_location_top_right(file_name,
                                                                                                                      x_2, y_2):
                    new_valid_locations.add((area, first_mirror_location, second_mirror_location, "FIRST BOTTOM LEFT"))

            else:
                # first left and up (top left)
                # second diagonale right bottom
                if initial_red_tile_location_top_left(file_name, x_1, y_1) and initial_red_tile_location_bottom_right(file_name,
                                                                                                                      x_2, y_2):
                    new_valid_locations.add((area, first_mirror_location, second_mirror_location, "FIRST TOP LEFT"))

    print(sorted(new_valid_locations))
    return sorted(new_valid_locations)[-1][0]



def test_part_1():
    assert calculate_rectangle_area(2, 5, 11, 1) == 50
    assert calculate_rectangle_area(7, 3, 2, 3) == 6
    assert calculate_rectangle_area(2, 5, 9, 7) == 24
    assert part_1(s) == 50
    assert part_1(l) == 4748985168


def test_part_2():
    assert part_2(s) == 24
    assert part_2(l) == 1550760868


if __name__ == "__main__":
    small_input = read_lines(s)
    large_input = read_lines(l)
    print(small_input)
    print("First part: ", part_1(l))
    print("Second part small: ", part_2(s))
    # print("Second part: ", part_2(l))

# part 2 too low:
# 93243 - result not correct for case if rectangle is in one line only

# part 2 too high:
# 4618517036

# part 2 fail:
# 1281264690