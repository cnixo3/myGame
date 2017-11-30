import pygame
import time
import random
from tkinter import *
#Chris Nixon
#11/29/2017
#Python final project.
pygame.init()
#Setting the varaibles to be used throughout the program
#Game window size:
disp_width = 1600
disp_height = 900
high_scores = {}
#Tuple's of the colors used:
black = (0,0,0)
blue = (106,160,247)
white = (255,255,255)
red = (255, 0 ,0)
green=(62,173,3)
dark_green=(2,89,2)
dark_red=(91,11,2)
grey = (113,116,119)
#pygame function to create the display window:
gameDisp = pygame.display.set_mode((disp_width, disp_height))
pygame.display.set_caption('Fire Everything!!')
clk = pygame.time.Clock()
#loads the cloud image and sets it to be the size of the game window
back = pygame.image.load('clouds.jpg')
back = pygame.transform.scale(back,(disp_width,disp_height))
class fighter(object):
#This class represents the player, it has an x and a y position and the ability to move.
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.y_change = 0
        self.x_change = 0
        self.disp_width = 1600
        self.disp_height = 900
        #loads the image to be used to represent the player.
        self.jetImg = pygame.image.load('fighter.png')
        self.jetImg = pygame.transform.scale(self.jetImg,(45,65))
        #loads the image to be used if the player crashes.
        self.crashImg = pygame.image.load('crashed.png')
        self.crashImg = pygame.transform.scale(self.crashImg,(45,65))
        #sets the current image to be the standard fighter image.
        self.curr = self.jetImg
    def update(self):
        #called to draw the image to the game display, not on screen until
        #pygame.display.update() is called elsewhere.
        gameDisp.blit(self.curr,(self.x,self.y))
    def crash(self):
        #called when the player hits one of the sides or a missile.
        #changes the current image and calls the update method.
        self.curr = self.crashImg
        self.update()
    def move(self, x,y):
        #changes the x and y coordinates.
        self.x=x
        self.y=y
        self.update()
class missile(object):
    #Missiles are the opponents to the player, they move at an increasing speed
    #and cause the player to crash when the occupy the same location as the player.
    def __init__(self,x,y):
        #creates a new missile at a specified location
        self.missileImg = pygame.image.load('missile.png')
        self.missileImg = pygame.transform.scale(self.missileImg,(20,100))
        self.x=x
        self.y=y
        #gives the missile a width and height.
        self.width = 20
        self.height = 100
        #variables to know when the missile goes off the screen
        self.paneWidth = 1600
        self.paneHeight = 900
        #increases the speed exponentially, slowly at first but quickly at the end.
        self.speed=1.00044
        #the initial speed of the missile.
        self.change = 5
    def update(self):
        #updates the missile so it is ready to be drawn to the screen
        gameDisp.blit(self.missileImg,(self.x,self.y))
    def move(self):
        #the missiles travel up in a straight line at an initial speed.
        self.y-=self.change
        #this speed is increased every frame by an ever increasing amount.
        self.change *=self.speed
        #When the missile inevitably reaches the top of the screen this section sets
        # its location to be slightly below the screen and at a random x location.
        if self.y<-100:
            self.y=self.paneHeight-50
            self.x = random.randrange(0,self.paneWidth)
        self.update()
    def check(self,playerx,playery):
        #One of the most crucial parts of this class is this method which constantly
        #checks to see if the player has collided with this missile, by checking if the box
        #the player occupies as any of the same x,y points as the missile's box.
        playerx2 = playerx+45
        playery2 = playery+65
        #playerx and playery represent the top left corner of the player box,
        #playerx2 and playery2 represent the bottom right corner of the player box.
        collisionx = False
        collisiony = False
        collision = False
        #The player and the missile can occupy the same x coordinate or the same y coordinate
        #with no problem but if the player occupies a coordinate who's x and y both fall
        #inside the missile box then it means the player and the missile have collided.
        for tmpx in range(int(playerx),int(playerx2)):
            if tmpx>self.x and tmpx<self.x+self.width:
                collisionx=True
                break
        for tmpy in range(int(playery),int(playery2)):
            if tmpy>self.y and tmpy<self.y+self.height:
                collisiony = True
                break
        if collisionx and collisiony:
            collision = True
        return collision
class horizontalMissile(object):
    #this class is exactly the same as the missile class except it moves in a straight
    #line across the x axis and the missile image is rotated 90 degrees.
    def __init__(self,x,y):
        self.missileImg = pygame.image.load('horizontalmissile.png')
        self.missileImg = pygame.transform.scale(self.missileImg,(100,20))
        self.x=x
        self.y=y
        self.width = 100
        self.height = 20
        self.paneWidth = 1600
        self.paneHeight = 900
        self.speed=1.00044
        self.change = 5
    def update(self):
        gameDisp.blit(self.missileImg,(self.x,self.y))
    def move(self):
        self.x+=self.change
        self.change *=self.speed
        if self.x>self.paneWidth+100:
            self.x = -100
            self.y = random.randrange(0,self.paneHeight)
        self.update()
    def check(self,playerx,playery):
        playerx2 = playerx+45
        playery2 = playery+65
        collisionx = False
        collisiony = False
        collision = False
        for tmpx in range(int(playerx),int(playerx2)):
            if tmpx>self.x and tmpx<self.x+self.width:
                collisionx=True
                break
        for tmpy in range(int(playery),int(playery2)):
            if tmpy>self.y and tmpy<self.y+self.height:
                collisiony = True
                break
        if collisionx and collisiony:
            collision = True
        return collision
#This next section contains the functions used by the game loop to make certain elements
#function and appear on screen.
def text_objects(txt,font):
    #This method creates the text box and returns the surface and the box it occupies.
    textSurface = font.render(txt,True, black)
    return textSurface, textSurface.get_rect()
def message_display(txt, score):
    #this method is the main part of displaying text on the screen, this function
    #is called when the player crashes specifically.
    #First it creates 2 font types, one large one slightly smaller.
    largeTxt = pygame.font.Font('freesansbold.ttf',100)
    scoreTxt=pygame.font.Font('freesansbold.ttf',80)
    #it then creates the first textbox with the text that was passed into the function.
    #the second textbox is used to display the score the player earned.
    Surf, Rect = text_objects(txt, largeTxt)
    Surf2, Rect2 = text_objects('Score: '+score, scoreTxt)
    Rect.center=((disp_width/2,disp_height/2))
    Rect2.center=((disp_width/2,(disp_height/2)+100))
    #the center of the boxes are set and then added to the list of things to be drawn on the screen.
    gameDisp.blit(Surf,Rect)
    gameDisp.blit(Surf2,Rect2)
    #draws all updates to the game screen.
    pygame.display.update()
    #allow the text to remain on the screen for 2 seconds.
    time.sleep(2)
    #prints the highscores.
    print_scores()
    #checks whether or not the high score dictionary is full, if it isnt then the
    #score automatically qualifies as a high score.
    if len(high_scores)<20:
        name_entry(score)
    else:
        #if there are already 20 entries it tests the score to see if it belongs on the list.
        test_score(score)
    game_intro()
def crash(score):
    #called when the player crashes, runs the crash message function.
    txt = "You Crashed"
    message_display(txt,str(score))
def timer(time):
    #this function displays the users score during the game, constantly updated by the game clock.
    txt = pygame.font.Font('freesansbold.ttf',60)
    txtsurf=txt.render(str(time),True,white)
    Rect = txtsurf.get_rect()
    #sets the score counter to be in the top right corner.
    Rect.center=((1500,60))
    gameDisp.blit(txtsurf,Rect)
    pygame.display.update()
def button(msg,x,y,w,h,light,dark,action=None):
    #function used to create a generic button to be used in the main menu.
    #constantly grabs the mouse's position and its position when clicked.
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    #if the mouse is currently over the button it becomes darker in order to make it easier to tell it is clickable.
    if x < mouse[0] < x+w and y < mouse[1] <y+h:
        pygame.draw.rect(gameDisp,dark,(x,y,w,h))
        if click[0]==1 and action != None:
            #if the mouse is over the button and it clicks then it runs one function for play and one for quit.
            if action =='play':
                game_loop()
            elif action == 'quit':
                write_scores()
                pygame.quit()
                quit()
    #if the mouse is not over the button it is then lighter in color.
    else:
        pygame.draw.rect(gameDisp,light,(x,y,w,h))
    smalltxt=pygame.font.Font('freesansbold.ttf',30)
    Surf2, Rect2 = text_objects(msg, smalltxt)
    Rect2.center=((x+(w/2),y+(h/2)))
    gameDisp.blit(Surf2,Rect2)
def game_intro():
    #this function creates the main menu of the function that runs at the start and after the player crashes.
    intro = True
    while intro:
        for event in pygame.event.get():
            #if they x out of the game.
            if event.type == pygame.QUIT:
                write_scores()
                pygame.quit()
                quit()
        #sets the background to be blue.
        gameDisp.fill(blue)
        #creates some text on screen showing the name of the program.
        introTxt=pygame.font.Font('freesansbold.ttf',100)
        Surf, Rect = text_objects("Fire Everything!!", introTxt)
        Rect.center=((disp_width/2,disp_height/2))
        gameDisp.blit(Surf,Rect)
        #draws 2 grey boxes that are slightly larger than the buttons to reinforce
        #the boundaries of the buttons.
        pygame.draw.rect(gameDisp,grey,(545,545,210,110))
        pygame.draw.rect(gameDisp,grey,(845,545,210,110))
        #creates a start and a quit button.
        button('Start!',550,550,200,100,green,dark_green,'play')
        button('Quit',850,550,200,100,red,dark_red,'quit')
        pygame.display.update()
def read_scores():
    #reads the highscores from a file at the launch of the game.
    #saves them to the high_scores dictionary.
    handle = open('HighScores.txt', 'r')
    for line in handle:
        tmp = line.split()
        high_scores[tmp[0]]= int(tmp[1])
    handle.close()
def write_scores():
    #writes the high scores to the file before any type of quit event.
    handle = open('HighScores.txt', 'w')
    for key in high_scores.keys():
        handle.write(key + ' ' + str(high_scores[key])+ '\n')
    handle.close()
def test_score(score):
    #tests the user's score to see if it belongs in the high scores.
    min = int(score)
    min_loc = ''
    #finds the location of the current lowest score and boots it if the user's score belongs on the list.
    for key, value in high_scores.items():
        if int(value)<int(min):
            min = int(value)
            min_loc = key
    if int(min)<int(score):
        high_scores.pop(min_loc)
        #calls the function to prompt the user to enter their name.
        name_entry(score)
def print_scores():
    #displays the highscores on screen for the user to see.
    smalltxt=pygame.font.Font('freesansbold.ttf',40)
    #creates a font to use and sets the background to red.
    gameDisp.fill(red)
    start_height = 20
    position = 1
    #sorts the dictionary by its values, printing the largest scores first.
    for key,value in sorted(high_scores.items(), key=lambda p:p[1], reverse=True):
        Surf, Rect= text_objects(str(position)+'. '+key+': '+  str(value),smalltxt)
        Rect.center=((disp_width/2,start_height))
        gameDisp.blit(Surf,Rect)
        position+=1
        start_height+=45
    pygame.display.update()
    time.sleep(4)
def name_entry(score):
    #uses the TKinter GUI library to create an entry box
    #allowing the user to enter their name or initials.
    top = Tk()
    def get_name():
        tmp = str(E1.get())
        top.destroy()
        high_scores[tmp] = int(score)
    L1 = Label(top, text="Please Enter Your Initials: ")
    L1.pack(side=LEFT)
    b = Button(top,text="Enter",width=5,command=get_name)
    b.pack(side=RIGHT)
    E1 = Entry(top, bd=10)
    E1.pack(side=RIGHT)
    top.mainloop()
    
def game_loop():
    #the "Main" function of the game, this is where the game starts and all the events are handled.
    #the player is started out approximately at the center of the screen with no movement.
    x=(disp_width*0.45)
    y=(disp_height*0.45)
    x_change = 0
    y_change = 0
    #missiles are spawn at certain times, their timers are initially 0.
    missile_time=0
    horizontal_time=0
    tmr=0
    tm=0
    #creates the player at coordinates x and y.
    player  = fighter(x,y)
    #creates 2 lists to hold missiles and horizontal missiles.
    missile_array = []
    horizontal_array=[]
    #creates an inital missile at a random x location and about half off the screen.
    comp = missile(random.randrange(0,disp_width),disp_height-50)
    missile_array.append(comp)
    Exit = False
    while not Exit:
        #the timer continues to run even when the game at the menu or highscore screen.
        #when the game is running the time between frames is between 18 and 22 milliseconds
        #this statement is used to discard any initially large times with a safe margin of error.
        if tm>200:
            tm=0
        #these statements are used to update the individual timers used in the game for score and missile spawning.
        tmr+=tm
        missile_time+=tm
        horizontal_time+=tm
        #grabs the time between the last 2 frames.
        tm = clk.get_time()
        #calls the score function.
        timer(tmr)
        #this is where events are handled, key presses being the most important.
        for event in pygame.event.get():
            #allows the user to quit at any time by hitting the x on top, this is not a given by default.
            if event.type == pygame.QUIT:
                write_scores()
                pygame.quit()
                quit()
            #the controls for the player are the ASDW and the arrow keys, each affecting the rate of change
            #for the player in a certain direction.
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    x_change = -5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change = 5
                if event.key==pygame.K_UP or event.key==pygame.K_w:
                    y_change = -5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y_change = 5
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    x_change = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change = 0
                if event.key==pygame.K_UP or event.key==pygame.K_w:
                    y_change = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y_change = 0
        #updates the player's x and y based on which keys were hit.
        x+=x_change
        y+=y_change
        player.move(x,y)
        #handles the array of horizontal missiles that have been created, each
        #loop has a missile move then check to see if a player has collided with it.
        for horiz in horizontal_array:
            horiz.move()
            crashed = horiz.check(x,y)
            if crashed:
                gameDisp.fill(red)
                player.crash()
                crash(tmr)
                tmr=0
        #does the same thing for the regular missiles.
        for temp in missile_array:
            temp.move()
            crashed = temp.check(x,y)
            if crashed:
                gameDisp.fill(red)
                player.crash()
                crash(tmr)
                tmr=0
        #crashes the player if it goes out of bounds, first on the x then on the y.
        if x>=disp_width-45 or x <= 0:
            if x<0:
                x=0
            if x>disp_width-45:
                x=disp_width-45
            gameDisp.fill(red)
            player.crash()
            crash(tmr)
            tmr=0
        if y>=disp_height-65 or y <= 0:
            if y<0:
                y=0
            if y>disp_width-65:
                y=disp_width-65
            gameDisp.fill(red)
            player.crash()
            crash(tmr)
            tmr=0
        #adds the clouds image to the game screen
        gameDisp.blit(back,(0,0))
        #adds the player to the game screen
        player.update()
        #adds all of the missiles in the array to the game screen
        for horiz in horizontal_array:
            horiz.update() 
        for temp in missile_array:
            temp.update()
        #draws the game screen
        pygame.display.update()
        #sets the frames per second
        clk.tick(90)
        #a new missile is created every 10 seconds at a random location on the x axis
        if missile_time>10000:
            tmp = missile(random.randrange(0,disp_width),disp_height-50)
            missile_array.append(tmp)
            missile_time=0
        #a new horizontal missile is created every 25 seconds and added to a
        #random location on the y axis.
        if horizontal_time>20000:
            tmp = horizontalMissile(-100,random.randrange(0,disp_height))
            horizontal_array.append(tmp)
            horizontal_time=0
#the main function section, the highscores are read from a file, then the intro is played
read_scores()
game_intro()

