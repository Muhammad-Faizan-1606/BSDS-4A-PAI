graph = {}
graph['A'] = ['B','C']
graph['B'] = ['A','D','E']
graph['C'] = ['A','F']
graph['D'] = ['B']
graph['E'] = ['B','F']
graph['F'] = ['C','E']

visited = []
queue = []

start = 'A'
goal = 'F'

queue.append(start)
visited.append(start)

print('BFS')

found = False
while len(queue) > 0:
    node = queue[0]
    queue.pop(0)
    print(node)
    
    if node == goal:
        print('found')
        found = True
        break
    
    for n in graph[node]:
        if n not in visited:
            visited.append(n)
            queue.append(n)

if found == False:
    print('not found')

print('done')

visited = []
stack = []

stack.append(start)

print('DFS')

found = False
while len(stack) > 0:
    node = stack.pop()
    
    if node not in visited:
        print(node)
        visited.append(node)
        
        if node == goal:
            print('found')
            found = True
            break
        
        for n in graph[node]:
            if n not in visited:
                stack.append(n)

if found == False:
    print('not found')
    
print('done')

grid = []
row1 = [0,0,0,0,0]
row2 = [0,1,1,0,0]
row3 = [0,0,0,0,0]
row4 = [0,1,0,1,0]
row5 = [0,0,0,0,0]
grid.append(row1)
grid.append(row2)
grid.append(row3)
grid.append(row4)
grid.append(row5)

start = (0,0)
goal = (4,4)

visited = []
queue = []

queue.append(start)
visited.append(start)

print('BFS grid')

found = False
while len(queue) > 0:
    pos = queue[0]
    queue.pop(0)
    
    print(pos)
    
    if pos == goal:
        print('reached')
        found = True
        break
    
    x = pos[0]
    y = pos[1]
    
    moves = []
    moves.append((x+1,y))
    moves.append((x-1,y))
    moves.append((x,y+1))
    moves.append((x,y-1))
    
    for m in moves:
        mx = m[0]
        my = m[1]
        
        if mx >= 0 and mx < 5 and my >= 0 and my < 5:
            if grid[mx][my] == 0:
                if m not in visited:
                    visited.append(m)
                    queue.append(m)

print('done')
