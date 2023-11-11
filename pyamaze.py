import random
from tkinter import *
from enum import Enum
from collections import deque

class COLOR(Enum): 
    dark=('gray11','white') # theme color #values represent the Canvas color and the Maze Line color respectively.
    #color for agent the first value is the color of the Agent and the second is the color of its footprint
    black=('black','dim gray')
    red=('red3','tomato')
    cyan=('cyan4','cyan4')
    green=('green4','pale green')
    blue=('DeepSkyBlue4','DeepSkyBlue2')
    yellow=('yellow2','yellow2')

class agent: #The agents can be placed on the maze to indcate the cell selected in Maze
    def __init__(self,parentMaze,x=None,y=None,goal=None,filled=False,footprints=False,color:COLOR=COLOR.blue):
        # x,y-->  vị trí của agent, mặc định là góc dưới cùng bên trái maze
        # goal-->     Mặc định là (1,1)
        # footprints->When agent move to other cell, its footprints on the previous cell can be placed by making this True
        # color-->    Color of the agent và footprints của nó
        # position--> Tọa độ hiện tại của agent (x,y)
        # _body-->    Tracks the body of the agent (the previous positions of it)
        self._parentMaze=parentMaze #mê cung mà agent đang đứng
        self.color=color # chọn màu cho agent
        self.filled=filled # điều chỉnh kích thước tác tử true = to, false = bé
        if x is None:x=parentMaze.rows # nếu không khởi tạo vị trí xuất phát của agent 
        if y is None:y=parentMaze.cols # thì mặc định là [rows, cols] --> điểm cuối của maze
        self.x=x
        self.y=y
        self.footprints=footprints
        self._parentMaze._agents.append(self) # thêm agent vào danh sách agent của mê cung
        if goal==None: self.goal=self._parentMaze._goal # nếu goal = None thì sẽ chọn goal mặc định (1,1)
        else:          self.goal=goal
        self._body=[] # theo dõi các vị trí trước đó của mê cung
        self.position=(self.x,self.y) # cập nhật vị trí xuất phát của agent
        
    @property # giống getter trong java
    def x(self): return self._x
    @x.setter # giống setter trong java
    def x(self,newX): self._x=newX
    @property
    def y(self): return self._y
    @y.setter
    def y(self,newY):
        self._y=newY
        w=self._parentMaze._cell_width # w là kíc thước của 1 cell
        x=self.x*w-w+self._parentMaze._LabWidth 
        y=self.y*w-w+self._parentMaze._LabWidth
        if self.filled:
                self._coord=(y, x,y + w, x + w) # tạo hình vuông to
        else:   # tạo hình vuông nhỏ với kích thước được thu gọn so với hình vuông to
                self._coord=(y + w/2.5, x + w/2.5,y + w/2.5 +w/4, x + w/2.5 +w/4) 
        #coord là tọa độ gồm 4 tham số xác định 1 vị trí trên canvas tkinter
        self._head=self._parentMaze._canvas.create_rectangle(*self._coord,fill=self.color.value[0],outline='')#stipple='gray75'
        # tạo ra 1 hình vuông với tọa độ cooord --> là tác tử được vẽ lên mê cung nhờ canvas
    
        self._parentMaze._redrawCell(self.x,self.y,theme=self._parentMaze.theme)
    @property
    def position(self):
        return (self.x,self.y)
    @position.setter
    def position(self,newpos):
        self.x=newpos[0]
        self.y=newpos[1]
        self._position=newpos
    
class textLabel: # tạo các nhãn
    def __init__(self,parentMaze,title,value):
        self.title=title
        self._value=value
        self._parentMaze=parentMaze # parentmaze-->   The maze on which Label will be displayed.
        self._var=None
        self.drawLabel()
    @property
    def value(self): return self._value
    @value.setter
    def value(self,v): # set lại value khi thay đổi
        self._value=v
        self._var.set(f'{self.title} : {v}')
    def drawLabel(self):
        self._var = StringVar()
        self.lab = Label(self._parentMaze._canvas, textvariable=self._var, bg="white", fg="black",font=('Helvetica bold',12),relief=RIDGE)
        self._var.set(f'{self.title} : {self.value}') # nhãn sẽ có cấu trúc title - value
        self.lab.pack(expand = True,side=LEFT,anchor=NW) #exphand = true-> cho phép mở rộng ko gian trống
        #anchor = NW -> nhãn nằm ở góc tây bắc North West
        #side = LEFT --> nhãn nằm ở bên trái --> nhãn nằm ở góc trên bên trái

class maze: #This is the main class to create maze.
    def __init__(self,rows=10,cols=10): #Need to pass just the two arguments. The rest will be assigned automatically
        self.rows=rows #rows--> No. of rows of the maze
        self.cols=cols #cols--> No. of columns of the maze
        self.maze_map={} #maze_map--> Will be set to a Dicationary
        # Keys will be cells and values will be another dictionary with keys=['E','W','N','S'] for
        # East West North South and values will be 0 or 1. 0 means direction(EWNS) is blocked, 1 means direction is open.
        self.grid=[] #grid--> A list of all cells
        self.path={} # Shortest path from start(bottom right) to goal(by default top left).It is a dictionary
        self._cell_width=50  #is cell width calculated automatically
        self._win=None # tạo 1 giao diện cửa sổ window để đặt mê cung vào
        self._canvas=None # tạo 1 đối tượng canvas để vẽ mê cung
        self._agents=[] #_agents-->  A list of aganets on the maze
        self.markCells=[] #Will be used to mark some particular cell during path trace by the agent
    @property
    def grid(self): return self._grid
    @grid.setter        
    def grid(self,n): # tạo grid và set tất cả các cell đều có tường bao quanh
        self._grid=[]
        y=0
        for n in range(self.cols): # mục đích để thiết lập tọa độ các ô là (1,1) -->(row, col)
            x = 1
            y = 1+y
            for m in range(self.rows):
                self.grid.append((x,y))
                self.maze_map[x,y]={'E':0,'W':0,'N':0,'S':0}
                x = x + 1 
    def _Open_East(self,x, y): # xóa tưởng ở phía East
        self.maze_map[x,y]['E']=1 # mở tường hướng E ở mê cung đang xét
        if y+1<=self.cols: # nếu bên phải đang còn ô 
            self.maze_map[x,y+1]['W']=1 # set phía W của ô đó là 1
    def _Open_West(self,x, y):
        self.maze_map[x,y]['W']=1
        if y-1>0:
            self.maze_map[x,y-1]['E']=1
    def _Open_North(self,x, y):
        self.maze_map[x,y]['N']=1
        if x-1>0:
            self.maze_map[x-1,y]['S']=1
    def _Open_South(self,x, y):
        self.maze_map[x,y]['S']=1
        if x+1<=self.rows:
            self.maze_map[x+1,y]['N']=1
    
    def CreateMaze(self,x=1,y=1,theme:COLOR=COLOR.dark):#important function to create a Random Maze
        _stack=[]
        _closed=[] # lưu những ô đã thăm
        self.theme=theme
        self._goal=(x,y) # mặc định là (1,1)
        # generate a randomly maze 
        _stack.append((x,y))
        _closed.append((x,y))
        while len(_stack) > 0:
            cell = []
            if(x , y +1) not in _closed and (x , y+1) in self.grid:     cell.append("E")
            if (x , y-1) not in _closed and (x , y-1) in self.grid:     cell.append("W")
            if (x+1, y ) not in _closed and (x+1 , y ) in self.grid:    cell.append("S")
            if (x-1, y ) not in _closed and (x-1 , y) in self.grid:     cell.append("N") 
            if len(cell) > 0:    
                current_cell = (random.choice(cell))
                if current_cell == "E":
                        self._Open_East(x,y)
                        self.path[x, y+1] = x, y
                        y = y + 1
                        _closed.append((x, y))
                        _stack.append((x, y))
                elif current_cell == "W":
                        self._Open_West(x, y)
                        self.path[x , y-1] = x, y
                        y = y - 1
                        _closed.append((x, y))
                        _stack.append((x, y))
                elif current_cell == "N":
                        self._Open_North(x, y)
                        self.path[(x-1 , y)] = x, y
                        x = x - 1
                        _closed.append((x, y))
                        _stack.append((x, y))
                elif current_cell == "S":
                        self._Open_South(x, y)
                        self.path[(x+1 , y)] = x, y
                        x = x + 1
                        _closed.append((x, y))
                        _stack.append((x, y))

            else:
                x, y = _stack.pop()
        ## Multiple Path Loops
        midx = self.rows // 2
        choices = [1] * 9 + [0] * 1
        for mid_cell_y in range(2,self.cols-2):
            t = random.choice(choices)
            if t :
               self._Open_North(midx, mid_cell_y)
               self._Open_South(midx, mid_cell_y)
               self._Open_West(midx-1, mid_cell_y)
               self._Open_East(midx+1, mid_cell_y)
        midy = self.cols // 2
        for mid_cell_x in range(2,self.rows-2):
            t = random.choice(choices)
            if t :
               self._Open_North(mid_cell_x, midy)
               self._Open_South(mid_cell_x, midy)
               self._Open_West(mid_cell_x, midy-1)
               self._Open_East(mid_cell_x, midy+1)
        self._drawMaze(self.theme)
        agent(self,*self._goal,filled=True,color=COLOR.green)

    def _drawMaze(self,theme): # tạo mê cung bằng tkinter
        self._LabWidth=26 # Space from the top for Labels, width of Label
        self._win=Tk()
        self._win.state('zoomed') # mở rộng cửa sổ để chiếm toàn bộ màn hình
        self._win.title('G6 INTRO AI') # tiêu đề của cửa sổ
        scr_width=self._win.winfo_screenwidth() # width của cửa sổ window mặc định - tùy máy tính (14 inch, 15 inch)
        scr_height=self._win.winfo_screenheight() # height của cửa sổ window hiển thị
        self._win.geometry(f"{scr_width}x{scr_height}+0+0") # tạo 1 window với kích thước width-height
        self._canvas = Canvas(width=scr_width, height=scr_height, bg=theme.value[0]) # 0,0 is top left corner
        self._canvas.pack(expand=YES, fill=BOTH)
        # Some calculations for calculating the width of the maze cell
        k=3.25
        if self.rows>=95 and self.cols>=95:   k=0
        elif self.rows>=80 and self.cols>=80: k=1
        elif self.rows>=70 and self.cols>=70: k=1.5
        elif self.rows>=50 and self.cols>=50: k=2
        elif self.rows>=35 and self.cols>=35: k=2.5
        elif self.rows>=22 and self.cols>=22: k=3
        self._cell_width=round(min(((scr_height-self.rows-k*self._LabWidth)/(self.rows)),((scr_width-self.cols-k*self._LabWidth)/(self.cols)),90),3)
        # min cell_width >= 90 và làm tròn đến 3 chữ số phần thập phân
        # Creating Maze lines
        if self._win is not None:
            if self.grid is not None:
                for cell in self.grid:
                    x,y=cell
                    w=self._cell_width #x,y,w --> tính tọa độ của tường -line trong create_line
                    x=x*w-w+self._LabWidth
                    y=y*w-w+self._LabWidth
                    if self.maze_map[cell]['E']==False:
                        l=self._canvas.create_line(y + w, x, y + w, x + w,width=2,fill=theme.value[1],tag='line')
                    if self.maze_map[cell]['W']==False:
                        l=self._canvas.create_line(y, x, y, x + w,width=2,fill=theme.value[1],tag='line')
                    if self.maze_map[cell]['N']==False:
                        l=self._canvas.create_line(y, x, y + w, x,width=2,fill=theme.value[1],tag='line')
                    if self.maze_map[cell]['S']==False:
                        l=self._canvas.create_line(y, x + w, y + w, x + w,width=2,fill=theme.value[1],tag='line')

    def _redrawCell(self,x,y,theme):
        # To redraw a cell. With Full sized square agent, it can overlap with maze lines
        # So the cell is redrawn so that cell lines are on top
        w=self._cell_width
        cell=(x,y)
        x=x*w-w+self._LabWidth
        y=y*w-w+self._LabWidth
        if self.maze_map[cell]['E']==False:
            self._canvas.create_line(y + w, x, y + w, x + w,width=2,fill=theme.value[1])
        if self.maze_map[cell]['W']==False:
            self._canvas.create_line(y, x, y, x + w,width=2,fill=theme.value[1])
        if self.maze_map[cell]['N']==False:
            self._canvas.create_line(y, x, y + w, x,width=2,fill=theme.value[1])
        if self.maze_map[cell]['S']==False:
            self._canvas.create_line(y, x + w, y + w, x + w,width=2,fill=theme.value[1])

    _tracePathList=[]
    def _tracePathSingle(self,a,p,kill,showMarked,delay):#tracePath method for tracing a path by agent.
        def killAgent(a): #if the agent should be killed after it reaches the Goal or completes the path
            for i in range(len(a._body)):
                self._canvas.delete(a._body[i])
            self._canvas.delete(a._head) 
        w=self._cell_width
        if((a.x,a.y) in self.markCells and showMarked):
            w=self._cell_width
            x=a.x*w-w+self._LabWidth
            y=a.y*w-w+self._LabWidth
            self._canvas.create_oval(y + w/2.5+w/20, x + w/2.5+w/20,y + w/2.5 +w/4-w/20, x + w/2.5 +w/4-w/20,fill='red',outline='red',tag='ov')
            self._canvas.tag_raise('ov')
       
        if (a.x,a.y)==(a.goal):
            del maze._tracePathList[0][0][a]
            if maze._tracePathList[0][0]=={}:
                del maze._tracePathList[0]
                if len(maze._tracePathList)>0:
                    self.tracePath(maze._tracePathList[0][0],kill=maze._tracePathList[0][1],delay=maze._tracePathList[0][2])
            if kill:
                self._win.after(300, killAgent,a)         
            return
        # If path is provided as Dictionary
        if(type(p)==dict):
            if(len(p)==0):
                del maze._tracePathList[0][0][a]
                return
            a.x,a.y=p[(a.x,a.y)]
        # If path is provided as String
        if (type(p)==str):
            if(len(p)==0):
                del maze._tracePathList[0][0][a]
                if maze._tracePathList[0][0]=={}:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList)>0:
                        self.tracePath(maze._tracePathList[0][0],kill=maze._tracePathList[0][1],delay=maze._tracePathList[0][2])
                if kill:
                    self._win.after(300, killAgent,a)         
                return
            # tính toán lại tọa độ của agent khi di chuyển   
            move=p[0]
            if move=='E':
                if a.y+1<=self.cols: a.y+=1
            elif move=='W':
                if a.y-1>0: a.y-=1
            elif move=='N':
                if a.x-1>0: a.x-=1
            elif move=='S':
                if a.x+1<=self.rows: a.x+=1
            p=p[1:] # cho agent trỏ đến vị trí tiếp theo
        # If path is provided as List
        if (type(p)==list):
            if(len(p)==0):
                del maze._tracePathList[0][0][a]
                if maze._tracePathList[0][0]=={}:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList)>0:
                        self.tracePath(maze._tracePathList[0][0],kill=maze._tracePathList[0][1],delay=maze._tracePathList[0][2])
                if kill:                    
                    self._win.after(300, killAgent,a)  
                return
            a.x,a.y=p[0]
            del p[0]
        self._win.after(delay, self._tracePathSingle,a,p,kill,showMarked,delay)    

    def tracePath(self,d,kill=False,delay=200,showMarked=False):
        #A method to trace path by agent you can provide more than one agent/path details
        self._tracePathList.append((d,kill,delay))
        if maze._tracePathList[0][0]==d: 
            for a,p in d.items():
                if a.goal!=(a.x,a.y) and len(p)!=0:
                    self._tracePathSingle(a,p,kill,showMarked,delay)
    def run(self):
        self._win.mainloop() # hàm trong tkinter để run app
