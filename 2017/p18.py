import sys
import re

def count_garbage(text):
    uncancelled = re.sub(r'!.', '', text)

    for match in re.findall(r'<[^>]*>', uncancelled):
        yield len(match) - 2

text = open(sys.argv[1]).read().strip()

print(sum(count_garbage(text)))
