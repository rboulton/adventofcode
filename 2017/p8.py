import sys

def has_duplicates(phrase):
    words = phrase.split()
    sorted_words = [''.join(sorted(word)) for word in words]

    already_seen = set()
    for word in sorted_words:
        if word in already_seen:
            return True
        already_seen.add(word)
    return False

def phrase_is_valid(phrase):
    return not has_duplicates(phrase)

def count_valid(phrases):
    return sum(1 for phrase in phrases if phrase_is_valid(phrase))

print(count_valid(file(sys.argv[1]).readlines()))