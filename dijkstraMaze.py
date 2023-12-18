from pyamaze import maze,agent,COLOR,textLabel
def dijkstra(m,*h,start=None): #*h là 1 list <=> truyền vào 1 số lượng biến không cố định
    if start is None:
        start=(m.rows,m.cols)

    hurdles=[(i.position,i.cost) for i in h] # some obtackes - chướng ngại vật

    unvisited={n:float('inf') for n in m.grid} # khởi tạo chi phí tất cả các ô chưa thăm = vô cực
    unvisited[start]=0 # lưu từ điển chi phí các ô
    visited={} # các ô đã thăm
    revPath={} # truy xuất đường đi ngược từ goal -> start
    leng_path = 0
    while unvisited:
        currCell=min(unvisited,key=unvisited.get) # chọn ô trong unvisited có phi phí nhỏ nhất để xét
        visited[currCell]=unvisited[currCell]
        if currCell==m._goal:
            break
        for d in 'EWNS':
            if m.maze_map[currCell][d]==True: # check lần lượt các hướng đi có thể
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                    leng_path += 1
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                    leng_path += 1
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                    leng_path += 1
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1]) 
                    leng_path += 1
                if childCell in visited: # nếu đã thăm thì xét đến hướng khác
                    leng_path -= 1
                    continue # childcell là ứng cử viên cho vị trí tiếp theo
                tempDist= unvisited[currCell]+1 # nếu tìm được 1 ô chưa thăm, 
                for hurdle in hurdles: # check lần lượt các chướng ngại vật
                    if hurdle[0]==currCell: # nếu vị trí của chướng ngại vật hi == ô hiện tại đang xét
                        tempDist+=hurdle[1]

                if tempDist < unvisited[childCell]:
                    unvisited[childCell]=tempDist
                    revPath[childCell]=currCell
        unvisited.pop(currCell)
    
    fwdPath={}
    cell=m._goal
    while cell!=start:
        fwdPath[revPath[cell]]=cell
        cell=revPath[cell]
    
    return fwdPath,visited[m._goal], m.rows*m.cols - len(unvisited)
            



if __name__=='__main__':
    myMaze=maze(20,20)
    myMaze.CreateMaze(1,4)

    h1=agent(myMaze,4,4,color=COLOR.red)
    h2=agent(myMaze,4,6,color=COLOR.red)
    h3=agent(myMaze,4,1,color=COLOR.red)
    h4=agent(myMaze,4,2,color=COLOR.red)
    h5=agent(myMaze,4,3,color=COLOR.red)
    h6=agent(myMaze,7,7,color=COLOR.red)
    h7=agent(myMaze,6,6,color=COLOR.red)
    h8=agent(myMaze,4,3,color=COLOR.red)
    h9=agent(myMaze,8,8,color=COLOR.red)
    h10=agent(myMaze,8,11,color=COLOR.red)
    h11=agent(myMaze,10,6,color=COLOR.red)
    h12=agent(myMaze,5,8,color=COLOR.red)
    h13=agent(myMaze,4,5,color=COLOR.red)
    h14=agent(myMaze,4,6,color=COLOR.red)
    h15=agent(myMaze,7,3,color=COLOR.red)
    h16=agent(myMaze,13,11,color=COLOR.red)
    h17=agent(myMaze,13,15,color=COLOR.red)
    h18=agent(myMaze,15,8,color=COLOR.red)
    h19=agent(myMaze,14,5,color=COLOR.red)
    h20=agent(myMaze,4,16,color=COLOR.red)
    h21=agent(myMaze,17,13,color=COLOR.red)
    h22=agent(myMaze,16,18,color=COLOR.red)
    h23=agent(myMaze,14,15,color=COLOR.red)
    h24=agent(myMaze,14,16,color=COLOR.red)
    h25=agent(myMaze,7,13,color=COLOR.red)
    h1.cost=10
    h2.cost=102
    h3.cost=13
    h4.cost=130
    h5.cost=140
    h6.cost=190
    h7.cost=101
    h8.cost=98
    h9.cost=180
    h10.cost=110
    h11.cost=20
    h12.cost=120
    h13.cost=190
    h14.cost=10
    h15.cost=100
    h16.cost=20
    h17.cost=30
    h18.cost=40
    h19.cost=50
    h20.cost=60
    h21.cost=70
    h22.cost=60
    h23.cost=70
    h24.cost=60
    h25.cost=70
    # path,c=dijstra(myMaze,h1,h2,h2,h3,h4,h5)
    path,c, leng_dijstra=dijkstra(myMaze,h1,h2,h3,h4,h5)
    textLabel(myMaze,'Total Cost',c)
    textLabel(myMaze, 'Dijstra search', leng_dijstra)

    # a=agent(myMaze,color=COLOR.cyan,filled=True,footprints=True)
    a=agent(myMaze,color=COLOR.cyan,filled=True,footprints=True)
    myMaze.tracePath({a:path}, delay=80)


    myMaze.run()