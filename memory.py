

import simplegui
import random 
#second element of list represents whether the card is closed 

cards = []
card1=None
card2=None
WIDTH=800
HEIGHT=200
CARD_WIDTH=WIDTH//16
TURNS=0
open_cards=0



def draw(canvas):
    global cards 
    for num in range(1,16):
        canvas.draw_line([num*CARD_WIDTH,0],[num*CARD_WIDTH,HEIGHT],2,'Grey')
    #draw the numbers on the card according to closed or open
    for index in range(16) : 
        if not cards[index][1]:  #if card is not closed then draw the num 
            canvas.draw_text(str(cards[index][0]),[index*CARD_WIDTH+CARD_WIDTH//2,HEIGHT/2],30,'Red')
    




def shuffle_cards():
    global cards 
    for num in range(1,9):
        cards.append([num,True])
    for num in range(1,9):
        cards.append([num,True])
    random.shuffle(cards)

def check_all_cards_open():
    global cards
    for card in cards:
        if card[1]:
            return False
    return True

def mouse_click_handler(pos):
    global cards,card1,card2,TURNS,open_cards
   # print(pos)
    card_number=pos[0]//CARD_WIDTH
    #print(TURNS)
    #print(card1,card2,cards)
    if cards[card_number][1]:   #if that card is closed then open that card
        cards[card_number][1]=False
        turns_label.set_text('Turns {}'.format(TURNS))
        open_cards+=1
        TURNS+=1
        if card1 is None and card2 is None: #if both of the prev cards are closed , we start afresh and store the flipped card in card1 
            card1=card_number
        elif card1 is not None and card2 is None : #if only first card is initialized then store current card in card2
            card2=card_number
        elif cards[card1][0]!=cards[card2][0]:  #both the card values are not equal
            cards[card1][1]=True
            cards[card2][1]=True #flip both the cards
            open_cards-=2
            card1=card_number
            card2=None
        elif cards[card1][0]==cards[card2][0]:
            card1=card_number
            card2=None
    if open_cards==16:
        success_label.set_text("Congratulations!. You have successfully completed the game. Click restart to restart the game.")

def start_game():
    global cards,card1,card2,TURNS,open_cards
    cards=[]
    card1=None
    card2=None
    TURNS=0
    open_cards=0
    turns_label.set_text('Turns {}'.format(TURNS))
    shuffle_cards()
    
        
        
            
  

frame=simplegui.create_frame('Memory',WIDTH,HEIGHT)
frame.set_draw_handler(draw)
frame.set_canvas_background('Green')
frame.set_mouseclick_handler(mouse_click_handler)
frame.add_button('Restart game', start_game)
turns_label=frame.add_label('Turns {}'.format(TURNS))
success_label=frame.add_label('')
start_game()
frame.start()

