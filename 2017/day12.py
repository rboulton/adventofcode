import sys

def read_pipes(filename):
    pipes = []
    for line in open(filename).readlines():
        a, b = line.split(' <-> ')
        pipes.append([int(a)] + map(lambda x: int(x.strip()), b.split(',')))
    return pipes

def group(pipes):
    members = {}
    group_nums = {}

    def set_group_nums(group_num, progs):
        for prog in progs:
            group_nums[prog] = group_num

    def merge_group(num1, num2):
        members1 = members.get(num1, set())
        members2 = members.get(num2, set())
        for m in members1:
            assert group_nums[m] == num1
        for m in members2:
            assert group_nums[m] == num2, [m, group_nums[m], num2, members]
        members[num1] = members1.union(members2)
        del members[num2]
        set_group_nums(num1, members2)
        for m in members1:
            assert group_nums[m] == num1
        for m in members2:
            assert group_nums[m] == num1
        for prog, group_num in group_nums.items():
            assert group_num != num2, [prog, group_num, num2]

    for pipe in pipes:
        unset_members = sorted(
            prog
            for prog in pipe
            if prog not in group_nums
        )
        if unset_members:
            new_group_num = unset_members[0]
            members[new_group_num] = set(unset_members)
            set_group_nums(new_group_num, unset_members)

        existing_groups = set(
            group_nums[prog]
            for prog in pipe
        )

        assert existing_groups
        group_num = min(existing_groups)
        existing_groups.remove(group_num)

        for other_group in existing_groups:
            merge_group(group_num, other_group)

    return members

pipes = read_pipes(sys.argv[1])
groups = group(pipes)
print(len(groups[0]))
print(len(groups))
