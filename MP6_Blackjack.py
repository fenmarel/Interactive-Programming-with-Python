'''
Created on Nov 26, 2012

Mini-project #6 - Blackjack

run at codeskulptor.org
http://www.codeskulptor.org/#user6-DQdrluRp3AibJFL.py
'''
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
win = ''

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), \
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, \
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return self.hand            

    def add_card(self, card):
        self.hand.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        value = 0
        for card in self.hand:
            value += VALUES[card.get_rank()]
        for card in self.hand:
            if 'A' == card.get_rank() and (value + 10) <= 21:
                value += 10
        return value

    def busted(self):
        return self.get_value() > 21
    
    def draw(self, canvas, y_pos):
        x_pos = 50
        for c in self.hand:
            c.draw(canvas, [x_pos, y_pos])
            x_pos += 85
                
# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for r in RANKS:
            for s in SUITS:
                self.deck.append(Card(s, r))

    # add cards back to deck and shuffle
    def shuffle(self):
        self.deck = []
        for r in RANKS:
            for s in SUITS:
                self.deck.append(Card(s, r))
        random.shuffle(self.deck)        

    def deal_card(self):
        return self.deck.pop(0)
    
    def __str__(self):
        return str(len(self.deck)) + " Cards Left"
    
#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, score, win
    player_hand = Hand()
    dealer_hand = Hand()
    deck.shuffle()
    win = ''
    if in_play:
        score -= 1
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())    
    in_play = True

def hit(): 
    # if the hand is in play, hit the player
    global in_play, score, win
    if in_play:
        player_hand.add_card(deck.deal_card())
   
    # if busted update in_play
    if player_hand.busted() and in_play:
        in_play = False
        score -= 1
        win = 'YOU LOSE'
        
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global in_play, score, win
    if in_play:
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.busted() or player_hand.get_value() > dealer_hand.get_value():
            score += 1
            win = 'YOU WIN!'
        else:
            score -= 1
            win = 'YOU LOSE'

# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", [50, 50], 38, "White")
    
    # dealer cards and scoring
    dealer_hand.draw(canvas, 200)
    if in_play:
        canvas.draw_text("Dealer:", [50, 150], 24, "Black")
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, \
                          [50 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_SIZE)
    elif dealer_hand.busted():
        canvas.draw_text("Dealer: " + str(dealer_hand.get_value()) + " BUSTED!", [50, 150], 24, "Black")        
    else:
        canvas.draw_text("Dealer: " + str(dealer_hand.get_value()), [50, 150], 24, "Black")        
        
    # player cards and scoring    
    player_hand.draw(canvas, 450)
    if in_play:
        canvas.draw_text("Hit or Stand?", [50, 430], 16, "Black")
    else:
        canvas.draw_text("New Deal?", [50, 430], 16, "Black")
    if player_hand.busted():
        canvas.draw_text("Player: " + str(player_hand.get_value()) + " BUSTED!", [50, 400], 24, "Black")
    else:
        canvas.draw_text("Player: " + str(player_hand.get_value()), [50, 400], 24, "Black")
    
    # outcome
    canvas.draw_text("Player Score: " + str(score), [375, 50], 24, "Black")
    canvas.draw_text(win, [375, 100], 35, "Black")
    
# initialization
def init():
    global deck, player_hand, dealer_hand
    deck = Deck()
    deal()
            
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
init()

# get things rolling
frame.start()
