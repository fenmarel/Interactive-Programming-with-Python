'''
Created on Oct 29, 2012

run in codeskulpter.org
http://www.codeskulptor.org/#user4-pqPBEJKgafQJgxU.py

# "Stopwatch: The Game"
import simplegui
import math

# global variables
score = 0
tries = 0
time = 0
stop_count = 1

# time into formatted string A:BC.D
def format(t):
    mins = math.floor(t / 600)
    ten_sec = math.floor((t%600) / 100)
    t = "0" + str(t)
    sec = t[-2]
    tenths = t[-1]
    return str(mins) + ":" + str(ten_sec) + str(sec) + "." + str(tenths)
    
# event handlers for buttons
def start():
    global stop_count
    stop_count = 0
    timer.start()

def stop():
    global score, tries, stop_count
    if stop_count == 0:
        timer.stop()
        stop_count += 1
        tries += 1
        if time % 10 == 0:
            score += 1
        
def reset():
    timer.stop()
    global time, score, tries, stop_count
    time = 0
    score = 0
    tries = 0
    stop_count = 1
    
# timer event handler, update time value (every 0.1 secs)
def times():
    global time
    time += 1

# print time and score in canvas
def draw(canvas):
    canvas.draw_text(format(time), [85, 120], 40, "White")
    canvas.draw_text("Score: " + str(score) + "/" + str(tries), [174, 25], 18, "Green")

# frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)

# buttons
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# timer
timer = simplegui.create_timer(100, times)

# canvas
frame.set_draw_handler(draw)

# start frame
frame.start()
'''