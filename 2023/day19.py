input = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''

input = open('2023/input19.txt', 'r').read()

class Rule:
    def __init__(self, rule):
        if ':' in rule:
            cond, self.action = rule.split(':')
        else:
            self.action = rule
            self.op = True
            return
        if '<' in cond:
            self.op = '<'
        else:
            self.op = '>'
        prop, value = cond.split(self.op)
        self.prop = prop
        self.value = int(value)
        
    def apply(self, part):
        if self.op == True:
            return self.action
        if self.op == '<':
            if part.props[self.prop] < self.value:
                return self.action
        if self.op == '>':
            if part.props[self.prop] > self.value:
                return self.action
        
class Workflow:
    def __init__(self, row):
        self.name, rules = row.split('{')
        rules = rules[:-1].split(',')
        self.rules = [Rule(r) for r in rules]
        
    def apply(self, part):
        for rule in self.rules:
            action = rule.apply(part)
            if action is not None:
                return action
        
class Part:
    def __init__(self, row):
        self.props = {}
        for v in row[1:-1].split(','):
            k, v = v.split('=')
            self.props[k] = int(v)

    @property
    def rating(self):
        return sum(self.props.values())
            
    def __repr__(self):
        return repr(self.props)
        
workflows, parts = input.strip().split('\n\n')
workflows = [
    Workflow(row)
    for row in workflows.split('\n')
]
workflows = {
    f.name: f for f in workflows
}

total = 0
for row in parts.strip().split('\n'):
    part = Part(row)
    wf = 'in'
    print(part, wf, "->", end=' ')
    while True:
        wf = workflows[wf].apply(part)
        if wf == 'R':
            print("R")
            break
        if wf == 'A':
            print("A")
            total += part.rating
            break
        print(wf, "->", end=' ')
print(total)