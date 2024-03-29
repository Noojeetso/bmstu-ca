import numpy as np

from spline import Spline
from newton_polynom import NewtonPolynom
from storage import PointTable


def print_matrix(matrix: np.array, func, arg, nx, ny, bottom_x, bottom_y):
    print(" {:10}".format(func + "\\" + arg), end='', sep='')
    for i in range(nx):
        x_idx = i + bottom_x
        print("|{:^10}".format(x_idx), sep='', end='')
    print("")
    for i in range(ny):
        y_idx = i + bottom_y
        print(" {:^10}".format(y_idx), end='', sep='')
        for j in range(nx):
            print("|{:^10.3g}".format(matrix[i][j]), sep='', end='')
        print("")


def print_array(array: np.array, func, arg, ny, bottom_y):
    print(" {:10}".format(arg), end='', sep='')
    for i in range(ny):
        y_idx = i + bottom_y
        print("|{:^10}".format(y_idx), sep='', end='')
    print("")

    print(" {:10}".format(func), end='', sep='')
    for i in range(ny):
        print("|{:^10.3g}".format(array[1][i]), sep='', end='')
    print("")


def get_partition(value: float, power: int, max_power: int) -> (int, int):
    base_idx = int(value)

    if base_idx >= max_power:
        return -1, -1

    if power > max_power:
        return -1, -1

    if base_idx + power // 2 < max_power:
        if base_idx - power + power // 2 + 1 >= 0:
            top_index = base_idx + power // 2
            bottom_index = top_index - (power - 1)
        else:
            bottom_index = 0
            top_index = power - 1
    else:
        top_index = max_power - 1
        bottom_index = top_index - (power - 1)

    return bottom_index, top_index


def nonlinear_newton(table: PointTable, x: float, y: float, z: float, nx: int, ny: int, nz: int) -> float:
    if nx > table.data.shape[2]:
        print("nx power is too big")
        return float('NaN')
    if ny > table.data.shape[1]:
        print("ny power is too big")
        return float('NaN')
    if nz > table.data.shape[0]:
        print("nz power is too big")
        return float('NaN')

    z_idx = int(z)
    if z_idx > table.data.shape[0]:
        print("error: extrapolation by z coordinate")
        return float('NaN')

    bottom_z, top_z = get_partition(z, nz, table.data.shape[0])
    if bottom_z == -1 or top_z == -1:
        print("error: extrapolation by z coordinate")
        return float('NaN')

    bottom_x, top_x = get_partition(x, nx, table.data.shape[2])
    if bottom_x == -1 or top_x == -1:
        print("error: extrapolation by x coordinate")
        return float('NaN')

    bottom_y, top_y = get_partition(y, ny, table.data.shape[1])
    if bottom_y == -1 or top_y == -1:
        print("error: extrapolation by y coordinate")
        return float('NaN')

    tmp_z_array = np.empty((2, nz))
    for i in range(nz):
        tmp_z_array[0][i] = i + bottom_z

    tmp_x_array = np.empty((2, nx))
    for i in range(nx):
        tmp_x_array[0][i] = i + bottom_x

    tmp_y_array = np.empty((2, ny))
    for i in range(ny):
        tmp_y_array[0][i] = i + bottom_y

    for i in range(nz):
        z_idx = bottom_z + i

        print("\nz =", z_idx)
        print_matrix(table.data[z_idx], 'y', 'x', nx, ny, bottom_x, bottom_y)

        for j in range(ny):
            y_idx = bottom_y + j

            tmp_x_array[1] = table.data[z_idx, y_idx, bottom_x:top_x + 1]
            polynom = NewtonPolynom(tmp_x_array, 'f', 'x')
            polynom.calculate_table(x, nx - 1)
            interpolated_in_x = polynom.get_value(x)

            tmp_y_array[1][j] = interpolated_in_x

        print("\nINTERPOLATED Y ARRAY (x = ",  x, "):", sep='')
        print_array(tmp_y_array, 'f', 'y', ny, bottom_y)

        polynom = NewtonPolynom(tmp_y_array, 'f', 'y')
        polynom.calculate_table(y, ny - 1)
        interpolated_in_y = polynom.get_value(y)
        tmp_z_array[1][i] = interpolated_in_y

        print("\nInterpolated function value (z = {:.3g})".format(interpolated_in_y))

    print("\nINTERPOLATED Z ARRAY:")
    print_array(tmp_z_array, 'f', 'z', nz, bottom_z)

    polynom = NewtonPolynom(tmp_z_array, 'f', 'z')
    polynom.calculate_table(z, nz - 1)

    return polynom.get_value(z)


def nonlinear_spline(table: PointTable, x: float, y: float, z: float) -> float:
    nx = table.data.shape[2]
    ny = table.data.shape[1]
    nz = table.data.shape[0]

    z_idx = int(z)
    if z_idx > table.data.shape[0]:
        print("error: extrapolation by z coordinate")
        return float('NaN')

    bottom_z, top_z = get_partition(z, nz, table.data.shape[0])
    if bottom_z == -1 or top_z == -1:
        print("error: extrapolation by z coordinate")
        return float('NaN')

    bottom_x, top_x = get_partition(x, nx, table.data.shape[2])
    if bottom_x == -1 or top_x == -1:
        print("error: extrapolation by x coordinate")
        return float('NaN')

    bottom_y, top_y = get_partition(y, ny, table.data.shape[1])
    if bottom_y == -1 or top_y == -1:
        print("error: extrapolation by y coordinate")
        return float('NaN')

    tmp_z_array = np.empty((2, nz))
    for i in range(nz):
        tmp_z_array[0][i] = i + bottom_z

    tmp_x_array = np.empty((2, nx))
    for i in range(nx):
        tmp_x_array[0][i] = i + bottom_x

    tmp_y_array = np.empty((2, ny))
    for i in range(ny):
        tmp_y_array[0][i] = i + bottom_y

    for i in range(nz):
        z_idx = bottom_z + i

        print("\nz =", z_idx)
        print_matrix(table.data[z_idx], 'y', 'x', nx, ny, bottom_x, bottom_y)

        for j in range(ny):
            y_idx = bottom_y + j

            tmp_x_array[1] = table.data[z_idx, y_idx, bottom_x:top_x + 1]

            spline = Spline(tmp_x_array, 0, 0)
            tmp_y_array[1][j] = spline.get_value(x)

        print("\nINTERPOLATED Y ARRAY (x = ",  x, "):", sep='')
        print_array(tmp_y_array, 'f', 'y', ny, bottom_y)

        spline = Spline(tmp_y_array, 0, 0)
        interpolated_in_y = spline.get_value(y)
        tmp_z_array[1][i] = interpolated_in_y

        print("\nInterpolated function value (z = {:.3g})".format(interpolated_in_y))

    print("\nINTERPOLATED Z ARRAY:")
    print_array(tmp_z_array, 'f', 'z', nz, bottom_z)

    spline = Spline(tmp_z_array, 0, 0)

    return spline.get_value(z)


def nonlinear_mixed(table: PointTable, x: float, y: float, z: float, nx: int, nz: int) -> float:
    ny = table.data.shape[1]
    if nx > table.data.shape[2]:
        print("nx power is too big")
        return float('NaN')
    if ny > table.data.shape[1]:
        print("ny power is too big")
        return float('NaN')
    if nz > table.data.shape[0]:
        print("nz power is too big")
        return float('NaN')

    z_idx = int(z)
    if z_idx > table.data.shape[0]:
        print("error: extrapolation by z coordinate")
        return float('NaN')

    bottom_z, top_z = get_partition(z, nz, table.data.shape[0])
    if bottom_z == -1 or top_z == -1:
        print("error: extrapolation by z coordinate")
        return float('NaN')

    bottom_x, top_x = get_partition(x, nx, table.data.shape[2])
    if bottom_x == -1 or top_x == -1:
        print("error: extrapolation by x coordinate")
        return float('NaN')

    bottom_y, top_y = get_partition(y, ny, table.data.shape[1])
    if bottom_y == -1 or top_y == -1:
        print("error: extrapolation by y coordinate")
        return float('NaN')

    tmp_z_array = np.empty((2, nz))
    for i in range(nz):
        tmp_z_array[0][i] = i + bottom_z

    tmp_x_array = np.empty((2, nx))
    for i in range(nx):
        tmp_x_array[0][i] = i + bottom_x

    tmp_y_array = np.empty((2, ny))
    for i in range(ny):
        tmp_y_array[0][i] = i + bottom_y

    for i in range(nz):
        z_idx = bottom_z + i

        print("\nz =", z_idx)
        print_matrix(table.data[z_idx], 'y', 'x', nx, ny, bottom_x, bottom_y)

        for j in range(ny):
            y_idx = bottom_y + j

            tmp_x_array[1] = table.data[z_idx, y_idx, bottom_x:top_x + 1]
            polynom = NewtonPolynom(tmp_x_array, 'f', 'x')
            polynom.calculate_table(x, nx - 1)
            interpolated_in_x = polynom.get_value(x)

            tmp_y_array[1][j] = interpolated_in_x

        print("\nINTERPOLATED Y ARRAY (x = ",  x, "):", sep='')
        print_array(tmp_y_array, 'f', 'y', ny, bottom_y)

        spline = Spline(tmp_y_array, 0, 0)
        interpolated_in_y = spline.get_value(y)
        tmp_z_array[1][i] = interpolated_in_y

        print("\nInterpolated function value (z = {:.3g})".format(interpolated_in_y))

    print("\nINTERPOLATED Z ARRAY:")
    print_array(tmp_z_array, 'f', 'z', nz, bottom_z)

    polynom = NewtonPolynom(tmp_z_array, 0, 0)
    polynom.calculate_table(z, nz - 1)

    return polynom.get_value(z)
