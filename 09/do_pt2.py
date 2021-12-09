import argparse


class Point:
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3

    def __init__(self, value, left=None, up=None, down=None, right=None, test=False):
        self.neighbors = [up, left, right, down]
        self.value = value
        self.test = test
        self.basin_set = None
        self._is_min = None

    def update_neighbor(self, position, val):
        self.neighbors[position] = val

    def is_min(self):
        if self._is_min is None:
            v = self.value
            l = self.neighbors[Point.LEFT]
            u = self.neighbors[Point.UP]
            d = self.neighbors[Point.DOWN]
            r = self.neighbors[Point.RIGHT]
            if (
                (l is None or v < l.value)
                and (u is None or v < u.value)
                and (d is None or v < d.value)
                and (r is None or v < r.value)
            ):
                self._is_min = True
                self.basin_set = set()
            else:
                self._is_min = False
        return self._is_min

    @property
    def risk_level(self):
        if self.is_min():
            return self.value + 1
        else:
            return 0

    def grow_basin_set(self, parent=None):
        if parent is None:
            parent = self
        parent.basin_set.add(self)
        for neighbor in self.neighbors:
            if (
                neighbor is not None
                and neighbor.value > self.value
                and neighbor.value < 9
            ):
                neighbor.grow_basin_set(parent)

    @property
    def basin_size(self):
        if self.is_min():
            return len(self.basin_set)
        else:
            return 0

    def __str__(self):
        if self.is_min():
            return f"-{self.value}-"
        else:
            return f" {self.value} "

    def __repr__(self):
        return str(self)


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.summary = {}
        self.data = self.read_input()

    def read_raw_line(self, raw_line, prev_line=None):
        points = [Point(int(val), test=self.test) for val in raw_line.strip()]
        FIRST_POINT_INDEX = 0
        LAST_POINT_INDEX = len(points) - 1
        for i, point in enumerate(points):
            if i > FIRST_POINT_INDEX:
                left_point = points[i - 1]
                point.update_neighbor(Point.LEFT, left_point)
                left_point.update_neighbor(Point.RIGHT, point)
            if i < LAST_POINT_INDEX:
                right_point = points[i + 1]
                point.update_neighbor(Point.RIGHT, right_point)
                right_point.update_neighbor(Point.LEFT, point)
            if prev_line is not None:
                up_point = prev_line[i]
                point.update_neighbor(Point.UP, up_point)
                up_point.update_neighbor(Point.DOWN, point)

        return points

    def read_input(self):
        data = []
        prev_line = None
        with open(self.input_file, "r") as f:
            for raw_line in f.readlines():
                new_row = self.read_raw_line(raw_line, prev_line=prev_line)
                prev_line = new_row
                data.append(new_row)
        return data

    def process_data(self):
        risk_level = 0
        basins = []
        for row in self.data:
            if self.test:
                print(row)
            for point in row:
                risk_level += point.risk_level
                if point.is_min():
                    point.grow_basin_set()
                    basin_size = point.basin_size
                    if self.test:
                        print(f"{point.value}: {basin_size}")
                    basins.append(basin_size)
        basins.sort()
        basins_value = 1
        for basin in basins[-3:]:
            basins_value *= basin
        return risk_level, basins_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Day 09: Smoke Basin")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--input_file")
    args = parser.parse_args()
    if args.input_file:
        input_file = args.input_file
    elif args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"

    runner = Runner(input_file, args.test)

    print(f"{runner.process_data()}")
