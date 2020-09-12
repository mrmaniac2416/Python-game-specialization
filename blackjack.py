import simplegui
import random


SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
CARD_IMAGE = simplegui.load_image('http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png')
CARD_HIDDEN_IMAGE=simplegui.load_image('http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png')
CANVAS_DIM=(800,500)
PADDING=100
DISTANCE_BETWEEN_CARDS_HORIZONTAL=30
DISTANCE_BETWEEN_CARDS_VERTICAL=80
WHOLE_CARD_IMAGE_DIM=(936, 384)
WHOLE_HIDDEN_IMAGE_DIM=(144,96)
SINGLE_CARD_IMAGE_DIM=(WHOLE_CARD_IMAGE_DIM[0]/13,WHOLE_CARD_IMAGE_DIM[1]/4)
SINGLE_HIDDEN_CARD_IMAGE_DIM=(WHOLE_HIDDEN_IMAGE_DIM[0]/2,WHOLE_HIDDEN_IMAGE_DIM[1])
blackjack=None
score=0
TITLE_POS=(PADDING,PADDING/3)

DEALER_POS=(PADDING,PADDING-20)
PLAYER_POS=(PADDING,PADDING-20+DISTANCE_BETWEEN_CARDS_VERTICAL+SINGLE_CARD_IMAGE_DIM[1])
RESULT_POS=(PLAYER_POS[0]+DISTANCE_BETWEEN_CARDS_HORIZONTAL+SINGLE_CARD_IMAGE_DIM[0],DEALER_POS[1])
PROMPT_POS=(PLAYER_POS[0]+DISTANCE_BETWEEN_CARDS_HORIZONTAL+SINGLE_CARD_IMAGE_DIM[0],PLAYER_POS[1])
SCORE_POS=(PLAYER_POS[0]+DISTANCE_BETWEEN_CARDS_HORIZONTAL+SINGLE_CARD_IMAGE_DIM[0],PADDING/3)





class Hand:
    def __init__(self,leftmost_center):
        self.cards=[]
        self.leftmost_center=leftmost_center
        
    
    #add a card
    def add_card(self,card):
        self.cards.append(card)
     
    
    #calculate the normal score of the hand 
    def score(self):
        totalScore=0
        for card in self.cards:
            totalScore+=VALUES[card.rank]
        return totalScore
    
    def calculateAces(self):
        count=0
        for card in self.cards:
            if card.rank=='A':
                count+=1
        return count
    
    def blackjackscore(self):
        normalscore=self.score()
        acescount=self.calculateAces()
        if acescount==0:
            return normalscore
        elif normalscore+10<=21:
            return normalscore+10
        else:
            return normalscore
    
    
    def __str__(self):
        ans=""
        for card in self.cards:
             ans+=(card.suit + ' ' + card.rank + '\n')
        return ans[:-1]
    
    def draw(self,canvas):
        for index in range(len(self.cards)):
            center=(self.leftmost_center[0]+index*(DISTANCE_BETWEEN_CARDS_HORIZONTAL+SINGLE_CARD_IMAGE_DIM[0]),self.leftmost_center[1])
            self.cards[index].draw(canvas,center)
        
    
  

class Card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        self.hidden=False
    
    def __str__(self):
        return self.suit + ' ' + self.rank 
    
    #draw the card .
    def draw(self,canvas,center):
     
        if self.hidden:
            canvas.draw_image(CARD_HIDDEN_IMAGE,(SINGLE_HIDDEN_CARD_IMAGE_DIM[0]/2,SINGLE_HIDDEN_CARD_IMAGE_DIM[1]/2),
                              SINGLE_HIDDEN_CARD_IMAGE_DIM,center, SINGLE_HIDDEN_CARD_IMAGE_DIM)
        else:
            suit_index=SUITS.index(self.suit)
            card_index=RANKS.index(self.rank)
            source_center=(card_index*SINGLE_CARD_IMAGE_DIM[0]+SINGLE_CARD_IMAGE_DIM[0]/2,
                       suit_index*SINGLE_CARD_IMAGE_DIM[1]+SINGLE_CARD_IMAGE_DIM[1]/2) 
            canvas.draw_image(CARD_IMAGE,source_center,SINGLE_CARD_IMAGE_DIM,center, SINGLE_CARD_IMAGE_DIM)
        
        
        
    

    
    
class Deck:
    def __init__(self,cards):
        self.cards=cards
        
        
    #randomly shuffle the deck 
    def shuffle(self):
        random.shuffle(self.cards)
    
    #pass a card to a given hand 
    def deal(self,hand):
        cardremoved=random.choice(self.cards)
        hand.add_card(cardremoved)
        self.cards.remove(cardremoved)
        

class Blackjack:
    def __init__(self):
        self.deck=Deck(initialize_cards())
        self.deck.shuffle()
        self.result_string=""
        self.prompt_string="Hit Or Stand?"
        self.score=0
        self.playerhand=Hand((PADDING+SINGLE_CARD_IMAGE_DIM[0]/2,PADDING+SINGLE_CARD_IMAGE_DIM[1] 
                              + DISTANCE_BETWEEN_CARDS_VERTICAL + SINGLE_CARD_IMAGE_DIM[1]/2 ))
        self.deck.deal(self.playerhand)
        self.deck.deal(self.playerhand)
        
        self.dealerhand=Hand((PADDING+SINGLE_CARD_IMAGE_DIM[0]/2,PADDING+SINGLE_CARD_IMAGE_DIM[1]/2))
        self.deck.deal(self.dealerhand)
        self.deck.deal(self.dealerhand)
        
        #make first card of dealer hidden
        self.dealerhand.cards[0].hidden=True
        self.result=None
    
     
    def hit_handler(self):
        global score
        if self.result is not None:
            if self.result:
                print('You have won')
            else:
                print('You have lost')
            
        else:
            self.deck.deal(self.playerhand)
            if self.playerhand.blackjackscore()>21:
                self.dealerhand.cards[0].hidden=False
                self.result_string="You have busted"
                self.prompt_string="New deal?"
                print('You have busted')
                self.result=False
                score-=1
    
        print(self.playerhand,self.playerhand.blackjackscore(),self.dealerhand.blackjackscore())
    
    def pass_handler(self):
        global score
        #make first card of dealer visible
        self.dealerhand.cards[0].hidden=False
        if self.result is not None:
            if self.result:
                print('You have won')
            else:
                print('You have lost')
        else:
            while self.dealerhand.blackjackscore()<17:
                self.deck.deal(self.dealerhand)
            if self.dealerhand.blackjackscore()>21:
                self.result_string="You Win"
                self.result=True
                print('You Win')
                score+=1
            elif self.dealerhand.blackjackscore()<self.playerhand.blackjackscore():
                self.result=True
                self.result_string="You Win"
                print('You win')
                score+=1
            else:
                self.result=False
                self.result_string="You lose"
                print('You lose')
                score-=1
            self.prompt_string="New deal?"
        
       
        print(self.dealerhand,self.dealerhand.blackjackscore(),self.playerhand.blackjackscore())
                
            
        
        
        
        
        
def initialize_cards():
    cards=[]
    for suit in SUITS:
        for rank in RANKS:
            cards.append(Card(suit,rank))
    
    return cards

     
    
def hit_handler():
    global blackjack
    blackjack.hit_handler()
def pass_handler():
    global blackjack
    blackjack.pass_handler()



def draw_handler(canvas):
    global blackjack,score
    blackjack.playerhand.draw(canvas)
    blackjack.dealerhand.draw(canvas)
    canvas.draw_text('BlackJack', TITLE_POS, 20, 'Blue')
    canvas.draw_text('Score: ' + str(score),SCORE_POS,20,'Black')
    canvas.draw_text('Dealer', DEALER_POS, 20, 'Black')
    canvas.draw_text('Player', PLAYER_POS, 20, 'Black')
    canvas.draw_text(blackjack.result_string, RESULT_POS, 20, 'Red')
    canvas.draw_text(blackjack.prompt_string, PROMPT_POS, 20, 'Red')
    
    
    
def start_game():
    global blackjack,result_string
    result_string=""
    blackjack=Blackjack()
    
    print(len(blackjack.deck.cards))
    print(blackjack.playerhand)
    print(blackjack.dealerhand)
    print(blackjack.playerhand.score(),blackjack.dealerhand.score())

    
    
    
    








frame = simplegui.create_frame('Blackjack', CANVAS_DIM[0], CANVAS_DIM[1])
frame.set_draw_handler(draw_handler)
frame.set_canvas_background('Green')

hitbutton = frame.add_button('Hit', hit_handler)
passbutton = frame.add_button('Stand', pass_handler, 50)
dealbutton=frame.add_button('Deal',start_game,50)


start_game()

frame.start()






    
