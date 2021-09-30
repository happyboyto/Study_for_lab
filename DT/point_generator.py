from vertex_and_triangle import Vertex

def gen_point_list(filepath):
    file = open(filepath, 'r')
    point_list = []
    while True:
        line = file.readline()
        if line == '':
            break
        ID,x,y = map(float, line.split('\t'))
        p = Vertex(x, y)
        point_list.append(p)

    return point_list
