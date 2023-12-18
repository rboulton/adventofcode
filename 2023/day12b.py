input = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''

input = open('2023/input12.txt', 'r').read()

def runs(input):
    out = []
    l = 0
    for ch in input:
        if ch == '#':
            l += 1
        else:
            if l > 0:
                out.append(l)
                l = 0
    if l > 0:
        out.append(l)
    return out

def possible(springs, startpos, seqlen):
    '''Is it possible to have a sequences starting at startpos of length seqlen.
    
    '''
    # print("Possible {} {} {}".format(springs, startpos, seqlen))
    if startpos > 0:
        if springs[startpos - 1] == '#':
            # print('Bad start')
            return False
    if startpos + seqlen > len(springs):
        # print('Too short')
        return False
    try:
        if springs[startpos + seqlen] == '#':
            # print(springs, startpos, seqlen, 'Bad end')
            return False
    except IndexError:
        pass
    # print(springs[startpos: startpos + seqlen])
    for ch in springs[startpos: startpos + seqlen]:
        if ch == '.':
            # print('dot')
            return False
    # print(springs, startpos, seqlen, 'Ok')
    return True

def strrep(seqsofar, springs):
    result = ['.'] * len(springs)
    for seq, l in seqsofar:
        for i in range(seq, seq + l):
            result[i] = '#'
    return ''.join(result)

def variations(springs, startpos, sequences, memo, seqsofar, requiredseq):
    if len(sequences) == 0:
        if '#' in springs[startpos:]:
            return 0

        s = strrep(seqsofar, springs)
        assert runs(s) == requiredseq, s
        # print("END", s, requiredseq, springs[startpos:])

        return 1
    
    key = (startpos, tuple(sequences))
    if key in memo:
        # print("mem", strrep(seqsofar, springs), repr(key), memo[key])
        return memo[key]
    
    firstseq, tailseq = sequences[0], sequences[1:]
    result = 0
    for i in range(startpos, len(springs) + 2 - sum(sequences) - len(sequences)):
        if possible(springs, i, firstseq):
            nextpos = i + firstseq + 1
            r = variations(springs, nextpos, tailseq, memo, seqsofar + [(i, firstseq)], requiredseq)
            # if r > 0: print(startpos, i, r, firstseq, springs[startpos:])
            result += r
        if springs[i] == '#':
            break
 
    # print(springs, startpos, sequences, result)   
    memo[key] = result
    return result

counts = []
for row in input.strip().split('\n'):
    springs, sequences = row.strip().split(' ')
    sequences = [int(a) for a in sequences.split(',')]
    
    springs = '?'.join([springs] * 5)
    sequences = sequences * 5

    r = variations(springs, 0, sequences, {}, [], sequences)
    print(r)
    counts.append(r)
    
print(sum(counts))