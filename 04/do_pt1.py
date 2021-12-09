import argparse
import json


class Bingo(int):
    """Stores the score of the winning board"""

    def __init__(self, score):
        self.score = score


class Row:
    NOT_FOUND = 0
    FOUND = 1

    def __init__(self, raw_row):
        self.values_remaining = list(raw_row)
        self.bingo = False

    def __str__(self):
        return str(self.values_remaining)

    def check(self, val):
        ret = Row.NOT_FOUND
        if val in self.values_remaining:
            ret = Row.FOUND
            self.values_remaining.remove(val)
            if self.values_remaining == []:
                self.bingo = True
        return ret


class Board:
    def __init__(self, raw_board):
        self.rows = []
        self.remaining_values = []
        for row in raw_board["rows"]:
            self.rows.append(Row(row))
            self.remaining_values.extend(row)

        for col in raw_board["cols"]:
            self.rows.append(Row(col))

    @property
    def score(self):
        return sum(self.remaining_values)

    def __repr__(self):
        ret = "{"
        for row in self.rows:
            ret += str(row) + "\n"
        ret += "}"
        ret += f"\nScore: {self.score}"
        return ret

    def check(self, val):
        """Check board for given number"""
        bingo = None

        while val in self.remaining_values:
            self.remaining_values.remove(val)

        for row in self.rows:
            ret = None
            while ret != Row.NOT_FOUND:
                ret = row.check(val)
            if row.bingo:
                bingo = Bingo(self.score)
        return bingo


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.num_bin_digits = 0
        self.data = self.read_input()

    def read_input(self):
        data = {"called_nums": [], "boards": []}
        with open(self.input_file, "r") as f:
            data["called_nums"] = [int(n) for n in f.readline().strip().split(",")]
            for line in f.readlines():
                if line.strip() == "":
                    board_raw = {"rows": [], "cols": []}
                    continue
                row = [int(n) for n in line.strip().split(" ") if n != ""]
                board_raw["rows"].append(tuple(row))
                nrows = len(board_raw["rows"])
                if row and nrows == len(row):
                    board_raw["cols"] = self.get_cols_from_rows(board_raw["rows"])
                    data["boards"].append(Board(board_raw))

        if self.test:
            print(f"\ndata:{data}")

        return data

    def get_cols_from_rows(self, rows):
        cols = []
        for i in range(len(rows)):
            cols.append([])
        for row in rows:
            for i, val in enumerate(row):
                cols[i].append(val)
        for i in range(len(cols)):
            cols[i] = tuple(cols[i])
        return cols

    def process_data(self):
        numbers = self.data["called_nums"]
        boards = self.data["boards"]
        while len(numbers):
            val = numbers.pop(0)
            for board in boards:
                bingo = board.check(val)
                if isinstance(bingo, Bingo):
                    print(board)
                    return bingo.score * val


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"

    runner = Runner(input_file, args.test)

    print(f"{runner.process_data()}")
