from timeit import timeit
from BFSDemo import BFS
from DFSDemo import DFS
from aStarHeuristicComparison import aStar, h_mahattan
from dijkstraMaze import dijkstra
from pyamaze import maze, textLabel, agent, COLOR
# Assuming you have defined your maze class and algorithms (DFS, BFS, aStar) properly
m = maze(30, 30)
m.CreateMaze()

searchPath, dfsPath, fwdDFSPath = DFS(m)
bSearch, bfsPath, fwdBFSPath = BFS(m)
path = aStar(m, h=h_mahattan)
dijPath,_,r= dijkstra(m)  # Assuming you have a dijkstra function
# Display path lengths
textLabel(m, 'AStar', len(path) + 1)
textLabel(m, 'DFS', len(fwdDFSPath) + 1)
textLabel(m, 'BFS', len(fwdBFSPath) + 1)
textLabel(m, 'Dijkstra', len(dijPath) + 1)
textLabel(m, 'DFS Search', len(searchPath) + 1)
textLabel(m, 'BFS Search', len(bSearch) + 1)
# textLabel(m, 'AStar Search', len(AsearchPath) + 1)
textLabel(m, 'Dijkstra Search', r )
# Create agents
a = agent(m, footprints=True, color=COLOR.green, filled=True)
b = agent(m, footprints=True, color=COLOR.yellow)
c = agent(m, footprints=True, color=COLOR.red)
d = agent(m, footprints=True, color=COLOR.cyan)

# Trace paths
m.tracePath({a: fwdBFSPath}, delay=40)
m.tracePath({b: fwdDFSPath}, delay=40)
m.tracePath({c: path}, delay=40)
m.tracePath({d: dijPath}, delay=40)

# Measure execution time
t1 = timeit(stmt='DFS(m)', number=100, globals=globals())
t2 = timeit(stmt='BFS(m)', number=100, globals=globals())
t3 = timeit(stmt='aStar(m, h_mahattan)', number=100, globals=globals())
t4 = timeit(stmt='dijkstra(m)', number=100, globals=globals())

# Display execution times
textLabel(m, 'DFS Time', t1)
textLabel(m, 'BFS Time', t2)
textLabel(m, 'Astar Time', t3)
textLabel(m, 'Dijkstra Time', t4)

# Run the maze
m.run()




# black=('black','dim gray')
#     red=('red3','tomato')
#     cyan=('cyan4','cyan4')
#     green=('green4','pale green')
#     blue=('DeepSkyBlue4','DeepSkyBlue2')
#     yellow=('yellow2','yellow2')