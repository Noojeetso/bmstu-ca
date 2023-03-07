from storage import PointTable
from spline import Spline
from approximation_tables import NewtonTable
from graph import draw_graph


def do_splines():
    table = PointTable()
    table.from_file("table.txt")
    table.print("Table")

    try:
        natural_spline = Spline(table.to_nparray(), 0, 0)
    except ValueError:
        return

    raw_input = input("Input argument: ")
    try:
        x = float(raw_input)
    except ValueError:
        print("Incorrect argument")
        return

    if not (table.points[0].x <= x <= table.points[-1].x):
        print("Error: extrapolation")
        return

    y = natural_spline.get_value(x)
    print("Interpolated value:", y)

    newton_table = NewtonTable(table)

    try:
        newton_table.calculate_table(0, 3)
    except ValueError:
        return
    left_second_derivative = newton_table.get_second_derivative(0, 1e-6)

    try:
        newton_table.calculate_table(table.points[-1].x, 3)
    except ValueError:
        return
    right_second_derivative = newton_table.get_second_derivative(table.points[-1].x, 1e-6)

    try:
        spline_newton_left_derivative = Spline(table.to_nparray(), left_second_derivative, 0)
    except ValueError:
        return

    try:
        spline_newton_corner_derivatives = Spline(table.to_nparray(), left_second_derivative, right_second_derivative)
    except ValueError:
        return

    try:
        newton_table.calculate_table(x, 3)
    except ValueError:
        return

    draw_graph(newton_table, natural_spline, spline_newton_left_derivative, spline_newton_corner_derivatives)


if __name__ == '__main__':
    do_splines()
