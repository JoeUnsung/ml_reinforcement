from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color) #공 좌표 및 색깔(oval : object 형태 타입)
                                ##  (좌측상단) (우측하단)
        self.canvas.move(self.id, 250, 100) #공을 캔버스 중앙으로 이동
        self.hit_bottom = False      

        starts = [-3,-2,-1,1,2,3]
        random.shuffle(starts)
        self.x = starts[0] ## 랜덤으로 -3~3 중의 숫자를 x에 저장
        self.y = -3
        
        canvas.configure(background = 'black') ## 배경을 블랙으로 설정
        
        self.canvas_height = canvas.winfo_height()
        self.canvas_width = canvas.winfo_width()
        
        print(self.canvas_height)
        print(self.canvas_width)
        
        self.hit_bottom = False


    def draw(self):

        self.canvas.move(self.id, self.x , self.y) ## x랑 y 만큼 이동시켜라
        pos = self.canvas.coords(self.id) ## self.id의 좌표를 찍어라
        #print(pos)
    
        if pos[1] <= 0 :
            self.y = 1 ## 아래로 내려가게 된다.
        if pos[3] >= self.canvas_height: ## 캔버스의 넓이(아래)에 우측 하단의 y좌표가 만나게 되면 다시 감소하도록
            self.hit_bottom = True
        if pos[0] <= 0: 
            self.x = 1 ## 왼쪽 벽에 닿으면 다시 증가하게 된다(오른쪽으로 이동하게 된다.)           
        if pos[2] >= self.canvas_width:
            self.x = -1 ## 오른쪽 벽에 닿으면 (canvas_width에 닿게 되면 왼쪽으로 감소하도록 한다.)
        if self.hit_paddle(pos) == True:
            self.y = -3

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]: ## 공의 x좌표계가 패들의 x좌표계에 포함되고
            if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]: ## 공의 y좌표계가 패들의 y좌표계에 포함될때
                return True ## true를 반환해라
        return False



class Paddle:
    def __init__(self,canvas,color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,100,10,fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0 # 패들을 캔버스 바깥으로 나가지 않게 하기 위해서 
        self.y = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>',self.turn_right)
        self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_down)

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0: ## 왼쪽벽에 부딪히면 멈추고
            self.x = 0
        elif pos[2] >= self.canvas_width: ## 오른쪽 벽에 부딪혀도 멈추어라
            self.x = 0
        if pos[1] <= 0: ## 맨위에 닿으면 멈추고
            self.y = 0
        elif pos[3] >= self.canvas_height: ## 맨 아래 닿아도 멈춰라
            self.y = 0

    def turn_left(self,evt): 
        self.x = -3
    def turn_right(self,evt):
        self.x = 3
    def turn_up(self,evt):
        self.y = -3
    def turn_down(self,evt):
        self.y = 3


tk = Tk()     # 1. tk 를 인스턴스화 한다.
tk.title("My Ping Pong!")  # 2. tk 객체의 title 메소드(함수)로 게임창에 제목을 부여한다.
tk.resizable(0, 0) # 3. 게임창의 크기는 가로나 세로로 변경될수 없다라고 말하는것이다.
tk.wm_attributes("-topmost", 1) #4. 다른 모든 창들 앞에 캔버스를 가진 창이 위치할것을 tkinter 에게 알려준다.
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0) ## 뒤의 파라미터 두개는 외곽선이 없도록 함

canvas.pack()       # 앞의 코드에서 전달된 폭과 높이는 매개변수에 따라 크기를 맞추라고 캔버스에에 말해준다.
tk.update()   # tkinter 에게 게임에서의 애니메이션을 위해 자신을 초기화하라고 알려주는것이다.

paddle = Paddle(canvas,'blue')
ball = Ball(canvas, paddle, 'red')  ## ball class를 인스턴스화 시킨 부분

while 1:
    ball.draw()
    paddle.draw()
    tk.update_idletasks()   # 우리가 창을 닫으라고 할때까지 계속해서 tkinter 에게 화면을 그리고 
    tk.update() 
    time.sleep(0.01)  # 100분의 1초마다 잠들어라 ! 