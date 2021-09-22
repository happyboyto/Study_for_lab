from vector2d import Vector2D
from point_generator import *
from draw_result import *
import time

def cross_product(v1, v2):
    z = v1.x*v2.y - v2.x*v1.y
    return z

def find_start_point(point_list):
    start_point = point_list[0]
    for curr_point in point_list[1:]:
        curr_y = curr_point.y
        if start_point.y > curr_y:
            start_point = curr_point

    return start_point

def cal_slope(p1, p2):
    slope = (p2.y-p1.y)/(p2.x-p1.x)

    return slope

def sort_all_point_as_CCW(reference_point, point_list):
    plus_slope_dict = dict()
    minus_slope_dict = dict()

    for curr_point in point_list:
        if curr_point == reference_point:
            continue
        else:
            slope = cal_slope(reference_point,curr_point)
        
            if slope >= 0:
                plus_slope_dict[slope] = curr_point
            elif slope < 0:
                minus_slope_dict[slope] = curr_point
    
    sorted_plus_slope_list = list(dict(sorted(plus_slope_dict.items())).values())
    sorted_minus_slope_list = list(dict(sorted(minus_slope_dict.items())).values())
    sorted_list = sorted_plus_slope_list + sorted_minus_slope_list
    sorted_list.insert(0,reference_point)

    return sorted_list

def check_points_side(original_point, target1, target2):
    reference_vector = Vector2D(original_point,target1)
    check_vector = Vector2D(original_point, target2)

    z = cross_product(reference_vector, check_vector)

    if z > 0:
        return "OK"

    elif z < 0:
        return "Not OK"

    elif z == 0:
        print('wow')
        return "On the line"


def graham_scan_algo(point_list):
    convex_hull_set = set([])
    start_point = find_start_point(point_list)
    sorted_list = sort_all_point_as_CCW(start_point, point_list)

    
    index_list = [0,1]
    for i in range(2,len(sorted_list)):
        index_list.append(i)
        while True:
            p1 = sorted_list[index_list[-3]]
            p2 = sorted_list[index_list[-2]]
            p3 = sorted_list[index_list[-1]]
            checker = check_points_side(p1,p2,p3)
            if checker == 'OK':
                break
            else:
                index_list.pop()

    for j in index_list:
        convex_hull_set.add(sorted_list[j])

    return convex_hull_set



if __name__ == "__main__":
    point_list = gen_point_list('./example_50.txt')
    
    time_start = time.time()
    convex_hull_set = graham_scan_algo(point_list)
    time_elasped = time.time() - time_start
    print(time_elasped)
    draw_result(set(point_list), convex_hull_set)