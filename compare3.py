from BFSDemo import BFS
from DFSDemo import DFS
from aStar import aStar, h_mahattan
from pyamaze import maze,agent,COLOR,textLabel
from timeit import timeit

m=maze(30,30)
m.CreateMaze()

searchPath,dfsPath,fwdDFSPath=DFS(m)
bSearch,bfsPath,fwdBFSPath=BFS(m)
path=aStar(m,h=h_mahattan) # path là đường đi tìm được



l=textLabel(m,'AStar',len(path)+1)
textLabel(m,'DFS',len(fwdDFSPath)+1)
textLabel(m,'BFS',len(fwdBFSPath)+1)
textLabel(m,'DFS Search',len(searchPath)+1)
textLabel(m,'BFS Search',len(bSearch)+1)

a=agent(m,footprints=True,color=COLOR.cyan,filled=True)
b=agent(m,footprints=True,color=COLOR.yellow)
c=agent(m,footprints=True) # a xem như người chơi và để lại dấu chân tìm mê cung
m.tracePath({a:fwdBFSPath},delay=70)
m.tracePath({b:fwdDFSPath},delay=70)
m.tracePath({c:path}, delay=70)

t1=timeit(stmt='DFS(m)',number=100,globals=globals())
t2=timeit(stmt='BFS(m)',number=100,globals=globals())
t3=timeit(stmt='aStar(m,h_mahattan)',number=100,globals=globals())

textLabel(m,'DFS Time',t1)
textLabel(m,'BFS Time',t2)
textLabel(m,'Astar Time',t3) # hiển thị nhãn với tên Mahattan Time và thời gian t1

m.run()
