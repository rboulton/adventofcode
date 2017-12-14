import sys
import re

def read_programs(filename):
    data = open(filename).readlines()

    programs = []

    for row in data:
        row = row.strip()
        if row == "":
            continue
        mo = re.match(r'^([a-z]+)\s+\((\d+)\)(?:\s->\s([a-z].*))?$', row)
        assert mo
        name, weight, deps = mo.groups()
        weight = int(weight)
        if deps:
            deps = [dep.strip() for dep in deps.split(',')]
        else:
            deps = []
        programs.append((name, weight, deps))
    return programs

def calc_parents(programs):
    parents = {}

    for name, weight, deps in programs:
        for dep in deps:
            assert dep not in parents
            parents[dep] = name

    return parents

def find_root(parents):
    program = parents.keys()[0]
    while program in parents:
        program = parents[program]
    return program

programs = read_programs(sys.argv[1])
parents = calc_parents(programs)

print(find_root(parents))
