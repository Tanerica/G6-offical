from pyamaze import maze,agent,textLabel
from queue import PriorityQueue
from math import sqrt
def h_euclide(cell1, cell2): #heuristic cho tọa độ 2 ô
    x1, y1 = cell1
    x2, y2 = cell2
    return sqrt((x1-x2)**2+(y1-y2)**2) # Euclide
def h_mahattan(cell1, cell2): #heuristic cho tọa độ 2 ô
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1 - x2) + abs(y1 - y2)) # mahattan
def h_diagonal(cell1, cell2): #heuristic cho tọa độ 2 ô
    x1, y1 = cell1
    x2, y2 = cell2
    
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    
    # dx = abs(current_cell.x – goal.x)
    # dy = abs(current_cell.y – goal.y)
    
    h = 1*(dx+dy) + (sqrt(2)-2*1)*min(dx,dy)
    # h = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    # where D is length of each node(usually = 1) and D2 is diagonal distance between each node (usually = sqrt(2) ). 
    return h
def aStar(m, h): # m is a maze with rows and column
    start=(m.rows,m.cols) # điểm bắt đầu ở cuối maze, (1,1) là đích
    g_score={cell:float('inf') for cell in m.grid} # g là chi phí từ nút gốc đến nút hiện tại n
    g_score[start]=0 # gán chi phí cho nút đầu tiên = 0
    f_score={cell:float('inf') for cell in m.grid} # f là tổng chi phí ước lượng qua nút hiện tại tới
    f_score[start]=h(start,(1,1))   # nút đích, gán f khởi tạo bằng giá trị hàm heuristic từ nút gốc
                       # đến nút hiện tại, trong trường hợp này nút đích là (1,1)

    open=PriorityQueue()
    open.put((h(start,(1,1)),h(start,(1,1)),start))
    aPath={} # là kiểu từ điển theo key: value <=> child : parent
    while not open.empty(): # trong khi hàng đợi ko rỗng
        currCell=open.get()[2] # lấy ô nhỏ có giá trị f nhỏ nhất trong hàng đợi ưu tiên và gán curr
        if currCell==(1,1): # nếu ô đó trùng (1,1) thì break
            break
        for d in 'ESNW': # east, south, north, west
            if m.maze_map[currCell][d]==True: # tìm các hướng có thể đi được trong 4 hướng
                if d=='E':                 
                    childCell=(currCell[0],currCell[1]+1)# childcell là ô sẽ đi tiếp theo
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1) # cập nhật tọa độ mới cho childcell theo hướng
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score=g_score[currCell]+1 # vì ô mới cách ô cũ 1 đơn vị
                temp_f_score=temp_g_score+h(childCell,(1,1)) # f mới bằng g mới + h mới

                if temp_f_score < f_score[childCell]:#nếu chi phí f mới < f cũ thì cập nhật f,g mới
                    g_score[childCell]= temp_g_score
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,h(childCell,(1,1)),childCell)) # ô childCell được thêm vào hàng
                    aPath[childCell]=currCell     # đợi ưu tiên để xem xét
    fwdPath={} # để đảo ngược lại thứ tự của aPath
    cell=(1,1) # aPath là từ đích về start còn fwdPath là từ start về đích
    while cell!=start:
        fwdPath[aPath[cell]]=cell # fwdPath(child: parent)
        cell=aPath[cell] # cell = nút cha của nó
    return fwdPath

if __name__=='__main__':
    m=maze(12,14)
    m.CreateMaze()
    path=aStar(m,h=h_mahattan) # path là đường đi tìm được

    a=agent(m,footprints=True) # a xem như người chơi và để lại dấu chân tìm mê cung
    m.tracePath({a:path})
    l=textLabel(m,'A Star Path Length',len(path)+1)

    m.run()
