from vertex_and_triangle import *
from vector2d import *
import numpy as np
import matplotlib.pyplot as plt
from point_generator import *
import time

def make_super_triangle(point_list):
    max_x = point_list[0].x
    min_x = point_list[0].x
    max_y = point_list[0].y
    min_y = point_list[0].y

    for point in point_list[1:]:
        if point.x < min_x:
            min_x = point.x
            
        if point.x > max_x:
            max_x = point.x

        if point.y < min_y:
            min_y = point.y

        if point.y > max_y:
            max_y = point.y  

    # st_p1 = Vertex((max_x + min_x)/2, 2*max_y-min_y, True)
    # st_p2 = Vertex(2*max_x-min_x+1, min_y-1, True)
    # st_p3 = Vertex(2*min_x-max_x-1, min_y-1, True)
    st_p1 = Vertex(-1e6,-2e6, True)
    st_p2 = Vertex(1e6,-2e6, True)
    st_p3 = Vertex(0, 1e6, True)
    super_triangle = Triangle(st_p1, st_p2, st_p3)

    return super_triangle





def search_for_target_triangle(point, triangle_set):
    for target_triangle in triangle_set:
        checker = check_inside_or_outside(point, target_triangle)
        if checker == "inside":
            return target_triangle

def check_inside_or_outside(target_point, triangle):
    triangle_vertices = sort_triangle_vertices(triangle.vertices)
    flag = True
    for i in range(3):
        vt = Vector2D(triangle_vertices[i-1], triangle_vertices[i])
        vk = Vector2D(triangle_vertices[i-1], target_point)
        z = cross_product(vt, vk)
        if z < 0:
            flag = False
            break    
    if flag:
        return "inside"
    
    else:
        #print("Fail to find")
        return "outside"

def sort_triangle_vertices(triangle_vertices):
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

def cross_product(v1, v2):
    z = v1.x*v2.y - v2.x*v1.y
    return z





def make_temp_triangle(target_edges_vertices, inner_point):
    temp_triangle= Triangle(target_edges_vertices[0],target_edges_vertices[1],inner_point)
    
    return temp_triangle

def find_adjacent_triangle(target_edges_vertices, inner_point):
    vertex_1 = target_edges_vertices[0]
    vertex_2 = target_edges_vertices[1]
    
    adjacent_triangle_list = list(((vertex_1.belonged_triangles & vertex_2.belonged_triangles) - inner_point.belonged_triangles))
    if len(adjacent_triangle_list) == 1:
        adjacent_triangle = adjacent_triangle_list[0]

    elif len(adjacent_triangle_list) == 0:
        adjacent_triangle = None
    
    else:
        #print('Fail to find correct adjacent triangle.')
        raise Exception('Fail to find correct adjacent triangle.')

    return adjacent_triangle

    new_adjacent_triangle_1 = find_adjacent_triangle([outer_point, common_vertices[0]], inner_point)
    update_delaunay_triangle(delaunay_triangle_set, fliped_triangle_1, new_adjacent_triangle_1)



def update_delaunay_triangle(delaunay_triangle_set, temp_triangle, adjacent_triangle, point):
    if adjacent_triangle:
        checker = check_flip_or_not(temp_triangle, adjacent_triangle, point) 
        if checker:
            delaunay_triangle_set.remove(adjacent_triangle)
            fliped_triangle_1, fliped_triangle_2 = make_fliped_triangle(temp_triangle, adjacent_triangle)
            
            delaunay_triangle_set.add(fliped_triangle_1)
            check_until_finish(delaunay_triangle_set, fliped_triangle_1, point)
            delaunay_triangle_set.add(fliped_triangle_2)
            check_until_finish(delaunay_triangle_set, fliped_triangle_2, point)
    
        else:
            delaunay_triangle_set.add(temp_triangle)

    else:
        delaunay_triangle_set.add(temp_triangle)

def update_successive_triangle(delaunay_triangle_set, temp_triangle, adjacent_triangle, point):
    if adjacent_triangle:
        checker = check_flip_or_not(temp_triangle, adjacent_triangle, point) 
        if checker:
            delaunay_triangle_set.remove(adjacent_triangle)
            delaunay_triangle_set.remove(temp_triangle)
            fliped_triangle_1, fliped_triangle_2 = make_fliped_triangle(temp_triangle, adjacent_triangle)
            
            delaunay_triangle_set.add(fliped_triangle_1)
            check_until_finish(delaunay_triangle_set, fliped_triangle_1, point)
            delaunay_triangle_set.add(fliped_triangle_2)
            check_until_finish(delaunay_triangle_set, fliped_triangle_2, point)

def check_until_finish(delaunay_triangle_set, fliped_triangle, inner_point):
    target_edge_vertices = list(set(fliped_triangle.vertices) - set([inner_point])) 
    adjacent_triangle = find_adjacent_triangle(target_edge_vertices, inner_point)
    update_successive_triangle(delaunay_triangle_set, fliped_triangle, adjacent_triangle, inner_point)

def check_flip_or_not(temp_triangle, adjacent_triangle, point):
    common_vertices, inner_point, outer_point = distinguish_vertices(temp_triangle, adjacent_triangle)
    if outer_point.is_superset:
        return False

    if inner_point != point:
        print("something_wrong!")
    result_1 = point_inclusion_test(inner_point, adjacent_triangle)
    result_2 = point_inclusion_test(outer_point, temp_triangle)
    
    if result_1 or result_2:
        return True

def make_fliped_triangle(temp_triangle, adjacent_triangle):
    common_vertices, inner_point, outer_point = distinguish_vertices(temp_triangle, adjacent_triangle)

    del_triangles(temp_triangle)
    del_triangles(adjacent_triangle)
    fliped_triangle_1 = Triangle(inner_point, outer_point, common_vertices[0])
    fliped_triangle_2 = Triangle(inner_point, outer_point, common_vertices[1])

    return fliped_triangle_1, fliped_triangle_2

def del_triangles(triangle):
    vertices = triangle.vertices
    for vertex in vertices:
        vertex.del_belonged_triangle(triangle)

def distinguish_vertices(temp_triangle, adjacent_triangle):
    common_vertices = list(set(temp_triangle.vertices) & set(adjacent_triangle.vertices))
    inner_point = list(set(temp_triangle.vertices) - set(common_vertices))[0]
    outer_point = list(set(adjacent_triangle.vertices) - set(common_vertices))[0]

    return common_vertices, inner_point, outer_point

def point_inclusion_test(target_point, triangle):
    center, radius = cal_circumcircle_center_and_radius(triangle)
    distance = np.linalg.norm(center-[target_point.x, target_point.y])
    
    if distance < radius:
        return True

def cal_circumcircle_center_and_radius(triangle):
    p1,p2,p3 = triangle.vertices
    vb_1 = cal_vertical_bisector(p1,p2)
    vb_2 = cal_vertical_bisector(p2,p3)
    A = np.array([vb_1[0],vb_2[0]])
    B = np.array([vb_1[1],vb_2[1]])

    center = np.linalg.solve(A,B)
    radius = np.linalg.norm(center-[p1.x,p1.y])

    return center, radius

def cal_vertical_bisector(p1,p2):
    incline = (p2.y-p1.y)/(p2.x-p1.x)
    try:
        a = -1/incline
        b = -1
        c = (p1.x+p2.x)/2*a - (p1.y+p2.y)/2
    except:
        a = 1
        b = 0
        c = (p1.x+p2.x)/2

    return [[a,b], c]



def make_delaunay_triangle_set(point_list):
    delaunay_triangle_set = set([])    
    super_triangle = make_super_triangle(point_list)
    delaunay_triangle_set.add(super_triangle)

    for point in point_list:
        #draw_triangles(delaunay_triangle_set, point)
        target_triangle = search_for_target_triangle(point, delaunay_triangle_set)
        delaunay_triangle_set.remove(target_triangle)
        del_triangles(target_triangle)

        for i in range(3):
            target_edges_vertices = (target_triangle.vertices[i-1], target_triangle.vertices[i])
            temp_triangle = make_temp_triangle(target_edges_vertices, point)
            #edge class로 정리하면 인접 삼각형 찾기 훨씬 간단할 것
            adjacent_triangle = find_adjacent_triangle(target_edges_vertices, point)
        
            update_delaunay_triangle(delaunay_triangle_set, temp_triangle, adjacent_triangle, point)
        
    del_super_triangle_line(super_triangle,delaunay_triangle_set)

    return delaunay_triangle_set

def del_super_triangle_line(super_triangle, delaunay_triangle_set):
    vertices = super_triangle.vertices
    connected_triangles = set(vertices[0].belonged_triangles) | set(vertices[1].belonged_triangles) | set(vertices[2].belonged_triangles)
    for triangle in connected_triangles:
        delaunay_triangle_set.remove(triangle)


def draw_triangles(triangle_set, point = None):
    plt.rcParams["figure.figsize"] = (10,10)
    plt.axes().set_aspect('equal')
    for triangle in triangle_set:
        x_list = [triangle.vertices[0].x, triangle.vertices[1].x, triangle.vertices[2].x, triangle.vertices[0].x]
        y_list = [triangle.vertices[0].y, triangle.vertices[1].y, triangle.vertices[2].y, triangle.vertices[0].y]
        

        plt.scatter(x_list, y_list, c = 'black')
        plt.plot(x_list, y_list, c = 'red')
        # try:
        #     plt.scatter(point.x, point.y, c = 'green')
        # except:
        #     continue
    plt.show()





if __name__ == "__main__":
    time_record_file = open("./time_record.txt",'w')

    for i in range(1):
        num = (i+1)*100
        point_list = gen_point_list('./example_files/example_{0}.txt'.format(7000))
        
        start_time = time.time()
        delaunay_triangle_set = make_delaunay_triangle_set(point_list)
        total_time = time.time()-start_time
        time_record_file.write('{0}\t{1}'.format(num, total_time))
        print(total_time)
        draw_triangles(delaunay_triangle_set)
    
    time_record_file.close()