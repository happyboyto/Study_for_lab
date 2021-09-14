# 점 세개를 골라 삼각형을 그리고 그 안에 있는 점들을 버린다.
from vector2d import Vector2D
from point_generator import Point


def cross_product(v1, v2):
    z = v1.x*v2.y - v2.x*v1.y
    return z


def sort_as_CCW(p1, p2, p3):
    v1 = Vector2D(p1, p2)
    v2 = Vector2D(p1, p3)
    z = cross_product(v1, v2)

    if z > 0:
        return [p1, p2, p3]

    elif z < 0:
        return [p1, p3, p2]

    elif z == 0:
        return -1


def check_inside_or_outside(triangle, point_list):
    filtered_point_list = []

    for point in point_list:
        for i in range(3):
            vt = Vector2D(triangle[i-1], triangle[i])  # 더 좋은빙법있나?
            vk = Vector2D(triangle[i], point)
            cross_product = cross_product(vk, vt)
            if cross_product > 0:
                continue
            else:
                filtered_point_list.append(point)
                break


if __name__ == "__main__":
    pass
