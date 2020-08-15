import pygame
import random
import os

 
pygame.init()
screen = pygame.display.set_mode((800, 600),pygame.DOUBLEBUF)
done=False
is_blue = True
# dimensions of table
x_table, y_table, w_table, h_table=(0, 0, 800, 600)

# dimension pf player slate
initial_position_player=(350,560,100,40)

# dimension pf cpu slate
initial_position_cpu=(350,0,100,40)
#center of Table
center_table=(int(x_table+(w_table/2)),int(y_table+(h_table/2)))


Stride=6  #stride of plate  
clock = pygame.time.Clock()


"""
Generates random centers for ball
"""
"""
def random_generate_center(x_initial,x_end, y_initial,y_end):
    clock.tick(6)
    x_center=random.randint(x_initial+10,x_end-10)
    y_center=random.randint(y_initial+10,y_end-10)
    return (x_center,y_center)
"""

"""
class Paddle
    Draws Paddle
    Set Moving Conditions
    Returns Position
"""
class Paddle():
    """
    screen: Main surface or screen on which it is drawn
    initial pos:initial postion of paddle. Tuple of(x,y.width,hight)
    Stride: Distance moved per key press
    """
    def __init__(self,screen,initial_pos,Stride):
        self.x=initial_pos[0]
        self.y=initial_pos[1]
        self.w=initial_pos[2]
        self.h=initial_pos[3]
        self.screen=screen
        self.draw()
        self.Stride=Stride
        self.score=0

    """
    Draw the paddle 
    """

    def draw(self):
        pygame.draw.rect(self.screen, (255,255,0), pygame.Rect(self.x,self.y,self.w,self.h))

    
    def position(self): #Return Position
        return (self.x,self.y,self.w,self.h)


    def move_left(self): # move left
        width,_= self.screen.get_size()
        if self.x>=0:
            self.x-=self.Stride
        self.draw()
    
    def move_right(self): # move Right 
        width,_= self.screen.get_size()
        if self.x<=width-self.w:
            self.x+= self.Stride
        self.draw()



"""
Draw Ball
Set and update its Center , And Four exteme point on left and right side
Detects Collision

"""


class Ball():
    def __init__(self,screen,center,speed,player):
        self.radius=10

        self.center=center
        self.screen=screen
        self.speed_x=speed[0]
        self.speed_y=speed[1]

        self.x1=center[0]-self.radius
        self.x2=center[0]+self.radius
        self.y1=center[1]-self.radius
        self.y2=center[1]+self.radius
        self.p1=player
        
        self.collide_count=0
        self.draw()
        self.move()

    """
    def get_ball_postions(self):
    
        return Ball position:
        Center , And Four exteme point on left and right side

    """
    def get_ball_postions(self):
        return(self.center,self.x1,self.x2,self.y1,self.y2)
    
    def draw(self):
        #print( self.center)
        pygame.draw.circle(self.screen,(255,0,0),self.center,self.radius)
    
    def move(self):
        width,hieght=self.screen.get_size() # width and hieght of the scene
        
        #self.center,self.x1,self.x2,self.y1,self.y2=self.get_ball_postions()
        self.center = (self.center[0]+self.speed_x,self.center[1]+self.speed_y)
        self.x1=max(self.x1+self.speed_x,0)
        self.x2=min(self.x2+self.speed_x,width)
        self.y1=max(self.y1+self.speed_y,0)
        self.y2=min(self.y2+self.speed_y,hieght)
        # stops the ball if boundary hits the ball
        if self.hit_boundary():

            if self.which_boundary()=="x":
                #self.speed_x= (-1)*int(self.speed_x+ (self.speed_x*0.1))#increase speed by 10 
                self.speed_x= (-1)*int(self.speed_x)# reverse xdirection
            if self.which_boundary()=="y_up":
                #self.speed_y= (-1)*int(self.speed_y+ (self.speed_y*0.1))increase speed by 10 
                self.speed_y= (-1)*int(self.speed_y)
                # reverse y direction
            if self.which_boundary()=="y_down":
                #self.speed_y= (-1)*int(self.speed_y+ (self.speed_y*0.1))increase speed by 10 
                self.speed_y= (-1)*int(self.speed_y)
                # reverse y direction            
                self.p1.score=self.p1.score-1
        
        # REDUCES THE SPEED WHENEVEVR IT COLLIDES WITH PADDLE
        if self.player_collision():
            
            self.p1.score=self.p1.score+1
            if self.p1.score % 10 and self.p1.score>0:
                self.speed_y= (-1) * int(self.speed_y+ 1)
                self.speed_x=  int(self.speed_x+ 1)
                self.p1.Stride+=2
            else:
                self.speed_y= (-1) * int(self.speed_y)

        self.draw()

        if abs(self.speed_y)>10:
            self.speed_y=self.speed_y-1


    def ball_on_table(self):   # condition to check if ball is out of playground
        width,hieght=self.screen.get_size()
        if self.hit_boundary():
            return True
        if self.center[0]>=0 and self.y1+self.speed_y>0 and self.center[0]<width+self.radius and self.center[1]<hieght+self.radius:
            return True


    
    # checks condition for boundary hit 
    def hit_boundary(self):
        width,hieght=self.screen.get_size()
        if self.x1==0 or self.x2==width or self.center[1]-self.radius+self.speed_y<0 or self.y2==hieght  :
            return True
    
    
    # checks which boundary ball collides
    def which_boundary(self):
        width,hieght=self.screen.get_size()
        if self.x1==0 or self.x2==width :
            return "x"
        if self.y1==0 :
            return "y_up"
        if self.y2==hieght:
            return "y_down"

    # checks If  ball collides with player paddle
    def player_collision(self):
        x,y,w,h = self.p1.position()
        if self.center[0]<x+w and self.center[0] >x and self.center[1]+self.radius+self.speed_y>y:
             return True
   













random_speed=[-4,-5,-6,5,7,4]

speed_x=random.choice(random_speed)
speed_y=random.choice(random_speed)
speed=(speed_x,speed_y)
p1=Paddle(screen,initial_position_player,Stride)


b1=Ball(screen,center_table,speed,p1)


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if is_blue: color = (56, 128, 255)
                else: color = (255, 100, 0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_blue = not is_blue
                
   
        pressed=pygame.key.get_pressed() 
        if pressed[pygame.K_LEFT]:
            p1.move_left()

        if pressed[pygame.K_RIGHT]:
            p1.move_right()

        screen.fill((0,0,0))
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        p1.draw()
       
        #pygame.draw.rect(screen, color, pygame.Rect(x_table,y_table,w_table,h_table))

        b1.move()
        s = pygame.Surface((800,600))  # the size of your rect
        s.set_alpha(128)                # alpha level
        s.fill((255,255,0))           # this fills the entire surface
        screen.blit(s, (0,0))    # (0,0) are the top-left coordinates
        if not b1.ball_on_table():
            done= True
        print (p1.score)
        # Draw table 
        pygame.display.flip()
        clock.tick(60)