from storage import PointTable
import numpy as np


class PartialTable:
    # point_table: PointTable
    array: np.ndarray
    bottom_index: int
    top_index: int
    # coordinates: list[list[float], list[float], list[float]]
    inverse: bool = False

    def __init__(self, array: np.ndarray):
        if self.array.shape[0] != 2:
            print("Incorrect array shape")
            raise ValueError

        # self.point_table = point_table
        self.array = array
        self.bottom_index = 0
        # max_amount = len(self.point_table)
        max_amount = len(self.array[0])
        max_index = max_amount - 1
        self.top_index = max_index
        # self.set_coordinates()

    def __len__(self) -> int:
        return max(self.top_index - self.bottom_index + 1, 0)

    def set_partition(self, value: float, amount: int) -> None:
        self.bottom_index = 0
        # max_amount = len(self.point_table)
        max_amount = len(self.array)
        max_index = max_amount - 1
        top_index = max_index
        self.top_index = top_index
        # self.set_coordinates()

        # for index in range(len(self.point_table)):
        #     if self.coordinates[0][index] > value:
        for index in range(len(self.array[0])):
            if self.array[0][index] > value:
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

        self.bottom_index = bottom_index
        self.top_index = top_index
        # self.set_coordinates()

    # def set_coordinates(self) -> None:
    #     coordinates: list[list[float], list[float], list[float]]
    #     coordinates = [[], [], []]
    #     for i in range(self.bottom_index, self.top_index + 1):
    #         point = self.point_table.points[i]
    #         coordinates[0].append(point.x)
    #         coordinates[1].append(point.y)
    #     if self.inverse:
    #         coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
    #         coordinates[2] = [1 / derivative for derivative in coordinates[2]]
    #     self.coordinates = coordinates

    # def get_coordinates(self) -> list[list[float], list[float], list[float]]:
    #     return self.coordinates

    def print(self) -> None:
        if self.bottom_index > self.top_index:
            print("Partial table is empty\n")
            return

        print("Partial table points:")
        # function = self.point_table.function
        # argument = self.point_table.argument
        # if self.inverse:
        #     function, argument = argument, function
        # print("\t\t{}\t\t|\t{}".format(argument, function))
        # for i in range(self.bottom_index, self.top_index + 1):
        #     print("{: 2}).\t".format(i), end='')
        #     if len(self.coordinates[2]) == 0:
        #         print("{:.3f}\t|\t{:.3f}".format(self.coordinates[0][i], self.coordinates[1][i]))
        #         continue
        #     print("{:.3f}\t|\t{:.3f}\t|\t{:.3f}".format(self.coordinates[0][i], self.coordinates[1][i], self.coordinates[2][i]))
        # print("")


class DiffsTable:
    inverse: bool = False
    argument: float
    # point_table: PointTable
    array: np.ndarray
    partial_table: PartialTable
    diffs: list[list[float], list[float]]
    power: int
    points_used: int

    def __init__(self, array: np.ndarray):
        if self.array.shape[0] != 2:
            print("Incorrect array shape")
            raise ValueError

        # self.point_table = point_table
        self.array = array
        self.partial_table = PartialTable(self.array)

    def get_value(self, argument: float) -> float:
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
        # function = self.point_table.function
        # argument = self.point_table.argument
        # if self.inverse:
        #     function, argument = argument, function
        # print("\t\t{:^10.10s}|{:^10.10s}".format(argument, function), end='')
        # for i in range(1, len(self.diffs) - 1):
        #     print("|{:^10.10s}".format("y" + "'" * i), end='')
        # print("")
        # for i in range(self.points_used):
        #     print("{:2}).\t{: ^ 10.3f}|{: ^ 10.3f}".format(self.partial_table.bottom_index + i + 1,
        #                                                    self.diffs[0][i], self.diffs[1][i]), end='')
        #     for j in range(2, len(self.diffs)):
        #         if len(self.diffs[j]) <= i:
        #             continue
        #         print("|{: ^ 10.3f}".format(self.diffs[j][i]), end='')
        #     print("")
        # print("")


class NewtonPolynom(DiffsTable):
    def calculate_table(self, argument: float, power: int):
        if not self.check_power(power):
            # print("Power is too big (max: ", len(self.point_table), ")", sep="")
            print("Power is too big (max: ", len(self.array[0]), ")", sep="")
            raise ValueError
        self.power = power
        self.update_partial_table(argument)
        self.calculate_diffs()
        self.argument = argument

    def get_value(self, argument: float) -> float:
        return super().get_value(argument)

    def get_derivative(self, argument: float, epsilon: float) -> float:
        x_1 = argument - epsilon
        x_2 = argument + epsilon

        y_1 = super().get_value(x_1)
        y_2 = super().get_value(x_2)

        return (y_2 - y_1) / epsilon

    def get_second_derivative(self, argument: float, epsilon: float) -> float:
        x_1 = argument - epsilon
        x_2 = argument
        x_3 = argument + epsilon

        y_1 = super().get_value(x_1)
        y_2 = super().get_value(x_2)
        y_3 = super().get_value(x_3)

        return (y_3 - 2 * y_2 + y_1) / epsilon ** 2

    def check_power(self, power: int) -> bool:
        # return len(self.point_table) >= power + 1
        return len(self.array[0]) >= power + 1

    def update_partial_table(self, argument: float):
        self.partial_table.inverse = self.inverse
        self.partial_table.set_partition(argument, self.power + 1)

    def calculate_diffs(self):
        # coordinates = self.partial_table.get_coordinates()
        diffs: list[list[float], list[float]] = [self.array[0], self.array[1]]

        for i in range(1, self.partial_table.top_index - self.partial_table.bottom_index + 1):
            row = []
            for j in range(self.partial_table.top_index - self.partial_table.bottom_index - i + 1):
                partial_x_difference = diffs[0][j] - diffs[0][j + i]
                partial_y_difference = diffs[i][j] - diffs[i][j + 1]
                row.append(partial_y_difference / partial_x_difference)
            diffs.append(row)
        self.diffs = diffs
        self.points_used = len(self.diffs[0])

    def print(self) -> None:
        super().print_("Newton's table")
