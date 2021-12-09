import argparse
from timeit import default_timer as timer


class Display:
    def __init__(self, key, patterns, test=False):
        self.test = test
        if self.test:
            print(f"{key}: {patterns}")

        self.key = self.sort_strings(key)
        self.digit_by_segments, self.segments_by_digit = self.decode_key(self.key)
        self.patterns = self.sort_strings(patterns)
        if self.test:
            print(f"{self.key}: {self.patterns}")
            print(f"{self.digit_by_segments}")
            print(f"{self.segments_by_digit}")

    def sort_strings(self, strings):
        sorted_strings = []
        for string in strings:
            char_list = list(string)
            char_list.sort()
            sorted_string = "".join(char_list)
            sorted_strings.append(sorted_string)
        return sorted_strings

    def count_standalones(self):
        ret = 0
        for p in self.patterns:
            num_illuminated = len(p)
            if num_illuminated in [7, 4, 3, 2]:
                ret += 1
        return ret

    def get_value(self):
        total = ""
        for p in self.patterns:
            total += str(self.digit_by_segments[p])
        return int(total)

    def unilluminated_segments(self, key_val):
        ret = ""
        for seg in "abcdefg":
            if seg not in key_val:
                ret += seg
        return ret

    def decode_key(self, key_raw):
        digit_by_segments = {}
        segments_by_digit = {}
        for_further_analysis = []
        raw_keys = key_raw
        for segments in raw_keys:
            keylen = len(segments)
            if keylen in [7, 4, 3, 2]:
                if keylen == 7:
                    digit = 8
                elif keylen == 4:
                    digit = 4
                elif keylen == 3:
                    digit = 7
                elif keylen == 2:
                    digit = 1
                digit_by_segments[segments] = digit
                segments_by_digit[digit] = segments
            else:
                for_further_analysis.append(segments)
        for segments in for_further_analysis:
            keylen = len(segments)
            if keylen == 5:
                unlit_1, unlit_2 = self.unilluminated_segments(segments)
                if unlit_1 in segments_by_digit[4] and unlit_2 in segments_by_digit[4]:
                    digit = 2
                else:
                    if (
                        unlit_1 not in segments_by_digit[1]
                        and unlit_2 not in segments_by_digit[1]
                    ):
                        digit = 3
                    else:
                        digit = 5
            elif keylen == 6:
                unlit_segment = self.unilluminated_segments(segments)
                if unlit_segment not in segments_by_digit[4]:
                    digit = 9
                elif unlit_segment not in segments_by_digit[1]:
                    digit = 0
                else:
                    digit = 6
            else:
                raise ValueError(
                    f"something went wrong: bad keylen for {segments}: {keylen}"
                )

            digit_by_segments[segments] = digit
            segments_by_digit[digit] = segments
        return digit_by_segments, segments_by_digit


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
                key_raw, patterns_raw = line.strip().split("|")
                key_raw = key_raw.strip()
                patterns_raw = patterns_raw.strip()
                key = key_raw.split(" ")
                patterns = patterns_raw.split(" ")
                data.append((key, patterns))
        return data

    def process_data(self):
        summary = {"standalones": 0, "total_value": 0}
        for key, patterns in self.data:
            display = Display(key, patterns, test=self.test)
            value = display.get_value()
            summary["total_value"] += value
            summary["standalones"] += display.count_standalones()

            if self.test:
                print(value)
                print(f"{summary['total_value']}")
        return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Day 08: Seven Segment Search")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--input_file")
    args = parser.parse_args()
    if args.input_file:
        input_file = args.input_file
    elif args.test:
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"

    start = timer()
    runner = Runner(input_file, args.test)
    print(f"{runner.process_data()}")
    print(f"runtime: {timer() - start}")
