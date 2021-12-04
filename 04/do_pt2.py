import argparse
import json


class Row:
    NOT_FOUND = 0
    FOUND = 1

    def __init__(self, raw_row):
        self.values_remaining = list(raw_row)
        self.bingo = False

    @property
    def score(self):
        return sum(self.values_remaining)

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
        self.winning_draw = 0
        self.bingo = False
        for row in raw_board["rows"]:
            self.rows.append(Row(row))
        self.rows.extend(self.get_cols_from_rows(self.rows))

    @property
    def score(self):
        return (sum([row.score for row in self.rows]) // 2) * self.winning_draw

    def __repr__(self):
        ret = f"{json.dumps([row.values_remaining for row in self.rows])}\nScore: {self.score}\n"
        return ret

    def get_cols_from_rows(self, rows):
        """Calculate board columns from its rows"""
        cols = []
        for i in range(len(rows)):
            cols.append([])
        for row in rows:
            for i, val in enumerate(row.values_remaining):
                cols[i].append(val)
        return [Row(col) for col in cols]

    def check(self, val):
        """Check board for given number"""
        if self.bingo:
            return False

        for row in self.rows:
            ret = None
            while ret != Row.NOT_FOUND:
                ret = row.check(val)
            if row.bingo:
                self.winning_draw = val
                self.bingo = True
        return self.bingo


class Runner:
    def __init__(self, input_file, test=False):
        self.input_file = input_file
        self.test = test
        self.num_bin_digits = 0
        self.data = self.read_input()

    def read_input(self):
        data = {"draw_pile": [], "boards": []}
        with open(self.input_file, "r") as f:
            data["draw_pile"] = [int(n) for n in f.readline().strip().split(",")]
            for line in f.readlines():
                if line.strip() == "":
                    board_raw = {"rows": []}
                    continue
                row = [int(n) for n in line.strip().split(" ") if n != ""]
                board_raw["rows"].append(row)
                nrows = len(board_raw["rows"])
                if row and nrows == len(row):
                    data["boards"].append(Board(board_raw))

        if self.test:
            print(f"\ndata:{data}")

        return data

    def process_data(self):
        """Draw numbers and check boards until last board gets Bingo"""
        draw_pile = self.data["draw_pile"]
        boards = self.data["boards"]
        first_winner = None
        last_winner = None
        while len(draw_pile):
            val = draw_pile.pop(0)
            for board in boards:
                if board.bingo:
                    continue
                board.check(val)
                if board.bingo:
                    if not first_winner:
                        first_winner = board
                    last_winner = board
        if self.test:
            print(last_winner)
        return first_winner.score, last_winner.score


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
