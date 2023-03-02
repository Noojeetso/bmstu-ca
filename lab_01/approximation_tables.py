from storage import *


class PartialTable:
    point_table: PointTable
    bottom_index: int
    top_index: int
    coordinates: list[list[float], list[float], list[float]]
    inverse: bool = False

    def __init__(self, point_table: PointTable):
        self.point_table = point_table
        self.bottom_index = 0
        max_amount = len(self.point_table)
        max_index = max_amount - 1
        self.top_index = max_index
        self.set_coordinates()

    def __len__(self) -> int:
        return max(self.top_index - self.bottom_index + 1, 0)

    def set_partition(self, value: float, amount: int) -> None:
        self.bottom_index = 0
        max_amount = len(self.point_table)
        max_index = max_amount - 1
        top_index = max_index
        self.top_index = top_index
        self.set_coordinates()

        for index in range(len(self.point_table)):
            if self.coordinates[0][index] > value:
                top_index = index
                break

        bottom_index = top_index

        while top_index - bottom_index < amount - 1:
            if bottom_index > 0:
                bottom_index -= 1
            if top_index - bottom_index == amount - 1:
                break
            if top_index < max_index:
                top_index += 1

        self.point_table = self.point_table
        self.bottom_index = bottom_index
        self.top_index = top_index
        self.set_coordinates()

    def set_coordinates(self) -> None:
        coordinates: list[list[float], list[float], list[float]]
        coordinates = [[], [], []]
        for i in range(self.bottom_index, self.top_index + 1):
            point = self.point_table.points[i]
            coordinates[0].append(point.x)
            coordinates[1].append(point.y)
            if len(point.derivatives):
                coordinates[2].append(point.derivatives[0])
        if self.inverse:
            coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
            coordinates[2] = [1 / derivative for derivative in coordinates[2]]
        self.coordinates = coordinates

    def get_coordinates(self) -> list[list[float], list[float], list[float]]:
        return self.coordinates

    def print(self) -> None:
        if self.bottom_index > self.top_index:
            print("Partial table is empty\n")
            return

        print("Partial table points:")
        function = self.point_table.function
        argument = self.point_table.argument
        if self.inverse:
            function, argument = argument, function
        if len(self.point_table.points[0].derivatives) == 0:
            print("\t\t{}\t\t|\t{}".format(argument, function))
        else:
            print("\t\t{}\t\t|\t{}\t\t|\t{}".format(argument, function, "derivative"))
        for i in range(self.bottom_index, self.top_index + 1):
            print("{: 2}).\t".format(i), end='')
            if len(self.coordinates[2]) == 0:
                print("{:.3f}\t|\t{:.3f}".format(self.coordinates[0][i], self.coordinates[1][i]))
                continue
            print("{:.3f}\t|\t{:.3f}\t|\t{:.3f}".format(self.coordinates[0][i], self.coordinates[1][i], self.coordinates[2][i]))
        print("")


class ExtendedList(list[float]):
    def __len__(self):
        return super().__len__() * 2

    def __getitem__(self, key: int):
        return super().__getitem__(key // 2)


class DiffsTable:
    inverse: bool = False
    point_table: PointTable
    partial_table: PartialTable
    diffs: list[list[float], list[float]]
    derivatives: list[float]
    power: int
    points_used: int

    def __init__(self, point_table: PointTable):
        self.point_table = point_table
        self.partial_table = PartialTable(self.point_table)

    def get_value(self, argument: float, power: int) -> float:
        factor = 1
        approximated_value = self.diffs[1][0]

        for i in range(2, len(self.diffs)):
            if not self.diffs[i]:
                continue
            factor *= argument - self.diffs[0][i - 2]
            approximated_value += factor * self.diffs[i][0]

        return approximated_value

    def print_(self, table_name: str) -> None:
        if len(self.diffs) == 0:
            print("{} is empty\n".format(table_name))
            return
        print(table_name)
        function = self.point_table.function
        argument = self.point_table.argument
        if self.inverse:
            function, argument = argument, function
        print("\t\t{:^10.10s}|{:^10.10s}".format(argument, function), end='')
        for i in range(1, len(self.diffs) - 1):
            print("|{:^10.10s}".format("y" + "'" * i), end='')
        print("")
        for i in range(self.points_used):
            print("{:2}).\t{: ^ 10.3f}|{: ^ 10.3f}".format(self.partial_table.bottom_index + i + 1,
                                                           self.diffs[0][i], self.diffs[1][i]), end='')
            for j in range(2, len(self.diffs)):
                if len(self.diffs[j]) <= i:
                    continue
                print("|{: ^ 10.3f}".format(self.diffs[j][i]), end='')
            print("")
        print("")


class HermiteDiffsTable(DiffsTable):
    def calculate_diffs(self, power: int):
        coordinates = self.partial_table.get_coordinates()
        diffs: list[list[float], list[float]] = [ExtendedList(coordinates[0]), ExtendedList(coordinates[1])]
        self.derivatives = ExtendedList(coordinates[2])

        for i in range(1, len(self.partial_table) * 2 - (power + 1) % 2):
            column = []
            for j in range(len(self.partial_table) * 2 - i - (power + 1) % 2):
                if i == 1 and j % 2 == 0:
                    column.append(self.derivatives[j])
                    continue
                partial_x_difference = diffs[0][j] - diffs[0][j + i]
                partial_y_difference = diffs[i][j] - diffs[i][j + 1]
                column.append(partial_y_difference / partial_x_difference)
            diffs.append(column)

        self.diffs = diffs
        self.points_used = len(self.diffs[0]) - (self.power + 1) % 2

    def update_partial_table(self, argument: float):
        self.partial_table.inverse = self.inverse
        self.partial_table.set_partition(argument, self.power // 2 + 1)

    def get_value(self, argument: float, power: int) -> float:
        self.power = power
        self.update_partial_table(argument)
        self.calculate_diffs(power)
        return super().get_value(argument, power)

    def print(self) -> None:
        super().print_("Hermite table")


class NewtonDiffsTable(DiffsTable):
    def calculate_diffs(self):
        coordinates = self.partial_table.get_coordinates()
        diffs: list[list[float], list[float]] = [coordinates[0], coordinates[1]]

        for i in range(1, self.partial_table.top_index - self.partial_table.bottom_index + 1):
            row = []
            for j in range(self.partial_table.top_index - self.partial_table.bottom_index - i + 1):
                partial_x_difference = diffs[0][j] - diffs[0][j + i]
                partial_y_difference = diffs[i][j] - diffs[i][j + 1]
                row.append(partial_y_difference / partial_x_difference)
            diffs.append(row)
        self.diffs = diffs
        self.points_used = len(self.diffs[0])

    def update_partial_table(self, argument: float):
        self.partial_table.inverse = self.inverse
        self.partial_table.set_partition(argument, self.power + 1)

    def configure(self, argument: float, power: int) -> None:
        self.power = power
        self.update_partial_table(argument)
        self.calculate_diffs()

    def get_value(self, argument: float, power: int) -> float:
        self.power = power
        self.update_partial_table(argument)
        self.calculate_diffs()
        return super().get_value(argument, power)

    def print(self) -> None:
        super().print_("Newton table")
