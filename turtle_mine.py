from random import randint
import turtle
import math

wn = turtle.Screen()
wn.bgcolor("grey")
wn.title("MINE SWEEPER")
wn.setup(600,600)

#global constants
#WIDTH = 40
NUM_BOMBS = 10
ROWS = 10
COLS = 10


MODE = "GAME_ON"


class Quadrant(object):
    def __init__(self):
        self.bomb = 0
        self.label = 0
        self.flagged = 0
        self.visible = 0
       


grid = [[Quadrant() for i in range(COLS)] for j in range(ROWS)]        
#grid = [[Tale() for i in range(COLS)] for j in range(ROWS)] 

class Tale(turtle.Turtle):
    def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("square")
            self.color("")
            self.penup()
            self.speed(0)         
         
            #self.bomb = False
            grid[y][x].bomb == 0
            #self.label = None
            grid[y][x].label = 0
            #self.visible = False
            grid[y][x].flagged = 0
            #self.flagged = False
            grid[y][x].visible = 0
           

def converting_grid():
    count=0
    for y in range(10):
        for x in range(10):
            screen_x = -288+(x*24)
            screen_y = 288-(y*24)
            grid[y][x]=(screen_x, screen_y)
            print(x,y)
            print(grid[y][x])
            #count=count+1
    #print(count)

for n in range(NUM_BOMBS):

    while True:
        x = randint(0, 9)
        y = randint(0, 9)
        screen_x = -288+(x*24)
        screen_y = 288-(y*24)
        #print(screen_x, screen_y)
        if grid[y][x].bomb == 0:
           grid[y][x].bomb = 1
           #print(grid[y][x].bomb)
           break




def setup_grid():
    if MODE == "GAME_ON":
        for y in range(10):
            for x in range(10):
                
                #calculate x,y coordinates

                screen_x = -288+(x*24)
                screen_y = 288-(y*24)

                tale.goto(screen_x, screen_y)
                tale.shape("square")
                if grid[y][x].bomb == 1:
                    tale.color("red")
                    tale.stamp()
                elif grid[y][x].visible == 1:
                    tale.color("pink")
                    tale.stamp()
                elif not grid[y][x].visible == 1:
                    tale.color("white")
                    tale.stamp()
                elif grid[y][x].flagged == 1:
                    labelPoint (tale,  screen_x, screen_y, "F")
                    
                
def get_mouse_click_coor(x, y):
    print(x, y)
    return(x,y)
    
turtle.onscreenclick(get_mouse_click_coor)

def get_mouse_click_coorL(x, y):
    print(x, y)
    m =12+ math.ceil(x/24)
    n =12 - math.floor(y/24)
    search(m, n)
    return(x,y)
    
turtle.onscreenclick(get_mouse_click_coorL)

def get_mouse_click_coorR(x, y):
    print(x, y)
    m =12+ math.ceil(x/24)
    n =12 - math.floor(y/24)
    grid[n][m].flagged = 1
    return(x,y)
    
turtle.onscreenclick(get_mouse_click_coorR)


def mousePressed(x,y):
        global MODE
        (x,y) = get_mouse_click_coor(x, y)
        #(x,y) = turtle.onscreenclick(get_mouse_click_coor)

        #if mouseButton == LEFT:
        turtle.onclick(get_mouse_click_coorL(x, y), btn=1, add=None)
        '''
        m =12+ math.ceil(x/24)
        n =12 - math.floor(y/24)
        search(m, n)'''
        #elif mouseButton == RIGHT:
        turtle.onclick(get_mouse_click_coorR(x, y), btn=2, add=None)
            #flag it
        '''
        m =12+ math.ceil(x/24)
        n =12 - math.floor(y/24)
        grid[n][m].flagged = 1'''

        game_won = True
        for j in grid:
            for i in j:
                if grid[j][i].bomb and not grid[j][i].flagged:
                    game_won = 0
                    break
        if game_won:
            MODE = "WON"
            wn.title("YOU WON")

def search(x,y):
    # already visited/ bomb/ off grid/ adj bomb
    if not inbounds(x,y):
        return
    #tile = grid[y][x]
    
    #already visited
    if grid[y][x].visible == 1:
        return

    #bomb
    if grid[y][x].bomb == 1:
        return

    grid[y][x].visible = 1

    s = num_of_bombs(x,y)
    if s>0:
        screen_x = x*24
        screen_y = y*24
        labelPoint (tale,  screen_x, screen_y, s)
        #grid[y][x].label = s
        return

    for (dx, dy) in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
        search(x+dx, y+dy)



def num_of_bombs(x,y):
    s = 0
    for (dx, dy) in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
        if inbounds(x+dx, y+dy) and grid[y+dy][x+dx].bomb:
            s = s+1
        return s


def inbounds(x,y):
    if x>=0 and x< COLS and y>=0 and y< ROWS:
        return True
    return False


tale = Tale()
setup_grid()
converting_grid()
#mouse_to_index()
#get_mouse_click_coor(x, y)
mousePressed(x,y)
#search(x,y)
turtle.mainloop()
wn.tracer(0)
while True:
    wn.update()
