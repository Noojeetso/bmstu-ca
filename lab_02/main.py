from storage import PointTable
from spline import Spline
from approximation_tables import NewtonTable
from graph import draw_graph


def do_splines():
    table = PointTable()
    table.from_file("table.txt")
    table.print("Table")

    try:
        natural_spline = Spline(table.to_nparray(), 0.0, 0.0)
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

    newton_table = NewtonTable(table)

    try:
        newton_table.calculate_table(table.points[0].x, 3)
    except ValueError:
        return
    left_second_derivative = newton_table.get_second_derivative(table.points[0].x)

    try:
        newton_table.calculate_table(table.points[-1].x, 3)
    except ValueError:
        return
    right_second_derivative = newton_table.get_second_derivative(table.points[-1].x)

    try:
        spline_newton_left_derivative = Spline(table.to_nparray(), left_second_derivative, 0.0)
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

    print("\n\tNewton's polynom:\n\ninterpolated value: {:.3g}\n".format(newton_table.get_value(x)))

    print("\tSplines:\n")
    print("start derivative: {:.3g}\n".format(natural_spline.start_derivative),
          "end_derivative: {:.3g}\n".format(natural_spline.end_derivative),
          "interpolated value: {:.3g}\n".format(natural_spline.get_value(x)),
          "ksi_2: {:.3g}\n".format(natural_spline.sweep_coefficients[0][1]),
          "eta_2: {:.3g}\n".format(natural_spline.sweep_coefficients[1][1]),
          "c_1: {:.3g}\n".format(natural_spline.spline_coefficients[2][1]),
          "c_N+1: {:.3g}\n".format(natural_spline.end_derivative / 2),
          sep='')

    print("start derivative: {:.3g}\n".format(spline_newton_left_derivative.start_derivative),
          "end_derivative: {:.3g}\n".format(spline_newton_left_derivative.end_derivative),
          "interpolated value: {:.3g}\n".format(spline_newton_left_derivative.get_value(x)),
          "ksi_2: {:.3g}\n".format(spline_newton_left_derivative.sweep_coefficients[0][1]),
          "eta_2: {:.3g}\n".format(spline_newton_left_derivative.sweep_coefficients[1][1]),
          "c_1: {:.3g}\n".format(spline_newton_left_derivative.spline_coefficients[2][1]),
          "c_N+1: {:.3g}\n".format(spline_newton_left_derivative.end_derivative / 2),
          sep='')

    print("start derivative: {:.3g}\n".format(spline_newton_corner_derivatives.start_derivative),
          "end_derivative: {:.3g}\n".format(spline_newton_corner_derivatives.end_derivative),
          "interpolated value: {:.3g}\n".format(spline_newton_corner_derivatives.get_value(x)),
          "ksi_2: {:.3g}\n".format(spline_newton_corner_derivatives.sweep_coefficients[0][1]),
          "eta_2: {:.3g}\n".format(spline_newton_corner_derivatives.sweep_coefficients[1][1]),
          "c_1: {:.3g}\n".format(spline_newton_corner_derivatives.spline_coefficients[2][1]),
          "c_N+1: {:.3g}\n".format(spline_newton_corner_derivatives.end_derivative / 2),
          sep='')

    draw_graph(newton_table, natural_spline, spline_newton_left_derivative, spline_newton_corner_derivatives)


if __name__ == '__main__':
    do_splines()
