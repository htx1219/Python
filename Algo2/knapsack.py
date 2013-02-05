s = 100
text = open("knapsack2.txt")
line = text.readline()
line = line.split()
w = int(int(line[0])/s)
num = int(line[1])
items = []
line = text.readline()
j = 0
while line:
    k = [int(i) for i in line.split()]
    items.append([k[0], (k[1]+s-1)/s])
    j += 1
    line = text.readline()

print len(items)

A = [[0]*(w+1) for i in range(0, num+1)]
for i in range(1, num+1):
    for j in range(0, w+1):
        item = items[i-1]
        if j >= item[1]:
            A[i][j] = max(A[i-1][j], A[i-1][j-item[1]] + item[0])
        else:
            A[i][j] = A[i-1][j]

print A[num][w]
