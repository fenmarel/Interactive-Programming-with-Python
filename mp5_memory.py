'''
Created on Nov 13, 2012

http://www.codeskulptor.org/#user5-Phx1RMaNaRFGm6M.py
run at codeskulptor.org

# implementation of card game - Memory
import simplegui
import random

# helper function to initialize globals
def init():
    global deck, score, card_pos, card_flipped, flip_count, flipped
    deck = [i // 2 for i in range(16)]
    random.shuffle(deck)
    score = 0
    flip_count = 0
    flipped = []    
    # generate dictionary {card: [pos, flipped, value, solved]}
    card_pos = [[i * 50, 0] for i in range(1, 17)]
    card_num = [i for i in range(16)]
    card_flipped = {}
    for i in card_num:
        card_flipped[i] = [card_pos[i], False, deck[i], False]

     
# define event handlers
def mouseclick(pos):
    global card_flipped, flip_count, flipped, score
    clicked = list(pos) 
    card_check = 0
    for card in card_pos:
        if (card[0] - 50) < clicked[0] <= card[0] \
            and flip_count <= 2 \
            and card_flipped[card_check][1] == False:
            # flip card, increase cards showing    
            card_flipped[card_check][1] = True
            flipped.append(card_check)
            flip_count += 1
        elif flip_count > 2:
            # solve matching cards
            if card_flipped[flipped[0]][2] == card_flipped[flipped[1]][2]:
                card_flipped[flipped[0]][3] = True
                card_flipped[flipped[1]][3] = True   
            # flip non-matching back
            for flip in flipped[:2]:
                if card_flipped[flip][3] != True:    
                    card_flipped[flip][1] = False
            # reset values and update score label
            score += 1
            l.set_text("Moves = " + str(score))
            flip_count = 1
            flipped = flipped[2:3]
        card_check += 1    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    loc = 15
    for card in deck:    
        canvas.draw_text(str(card), [loc, 70], 40, "Red")
        loc += 800 // 16
    for card, values in card_flipped.items():
        p1 = values[0][:]  
        p2 = [p1[0] - 50, p1[1]] 
        p3 = [p2[0], p2[1] + 100] 
        p4 = [p3[0] + 50, p3[1]] 
        if values[1] == False:
            canvas.draw_polygon([p1, p2, p3, p4], 1, "Black", "Green")
    
# initialize global variables
init()

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
l=frame.add_label("Moves = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
'''