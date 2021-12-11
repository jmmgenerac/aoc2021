import argparse
import json


class LanternFish:
    def __init__(self, time_left):
        self.time_left = time_left

    def tick(self):
        if self.time_left == 0:
            self.time_left = 6
            return 1
        self.time_left -= 1
        return 0

    def __str__(self):
        return str(self.time_left)


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.summary = {}
        self.data = self.read_input()

    def read_input(self):
        with open(self.input_file, "r") as f:
            data = [int(n) for n in f.read().strip().split(",")]
        if self.test:
            print(data)

        return data

    def process_data(self, num_days):
        summary = {}
        for i in range(8 + 1):
            summary[i] = 0
        for timer_val in self.data:
            summary[timer_val] += 1

        for day in range(num_days):
            new_hatches = summary[0]
            for timer_val in range(8):
                summary[timer_val] = summary[timer_val + 1]
            summary[6] += new_hatches
            summary[8] = new_hatches
            population = sum(summary.values())
            if self.test:
                print(population)
                # print(f"Day {day + 1}: {population}: {summary}")
                # print(f'After {day + 1} days: ({len(population)}) {",".join([str(fish.time_left) for fish in population])}')
        return population


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Day 06: lanternfish")
    parser.add_argument("--test", action="store_true")
    parser.add_argument(
        "num_days", help="Number of days to run the simulation", default=18, type=int
    )
    parser.add_argument("--input_file")
    args = parser.parse_args()
    if args.input_file:
        input_file = args.input_file
    elif args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"

    runner = Runner(input_file, args.test)

    print(f"{runner.process_data(args.num_days)}")
