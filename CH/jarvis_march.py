from vector2d import Vector2D
from point_generator import *
from draw_result import *
import time


def cross_product(v1, v2):
    z = v1.x*v2.y - v2.x*v1.y
    return z


def check_points_side(original_vector, target_point):
    target_vector = Vector2D(original_vector.start_point, target_point)
    z = cross_product(original_vector, target_vector)

    if z > 0:
        return "Left"

    elif z < 0:
        return "Right"

    elif z == 0:
        return "On the line"


def find_most_left_side_point(point_list):
    most_left_side_point = None
    for curr_point in point_list:
        curr_x = curr_point.x
        if most_left_side_point == None:
            most_left_side_point = curr_point
        elif most_left_side_point.x > curr_x:
            most_left_side_point = curr_point

    return most_left_side_point


def find_next_point(prev_point, point_list):
    next_point = point_list[0]

    for i in range(1, len(point_list)):
        original_vector = Vector2D(prev_point, next_point)
        target_point = point_list[i]
        result = check_points_side(original_vector, target_point)
        if result == 'Left':
            next_point = point_list[i]

    return next_point


def jarvis_march_algo(point_list):
    convex_hull_set = set([])
    first_point = find_most_left_side_point(point_list)
    convex_hull_set.add(first_point)
    start_point = first_point
    while True:
        next_point = find_next_point(start_point, point_list)
        if first_point == next_point:
            break
        else:
            convex_hull_set.add(next_point)
            start_point = next_point

    return convex_hull_set


if __name__ == "__main__":
    point_list = gen_point_list('./example_500.txt')
    
    time_start = time.time()
    convex_hull_set = jarvis_march_algo(point_list)
    time_elasped = time.time() - time_start
    print(time_elasped)
    draw_result(set(point_list), convex_hull_set)
    