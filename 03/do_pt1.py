import argparse
import json


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.num_bin_digits = 0
        self.data = self.read_input()
        self.summary = self.process_data()

    def read_input(self):
        data = []
        with open(self.input_file, "r") as f:
            for line in f.readlines():
                value_bin = line.strip()
                if len(value_bin) > self.num_bin_digits:
                    self.num_bin_digits = len(value_bin)
                value_int = int(value_bin, 2)
                data.append(value_int)
        if self.test:
            print("\ndata:")
            for line in data:
                print(line)
        return data

    def process_data(self):
        summary = {
            "signs": [0 for i in range(self.num_bin_digits)],
            "leader": [],
            "gamma_bin": "",
            "epsilon_bin": "",
            "gamma_int": 0,
            "epsilon_int": 0,
            "power": 0,
        }
        for value in self.data:
            for i in range(self.num_bin_digits):
                if value & (1 << i):
                    summary["signs"][i] += 1
                else:
                    summary["signs"][i] -= 1
        for i in range(self.num_bin_digits):
            if summary["signs"][i] > 0:
                value = True
            elif summary["signs"][i] < 0:
                value = False
            else:
                value = None
            summary["leader"].append(value)
            summary["gamma_int"] += value << i
            summary["epsilon_int"] += (not value) << i

        summary["gamma_bin"] = "{value_int:0{width}b}".format(
            value_int=summary["gamma_int"], width=self.num_bin_digits
        )
        summary["epsilon_bin"] = "{value_int:0{width}b}".format(
            value_int=summary["epsilon_int"], width=self.num_bin_digits
        )
        summary["power"] = summary["gamma_int"] * summary["epsilon_int"]
        if self.test:
            print(f"\nsummary:\n{json.dumps(summary, indent=2)}")

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
    print(json.dumps(runner.summary, indent=2))
