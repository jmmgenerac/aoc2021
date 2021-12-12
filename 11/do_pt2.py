import argparse


class Octo:
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3
    UPPER_LEFT = 4
    UPPER_RIGHT = 5
    LOWER_LEFT = 6
    LOWER_RIGHT = 7

    def __init__(
        self,
        value,
        left=None,
        up=None,
        down=None,
        right=None,
        upper_left=None,
        upper_right=None,
        lower_left=None,
        lower_right=None,
        test=False,
    ):
        self.neighbors = [
            up,
            left,
            right,
            down,
            upper_left,
            upper_right,
            lower_left,
            lower_right,
        ]
        self.value = value
        self.test = test
        self.flashing = False

    def update_neighbor(self, position, point):
        self.neighbors[position] = point

    def increment(self):
        if not self.flashing:
            self.value += 1
        if self.value == 10:
            self.flashing = True
        return self.flashing

    def propagate_flash(self):
        if not self.flashing:
            return 0
        for neighbor in self.neighbors:
            if neighbor is not None and not neighbor.flashing:
                neighbor.increment()
                neighbor.propagate_flash()
        return 0

    def cycle_end(self):
        if self.flashing:
            self.flashing = False
            self.value = 0
            return 1
        return 0

    def __str__(self):
        if self.value > 9:
            return "*"
        return str(self.value)

    def __repr__(self):
        return str(self)


class Runner:
    def __init__(self, input_file, num_steps, test=False):
        self.input_file = input_file
        self.num_steps = num_steps
        self.test = test
        self.summary = {}
        self.data = self.read_input()

    def read_raw_line(self, raw_line, prev_line=None):
        points = [Octo(int(val), test=self.test) for val in raw_line.strip()]
        FIRST_POINT_INDEX = 0
        LAST_POINT_INDEX = len(points) - 1
        for i, point in enumerate(points):
            if i > FIRST_POINT_INDEX:
                left_point = points[i - 1]
                point.update_neighbor(Octo.LEFT, left_point)
                left_point.update_neighbor(Octo.RIGHT, point)
            if i < LAST_POINT_INDEX:
                right_point = points[i + 1]
                point.update_neighbor(Octo.RIGHT, right_point)
                right_point.update_neighbor(Octo.LEFT, point)
            if prev_line is not None:
                up_point = prev_line[i]
                point.update_neighbor(Octo.UP, up_point)
                up_point.update_neighbor(Octo.DOWN, point)
                if i > FIRST_POINT_INDEX:
                    upper_left_point = prev_line[i - 1]
                    point.update_neighbor(Octo.UPPER_LEFT, upper_left_point)
                    upper_left_point.update_neighbor(Octo.LOWER_RIGHT, point)
                if i < LAST_POINT_INDEX:
                    upper_right_point = prev_line[i + 1]
                    point.update_neighbor(Octo.UPPER_RIGHT, upper_right_point)
                    upper_right_point.update_neighbor(Octo.LOWER_LEFT, point)
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
        total_flash_count = 0
        first_synchronous_flash = None
        if self.test:
            for row in self.data:
                print("".join([str(point) for point in row]))
            print()
        for step in range(self.num_steps):
            this_step_flash_count = 0
            flashing_octos = []

            # increment all octo energy levels
            for row in self.data:
                for octo in row:
                    octo.increment()
                    if octo.flashing:
                        flashing_octos.append(octo)

            if self.test:
                print(f"step {step + 1}, increment")
                for row in self.data:
                    print("".join([str(point) for point in row]))

            # propagate energy from each octo that flashed
            for octo in flashing_octos:
                octo.propagate_flash()

            if self.test:
                print(f"step {step + 1}, propagate flash")
                for row in self.data:
                    print("".join([str(point) for point in row]))

            # count up all the octos that flashed during this step
            for row in self.data:
                for octo in row:
                    this_step_flash_count += octo.cycle_end()

            if self.test:
                print(f"step {step + 1}, finish step")
                for row in self.data:
                    print("".join([str(point) for point in row]))

            if self.test:
                print(f"flash count: {this_step_flash_count}\n")

            total_flash_count += this_step_flash_count

            if this_step_flash_count == 100:
                first_synchronous_flash = step + 1
                return total_flash_count, first_synchronous_flash

        if self.test:
            for row in self.data:
                print("".join([str(point) for point in row]))
        return total_flash_count, first_synchronous_flash


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Day 11: Dumbo Octopus")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--input_file")
    parser.add_argument(
        "num_steps", help="Number of steps to run the simulation", type=int
    )
    args = parser.parse_args()
    if args.input_file:
        input_file = args.input_file
    elif args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"

    runner = Runner(input_file, args.num_steps, test=args.test)

    print(f"{runner.process_data()}")
