from collections import Counter

input = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''

input = open("2023/input2.txt", "r").read().strip()

def parse_items(items):
    result = {}
    for item in items.strip().split(','):
        num, colour = item.strip().split()
        result[colour] = int(num)
    return result

def power(groups):
    max_items = Counter()
    for items in groups.split(';'):
        items = parse_items(items)
        for k, v in items.items():
            max_items[k] = max(max_items[k], v)
    r = 1
    for v in max_items.values():
        r = r*v
    return r
        
 
powers = []
for line in input.strip().split('\n'):
    game, groups = line.split(':')
    game_num = int(game[5:])
    p = power(groups)
    powers.append(p)

print(sum(powers))