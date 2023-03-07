from approximation_tables import NewtonTable
import numpy as np
import matplotlib.pyplot as plt
from spline import Spline

points_amount = 1000


def draw_newton_polynom(newton_table: NewtonTable, color: str, label: str, width='1'):
    array = newton_table.point_table.to_nparray()
    x_values = np.linspace(array[0][0], array[0][-1], points_amount)
    y_values = list()

    start_offset = 0
    end_offset = 0
    for x in x_values:
        end_offset += 1
        if x < newton_table.argument - 1:
            start_offset += 1
        if x > newton_table.argument + 1:
            break

    for x in x_values[start_offset:end_offset]:
        y = newton_table.get_value(x)
        y_values.append(y)

    plt.plot(x_values[start_offset:end_offset], y_values, '-', color=color, linewidth=width, label=label)


def draw_spline(spline: Spline, color: str, label: str, width='1'):
    x_values = np.linspace(spline.array[0][0], spline.array[0][-1], points_amount)
    y_values = list()

    for x in x_values:
        y_values.append(spline.get_value(x))

    plt.plot(x_values, y_values, '-', color=color, linewidth=width, label=label)


def draw_dots(newton_table: NewtonTable, color: str, label: str):
    x_values = list()
    y_values = list()
    for point in newton_table.point_table.points:
        x_values.append(point.x)
        y_values.append(point.y)

    plt.plot(x_values, y_values, 'o', color=color, linewidth='1', label=label)


def draw_graph(newton_table: NewtonTable, spline_1: Spline, spline_2: Spline, spline_3: Spline):
    plt.title('spline')
    plt.xlabel("X")
    plt.ylabel("Y")

    draw_newton_polynom(newton_table, "blue", "Newton's polynom", width='7')
    draw_spline(spline_1, 'green', "Natural", width='5')
    draw_spline(spline_3, 'red', "Newton both", width='3')
    draw_spline(spline_2, 'gold', "Newton left")
    draw_dots(newton_table, "lime", "Table's points")

    plt.legend()
    plt.show()
