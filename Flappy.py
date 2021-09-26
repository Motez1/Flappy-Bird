'''

///////////////////////////////////////////////////////////////////////////////////////////////////

/////////  ///             ////        //////////     //////////     ///       ///
///        ///           ////////     ///       //   ///       //     ///    ///
///        ///          ///    ///    ///       //   ///       //      /// ///
/////////  ///         ////////////   ///////////    ///////////        ////
///        ///         ////    ////   ///            ///                ///
///        ///         ////    ////   ///            ///                ///
///        //////////  ////    ////   ///            ///                ///

///////////      ///////////     //////////         //////////
///       ///        ///         ///      //        ///      ///
///       ///        ///         ///      //        ///       ///
//////////           ///         //////////         ///       ///
///       ///        ///         ///     ///        ///       ///
///       ///        ///         ///      ///       ///      ///
///////////      ///////////     ///       ///      //////////

///////////////////////////////////////////////////////////////////////////////////////////////////

======================================
Created by: Motez Ouledissa 
======================================

Description:
    flappy bird is a game where you try to get pass the pipes
    without falling down to the ground or touching the pipes

Controls:
    Jump : space
    Pause : p

    if you lose press c to play again
    or press escape to close the game

======================================
Classes interfaces
======================================

Bird class :

    Attributes:
        x : x coordinate of the bird
        y : y coordinate of the bird
        vel : velocity of the bird
        accel : acceleration of the bird
        img : the current image of the bird
        ind : the current index of the image of the bird
        t : time variable for the movement of the bird
        isCollidingPipe : boolean to indicate the collision state of the bird and the pipes
        isCollidingBase : boolean to indicate the collision state of the bird and the base
    
    Methods:
        jump() : called each time you press space so the bird jumps
        hasLost() : checks if the bird is colliding (True if a collision happens and False if not)
        update() : handles the logic of the bird 
        animate() : handles the flapping animation of the bird
        draw(win) : draws the bird on the window

Base class :

    Attributes:
        x1 : top left corner of the base
        x2 : top right corner of the base
        y : y coordinate of the base
        vel : velocity of the base
        img : the current image of the base
    
    Methods:
        update() : handles the logic of the base
        draw(win) : draws the base on the window
        collide(bird) : handles the collision of a bird with the base

Pipe class :

    Attributes:
        x : x coordinate of the pipe
        y : y coordinate of the pipe
        vel : velocity of the pipe
        gap : gap between the pipes
        bottom_pipe : the image of the bottom pipe
        top_pipe : the image of the top pipe (image of bottom pipe inverted)
        pos : position of the gap
        passed : if the pipe is passed by a bird , this becomes true

    Methods:
        update(bird,score) : handles the logic of the pipe and each time a pipe is passed
                             increases the score by 1 and returns the new score
        draw(win) : draws the pipe on the window
        collide(bird) : handles the cllision of the top and bottom pipes with the bird
'''

#libraries:
import pygame
import random
import os

#intializing the pygame module and the font to allow us 
#to write text and render it on screen
pygame.init()
pygame.font.init()

#loading the images files that are used in the game
bird_img = [pygame.image.load(os.path.join("imgs","bird1.png")),
            pygame.image.load(os.path.join("imgs","bird2.png")),
            pygame.image.load(os.path.join("imgs","bird3.png")),
            pygame.image.load(os.path.join("imgs","bird2.png"))]

base_img = pygame.image.load(os.path.join("imgs","base.png"))
pipe_img = pygame.image.load(os.path.join("imgs","pipe.png"))
bg_img = pygame.image.load(os.path.join("imgs","bg.png"))

#choosing a the font and setting a basic window and changing
#its title to Flappy bird
font = pygame.font.SysFont("comicsans",30)
width , height = bg_img.get_width(), bg_img.get_height()
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Flappy bird")

class Bird:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel = 0
        self.accel = 0.6
        self.img_ind = 0
        self.img = bird_img[self.img_ind]
        self.t = 0
        self.isCollidingPipe = False
        self.isCollidingBase = False
    
    def jump(self):
        self.vel = -12
        self.y += self.vel
        self.t = 0

    def hasLost(self):
        if self.isCollidingPipe or self.isCollidingBase:
            return True
        return False

    def animate(self):
        self.img_ind = (self.img_ind + 1) % 4
        self.img = bird_img[self.img_ind]

    def update(self):
        self.animate()
        self.vel += self.accel * self.t
        if self.vel < -12:
            self.vel = -12
        elif self.vel > 12:
            self.vel = 12
        
        self.y += 0.5*self.accel*self.t**2 + self.vel*self.t
        self.t += 0.1
        if self.t > 5 :
            self.t = 5

    def draw(self,win):
        win.blit(self.img,(int(self.x),int(self.y)))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    def __init__(self,x,y):
        self.x = x 
        self.y = y
        self.vel = 5
        self.gap = 170
        self.bottom_pipe = pipe_img
        self.top_pipe = pygame.transform.flip(self.bottom_pipe,False,True)
        self.pos = random.randint(-100,100)
        self.passed = False

    def update(self,bird,score):
        self.x -= self.vel
        if self.x + self.top_pipe.get_width() < 0 :
            self.x = 300
            self.pos = random.randint(-100,100)
            self.passed = False

        self.collide(bird)
        if bird.x > self.x +  self.top_pipe.get_width() :
            if self.passed == False:
                self.passed = True
                score += 1
        
        return score


    def draw(self,win):
        win.blit(self.bottom_pipe,(self.x,self.y + self.pos))
        win.blit(self.top_pipe ,(self.x,self.pos - self.gap))

    def collide(self,bird):
        #generates the masks of each images and calculating the offsets
        #and the overlaps the images on top of others and check if there
        #are pixels that collide
        top_pipe_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_pipe_mask = pygame.mask.from_surface(self.bottom_pipe)
        bird_mask = bird.get_mask()

        bottom_offset = (self.x - bird.x , self.y + self.pos - round(bird.y))
        top_offset = (self.x - bird.x , self.pos - self.gap - round(bird.y))

        bottom_collision = bird_mask.overlap(bottom_pipe_mask,bottom_offset)
        top_collision = bird_mask.overlap(top_pipe_mask,top_offset)

        if top_collision or bottom_collision:
            if bird.isCollidingPipe == False :
                bird.isCollidingPipe = True
        else:
            bird.isCollidingPipe = False
    
class Base:
    def __init__(self,x,y):
        self.x1 = x
        self.x2 = x + base_img.get_width()
        self.y = y
        self.vel = 5
        self.img = base_img
    
    def update(self,bird):
        self.x1 -= self.vel
        self.x2 -= self.vel 

        #this is used to ensure that the base keep animating in a cycle
        if self.x2 < 0:
            self.x1 = self.x2 + self.img.get_width()
        if self.x1 < 0:
            self.x2 = self.x1 + self.img.get_width()
        
        self.collide(bird)
    
    def draw(self,win):
        win.blit(self.img,(self.x1,self.y))
        win.blit(self.img,(self.x2,self.y))

    
    def collide(self,bird):
        if bird.y + bird.img.get_height() > self.y:
            if bird.isCollidingBase == False :
                bird.isCollidingBase = True
        else:
            bird.isCollidingBase == False

#main function is the entry point to our program
#game function defines the the game of the flappy bird
#pause function is called when you press p button to pause the game
#loss function is called when the bird collides with something , if you press c
#you will start a new game and if you press escape the program will end

def main():
    run = True
    while run:
        game()
        run = loss()

def game():
    run = True
    score = 0
    bird = Bird(100,100)
    pipe = Pipe(0,300)
    base = Base(0,450)
    
    #clock to limit the speed of frames (30 frames per second)
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_p:
                    pause()

        base.update(bird)
        #setting the score to the new score
        score = pipe.update(bird,score)
        bird.update()

        if bird.hasLost():
            run = False

        win.blit(bg_img,(0,0))
        base.draw(win)
        pipe.draw(win)
        bird.draw(win)

        #writing the game score each frame
        score_text = font.render(f"SCORE: {score}",True,(255,255,255))
        render_pos = (width - score_text.get_width() , 0)
        win.blit(score_text,render_pos)
        pygame.display.update()
        

def loss():
    run = True
    text = font.render("YOU LOST",True,(255,255,255))
    render_pos = (int((width - text.get_width())/2), int((height - text.get_height())/2))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    run  = False
                    return True
                if event.key == pygame.K_ESCAPE:
                    run = False
                    return False
        win.blit(text,render_pos)
        pygame.display.update()

def pause():
    run = True
    text = font.render("PAUSE",True,(255,255,255))
    render_pos = ((width - text.get_width())/2 , (height - text.get_height())/2)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    run  = False
        win.blit(text,render_pos)
        pygame.display.update()

#entry point of the program
main()


    