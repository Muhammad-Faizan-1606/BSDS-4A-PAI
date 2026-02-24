n = 8

board = []
for i in range(n):
    row = []
    for j in range(n):
        row.append(0)
    board.append(row)

def safe(b,r,c):
    for i in range(c):
        if b[r][i] == 1:
            return False
    
    i = r
    j = c
    while i >= 0 and j >= 0:
        if b[i][j] == 1:
            return False
        i = i-1
        j = j-1
    
    i = r
    j = c
    while i < n and j >= 0:
        if b[i][j] == 1:
            return False
        i = i+1
        j = j-1
    
    return True

def solve_nqueens(b,col):
    if col >= n:
        return True
    
    for i in range(n):
        if safe(b,i,col) == True:
            b[i][col] = 1
            
            if solve_nqueens(b,col+1) == True:
                return True
            
            b[i][col] = 0
    
    return False

if solve_nqueens(board,0) == True:
    print('solution')
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                print('Q',end=' ')
            else:
                print('.',end=' ')
        print()
else:
    print('no solution')

import random

n = 8
queens = []
for i in range(n):
    queens.append(random.randint(0,n-1))

def count_conflicts(q):
    c = 0
    for i in range(len(q)):
        for j in range(i+1,len(q)):
            if q[i] == q[j]:
                c = c+1
            
            if abs(q[i]-q[j]) == abs(i-j):
                c = c+1
    return c

print('hill climb')
print(count_conflicts(queens))

max_steps = 1000
step = 0

while step < max_steps:
    current = count_conflicts(queens)
    
    if current == 0:
        print('solved')
        break
    
    best = current
    best_q = []
    for x in queens:
        best_q.append(x)
    
    for col in range(n):
        for row in range(n):
            temp = []
            for x in queens:
                temp.append(x)
            
            temp[col] = row
            
            conf = count_conflicts(temp)
            
            if conf < best:
                best = conf
                best_q = []
                for x in temp:
                    best_q.append(x)
    
    if best >= current:
        queens = []
        for i in range(n):
            queens.append(random.randint(0,n-1))
    else:
        queens = best_q
    
    step = step+1

print(count_conflicts(queens))
print(queens)
print('done')
