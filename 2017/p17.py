import sys
import re

def remove_garbage(text):
    return re.sub(r'<([^!>]|(!.))*>', '', text)

def count(text, level):
    print("Counting len {} at level {}".format(len(text), level))
    if text == '':
        return 0
    assert text[0] == '{'
    assert text[-1] == '}'

    return level + sum(
        count(subtext, level + 1)
        for subtext in text[1:-1].split(',%02d' % level)
    )

def mark_comma_levels(text):
    chars = []
    level = 0
    for ch in text:
        if ch == '{':
            level += 1
        elif ch == '}':
            level -= 1
        else:
            assert ch == ','
            ch = ',%02d' % level
        chars.append(ch)
    return ''.join(chars)

text = open(sys.argv[1]).read().strip()
clean_text = remove_garbage(text)
marked = mark_comma_levels(clean_text)
print(marked)

print(count(marked, 1))
