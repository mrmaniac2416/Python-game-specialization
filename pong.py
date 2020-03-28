import simplegui 
import random


WIDTH=1000
HEIGHT=700
PADDLE_WIDTH=15
PADDLE_HEIGHT=70
BALL_RADIUS=15
INTIAL_BALL_VELOCITY=2
PADDLE_VELOCITY=5
VELOCITY_INCREMENT_FACTOR=1.25
ball_position=[]
ball_velocity=[]
player1_score=0
player2_score=0


paddle1_position=[0,HEIGHT/2]
paddle1_velocity=[0,0]

paddle2_position=[WIDTH,HEIGHT/2]
paddle2_velocity=[0,0]








def draw(canvas):
    global player1_score,player2_score
    canvas.draw_line([PADDLE_WIDTH,0],[PADDLE_WIDTH,HEIGHT],2,'Grey') #Gutter1
    canvas.draw_line([WIDTH-PADDLE_WIDTH,0],[WIDTH-PADDLE_WIDTH,HEIGHT],2,'Grey')      #Gutter2
    canvas.draw_line([WIDTH/2,0],[WIDTH/2,HEIGHT],2,'Grey') #middle line 
    
    
    #handling the paddle on the edges 
    
    paddle1_position[1]+=paddle1_velocity[1]
    if paddle1_position[1] < 0:
        paddle1_position[1]=0
    elif paddle1_position[1] > (HEIGHT-PADDLE_HEIGHT):
        paddle1_position[1]=HEIGHT-PADDLE_HEIGHT
    
    paddle2_position[1]+=paddle2_velocity[1]
    if paddle2_position[1] < 0:
        paddle2_position[1]=0
    elif paddle2_position[1] > (HEIGHT-PADDLE_HEIGHT):
        paddle2_position[1]=HEIGHT-PADDLE_HEIGHT
        
    
    #updating the ball's position according to velocity
    
    ball_position[0]+=ball_velocity[0]
    ball_position[1]+=ball_velocity[1]
    
    #handle collision of ball with vertical wall  
    if ball_position[1]>(HEIGHT-BALL_RADIUS) or ball_position[1] < (BALL_RADIUS):
        ball_velocity[1]=-ball_velocity[1]
    
    #handle collision with left gutter   
    if ball_position[0]<(PADDLE_WIDTH+BALL_RADIUS) :
        #if there is paddle behind just reverse the horizontal velocity and increase velocity of ball with the increment factor
        if ball_position[1]+BALL_RADIUS >= paddle1_position[1] and ball_position[1]-BALL_RADIUS <= paddle1_position[1]+PADDLE_HEIGHT:
            ball_velocity[0]=-VELOCITY_INCREMENT_FACTOR*ball_velocity[0]
        else:
            #player 2 scores 
            player2_score+=1
            spawn_ball()
     
    #handle collision with right gutter 
    if ball_position[0]>(WIDTH-(PADDLE_WIDTH+BALL_RADIUS)):
        #if there is paddle behind just reverse the horizontal velocity and increase velocity of ball with the increment factor
        if ball_position[1]+BALL_RADIUS >= paddle2_position[1] and ball_position[1]-BALL_RADIUS <= paddle2_position[1]+PADDLE_HEIGHT:
            ball_velocity[0]=-VELOCITY_INCREMENT_FACTOR*ball_velocity[0]
        else:
            player1_score+=1
            spawn_ball()
    
    
    
    #drawing the paddles and ball 
    canvas.draw_polygon([ [paddle1_position[0],paddle1_position[1]],[paddle1_position[0]+PADDLE_WIDTH,paddle1_position[1]],
                           [paddle1_position[0]+PADDLE_WIDTH,paddle1_position[1]+PADDLE_HEIGHT],
                           [paddle1_position[0],paddle1_position[1]+PADDLE_HEIGHT]],2,'Black','Grey') #Paddle1
    
    canvas.draw_polygon([[paddle2_position[0],paddle2_position[1]],[paddle2_position[0],paddle2_position[1]+PADDLE_HEIGHT],
                           [paddle2_position[0]-PADDLE_WIDTH,paddle2_position[1]+PADDLE_HEIGHT],
                           [paddle2_position[0]-PADDLE_WIDTH,paddle2_position[1]]],2,'Black','Grey') #Paddle 2 
    
    canvas.draw_circle([ball_position[0],ball_position[1]],BALL_RADIUS,2,'White','Blue') #Ball 
    
    #draw the scores of the players 
    canvas.draw_text(str(player1_score), [WIDTH/2-50,50], 50, 'White')
    canvas.draw_text(str(player2_score),[WIDTH/2+50,50],50,'White')
    

    


def ball_control_handler(key):
        if key==simplegui.KEY_MAP['w']:
            #print('key handdler called')
            paddle1_velocity[1]=-PADDLE_VELOCITY
        elif key==simplegui.KEY_MAP['s']:
            paddle1_velocity[1]=PADDLE_VELOCITY
        elif key==simplegui.KEY_MAP['up']:
            paddle2_velocity[1]=-PADDLE_VELOCITY
        elif key==simplegui.KEY_MAP['down']:
            paddle2_velocity[1]=PADDLE_VELOCITY


def ball_control_keyup_handler(key):
    if key==simplegui.KEY_MAP['w'] or key==simplegui.KEY_MAP['s']:
        paddle1_velocity[1]=0
    elif key==simplegui.KEY_MAP['up'] or key==simplegui.KEY_MAP['down']:
        paddle2_velocity[1]=0
    
            
        
 

def start_game():
    global player1_score,player2_score
    spawn_ball()
    player1_score=0
    player2_score=0
        
    

def spawn_ball():
    global ball_position,ball_velocity
    DIRECTION1=random.randint(0, 1)
    DIRECTION2=random.randint(0, 1)

    DIRECTION1= -1 if DIRECTION1==0 else 1 
    DIRECTION2= -1 if DIRECTION2==0 else 1
    ball_position=[WIDTH/2,HEIGHT/2]
    ball_velocity=[DIRECTION1*INTIAL_BALL_VELOCITY,DIRECTION2*INTIAL_BALL_VELOCITY]
    
    
    
    
    


frame=simplegui.create_frame('Pong',WIDTH,HEIGHT)
frame.set_draw_handler(draw)

#define keys for controlling the paddles 
frame.set_keydown_handler(ball_control_handler)
frame.set_keyup_handler(ball_control_keyup_handler)
restart_button=frame.add_button('Restart Game',start_game)

frame.start()
start_game()
