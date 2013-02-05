# -*- coding: utf-8 -*-
nums = open("yob1995.txt")
names = []
line = nums.readline()
while line:
    nodes = line.split(',')
    names.append((int(nodes[2]), nodes[1], nodes[0]))
    line = nums.readline()

names.sort(reverse = True)
print names[:10]
