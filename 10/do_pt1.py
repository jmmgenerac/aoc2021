import argparse
from os import close


open_by_close = {"]": "[", ")": "(", "}": "{", ">": "<"}

close_by_open = {}

for value in open_by_close:
    key = open_by_close[value]
    close_by_open[key] = value

bracket_value = {")": 3, "]": 57, "}": 1197, ">": 25137}


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.summary = {}
        self.data = self.read_input()

    def read_input(self):
        data = []
        with open(self.input_file, "r") as f:
            for raw_line in f.readlines():
                data.append(raw_line.strip())
        return data

    def process_line(self, line):
        opens = []
        for char in line:
            if char in open_by_close.values():
                opens.append(char)
                if self.test:
                    print(f"{char}: {opens}")
            elif char in open_by_close.keys():
                # this is a closing bracket
                if opens[-1] == open_by_close[char]:
                    opens.pop()
                else:
                    raise ValueError(char)

    def process_data(self):
        score = 0
        for line in self.data:
            if self.test:
                print(line)
            try:
                self.process_line(line)
            except Exception as ex:
                this_score = int(bracket_value.get(str(ex)))
                score += this_score
                if self.test:
                    print(ex, this_score)
        return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Day 10: Syntax Scoring")
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
