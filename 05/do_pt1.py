import argparse
import json




class Grid:
    def __init__(self, max_x, max_y):
        self.grid = [[0 for x in range(max_x+1)] for y in range(max_y+1)]
        self.intersections = set([])

    def draw_line(self, point_pair):
        try:
            (x1, y1), (x2, y2) = point_pair
            if x1 != x2 and y1 != y2:
                return
            x_start = min(x1, x2)
            x_end = max(x1,x2) + 1
            y_start = min(y1,y2)
            y_end = max(y1,y2) + 1

            for y in range(y_start, y_end):
                for x in range(x_start, x_end):
                    self.grid[y][x] += 1
                    if self.grid[y][x] > 1:
                        self.intersections.add((x,y))
        except Exception as ex:
            print(f"Exception drawing point pair {point_pair}")
            print(f"grid dims: {len(self.grid[0])}, {len(self.grid)}")
            raise ex

    def __str__(self):
        ret = ""
        for i, row in enumerate(self.grid):
            if i != 0:
                ret += "\n"
            ret += "".join(["." if x == 0 else str(x) for x in row])
        return ret



class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.num_bin_digits = 0
        self.summary = {}
        self.grid = None
        self.data = self.read_input()

    def read_input(self):
        data = []
        max_x = max_y = 0
        with open(self.input_file, "r") as f:
            for line in f.readlines():
                coords_str = (
                    tuple(coord.split(","))
                    for coord in line.strip().replace(" -> ", ".").split(".")
                )
                line_seg = []
                for x_str, y_str in coords_str:
                    x = int(x_str)
                    y = int(y_str)
                    point = (x, y)
                    line_seg.append(point)
                    if x > max_x:
                        max_x = x
                    if y > max_y:
                        max_y = y
                line_seg = tuple(line_seg)
                if self.test:
                    print(line_seg)
                data.append(line_seg)

        self.summary = {"dims": (max_x, max_y)}

        self.grid = self.draw_grid(max_x, max_y)

        if self.test:
            print(f"{self.summary}")

        return data

    def draw_grid(self, max_x, max_y):
        return Grid(max_x, max_y)

    def process_data(self):
        for point_pair in self.data:
            self.grid.draw_line(point_pair)
        if self.test:
            print(self.grid)
            print(self.grid.intersections)
        return len(self.grid.intersections)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"

    runner = Runner(input_file, args.test)

    print(f"{runner.process_data()}")
