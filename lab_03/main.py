from storage import PointTable
from non_linear_approximation import *
# from graph import draw_graph


def do_splines():
    table = PointTable()
    table.from_file("data.txt")
    # table.print("Table")

    x = 1.5
    y = 1.5
    z = 1.5

    nx = 3
    ny = 4
    nz = 2

    # x = float(input("Введите координату x:"))
    # y = float(input("Введите координату y:"))
    # z = float(input("Введите координату z:"))
    #
    # nx = float(input("Введите степень аппроксимации nx:"))
    # ny = float(input("Введите степень аппроксимации ny:"))
    # nz = float(input("Введите степень аппроксимации nz:"))

    result = approximate_non_linear(table, x, y, z, nx, ny, nz)
    print("Result: {:.3g}".format(result))

    # try:
    #     natural_spline = Spline(table.to_nparray(), 0.0, 0.0)
    # except ValueError:
    #     return
    #
    # raw_input = input("Input argument: ")
    # try:
    #     x = float(raw_input)
    # except ValueError:
    #     print("Incorrect argument")
    #     return
    #
    # if not (table.points[0].x <= x <= table.points[-1].x):
    #     print("Error: extrapolation")
    #     return
    #
    # newton_table = NewtonTable(table)
    #
    # try:
    #     newton_table.calculate_table(table.points[0].x, 3)
    # except ValueError:
    #     return
    # left_second_derivative = newton_table.get_second_derivative(table.points[0].x, 1e-6)
    #
    # try:
    #     newton_table.calculate_table(table.points[-1].x, 3)
    # except ValueError:
    #     return
    # right_second_derivative = newton_table.get_second_derivative(table.points[-1].x, 1e-6)
    #
    # try:
    #     spline_newton_left_derivative = Spline(table.to_nparray(), left_second_derivative, 0.0)
    # except ValueError:
    #     return
    #
    # try:
    #     spline_newton_corner_derivatives = Spline(table.to_nparray(), left_second_derivative, right_second_derivative)
    # except ValueError:
    #     return
    #
    # try:
    #     newton_table.calculate_table(x, 3)
    # except ValueError:
    #     return


if __name__ == '__main__':
    do_splines()
