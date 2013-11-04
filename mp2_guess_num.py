# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
'''
run in www.codeskulpter.org
http://www.codeskulptor.org/#user3-R9fVHOKcN4pah3z.py

#import modules
import simplegui
import random
import math

# initialize global variables used in your code
guess_range = 100
guesses = 7
number = random.randint(0, 100)

# define helper functions
def startup():
    global guesses, number
    number = random.randint(0, guess_range)
    if guess_range == 100:
        guesses = 7
    elif guess_range == 1000:
        guesses = 10
    else:
        print "Error! Please restart!"
        return
    print "\nNew game. Range is from 0 to", guess_range
    print "Numer of remaining guesses is", guesses

# define event handlers for control panel    
def range100():
    # button that changes range to range [0,100) and restarts
    global guess_range, guesses
    guess_range = 100
    startup()    

def range1000():
    # button that changes range to range [0,1000) and restarts
    global guess_range, guesses
    guess_range = 1000
    startup()    
    
def get_input(guess):
    # main game logic    
    global guesses
    print "\nGuess was", guess
    guesses -= 1
    print "Number of remaining guesses is", guesses
    
    # win/lose conditions
    if int(guess) == number:
        print "Correct, the number was " + str(number) + "! You win!"
        startup()
        return
    elif guesses <= 0:
        print "You ran out of guesses. The number was", number
        startup()
        return
    
    # next guess hints
    if int(guess) > number:
        print "Lower!"
        return
    elif int(guess) < number:
        print "Higher!"
        return
    else:
        print "Error, please restart!"
        return    
               
# create frame
frame = simplegui.create_frame("Guess the Number!", 200, 200)

# register event handlers for control elements
frame.add_button("Range is [0 to 100)", range100, 200)
frame.add_button("Range is [0 to 1000)", range1000, 200)
frame.add_input("Enter a Guess!", get_input, 200)

# start frame
frame.start()

# game start
startup()

# always remember to check your completed program against the grading rubric
'''