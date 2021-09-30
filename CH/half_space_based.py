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
    result_file = open('half_space_based_computation_time.txt','w')
    for i in range(50):
        filename = './example_{0}.txt'.format((i+1)*10)
        point_list = gen_point_list(filename)
        time_start = time.time()
        convex_hull_set = half_space_based_algo(point_list)
        time_elasped = time.time() - time_start
        result_file.write(str(i*10)+'\t'+str(time_elasped)+'\n')
        print('done',(i+1)*10,time_elasped)
        #draw_result(set(point_list), convex_hull_set)
    result_file.close()