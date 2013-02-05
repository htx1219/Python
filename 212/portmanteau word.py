def natalie(words):
    "Find the best Portmanteau word formed from any two of the list of words."
    pre = set(p for word in words for p in prefixes(word))
    res = []
    for start in pre:
        for word1 in words:
            if pre_word(start, word1):
                mid = word1[len(start):]
                if mid in pre:
                    for word2 in words:
                        if pre_word(mid, word2) and word1 != word2:
                            res.append((start, mid, word2[len(mid):]))
    if res == []:
        return None
    res.sort(key = word_score, reverse = True)
    return res[0][0]+res[0][1]+res[0][2]

def word_score(p_word):
    start, mid, end = p_word 
    length = len(start+mid+end)
    score = length - abs(len(start) - length/4) - abs(len(mid) - length/2) - abs(len(end) - length/4)
    #print score, start,mid,end
    return score
    
def pre_word(pre, word):
    if len(pre) > len(word):
        return False
    for i in range(len(pre)):
        if pre[i] != word[i]:
            return False
    return True

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(1, len(word))]

def test_natalie():
    "Some test cases for natalie"
    assert natalie(['adolescent', 'scented', 'centennial', 'always', 'ado']) == 'adolescented'
    #assert natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese']) == 'eskimono'
    assert natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage']) == 'kimcheese'
    assert natalie(['circus', 'elephant', 'lion', 'opera', 'phantom']) == 'elephantom'
    assert natalie(['programmer', 'coder', 'partying', 'merrymaking']) == 'programmerrymaking'
    assert natalie(['int', 'intimate', 'hinter', 'hint', 'winter']) == 'hintimate'
    assert natalie(['morass', 'moral', 'assassination']) == 'morassassination'
    assert natalie(['entrepreneur', 'academic', 'doctor', 'neuropsychologist', 'neurotoxin', 'scientist', 'gist']) == 'entrepreneuropsychologist'
    assert natalie(['perspicacity', 'cityslicker', 'capability', 'capable']) == 'perspicacityslicker'
    assert natalie(['backfire', 'fireproof', 'backflow', 'flowchart', 'background', 'groundhog']) == 'backgroundhog'
    assert natalie(['streaker', 'nudist', 'hippie', 'protestor', 'disturbance', 'cops']) == 'nudisturbance'
    assert natalie(['night', 'day']) == None
    assert natalie(['dog', 'dogs']) == None
    assert natalie(['test']) == None
    assert natalie(['']) ==  None
    assert natalie(['ABC', '123']) == None
    assert natalie([]) == None
    return 'tests pass'


print test_natalie()
    
