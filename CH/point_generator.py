class Point:
    def __init__(self, ID, x, y):
        self.__ID = ID
        self.__x = x
        self.__y = y

    @property
    def ID(self):
        return self.__ID

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


def gen_point_list(filepath):
    file = open(filepath, 'r')
    point_list = []
    while True:
        line = file.readline()
        if line == '':
            break
        line = map(int, line.split('\t'))
        p = Point(line[0], line[1], line[2])
        point_list.append(p)

    return point_list
