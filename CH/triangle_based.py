# 점 세개를 골라 삼각형을 그리고 그 안에 있는 점들을 버린다.
from vector2d import Vector2D
from point_generator import *
from draw_result import *
import time

def cross_product(v1, v2):
    z = v1.x*v2.y - v2.x*v1.y
    return z


def sort_as_CCW(triangle_vertices):
    p1,p2,p3 = triangle_vertices
    v1 = Vector2D(p1, p2)
    v2 = Vector2D(p1, p3)
    z = cross_product(v1, v2)

    if z > 0:
        return [p1, p2, p3]

    elif z < 0:
        return [p1, p3, p2]

    elif z == 0:
        return -1


def check_inside_or_outside(triangle, point_list, survived_list):
    updated_survived_set = set([])
    
    for point in survived_list:
        for i in range(3):
            vt = Vector2D(triangle[i-1], triangle[i])
            vk = Vector2D(triangle[i-1], point)
            z = cross_product(vt, vk)
            if z > 0:
                continue
            else:
                updated_survived_set.add(point)
                break

    return updated_survived_set


def triangle_based_algo(point_list):
    survived_set = set(point_list)

    for i in range(len(point_list)-2):
        for j in range(i+1,len(point_list)-1):
            for k in range(j+1,len(point_list)):
                if point_list[i] not in survived_set or point_list[j] not in survived_set or point_list[k] not in survived_set:
                    continue
                else:
                    curr_triangle_vertices = point_list[i], point_list[j], point_list[k]
                    sorted_triangle = sort_as_CCW(curr_triangle_vertices)
                    if sorted_triangle == -1:
                        continue
                    survived_set = check_inside_or_outside(sorted_triangle, point_list, list(survived_set))
                

    convex_hull_set = survived_set

    return convex_hull_set
 
if __name__ == "__main__":
    result_file = open('triangle_based_computation_time.txt','w')
    for i in range(50):
        filename = './example_{0}.txt'.format((i+1)*10)
        point_list = gen_point_list(filename)
        time_start = time.time()
        convex_hull_set = triangle_based_algo(point_list)
        time_elasped = time.time() - time_start
        result_file.write(str(i*10)+'\t'+str(time_elasped)+'\n')
        print('done',(i+1)*10,time_elasped)
        #draw_result(set(point_list), convex_hull_set)
    result_file.close()