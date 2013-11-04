'''
Created on Nov 6, 2012

run at codeskulptor.org
http://www.codeskulptor.org/#user4-mlY9v8Rk85jc15m.py

# Implementation of classic arcade game Pong
import simplegui
import random

# initialize globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# spawn ball, set ball velocity
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if right:
        ball_vel = [(random.randrange(120, 240) / 60.), (-random.randrange(60, 180) / 60.)]  
    else:
        ball_vel = [(-random.randrange(120, 240) / 60.), (-random.randrange(60, 180) / 60.)]
    pass

# event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    global start_dir
    start_dir = True
    score1, score2 = 0, 0
    paddle1_vel, paddle2_vel = 0, 0
    paddle1_pos = float((HEIGHT/2) + HALF_PAD_HEIGHT)
    paddle2_pos = float((HEIGHT/2) + HALF_PAD_HEIGHT) 
    ball_init(start_dir)
    pass

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, start_dir
 
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= PAD_HEIGHT and paddle1_pos + paddle1_vel <= HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= PAD_HEIGHT and paddle2_pos + paddle2_vel <= HEIGHT:
        paddle2_pos += paddle2_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # draw paddles
    c.draw_line([4, paddle1_pos], [4, paddle1_pos - PAD_HEIGHT], PAD_WIDTH, "White")
    c.draw_line([WIDTH-4, paddle2_pos], [WIDTH-4, paddle2_pos - PAD_HEIGHT], PAD_WIDTH, "White")
    
    # vert ball bounce
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    # paddle bounce/score, speed increases
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if (paddle1_pos - PAD_HEIGHT) <= ball_pos[1] <= paddle1_pos:
            ball_vel[0] = -ball_vel[0]          # reflect
            ball_vel[0] += ball_vel[0] * 0.10   # 10% speed increase x
            ball_vel[1] += ball_vel[1] * 0.10   # 10% speed increase y
        else:
            score2 += 1
            start_dir = True
            ball_init(start_dir)
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if (paddle2_pos - PAD_HEIGHT) <= ball_pos[1] <= paddle2_pos:
            ball_vel[0] = -ball_vel[0]          # reflect
            ball_vel[0] += ball_vel[0] * 0.10   # 10% speed increase x
            ball_vel[1] += ball_vel[1] * 0.10   # 10% speed increase y
        else:
            score1 += 1
            start_dir = False
            ball_init(start_dir)
            
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    c.draw_text(str(score1), [WIDTH/4 + 50, HEIGHT/4], 54, "White")
    c.draw_text(str(score2), [(WIDTH/4)*3 - 90, HEIGHT/4], 54, "White")    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
   
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)

# start frame
init()
frame.start()


'''
