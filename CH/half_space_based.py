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
        return 1
    
    elif z < 0:
        return -1

    elif z == 0:
        return 0
    

def half_space_based_algo(point_list):
    convex_hull_set = set([])
    
    for i in range(len(point_list)-1):
        for j in range(i+1,len(point_list)):
            line_vector = Vector2D(point_list[i],point_list[j])
            if line_vector.x == 0 and line_vector.y == 0:
                continue
            
            discriminator = 0
            flag = True
            for target_point in point_list:
                current = discriminator + check_points_side(line_vector,target_point)
                if abs(discriminator) > abs(current):
                    flag = False
                    break
                else:
                    discriminator = current
            
            if flag:
                convex_hull_set.add(point_list[i])
                convex_hull_set.add(point_list[j])
    
    return convex_hull_set


if __name__ == "__main__":
    point_list = gen_point_list('./example_500.txt')
    
    time_start = time.time()
    convex_hull_set = half_space_based_algo(point_list)
    time_elapsed = time.time()-time_start
    print(time_elapsed)
    draw_result(set(point_list),convex_hull_set)