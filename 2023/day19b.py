from numpy import kaiser


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

input = '''in{a<2006:A,R}

{x=787,m=2655,a=1222,s=2876}
'''

input = open('2023/input19.txt', 'r').read()

class Range:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        
    def len(self):
        assert self.max >= self.min
        return 1 + self.max - self.min
    
    def setmax(self, v):
        if self.max > v:
            self.max = v
        
    def setmin(self, v):
        if self.min < v:
            self.min = v
            
    def __repr__(self):
        return '{}..{}'.format(self.min, self.max)
            
class Selection:
    def __init__(self, rules=None):
        if rules is None:
            self.rules = ()
        else:
            self.rules = rules
        
    def split(self, rule):
        if rule.op == True:
            return self, rule.action, None
        if rule.op == '<':
            tail1 = (rule.prop, '<', rule.value)
            tail2 = (rule.prop, '>', rule.value - 1)
        else:
            assert rule.op == '>'
            tail1 = (rule.prop, '>', rule.value)
            tail2 = (rule.prop, '<', rule.value + 1)
        r1 = self.rules + (tail1,)
        r2 = self.rules + (tail2,)
        return (Selection(r1), rule.action, Selection(r2))
    
    def size(self):
        rs = dict(
            x=Range(1, 4000),
            m=Range(1, 4000),
            a=Range(1, 4000),
            s=Range(1, 4000),
        )
        for r in self.rules:
            if r[1] == '<':
               rs[r[0]].setmax(r[2] - 1)
            if r[1] == '>':
               rs[r[0]].setmin(r[2] + 1)
        r = 1
        for v in rs.values():
            r *= v.len()
        return r
    
    def __repr__(self):
        rules = ','.join(
            ''.join(map(lambda x: str(x), rule)) for rule in self.rules
        )
        return 'Sel[{}, {}]'.format(rules, self.size())

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
        
class Workflow:
    def __init__(self, row):
        self.name, rules = row.split('{')
        rules = rules[:-1].split(',')
        self.rules = [Rule(r) for r in rules]
        
       
workflows, _ = input.strip().split('\n\n')
workflows = [
    Workflow(row)
    for row in workflows.split('\n')
]
workflows = {
    f.name: f for f in workflows
}

def count(selection, wf):
    accepted = 0
    rejected = 0
    w = workflows[wf]
    for rule in w.rules:
        s1, act, s2 = selection.split(rule)
        print(s1, act, s2)
        if act == 'R':
            print("Rejecting {}".format(s1))
            rejected += s1.size()
        elif act == 'A':
            print("Accepting {}".format(s1))
            accepted += s1.size()
        else:
            a, r = count(s1, act)
            accepted += a
            rejected += r
        selection = s2
    assert selection is None
    return accepted, rejected
        
 
a, r = count(Selection(), 'in')
print(a+r)
print(a)