'''
Created on Oct 18, 2012

@author: Jonno
'''


def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
def number_to_name(num):
    if num == 0:
        return 'rock'
    elif num == 1:
        return 'Spock'
    elif num == 2:
        return 'paper'
    elif num == 3:
        return 'lizard'
    elif num == 4:
        return 'scissors'
    
def rpsls(guess):
    import random
    player_number = name_to_number(guess)
    comp_number = random.randrange(0, 5)
    print "\nPlayer chooses " + number_to_name(player_number)
    print "Computer chooses " + number_to_name(comp_number)
    if comp_number == player_number:
        print "Player and computer tie!"
    elif 1 <= (comp_number - player_number) % 5 <= 2:
        print "Computer wins!"
    else:
        print "Player wins!"
    
    
    
    
    
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
    