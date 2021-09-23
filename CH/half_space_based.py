from vector2d import Vector2D
from point_generator import *
from draw_result import *
import time

def cross_product(v1, v2):
    z = v1.x*v2.y - v2.x*v1.y
    return z

def check_points_side(line_vector, target_point):
    target_vector = Vector2D(line_vector.start_point, target_point)
    z = cross_product(line_vector,target_vector)

    if z > 0:
        return 'Right'
    
    elif z < 0:
        return 'Left'

    # elif z == 0:
    #     return 'On the line'
    

def half_space_based_algo(point_list):
    convex_hull_set = set([])
    for i in range(len(point_list)-1):
        for j in range(i+1,len(point_list)):
            line_vector = Vector2D(point_list[i],point_list[j])
            if point_list[i].x == point_list[j].x and point_list[i].y == point_list[j].y:
                continue

            flag = True
            left_num = 0
            right_num = 0 
            for target_point in point_list:
                current = check_points_side(line_vector,target_point)
                if current == 'Right':
                    right_num +=1
                elif current == 'Left':
                    left_num +=1
                # elif current == 'On the line':
                #     continue

                if left_num and right_num:
                    flag = False
                    break
                
            if flag:
                convex_hull_set.add(line_vector.start_point)
                convex_hull_set.add(line_vector.end_point)

    return convex_hull_set


if __name__ == "__main__":
    point_list = gen_point_list('./example_500.txt')
    
    time_start = time.time()
    convex_hull_set = half_space_based_algo(point_list)
    time_elapsed = time.time()-time_start
    print(time_elapsed)
    draw_result(set(point_list),convex_hull_set)