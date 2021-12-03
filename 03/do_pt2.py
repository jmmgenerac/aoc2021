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

    def int_to_bin(self, value_int):
        return "{value_int:0{width}b}".format(
            value_int=value_int, width=self.num_bin_digits
        )

    def invert_bin(self, value_bin):
        inverted = "".join(["1" if bit == "0" else "0" for bit in value_bin])
        return inverted

    def process_data(self):
        summary = {
            "signs": [0 for i in range(self.num_bin_digits)],
            "leader": [],
            "gamma_bin": "",
            "epsilon_bin": "",
            "gamma_int": 0,
            "epsilon_int": 0,
            "power": 0,
            "oxygen_bin": 0,
            "oxygen_int": 0,
            "c02_bin": 0,
            "c02_int": 0,
        }
        for value in self.data:
            for i in range(self.num_bin_digits):
                if value & (1 << i):
                    summary["signs"][i] += 1
                else:
                    summary["signs"][i] -= 1
        for i in range(self.num_bin_digits):
            if summary["signs"][i] >= 0:
                value = True
            elif summary["signs"][i] < 0:
                value = False

            summary["leader"].append(value)
            summary["gamma_int"] += value << i

        summary["gamma_bin"] = self.int_to_bin(summary["gamma_int"])
        summary["epsilon_bin"] = self.invert_bin(summary["gamma_bin"])
        summary["epsilon_int"] = int(summary["epsilon_bin"], 2)
        summary["power"] = summary["gamma_int"] * summary["epsilon_int"]

        oxygen_filter = self.data
        for i in range(self.num_bin_digits):
            if len(oxygen_filter) == 1:
                break
            oxygen_filter = self.filter_data(oxygen_filter, i, "oxy")

        c02_filter = self.data
        for i in range(self.num_bin_digits):
            if len(c02_filter) == 1:
                break
            c02_filter = self.filter_data(c02_filter, i, "c02")

        summary["oxygen_int"] = oxygen_filter[0]
        summary["oxygen_bin"] = self.int_to_bin(summary["oxygen_int"])
        summary["c02_int"] = c02_filter[0]
        summary["c02_bin"] = self.int_to_bin(summary["c02_int"])

        if self.test:
            print(f"\nsummary:\n{json.dumps(summary, indent=2)}")

        return summary

    def filter_data(self, data, left_index, oxy_or_c02):
        if self.test:
            print("Running filter")
            print(f"data: {data}, left_index: {left_index}, oxy_or_c02: {oxy_or_c02}")
        filtered_data = {"0": [], "1": []}
        for value_int in data:
            value_bin = self.int_to_bin(value_int)
            digit_val = value_bin[left_index]
            filtered_data[digit_val].append(value_int)
            if self.test:
                print(f"{value_bin}")

        num0 = len(filtered_data["0"])
        num1 = len(filtered_data["1"])

        if oxy_or_c02 == "oxy":
            if num0 > num1:
                return filtered_data["0"]
            elif num0 < num1 or num0 == num1:
                return filtered_data["1"]

        elif oxy_or_c02 == "c02":
            if num0 < num1 or num0 == num1:
                return filtered_data["0"]
            elif num0 > num1:
                return filtered_data["1"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"

    runner = Runner(input_file, args.test)
    print(runner.summary["oxygen_int"] * runner.summary["c02_int"])
