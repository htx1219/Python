jobs = open("jobs.txt")
l_j1 = []
l_j2 = []
line = jobs.readline()
line = jobs.readline()
while line:
    job = line.split()
    job = [int(i) for i in job]
    l_j1.append((job[0] - job[1], job[0], (job[0], job[1])))
    l_j2.append((job[0]*1.0/job[1], (job[0], job[1])))
    line = jobs.readline()

print len(l_j1)
print len(l_j2)

l_j1.sort(reverse = True)
l_j2.sort(reverse = True)

def compute_sw(l_j):
    t = 0
    s = 0
    for j in l_j:
        t += j[-1][1]
        s += t*j[-1][0]
    return s

print compute_sw(l_j1)
print compute_sw(l_j2)
