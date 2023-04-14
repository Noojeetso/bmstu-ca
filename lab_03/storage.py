import os.path
import numpy as np


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def print(self):
        print("{: ^ 10.3f}|{: ^ 10.3f}".format(self.x, self.y))


class ApproximationArray:
    data: np.ndarray

    def __init__(self, x: int):
        self.data = np.empty((x,))


class ApproximationPlane:
    data: np.ndarray

    def __init__(self, x: int, y: int):
        self.data = np.empty((x, y))


class PointTable:
    epsilon = 1e-6
    points: list[Point]
    data: np.ndarray
    function = 'y'
    argument = 'x'

    def __len__(self):
        return len(self.points)

    def from_points(self, points: list[Point]) -> None:
        self.points = points

    @staticmethod
    def get_shape(file_name: str) -> tuple[int, int, int]:
        x_size = -1
        y_size = -1
        x_indices = set()
        y_indices = set()
        z_indices = set()

        with open(file_name, 'r') as file:
            for i, line in enumerate(file):
                i += 1
                line = line.strip()

                if "z=" in line:
                    str_idx = line.find("z=")
                    current_index = line[str_idx + 2]
                    current_index = int(current_index)

                    if current_index in z_indices:
                        print("Z index redefinition in line:", i)
                        raise ValueError
                    z_indices.add(current_index)

                    if not x_indices or not y_indices:
                        continue
                    if (not (max(x_indices) == len(x_indices) - 1 and
                             max(y_indices) == len(y_indices) - 1) or
                            not (min(x_indices) == min(y_indices) == min(z_indices) == 0)):
                        print("Some of X/Y indices out of bounds, before z =", current_index)
                        raise ValueError

                    if x_size == -1:
                        x_size = len(x_indices)
                        y_size = len(y_indices)
                    elif x_size != len(x_indices) or y_size != len(y_indices):
                        print("Indices reshape is prohibited, before z =", current_index)
                        raise ValueError

                    x_indices.clear()
                    y_indices.clear()

                elif "y\\x" in line:
                    line = line.lstrip("y\\x")
                    items = line.split()
                    indices = list(map(int, items))
                    for current_index in indices:
                        if current_index in x_indices:
                            print("X index redefinition in line:", i)
                            raise ValueError
                        x_indices.add(current_index)

                elif not line:
                    continue

                else:
                    items = line.split()
                    values = list(map(int, items))
                    current_index = values[0]
                    if current_index in y_indices:
                        print("Y index redefinition in line:", i)
                        raise ValueError
                    y_indices.add(current_index)

        if (not (max(z_indices) == len(z_indices) - 1) or
                not (min(z_indices) == 0)):
            print("Some of Z indices out of bounds")
            raise ValueError

        return len(z_indices), y_size, x_size

    def from_file(self, file_name: str) -> None:
        if not os.path.isfile(file_name):
            print("No such file:", file_name)
            raise IOError

        shape = self.get_shape("data.txt")
        self.data = np.empty(shape)

        z_index = 0
        with open(file_name, 'r') as file:
            for i, line in enumerate(file):
                line = line.strip()

                if "z=" in line:
                    str_idx = line.find("z=")
                    z_index = line[str_idx + 2]
                    z_index = int(z_index)
                    # print(z_index)

                elif "y\\x" in line:
                    line = line.lstrip("y\\x")
                    items = line.split()
                    x_indices = list(map(int, items))

                elif not line:
                    continue

                else:
                    items = line.split()
                    values = list(map(int, items))
                    y_index = values[0]

                    for index in range(1, len(values)):
                        x_index = x_indices[index - 1]
                        self.data[z_index][y_index][x_index] = values[index]

        # print()
        # print(self.data)

    def print(self, table_name: str):
        print(self.data)
        # if len(self.points) == 0:
        #     print("{} is empty\n".format(table_name))
        #     return
        #
        # print("{}:".format(table_name))
        # print("\t\t{:^10.10s}|{:^10.10s}".format(self.argument, self.function))
        # for i, point in enumerate(self.points):
        #     print("{: 2}).\t".format(i), end='')
        #     point.print()
        # print("")
