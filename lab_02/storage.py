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


class PointTable:
    epsilon = 1e-6
    function = 'y'
    argument = 'x'
    inverse: bool = False
    points: list[Point]

    def __len__(self):
        return len(self.points)

    def from_points(self, points: list[Point]) -> None:
        self.points = points

    def from_file(self, file_name: str) -> None:
        if not os.path.isfile(file_name):
            print("No such file:", file_name)
            raise IOError

        self.points: list[Point] = []
        with open(file_name, 'r') as file:
            for i, line in enumerate(file):
                line = line.rstrip()
                item = line.split(" ")
                try:
                    float(item[0])
                except ValueError:
                    if i != 0:
                        raise ValueError
                    continue

                if len(item) != 2:
                    print("Incorrect amount of values in line:", line, "expected", 2, "values")
                    raise ValueError
                try:
                    x, y = map(float, item[:2])
                except ValueError:
                    print("File contains corrupted line:", line)
                    raise ValueError
                new_point = Point(x, y)
                self.points.append(new_point)
        self.sort()

    def sort(self):
        if not self.inverse:
            self.points.sort(key=lambda point: point.x)
        else:
            self.points.sort(key=lambda point: point.y)

    def to_nparray(self):
        return np.array([[point.x for point in self.points],
                         [point.y for point in self.points]])

    def print(self, table_name: str):
        if len(self.points) == 0:
            print("{} is empty\n".format(table_name))
            return

        print("{}:".format(table_name))
        print("\t\t{:^10.10s}|{:^10.10s}".format(self.argument, self.function))
        for i, point in enumerate(self.points):
            print("{: 2}).\t".format(i), end='')
            point.print()
        print("")
