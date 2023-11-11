from pyamaze import maze,agent,COLOR,textLabel
from timeit import timeit
from queue import PriorityQueue
from math import sqrt
def h_euclide(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return sqrt((x1-x2)**2+(y1-y2)**2) #Euclide
def h_mahattan(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1 - x2) + abs(y1 - y2)) # mahattan
def aStar(m,h,start=None):
    if start is None:
        start=(m.rows,m.cols)
    open = PriorityQueue()
    open.put((h(start, m._goal), start))
    aPath = {}
    g_score = {row: float("inf") for row in m.grid}
    g_score[start] = 0
    f_score = {row: float("inf") for row in m.grid}
    f_score[start] = h(start, m._goal)
    searchPath=[start]
    while not open.empty():
        currCell = open.get()[1]
        searchPath.append(currCell)
        if currCell == m._goal:
            break        
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, m._goal)

                if temp_f_score < f_score[childCell]:   
                    aPath[childCell] = currCell
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_g_score + h(childCell, m._goal)
                    open.put((h(childCell, m._goal), childCell))
    fwdPath={}
    cell=m._goal
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return searchPath,aPath,fwdPath

myMaze=maze(16,15)
myMaze.CreateMaze()
searchPath,aPath,fwdPath=aStar(myMaze,h_mahattan)
searchPath2,aPath2,fwdPath2=aStar(myMaze,h_euclide)

l=textLabel(myMaze,'ManhatPath',len(fwdPath)+1)
l=textLabel(myMaze,'EuclidPath',len(fwdPath2)+1)
l=textLabel(myMaze,'ManhatSearch',len(searchPath)+1)
l=textLabel(myMaze,'EuclidSeach',len(searchPath2)+1)

a=agent(myMaze,footprints=True,color=COLOR.cyan,filled=True)
b=agent(myMaze,footprints=True,color=COLOR.yellow)
myMaze.tracePath({a:fwdPath},delay=100)
myMaze.tracePath({b:fwdPath2},delay=100)

t1=timeit(stmt='aStar(myMaze,h_mahattan)',number=100,globals=globals())
t2=timeit(stmt='aStar(myMaze,h_euclide)',number=100,globals=globals())

textLabel(myMaze,'Manhattan Time',t1) # hiển thị nhãn với tên Mahattan Time và thời gian t1
textLabel(myMaze,'Euclidean Time',t2)


myMaze.run()
