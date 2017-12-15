import csv
import sys

rows = [
    [int(item) for item in row]
    for row in csv.reader(open(sys.argv[1], "rb"), "excel-tab")
]

def find_coprime_ratio(row):
    items = set(row)
    for item in sorted(row):
        items.remove(item)
        for item2 in items:
            if item2 % item == 0:
                return item2 / item
    raise ValueError("Nothing coprime")

print(sum(find_coprime_ratio(row) for row in rows))