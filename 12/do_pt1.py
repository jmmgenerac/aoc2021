import argparse


class Path:
    def __init__(self, start, points=[], test=False):
        self.test = test
        self.start = start
        self.points = points
        self.finished = False
        self.add_point(start)

    def add_point(self, point):
        times_visited = self.points.count(point)

        if not self.finished and (point.is_big or times_visited == 0):
            self.points.append(point)
            if point.name == "end":
                self.finished = True
            return True
        return False

    def copy(self):
        new_path = type(self)(self.start, self.points.copy())
        return new_path

    def traverse(self, paths=[]):
        if self.finished:
            if self.test:
                print("end is found")
            return paths

        last_point = self.points[-1]
        starting_path = self.copy()
        if self.test:
            print(f"\nseeing {','.join([pt.name for pt in last_point.connections])}")
        for conn in last_point.connections:
            path = starting_path.copy()
            if self.test:
                print(f"adding point to {path}: {conn.name}")
            added = path.add_point(conn)
            if added:
                if path.finished:
                    if self.test:
                        print(f"adding finished path: {path}")
                    paths.append(path)
                else:
                    if self.test:
                        print(f"visiting {conn.name}")
                    paths = path.traverse(paths)

        return paths

    def __str__(self):
        return ",".join([point.name for point in self.points])

    def __repr__(self):
        return str(self)


class Point:
    def __init__(self, name):
        self.name = name
        self.connections = set()
        self.is_big = name.upper() == name

    def add_connection(self, point):
        self.connections.add(point)

    def __str__(self):
        conn_names = [conn.name for conn in self.connections]
        return f"{self.name}: {conn_names}"

    def __repr__(self):
        return str(self)


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.summary = {}
        self.data = self.read_input()

    def read_input(self):
        data = {}
        with open(self.input_file, "r") as f:
            for raw_line in f.readlines():
                pt1_name, pt2_name = raw_line.strip().split("-")
                # create point objects if they don't exist yet
                for pt_name in pt1_name, pt2_name:
                    if pt_name not in data:
                        pt = Point(pt_name)
                        data[pt_name] = pt
                data[pt1_name].add_connection(data[pt2_name])
                data[pt2_name].add_connection(data[pt1_name])

        return data

    def process_data(self):
        if self.test:
            for point in self.data.values():
                print(point)
        start = Path(self.data["start"], test=self.test)
        paths = start.traverse()
        if self.test:
            print("\npaths:")
            for path in paths:
                print(path)
        return len(paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Day 12: ")
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
