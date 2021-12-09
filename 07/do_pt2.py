import argparse
import json


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.summary = {}
        self.data = self.read_input()
        self.fuel_calc_cache = {}

    def read_input(self):
        with open(self.input_file, "r") as f:
            data = [int(n) for n in f.read().strip().split(",")]
        if self.test:
            print(data)

        return data

    def calc_fuel(self, dist):
        if dist not in self.fuel_calc_cache:
            fuel = 0
            for i in range(1, dist + 1):
                fuel += i
            self.fuel_calc_cache[dist] = fuel
        return self.fuel_calc_cache[dist]

    def get_dists(self, a):
        dists = []
        for x in self.data:
            fuel = self.calc_fuel(abs(x - a))
            dists.append(fuel)
        return sum(dists), dists

    def process_data(self):
        self.summary = {}
        min_fuel = None
        min_dists = None
        optimal_spot = None
        for i in range(min(self.data), max(self.data) + 1):
            total_fuel, dists = self.get_dists(i)
            self.summary[i] = {"dists": dists, "fuel": total_fuel}
            if min_fuel is None or total_fuel < min_fuel:
                min_fuel = total_fuel
                min_dists = dists
                optimal_spot = i
        return optimal_spot, min_fuel


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Day 07: crab submarines")
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
