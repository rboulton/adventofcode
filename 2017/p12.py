import sys
import copy

initial_sizes = [int(value) for value in open(sys.argv[1]).readline().split('\t')]

def reallocate(sizes):
    to_allocate = max(sizes)
    bank = sizes.index(to_allocate)
    new_sizes = copy.copy(sizes)
    new_sizes[bank] = 0

    for _ in range(to_allocate):
        bank = (bank + 1) % len(sizes)
        new_sizes[bank] += 1

    return new_sizes

def iterate(sizes):
    step = 0
    old_sizes = []
    while True:
        old_sizes.append(sizes)
        sizes = reallocate(sizes)
        step += 1
        if sizes in old_sizes:
            return sizes, step

new_sizes, steps = iterate(initial_sizes)

print iterate(new_sizes)[1]