colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

row = len(colors)
col = len(colors[0])
p = [[1.0/(row*col)]*col]*row

def sense_2D(p, Z):
    q = [[0]*len(i) for i in p]
    for i in range(row):
        for j in range(col):
            hit = (Z == colors[i][j])
            q[i][j] = (p[i][j] * (hit * sensor_right + (1-hit) * (1-sensor_right)))
    s = sum([sum(i) for i in q])
    for i in range(row):
        for j in range(col):
            q[i][j] = q[i][j] / s
    return q

def move_2D(p, U):
    q = [[0]*len(i) for i in p]
    for i in range(row):
        for j in range(col):
            q[(i+U[0]) % row][(j+U[1]) % col] = p[i][j]*p_move + p[(i+U[0]) % row][(j+U[1]) % col]*(1-p_move)
    return q

##p = sense_2D(p, "green")
##show(p)
##show(move_2D(p, [1,0]))
##show(move_2D(p, [0,1]))

for k in range(len(measurements)):
    p = move_2D(p, motions[k])
    p = sense_2D(p, measurements[k])
    


#Your probability array must be printed 
#with the following code.

show(p)

colors = [['green','green','green'],
          ['green','red','red'],
          ['green','green','green']]
measurements = ['red','red']
motions = [[0,0], [0,1]]
sensor_right = 0.8
p_move = 1.0

row = len(colors)
col = len(colors[0])
p = [[1.0/(row*col)]*col]*row
for k in range(len(measurements)):
    p = move_2D(p, motions[k])
    p = sense_2D(p, measurements[k])

show(p)
