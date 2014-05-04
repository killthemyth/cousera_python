"""
    Will run only in cokeskulptor, http://www.codeskulptor.org/
    copy paste this code in left column of codeskulptor
"""

# Implementation of classic arcade game Pong
import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
HALF_WIDTH = WIDTH / 2
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ACC = 5 #Accelaration

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [5,4]
paddle1_vel = [0, 0]
paddel2_vel = [0, 0]
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if(direction == "RIGHT"):
        ball_vel[0] = 	random.randrange(2, 4)
        ball_vel[1] = - random.randrange(1, 3)
    elif(direction == "LEFT"):
        ball_vel[0] = - random.randrange(2, 4)
        ball_vel[1] = - random.randrange(1, 3)

# define event handlers
def button_handler():
    new_game()

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global LEFT, RIGHT
    score1 = 0
    score2 = 0
    if RIGHT is True:
        RIGHT = False
        LEFT = True
        spawn_ball("RIGHT")
    elif LEFT is True:
        LEFT = False
        RIGHT = True
        spawn_ball("LEFT")

    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    paddle1_pos = [[0, HEIGHT / 2 - HALF_PAD_HEIGHT], [0, HEIGHT / 2 + HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
    paddle2_pos = [[WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT], [WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    if (ball_pos[0] <= HALF_WIDTH and ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and ball_pos[1] + BALL_RADIUS >= paddle1_pos[0][1] and ball_pos[1] - BALL_RADIUS <= paddle1_pos[1][1]):
        ball_vel[0] = -(110 * ball_vel[0] / 100)

    elif (ball_pos > HALF_WIDTH and ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH and ball_pos[1] + BALL_RADIUS >= paddle2_pos[0][1] and ball_pos[1] - BALL_RADIUS <= paddle2_pos[1][1]):
        ball_vel[0] = -(110 * ball_vel[0] / 100)

    elif(ball_pos[0] <= BALL_RADIUS + PAD_WIDTH):
        score2 += 1
        spawn_ball("RIGHT")

    elif(ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH):
        score1 += 1
        spawn_ball("LEFT")

    if(ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    elif (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]

    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "white", "white")

    # update paddle's vertical position, keep paddle on the screen
    toadd = paddle1_vel[1]
    if(paddle1_pos[0][1] + toadd < 0):
        toadd = -paddle1_pos[0][1]
    elif(paddle1_pos[1][1] + toadd > HEIGHT):
        toadd = HEIGHT - paddle1_pos[1][1]

    paddle1_pos[0][1] += toadd
    paddle1_pos[1][1] += toadd
    paddle1_pos[2][1] += toadd
    paddle1_pos[3][1] += toadd

    toadd = paddle2_vel[1]
    if(paddle2_pos[0][1] + toadd < 0):
        toadd = -paddle2_pos[0][1]
    elif(paddle2_pos[1][1] + toadd > HEIGHT):
        toadd = HEIGHT - paddle2_pos[1][1]

    paddle2_pos[0][1] += toadd
    paddle2_pos[1][1] += toadd
    paddle2_pos[2][1] += toadd
    paddle2_pos[3][1] += toadd

    # draw paddles
    canvas.draw_polygon(paddle1_pos, PAD_WIDTH, "Red", 'None')
    canvas.draw_polygon(paddle2_pos, PAD_WIDTH, "Red", 'None')

    # draw scores
    canvas.draw_text(str(score1), [150, 100], 40, "Red")
    canvas.draw_text(str(score2), [450, 100], 40, "Red")

def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= ACC
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += ACC

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= ACC
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += ACC

def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] += ACC
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] -= ACC

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] += ACC
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] -= ACC


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", button_handler, 100)

# start frame
new_game()
frame.start()
