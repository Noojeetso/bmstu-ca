import os.path


class Point:
    x: float
    y: float
    derivatives: list[float]

    def __init__(self, x: float, y: float, derivatives: list[float]):
        self.x = x
        self.y = y
        self.derivatives = derivatives

    def print(self):
        if len(self.derivatives) == 0:
            print("{: ^ 10.3f}|{: ^ 10.3f}".format(self.x, self.y))
            return
        print("{: ^ 10.3f}|{: ^ 10.3f}|{: ^ 10.3f}".format(self.x, self.y, self.derivatives[0]))


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
        with open(file_name, 'r') as file:
            line = file.readline()
            line = line.rstrip()
            item = line.split(" ")
            try:
                float(item[0])
            except ValueError:
                self.argument = item[0]
                self.function = item[1]
                line = file.readline()
                line = line.rstrip()
                item = line.split(" ")
            value_amount = len(item)

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

                if len(item) != value_amount:
                    print("Incorrect amount of values in line:", line, "expected", value_amount, "values")
                    raise ValueError
                derivatives = []
                try:
                    x, y = map(float, item[:2])
                    if len(item) > 2:
                        derivatives = list(map(float, item[2:]))
                    if any(derivative == 0 for derivative in derivatives):
                        print("Zero derivatives are not allowed:", line)
                        raise ValueError
                except ValueError:
                    print("File contains corrupted line:", line)
                    raise ValueError
                new_point = Point(x, y, derivatives)
                self.points.append(new_point)
        # if flip_relation:
        #     self.flip_relation()
        self.sort()

    # def flip_relation(self):
    #     self.function, self.argument = self.argument, self.function
    #     print("()->():",  self.function, self.argument)

    def sort(self):
        if not self.inverse:
            self.points.sort(key=lambda point: point.x)
        else:
            self.points.sort(key=lambda point: point.y)

    def get_coordinates(self):
        coordinates: list[list[float], list[float], list[float]] = [[], [], []]
        for point in self.points:
            coordinates[0].append(point.x)
            coordinates[1].append(point.y)
            if len(point.derivatives):
                coordinates[2].append(point.derivatives[0])
        return coordinates

    def print(self, table_name: str):
        if len(self.points) == 0:
            print("{} is empty\n".format(table_name))
            return

        print("{}:".format(table_name))
        if len(self.points[0].derivatives) == 0:
            print("\t\t{:^10.10s}|{:^10.10s}".format(self.argument, self.function))
        else:
            print("\t\t{:^10.10s}|{:^10.10s}|{:^10.10s}".format(self.argument, self.function, "derivative"))
        for i, point in enumerate(self.points):
            print("{: 2}).\t".format(i), end='')
            point.print()
        print("")
