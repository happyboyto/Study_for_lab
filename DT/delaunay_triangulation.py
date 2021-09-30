from vertex_and_triangle import *
from vector2d import *
import numpy as np
import matplotlib.pyplot as plt
from point_generator import *

def make_super_set_triangle(point_list):
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

    st_p1 = Vertex((max_x + min_x)/2, 2*max_y-min_y)
    st_p2 = Vertex(2*max_x-min_x+1, min_y-1)
    st_p3 = Vertex(2*min_x-max_x-1, min_y-1)
    super_triangle = Triangle(st_p1, st_p2, st_p3)

    return super_triangle





def search_target_triangle(point, triangle_set):
    for target_triangle in triangle_set:
        checker = check_inside_or_outside(point, target_triangle)
        if checker == "inside":
            return target_triangle

def check_inside_or_outside(target_point, triangle):
    triangle_vertices = sort_as_CCW(triangle.vertices)
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

def cross_product(v1, v2):
    z = v1.x*v2.y - v2.x*v1.y
    return z





def make_temp_triangle(target_edge, inner_point):
    temp_triangle= Triangle(target_edge[0],target_edge[1],inner_point)
    
    return temp_triangle

def find_adjacent_triangle(target_triangle, inner_point, index):
    vertex_1 = target_triangle.vertices[index]
    vertex_2 = target_triangle.vertices[index+1]
    
    adjacent_triangle = list(((vertex_1.belonged_triangles & vertex_2.belonged_triangles) - inner_point.belonged_triangles)) 
    if len(adjacent_triangle)>1:
        adjacent_triangle.append(target_triangle)
        draw_triangles(adjacent_triangle)
    else:
        pass

    return adjacent_triangle





def update_delaunay_triangle(delaunay_triangle_set, temp_triangle, adjacent_triangle = None):
    if adjacent_triangle:
        flag, new_triangle_1, new_triangle_2 = generate_triangle(temp_triangle, adjacent_triangle[0])
        if flag:
            delaunay_triangle_set.remove(adjacent_triangle[0])
            delaunay_triangle_set.add(new_triangle_1)
            delaunay_triangle_set.add(new_triangle_2)
        
    
        else:
            delaunay_triangle_set.add(new_triangle_1)
            delaunay_triangle_set.add(new_triangle_2)
    else:
        delaunay_triangle_set.add(temp_triangle)

def generate_triangle(temp_triangle, adjacent_triangle):
    middle_line, inner_point, outer_point = distinguish_vertices(temp_triangle ,adjacent_triangle)
    checker = check_flip_or_not(temp_triangle,adjacent_triangle)

    if checker:
        flag = True
        del_triangle(temp_triangle)
        del_triangle(adjacent_triangle)
        new_triangle_1 = Triangle(inner_point, outer_point, middle_line[0])
        new_triangle_2 = Triangle(inner_point, outer_point, middle_line[1])
    else:
        flag = False
        new_triangle_1 = temp_triangle
        new_triangle_2 = adjacent_triangle
    
    return flag, new_triangle_1, new_triangle_2

def del_triangle(triangle):
    vertices = triangle.vertices
    for vertex in vertices:
        vertex.del_belonged_triangle(triangle)

def check_flip_or_not(temp_triangle, adjacent_triangle):
    middle_line, inner_point, outer_point = distinguish_vertices(temp_triangle, adjacent_triangle)

    result_1 = point_inclusion_test(inner_point, adjacent_triangle)
    result_2 = point_inclusion_test(outer_point, temp_triangle)
    if result_1 or result_2:
        return True

def distinguish_vertices(temp_triangle, adjacent_triangle):
    middle_line = list(set(temp_triangle.vertices) & set(adjacent_triangle.vertices))
    inner_point = list(set(temp_triangle.vertices) - set(middle_line))[0]
    outer_point = list(set(adjacent_triangle.vertices) - set(middle_line))[0]

    return list(middle_line), inner_point, outer_point

def point_inclusion_test(target_point, triangle):
    triangle_vertices = triangle.vertices
    center, radius = cal_circumcircle_center_and_radius(triangle_vertices[0], triangle_vertices[1], triangle_vertices[2])
    distance = np.linalg.norm(center-[target_point.x, target_point.y])
    
    if distance < radius:
        
        return True

def cal_circumcircle_center_and_radius(p1,p2,p3):
    line_1 = cal_vertical_bisector(p1,p2)
    line_2 = cal_vertical_bisector(p2,p3)
    A = np.array([line_1[0],line_2[0]])
    B = np.array([line_1[1],line_2[1]])

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






def cal_delaunay_triangluation(point_list):
    delaunay_triangle_set = set([])    
    super_triangle = make_super_set_triangle(point_list)
    delaunay_triangle_set.add(super_triangle)
    for point in point_list:
        #draw_triangles(delaunay_triangle_set, point)
        target_triangle = search_target_triangle(point, delaunay_triangle_set)
        delaunay_triangle_set.remove(target_triangle)

        for i in range(3):
            target_edge = (target_triangle.vertices[i-1], target_triangle.vertices[i])
            target_edge[0].del_belonged_triangle(target_triangle)
            temp_triangle = make_temp_triangle(target_edge, point)
            adjacent_triangle = find_adjacent_triangle(target_triangle, point, i-1)
            update_delaunay_triangle(delaunay_triangle_set, temp_triangle, adjacent_triangle)
        
    del_super_triangle_line(super_triangle,delaunay_triangle_set)

    return delaunay_triangle_set

def del_super_triangle_line(super_triangle, delaunay_triangle_set):
    vertices = super_triangle.vertices

    for vertex in vertices:
        triangles = vertex.belonged_triangles
        for triangle in triangles:
            try:
                delaunay_triangle_set.remove(triangle)
            except:
                continue

def del_triangle(triangle):
    vertices = triangle.vertices
    for vertex in vertices:
        vertex.del_belonged_triangle(triangle)

def draw_triangles(triangle_set, point = None):
    plt.rcParams["figure.figsize"] = (15,15)
    plt.axes().set_aspect('equal')
    for triangle in triangle_set:
        x_list = [triangle.vertices[0].x, triangle.vertices[1].x, triangle.vertices[2].x, triangle.vertices[0].x]
        y_list = [triangle.vertices[0].y, triangle.vertices[1].y, triangle.vertices[2].y, triangle.vertices[0].y]
        

        plt.scatter(x_list, y_list, c = 'black')
        plt.plot(x_list, y_list, c = 'red')
        #plt.scatter(point.x, point.y, c = 'green')

    
    plt.show()

if __name__ == "__main__":
    point_list = gen_point_list('./example_100.txt')
    delaunay_triangle_set = cal_delaunay_triangluation(point_list)
    draw_triangles(delaunay_triangle_set)