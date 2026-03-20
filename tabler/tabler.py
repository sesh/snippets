import re


def tabler(headers, data):
    def _trailing_padding(s, width):
        no_ansi_len = len(re.sub("\x1b\\[(K|.*?m)", "", s))
        return s + " " * (width - no_ansi_len)

    data = [headers] + data
    col_widths = [max([len(d[i]) for d in data]) for i in range(len(data[0]))]

    if sum(col_widths) < 180:
        col_widths = [x + 2 for x in col_widths]

    rows = [
        "|"
        + "|".join(
            f" {_trailing_padding(val, width)}" for width, val in zip(col_widths, row)
        )
        + "|"
        for row in data
    ]

    print("-" * len(rows[0]))
    print(rows[0])
    print("-" * len(rows[0]))
    print(*rows[1:], sep="\n")
    print("-" * len(rows[0]))


if __name__ == "__main__":
    import sys
    import csv

    fn = sys.argv[-1]
    with open(fn, "r") as f:
        reader = csv.reader(f)
        rows = [r for r in reader]
        tabler(rows[0], rows[1:])
