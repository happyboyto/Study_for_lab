class Vector2D:
    def __init__(self, p1, p2):
        self.start_point = p1
        self.end_point = p2
        self.__x = None
        self.__y = None

        self.cal_vector()

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def cal_vector(self):
        self.__x = self.end_point.x - self.start_point.x
        self.__y = self.end_point.y - self.start_point.y
