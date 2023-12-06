input = '''
Time:      7  15   30
Distance:  9  40  200
'''

input = open('2023/input6.txt', 'r').read()

def dist(race_time, hold_time):
    return (race_time - hold_time) * hold_time

def winning_options(race_time, distance):
    count = 0
    for hold_time in range(1, race_time):
        if dist(race_time, hold_time) > distance:
            count += 1
    return count

times, distances = input.strip().split('\n')
times = [int(t) for t in times.split(" ")[1:] if t != '']
distances = [int(d) for d in distances.split(" ")[1:] if d != '']

opts = []
ans = 1
for t, d in zip(times, distances):
    o = winning_options(t, d)
    opts.append(o)
    ans *= o
print(opts)
print(ans)

