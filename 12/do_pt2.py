import argparse
from timeit import default_timer as timer


class Path:
    def __init__(self, start, test=False):
        self.test = test
        self.start = start
        self.points = []
        self.special_visit = False
        self.finished = False
        self.add_point(start)

    def add_point(self, point):
        times_visited = self.points.count(point)

        if (
            point.is_big
            or (not point.is_big and times_visited == 0)
            or (
                not point.is_big
                and times_visited == 1
                and not self.special_visit
                and point.name not in ("start", "end")
            )
        ):
            if not point.is_big and times_visited > 0:
                self.special_visit = True

            self.points.append(point)
            if point.name == "end":
                self.finished = True
            return True
        return False

    def copy(self):
        new_path = type(self)(self.start)
        new_path.points = self.points.copy()
        new_path.special_visit = self.special_visit
        new_path.finished = self.finished
        new_path.test = self.test
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
            if not path.finished:
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
    parser = argparse.ArgumentParser("Day 12")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--input_file")
    args = parser.parse_args()
    if args.input_file:
        input_file = args.input_file
    elif args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"


    start = timer()
    runner = Runner(input_file, args.test)
    print(f"{runner.process_data()}")
    print(f"runtime: {timer() - start}")
