import operator
import time

import numpy as np

# import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d


class dll_object:
    def __init__(self, data):
        self.data = data
        self.before = None
        self.after = None

    def get_data(self):
        return self.data

    def set_next(self, point):
        self.after = point

    def get_next(self):
        return self.after

    def set_before(self, point):
        self.before = point

    def get_before(self):
        return self.before

    def delete_point(self):
        self.get_before().set_next(self.get_next())
        self.get_next().set_before(self.get_before())

# FIXME -- what the fuck is happening here?

# def clean_array(in_file):
#     # map(function, iterable input) produces a list of float values for each line in *.crd
#     # returns an outer list (for the entire file) containing inner lists (for each line) made of float values
#     # np.array() turns an input list of lists into a 1 column array
#
#     f = open(in_file, "r+")  # open *.crd file as a file_object
#     n_dim = np.array([list(map(float, line.split())) for line in f.readlines()])
#     f.close()
#     return n_dim


# FIXME -- input is array but should be a list of Point objects

# def visualize(arr):
#     fig = plt.figure()
#     ax = plt.axes(projection='3d')
#
#     zdata = arr[:, [2]].flatten()
#     xdata = arr[:, [0]].flatten()
#     ydata = arr[:, [1]].flatten()
#     ax.scatter3D(xdata, ydata, zdata, cmap='Greens')
#     ax.plot3D(xdata, ydata, zdata, color='b')
#
#     fig.show()


class Vector:
    def __init__(self, pointA, pointB):
        # __sub__(a, b) returns (a - b)
        self.x = operator.sub(pointB, pointA)[0]
        self.y = operator.sub(pointB, pointA)[1]
        self.z = operator.sub(pointB, pointA)[2]

    def __str__(self):
        return "[%.5f %.5f %.5f]" % (self.x, self.y, self.z)

    def __mul__(self, mul):
        return

    def __truediv__(self, div):
        return Vector(Point(), Point([self.x / div, self.y / div, self.z / div]))

    def cross(self, new_vector):
        C_x: float = (self.y * new_vector.z) - (self.z * new_vector.y)
        C_y: float = (self.z * new_vector.x) - (self.x * new_vector.z)
        C_z: float = (self.x * new_vector.y) - (self.y * new_vector.x)

        cross_vector = Vector(Point(), Point([C_x, C_y, C_z]))
        return cross_vector

    def dot(self, new_vector):
        return (self.x * new_vector.x) + (self.y * new_vector.y) + (self.z * new_vector.z)


class Point:
    def __init__(self, point_list=None):
        if point_list is None:
            point_list = [0, 0, 0]
        self.x: float = point_list[0]
        self.y: float = point_list[1]
        self.z: float = point_list[2]
        self.flatten_status = False

    def __str__(self):
        return "[%.5f %.5f %.5f]" % (self.x, self.y, self.z)

    def __add__(self, number):
        return Point([self.x + number.x, self.y + number.y, self.z + number.z])

    def __sub__(self, point):
        return [self.x - point.x, self.y - point.y, self.z - point.z]

    def __mul__(self, scalar):
        return Point([self.x * scalar, self.y * scalar, self.z * scalar])

    def __truediv__(self, div):
        return Point([self.x / div, self.y / div, self.z / div])

    def set_data(self, new_point):
        self.x, self.y, self.z = new_point[0], new_point[1], new_point[2]

    def set_flatten(self, boolean):
        if boolean is True or boolean is False:
            self.flatten_status = boolean
        else:
            return "Please pass boolean argument"


def clean_list(in_file):
    """ creates a list with each node being of Class "Point" returns the list """

    f = open(in_file, "r+")
    n_dim = list(Point(list(float(i) for i in line.split())) for line in f.readlines())
    f.close()
    return n_dim


# FIXME -- reformat to take Point objects as input
# def tube_eval(pointA, pointC, pointB):
#     """ returns 1 for a near-colinear spatial arrangement and 0 for a non colinear arrangement """
#
#     pq = pointC - pointB
#     u = pointC - pointA
#
#     norma = np.linalg.norm(np.cross(pq, u))
#     normb = np.linalg.norm(u)
#     d = norma / normb
#
#     if d <= 0.3:
#         return 1
#     else:
#         return 0


def moller_trumbore(PointB_prime_prev, PointB, PointB_prime, PointC, Origin, end_point):
    """This algorithm will calculate intersections for both {i - 1} triangle and {i + 1} triangle
    PointB_prime and PointB_prime_prev must be computed prior to being passed as an argument.
    The default syntax will have Origin being the point closest to first point in the list while
    the end_point will be closer to the last point """

    D = Vector(Origin, end_point)

    # i' - 1 triangle MT calculations

    E1, E2 = Vector(PointB_prime_prev, PointB), Vector(PointB_prime_prev, PointB_prime)
    T = Vector(PointB_prime_prev, Origin)
    P = D.cross(E2)
    inv_det = 1 / P.dot(E1)

    prev_triangle = [T.cross(E1).dot(E2) * inv_det,
                     D.cross(E2).dot(T) * inv_det, T.cross(E1).dot(D) * inv_det]

    if 0 <= prev_triangle[0] <= 1 and 0 <= prev_triangle[1] <= 1 and 0 <= prev_triangle[2] <= 1 \
            and 0 <= prev_triangle[1] + prev_triangle[2] <= 1:
        prev_status = True
    else:
        prev_status = False

    # i + 1 triangle MT calculations

    E3, E4 = Vector(PointB_prime, PointB), Vector(PointB_prime, PointC)
    T = Vector(PointB_prime, Origin)
    P1 = D.cross(E4)
    inv_det_two = 1 / P1.dot(E3)

    post_triangle = [T.cross(E3).dot(E4) * inv_det_two,
                     D.cross(E4).dot(T) * inv_det_two, T.cross(E3).dot(D) * inv_det_two]

    if 0 <= post_triangle[0] <= 1 and 0 <= post_triangle[1] <= 1 and 0 <= post_triangle[2] <= 1 \
            and 0 <= post_triangle[1] + post_triangle[2] <= 1:
        post_status = True
    else:
        post_status = False

    print("MT output test: ", prev_triangle, prev_status, post_triangle, post_status, P, P.dot(E1), inv_det)
    return prev_status, post_status


def intersect_check_prev(list_in):
    # Computes the MT algorithm for same plane of tri(A, B, C) of varying line segments
    # beginning at the start of the list up to point {i - 1}

    PointA_prime, PointB, PointB_prime, PointC, list_in, end_index = list_in[0:]
    for i in range(0, end_index):
        if True in moller_trumbore(PointA_prime, PointB, PointB_prime, PointC, list_in[i], list_in[i + 1]):
            return True
        else:
            pass


def intersect_check_post(list_in):
    # Computes the MT algorithm for same plane of tri(A, B, C) of varying line segments
    # beginning at {i + 1} to end of list

    PointA_prime, PointB, PointB_prime, PointC, list_in, start_index = list_in[0:]
    for i in range(start_index, len(list_in)-1):
        if True in moller_trumbore(PointA_prime, PointB, PointB_prime, PointC, list_in[i], list_in[i + 1]):
            return True
        else:
            pass


a = Point([1, 2, 3])
b = Point([4, 5, 6])
vec = Vector(a, b)

# start = time.time()
# o_dim = clean_list("/Users/jormungandr/Desktop/Knotty_ecs_129/data/knotted_1_crd.txt")
# print(time.time() - start
