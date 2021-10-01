class Vertex:
    def __init__(self,x,y, superset = False):
        self.__x = x
        self.__y = y
        self.__belonged_triangles = set([])
        self.__is_superset = superset
        #self.__belonged_edges = set([])

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def belonged_triangles(self):
        return self.__belonged_triangles
    
    @property
    def is_superset(self):
        return self.__is_superset
    
    @is_superset.setter
    def is_superset(self, superset):
        self.__is_superset = superset

    def add_belonged_triangle(self, triangle):
        self.__belonged_triangles.add(triangle)

    def del_belonged_triangle(self, triangle):
        try:
            self.__belonged_triangles.remove(triangle)
        except:
            print("already_deleted")

    # @property
    # def belonged_edges(self):
    #     return self.__belonged_edges

    # def add_belonged_edge(self, edge):
    #     self.__belonged_edges.add(edge)
    
    # def del_belonged_edge(self, edge):
    #     self.__belonged_edges.remove(edge)

class Triangle:
    def __init__(self, p1, p2, p3):
        self.__vertices = (p1,p2,p3)
        self.add_triangle_info_to_vertices()

    @property
    def vertices(self):
        return self.__vertices
    
    def add_triangle_info_to_vertices(self):
        self.__vertices[0].add_belonged_triangle(self)
        self.__vertices[1].add_belonged_triangle(self)
        self.__vertices[2].add_belonged_triangle(self)



# class Edge:
#     def __init__(self, sv, ev):
#         self.__start_vertex = sv
#         self.__end_vertex = ev
#         self.__left_face = None
#         self.__right_face = None

#         sv.add_belonged_edge(self)
#         ev.add_belonged_edge(self)

#     @property
#     def start_vertex(self):
#         return self.__start_vertex
    
#     @property
#     def end_vertex(self):
#         return self.__end_vertex
    
#     @property
#     def left_face(self):
#         return self.__left_face

#     @property
#     def right_face(self):
#         return self.__left_face

#     @left_face.setter
#     def left_face(self, new_face):
#         self.__left_face = new_face

#     @right_face.setter
#     def right_face(self, new_face):
#         self.__right_face = new_face

#     def is_including(self, vertex):
#         if vertex != self.start_vertex and vertex != self.end_vertex:
#             return False    
#         return True

# class Triangle:
#     def __init__(self, e1, e2, e3):
#         self.__edges = [e1,e2,e3]
#         self.set_vertices
#         self.set_topolgy()

#     def set_vertices(self):
#         self.__vertices = set([i.start_vertex, i.end_vertex for i in self.__edges])
    
#     def set_topology(self):
#         for edge in self.__edges:
#             for vertex in self.__vertices:
#                 if not edge.is_including(vertex):
                    
#                     break


#     @property
#     def vertices(self):
#         return self.__vertices
    
#     @property
#     def edges(self):
#         return self.__edges



# class Vector2D:
#     def __init__(self, p1, p2):
#         self.start_point = p1
#         self.end_point = p2
#         self.__x = None
#         self.__y = None

#         self.cal_vector()

#     @property
#     def x(self):
#         return self.__x

#     @property
#     def y(self):
#         return self.__y

#     def cal_vector(self):
#         self.__x = self.end_point.x - self.start_point.x
#         self.__y = self.end_point.y - self.start_point.y

        
#     def cross_product(self, vector):
#         z = v1.x*v2.y - v2.x*v1.y
#         return z

# def check_points_side(line_vector, target_point):
#     target_vector = Vector2D(line_vector.start_point, target_point)
#     z = cross_product(line_vector,target_vector)

#     if z > 0:
#         return 'Right'
    
#     elif z < 0:
#         return 'Left'