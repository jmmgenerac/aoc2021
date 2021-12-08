import argparse
import json


class Display:
    def __init__(self, key, patterns):
        self.key = key
        self.patterns = patterns

    def count_standalones(self):
        ret = 0
        for p in self.patterns:
            num_illuminated = len(p)
            if num_illuminated in [7, 4, 3, 2]:
                ret += 1
        return ret

class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.summary = {}
        self.data = self.read_input()

    def read_input(self):
        data = []
        with open(self.input_file, "r") as f:
            for line in f.readlines():
                key_raw, patterns_raw = line.strip().split('|')
                key = key_raw.split(' ')
                patterns = patterns_raw.split(" ")
                data.append((key, patterns))
        return data


    def is_8(self, input):
        return len(input) == 7

    def process_data(self):
        summary = {"standalones": 0}
        for key, patterns in self.data:
            display = Display(key, patterns)
            num_standalones = display.count_standalones()
            summary["standalones"] += num_standalones
            if self.test:
                print(f"{num_standalones}: raw_display: {patterns}")
        return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Day 07: crab submarines')
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
