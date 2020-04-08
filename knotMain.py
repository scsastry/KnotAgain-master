from knotAux import *


# np.vstack((arr_a, arr_b)) --> stacks two arrays vertically
# np.hstack((arr_a, arr_b)) --> stacks two array inputs horizontally
# np.delete(arr, row_index, axis=0) --> deletes an entire row in array


# def point_dist(pointA, pointB):
#     # takes in two points and calculates the 3 dimensional distance between them
#
#     a = np.array(pointA)
#     b = np.array(pointB)
#
#     dist = np.linalg.norm(b - a)
#     return dist
#
#
# def max_dist(array):
#     listout = []
#     for i in range(2, len(array)):
#         listout.append(point_dist(array[i], array[i-1]))
#     return max(listout), statistics.mean(listout), min(listout)
#
#
# def mt_check(node):
#     # Input is the node to be optimized
#
#     prev, curr, after = node.get_before(), node, node.get_next()

#
# pointA = Point([1, 0, 0])
# pointB = Point([0, 1, 0])
# pointC = Point([0, 0, 1])
# pointB_prime = (pointA + pointB + pointC) / 3
# origin = Point([0, 0, 0])
# end = Point([1, 0, 1])


def main():
    file_in = input("Please enter file directory: ")
    point_list = clean_list(file_in)

    # for i in range(2, len(point_list) - 1):
    for i in range(1, 5):

        # Conditional check ensures that the termini are not obliterated by negative indices
        # produced during calculation of i' - 1
        if i - 2 >= 0:
            prev_point_prime = (point_list[i - 2] + point_list[i - 1] + point_list[i]) / 3
        else:
            prev_point_prime = point_list[i - 1]

        point, next_point = point_list[i], point_list[i + 1]
        point_prime = (point_list[i - 1] + point + next_point) / 3

        print("Main function output test for point_prime_prev:", point_list[i - 1], " prev_point:",
              prev_point_prime, "point:", point, "point_prime:", point_prime)

        # TESTING -- check to see intersection function can run for all planes and one line segment
        # intersect_left, intersect_right = moller_trumbore(prev_point_prime, point, point_prime,
        #                                                   next_point, point_list[15], point_list[16])
        left = [prev_point_prime, point, point_prime, next_point, point_list, i]
        right = [prev_point_prime, point, point_prime, next_point, point_list, i + 1]
        intersect_left, intersect_right = intersect_check_prev(left), intersect_check_post(right)
        print("Main function output test for bool value returned by MT for left and right Triangles: ",
              intersect_left, intersect_right, end="\n\n")
        # file = "/Users/jormungandr/Downloads/knot1.crd"
        # pos_arr = clean_array(file)  # produces an array of position values based on output of clean_array
        # pos_list = clean_list(file)
        #
        # visualize(pos_arr)


if __name__ == '__main__':
    main()
