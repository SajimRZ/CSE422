# %%
#  TASK 1

import heapq
# get row, coloum from input
in_file = open('input.txt')
row, coloum = list(map(int,in_file.readline().split(' ')))

#get start and end location
start = list(map(int,in_file.readline().split(' ')))
goal = list(map(int,in_file.readline().split(' ')))

#make the grid 
maze = []
for i in range(row):
    temp = []
    cols = in_file.readline() 
    for j in cols:
        if j != '\n':
            temp.append(j)
    maze.append(temp) # (row number, coloum number) = (y,x)
# calculate h(n)
def manhat_dis(start,end):
    hn = abs( start[1] - end[1] ) + abs( start[0] - end[0] )
    return hn

# Blank row x coloum matrix
cell_details = []
for i in range(row):
    cell_details.append([])
    for j in range(coloum):
        cell_details[i].append([])

#start node
start_hn = manhat_dis(start,goal)
cell_details[start[0]][start[1]] = [start_hn, start_hn, 0, start, None, ''] #[f(n), h(n), g(n), cord, parent, direction]
open_list = [] # priority queue
heapq.heappush(open_list, cell_details[start[0]][start[1]] ) 

directions = {'U':[-1,0], 'D':[1,0], 'L':[0,-1], 'R':[0,1]}
path = ''

#A-star algorithm runs from here
while open_list:
    fn, hn, gn, cur_cell, parent, move = heapq.heappop(open_list)

    if cur_cell == goal:
        parent = goal
        while parent != None:
            path += cell_details[parent[0]][parent[1]][5]  
            parent = cell_details[parent[0]][parent[1]][4]  

        print(len(path))
        print(path[::-1])
        break
    
    #get possible moves to take
    neighbours = []
    for i in directions.keys():
        ny = cur_cell[0] + directions[i][0]
        nx = cur_cell[1] + directions[i][1]
        # check if the position is valid
        if nx >= 0 and nx < coloum and ny >= 0 and ny < row and maze[ny][nx] != '#':
            neighbours.append([gn+1+manhat_dis([ny,nx],goal), manhat_dis([ny,nx],goal), gn+1, [ny,nx], cur_cell, i])
    
    #take the neighbours and compare them to existing cell details
    for i in neighbours:
        new_fn, new_hn, new_gn, new_cell, new_parent, new_move = i #neighbour details
        
        prev_info = cell_details[new_cell[0]][new_cell[1]] #existing cell details
        if prev_info == [] or prev_info[0] > new_fn:
            cell_details[new_cell[0]][new_cell[1]] = [new_fn, new_hn, new_gn, new_cell, new_parent, new_move] #overwriting existing data with better option
            heapq.heappush(open_list, cell_details[new_cell[0]][new_cell[1]]) #re-insert into queue

if path == '':
    print(-1)


    





# %%
# Task 2
import heapq
#unpack inputs
in_file = open('input2.txt')
v, e = list(map(int, in_file.readline().split(' ')))
start, end = list(map(int, in_file.readline().split(' ')))

#track h(n)
heurstics_list = {}
for i in range(v):
    n, hn = list(map(int, in_file.readline().split(' ')))
    heurstics_list[n] = hn

#make adjList
graph = {}
for i in range(e):
    v1, v2 = list(map(int, in_file.readline().split(' ')))
    if v1 in graph.keys():
        graph[v1].append(v2)
    else:
        graph[v1] = []
        graph[v1].append(v2)
    
    if v2 in graph.keys():
        graph[v2].append(v1)
    else:
        graph[v2] = []
        graph[v2].append(v1)

checked = {}
Q = []
heapq.heappush(Q,[0,end])
inadmiss = []

while Q:
    w1, v = heapq.heappop(Q)
    if v in checked.keys(): 
        continue
    else:
        checked[v] = w1 
        if w1 < heurstics_list[v]:
            inadmiss.append(v)

        for u in graph[v]:
            heapq.heappush(Q, [w1+1,u] )

if len(inadmiss) > 0:
    print(0)
    st = ''
    inadmiss.sort()
    for i in inadmiss:
        st += str(i) + ', '
    print(f'Here nodes {st[:len(st)-2]} are in admissible.')
else:
    print(1)





# %%
