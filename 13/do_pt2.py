import argparse


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.summary = {}
        self.data = self.read_input()
        self.bitmap = ""

    def read_input(self):
        data = {"points": set([]), "folds": []}
        with open(self.input_file, "r") as f:
            for raw_line in f.readlines():
                line = raw_line.strip()
                if line.startswith("fold along"):
                    index_of_equals = line.index("=")
                    varname = line[index_of_equals - 1]
                    val = int(line[index_of_equals + 1 :])
                    data["folds"].append({varname: val})
                else:
                    try:
                        point = tuple([int(e) for e in line.split(",")])
                    except:
                        pass
                    else:
                        data["points"].add(point)
        return data

    def reflect(self, point, fold):
        x, y = point
        if "y" in fold and y > fold["y"]:
            dist = y - fold["y"]
            reflected = (x, y - 2 * dist)
            if self.test:
                print(f"reflecting {point} to {reflected}")
            return reflected
        elif "x" in fold and x > fold["x"]:
            dist = x - fold["x"]
            reflected = (x - 2 * dist, y)
            if self.test:
                print(f"reflecting {point} to {reflected}")
            return reflected
        else:
            return point

    def get_bitmap(self):
        points = self.data["points"].copy()
        # points.sort(key=lambda x:x[1])
        pointmap = {}
        bitmap_str = ""
        for x, y in points:
            if pointmap.get(y) is None:
                pointmap[y] = []
            pointmap[y].append(x)

        for row in range(max(pointmap.keys()) + 1):
            max_x = max(pointmap.get(row, [0]))
            row_str = ""
            for x in range(max_x + 1):
                if x in pointmap.get(row):
                    row_str += "#"
                else:
                    row_str += " "
            bitmap_str += row_str + "\n"
        return bitmap_str

    def process_data(self):
        for fold in self.data["folds"]:
            reflected_points = set([])
            if self.test:
                print(fold)
            for point in self.data["points"]:
                reflected_points.add(self.reflect(point, fold))
            self.data["points"] = reflected_points
        self.bitmap = self.get_bitmap()
        return len(self.data["points"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Day 13: Transparent Origami")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--input_file")
    args = parser.parse_args()
    if args.input_file:
        input_file = args.input_file
    elif args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"

    runner = Runner(input_file, test=args.test)

    print(f"{runner.process_data()}")
    print(runner.bitmap)
