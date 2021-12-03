import argparse

class Runner():
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.data = self.read_input()
        self.summary = self.process_data()

    def read_input(self):
        with open(self.input_file, "r") as f:
            data = [tuple(line.strip().split(' ')) for line in f.readlines()]
        if self.test:
            print("\ndata:")
            for line in data:
                print(line)
        return data

    def process_data(self):
        summary = {
            "horizontal": 0,
            "depth": 0,
        }
        for direction, value in self.data:
            if direction == "forward":
                summary['horizontal'] += int(value)
            elif direction == "up":
                summary['depth'] -= int(value)
            elif direction == "down":
                summary['depth'] += int(value)
        if self.test:            
            print(f"\nsummary:\n{summary}")

        return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt" 

    runner = Runner(input_file, args.test)
    print(f"{runner.summary['depth'] * runner.summary['horizontal']}")
