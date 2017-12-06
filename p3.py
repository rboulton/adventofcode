import csv
import sys

rows = [
    [int(item) for item in row]
    for row in csv.reader(open(sys.argv[1], "rb"), "excel-tab")
]
rowsums = sum(
    max(row) - min(row)
    for row in rows
)
print(rowsums)
