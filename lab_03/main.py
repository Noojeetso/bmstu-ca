from storage import PointTable
from non_linear_approximation import *
# from graph import draw_graph


def do_splines():
    table = PointTable()
    table.from_file("data.txt")
    # table.print("Table")

    # x = 1.5
    # y = 1.5
    # z = 3.99
    #
    # nx = 3
    # ny = 4
    # nz = 2

    run_menu = True
    while run_menu:
        print("\n1. Newton non-linear interpolation\n"
              "2. Spline non-linear interpolation\n"
              "3. Mixed non-linear interpolation\n"
              "0. Exit")
        try:
            key = int(input("Input menu number: "))
        except ValueError:
            print("Error: incorrect number")
            continue
        if key == 0:
            run_menu = False
        elif key == 1:
            x = float(input("Input coordinate x: "))
            y = float(input("Input coordinate y: "))
            z = float(input("Input coordinate z: "))
            nx = int(input("Input polynom power nx: "))
            ny = int(input("Input polynom power ny: "))
            nz = int(input("Input polynom power nz: "))
            result = nonlinear_newton(table, x, y, z, nx + 1, ny + 1, nz + 1)
            print("\nResult: {:.3g}".format(result))
        elif key == 2:
            x = float(input("Input coordinate x: "))
            y = float(input("Input coordinate y: "))
            z = float(input("Input coordinate z: "))
            result = nonlinear_spline(table, x, y, z)
            print("\nResult: {:.3g}".format(result))
        elif key == 3:
            x = float(input("Input coordinate x: "))
            y = float(input("Input coordinate y: "))
            z = float(input("Input coordinate z: "))
            nx = int(input("Input polynom power nx: "))
            # ny = int(input("Input polynom power ny: "))
            nz = int(input("Input polynom power nz: "))
            result = nonlinear_mixed(table, x, y, z, nx + 1, nz + 1)
            print("\nResult: {:.3g}".format(result))
        else:
            print("Error: unknown command")


if __name__ == '__main__':
    do_splines()
