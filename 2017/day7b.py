import sys
import re

def read_programs(filename):
    data = open(filename).readlines()

    programs = {}

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
        programs[name] = (weight, deps)
    return programs

def calc_parents(programs):
    parents = {}

    for name, (weight, deps) in programs.items():
        for dep in deps:
            assert dep not in parents
            parents[dep] = name

    return parents

def find_root(parents):
    program = parents.keys()[0]
    while program in parents:
        program = parents[program]
    return program

def calc_total_weights(tot_weights, programs, program):
    weight, deps = programs[program]
    for dep in deps:
        weight += calc_total_weights(tot_weights, programs, dep)
    tot_weights[program] = weight
    return weight

def find_unbalanced(tot_weights, programs, program):
    SENTINEL = -100000
    _, deps = programs[program]
    if not deps:
        return SENTINEL

    child_weights = [tot_weights[dep] for dep in deps]
    if max(child_weights) == min(child_weights):
        return SENTINEL

    # Unbalanced at this level; check lower levels
    dep_unbalanced = max(
            find_unbalanced(tot_weights, programs, dep)
        for dep in deps
    )
    if dep_unbalanced != SENTINEL:
        return dep_unbalanced

    assert(len(child_weights) > 2) # Or we can't work out the unique one to change
    correct_weight = sorted(child_weights)[1]
    for dep, weight in zip(deps, child_weights):
        if weight != correct_weight:
            dep_weight = programs[dep][0]
            fixed_weight = correct_weight - weight + dep_weight
            print(dep, weight, correct_weight, dep_weight, fixed_weight)
            return fixed_weight
    assert False
    

programs = read_programs(sys.argv[1])
parents = calc_parents(programs)
root = find_root(parents)
tot_weights = {}
calc_total_weights(tot_weights, programs, root)
print(find_unbalanced(tot_weights, programs, root))
