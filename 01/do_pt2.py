import argparse


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.data = self.read_input()

    def read_input(self):
        with open(self.input_file, "r") as f:
            data = [int(line.strip()) for line in f.readlines()]
        if self.test:
            print("data:")
            for line in data:
                print(line)
        return data

    def count_increases(self, data):
        cnt = 0
        increases = []
        for i in range(1, len(data)):
            increase = data[i] > data[i - 1]
            if self.test:
                print(f"{data[i]} > {data[i-1]}: {increase}")
            increases.append(increase)
        cnt = sum(increases)
        if self.test:
            print(f"sum: {cnt}")
        return cnt

    def get_windows(self, data, window_len):
        windows = []
        if self.test:
            print(f"windows (data len: {len(data)}, window_len: {window_len}:")
        for i in range(len(data) - window_len + 1):
            if self.test:
                print(f"i = {i}")
            window = []
            for j in range(window_len):
                window.append(data[i + j])
            window_sum = sum(window)
            if self.test:
                print(f"{window}: {window_sum}")
            windows.append(window_sum)
        return windows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"

    runner = Runner(input_file, args.test)
