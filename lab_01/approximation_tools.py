from approximation_tables import *


def get_argument() -> float:
    arg_str = input("Input argument: ")
    arg = float(arg_str)
    return arg


def get_power() -> int:
    power_str = input("Input power: ")
    power = int(power_str)
    if power < 0:
        raise ValueError
    return power


def adjust_table(converting_point_table: PointTable, origin_point_table: PointTable, power: int) -> PointTable:
    src_coordinates: list[list[float], list[float]] = origin_point_table.get_coordinates()[:2]

    newton_table = NewtonDiffsTable(converting_point_table)
    newton_table.inverse = True
    new_points: list[Point] = []
    for new_x in src_coordinates[0]:
        new_y = newton_table.get_value(new_x, power)
        point = Point(new_x, new_y, [])
        new_points.append(point)

    result_point_table = PointTable()
    result_point_table.from_points(new_points)

    return result_point_table


def subtract_tables(table_from: PointTable, table_which: PointTable):
    from_coordinates: list[list[float], list[float]] = table_from.get_coordinates()[:2]
    which_coordinates: list[list[float], list[float]] = table_which.get_coordinates()[:2]

    new_points: list[Point] = []
    for i, new_x in enumerate(from_coordinates[0]):
        new_y = from_coordinates[1][i]
        new_y -= which_coordinates[1][i]
        point = Point(new_x, new_y, [])
        new_points.append(point)

    result_point_table = PointTable()
    result_point_table.from_points(new_points)

    return result_point_table


def solve_equations():
    point_table_1 = PointTable()
    point_table_1.from_file("table1.txt")
    point_table_1.print("First equation table")
    point_table_2 = PointTable()
    point_table_2.from_file("table2.txt")
    point_table_2.print("Second equation table")

    try:
        power = get_power()
    except ValueError:
        print("Invalid power")
        return

    adjusted_points_table = adjust_table(point_table_1, point_table_2, power)
    adjusted_points_table.print("First table after adjustment")

    subtracted_point_table = subtract_tables(point_table_2, adjusted_points_table)
    subtracted_point_table.print("Second table after subtraction")
    subtracted_point_table.sort()

    newton_table_subtracted = NewtonDiffsTable(subtracted_point_table)
    newton_table_subtracted.inverse = True
    result_x = newton_table_subtracted.get_value(0, power)
    newton_table_subtracted.print()

    newton_table_2 = NewtonDiffsTable(point_table_2)
    result_y = newton_table_2.get_value(result_x, power)
    newton_table_2.print()

    print("Root by Newton's method: x = {:.3f}; y = {:.3f}".format(result_x, result_y))


def compare_approximation():
    point_table = PointTable()
    point_table.from_file("table.txt")
    point_table.print("Table")
    newton_diff_table = NewtonDiffsTable(point_table)
    hermite_diff_table = HermiteDiffsTable(point_table)

    try:
        arg = get_argument()
    except ValueError:
        print("Invalid argument")
        return

    if arg > point_table.points[-1].x or arg < point_table.points[0].x:
        print("Warning: extrapolation")

    try:
        power = get_power()
    except ValueError:
        print("Invalid power")
        return

    result = newton_diff_table.get_value(arg, power)
    newton_diff_table.print()
    print("Approximation by Newton's method: {:.3f}\n".format(result))
    result = hermite_diff_table.get_value(arg, power)
    hermite_diff_table.print()
    print("Approximation by Hermite's method: {:.3f}".format(result))


def compare_root_finding():
    point_table = PointTable()
    point_table.inverse = True
    point_table.from_file("table.txt")
    # point_table.flip_relation()
    point_table.sort()
    point_table.print("Table")
    newton_diff_table = NewtonDiffsTable(point_table)
    hermite_diff_table = HermiteDiffsTable(point_table)

    try:
        power = get_power()
    except ValueError:
        print("Invalid power")
        return

    newton_diff_table.inverse = True
    result = newton_diff_table.get_value(0, power)
    newton_diff_table.print()
    print("Root by Newton's method: {:.3f}\n".format(result))

    hermite_diff_table.inverse = True
    result = hermite_diff_table.get_value(0, power)
    hermite_diff_table.print()
    print("Root by Hermite's method: {:.3f}".format(result))
