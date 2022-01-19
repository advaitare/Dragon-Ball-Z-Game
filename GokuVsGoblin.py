import pygame


pygame.init()

win=pygame.display.set_mode((500,480))
pygame.display.set_caption("Goku Vs Goblins")
#loading player images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg111.jpg') #bg image
char = pygame.image.load('standing.png')

block = pygame.image.load('block1.png') 

clk=pygame.time.Clock()             #clock for frame rates

bulletSound = pygame.mixer.Sound("bullet.wav")
hitSound = pygame.mixer.Sound("hit.wav")

bgmusic = pygame.mixer.music.load("Clash Of Gods AMV - Ultra Instinct-[AudioTrimmer.com].mp3")
pygame.mixer.music.play(-1) 

score =0

#player class
class Player(object):
    def __init__(self, x, y, w, h):
        self.x = x  #50
        self.y = y  #410
        self.w = w  #w=h=64
        self.h = h
        self.vel = 5
        self.isJump= False
        self.jumpCount=10
        self.left=False
        self.right=False
        self.walkCount=0
        self.standing=True
        self.collide = False
        self.won= True
        self.hitbox=(self.x+17, self.y+11 ,29 ,52 )

    def draw(self, win):
        if self.walkCount+1 >=27:           #since were using 9 sprites 3 times in a frame [gives illusion of walking]
            self.walkCount =0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1

        else :
            if self.right:
                win.blit(walkRight[0], (self.x,self.y))
            else :
                win.blit(walkLeft[0], (self.x,self.y))
        self.hitbox=(self.x+17, self.y +11 ,29 ,52 )
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        self.isJump= False  #bugfix- so that our charcter stops jumping
        self.jumpCount=10   #bugfix- Reset to initial jumpCount
        self.x= 40
        self.y= 410
        self.walkCount = 0
        font1= pygame.font.SysFont("comicsansms" , 70)
        text1= font1.render("-5" , 1, (255,0,0))
        win.blit(text1, (250 -(text1.get_width()/2),200))
        pygame.display.update()
        i=0                     #to hold the text for 1s
        while i< 100:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    i=151
                    pygame.quit()

    def decide(self,res):
        if res==1:
            font1= pygame.font.SysFont("comicansms" , 100)
            text1= font1.render("Weehee! YOU WON!!!" , 1, (255,180,0))
            win.blit(text1, (250 -(text1.get_width()/2),200))
            i=0                     #to hold the text for 10s
            while i< 300:
                pygame.time.delay(10)
                i+=1
                #goback to menu
        else:
            font1= pygame.font.SysFont("Stencil Std" , 100, True)
            text1= font1.render("Weehee! YOU LOSE!!!" , 1, (255,180,0))
            win.blit(text1, (250 -(text1.get_width()/2),200))
            i=0                     #to hold the text for 10s
            while i< 300:
                pygame.time.delay(10)
                i+=1
    

    
                

class blocks(object):
    def __init__(self, x,y):
        self.x=x
        self.y=y
        self.hitbox = (self.x, self.y, 64,64)

    def draw(self, win):
        win.blit(block, (self.x, self.y))
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        

            
#projectile class for bullets
class projectile(object):
    def __init__(self,x,y,rad,color,facing):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.facing = facing
        self.vel= 8*facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.rad )


#enemy class
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self,x,y,w,h,end):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.end = end
        self.walkCount=0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox=(self.x+17 , self.y+2 , 31, 57)
        self.health = 10;
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible :
            if self.walkCount + 1 >=33:
                self.walkCount=0
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0] , self.hitbox[1]-20 , 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0] , self.hitbox[1]-20 , 50 - ((50/10)*(10 - self.health)), 10))
            self.hitbox=(self.x+17, self.y+2 ,31 ,57 )
        else:
            self.visible=False
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        
    def move(self):
        if self.vel>0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x+=self.vel
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x+=self.vel
                self.walkCount=0

    def hit(self):
        if self.health <= 0:
           self.visible = False
        else:
            self.health -= 1
            print("Boom! hit")
        pass
    

#screen update 
def redrawGameWindow():
    win.blit(bg, (0,0))
    block1.draw(win)
    text= font.render("Score: " + str(score) , 1, (94,43,102))
    win.blit(text, (370,10))
    man.draw(win)
    goblin.draw(win)

    
    
    for bullet in bullets:
        bullet.draw(win)
        
    pygame.display.update()

#mainloop
man = Player(40,410,64,64)
bullets= []
goblin = enemy(205,415,64,64,400)
block1 = blocks(160,410)
font = pygame.font.SysFont("Times New Roman",30, True)
shootloop = 0
onBox=False
run=True
while run:
    clk.tick(27)

    #for man and block collision
    if man.hitbox[1] < block1.hitbox[1] + block1.hitbox[3] and man.hitbox[1] + man.hitbox[3] > block1.hitbox[1] : # man -> above the bottom of rect and below the top and if goblin is not dead
                if man.hitbox[0] < block1.hitbox[0] + block1.hitbox[2] and man.hitbox[0] + man.hitbox[2] > block1.hitbox[0]:
                    man.collide = True
                else:
                    man.collide= False
    else:
        man.collide = False
    
    #for man goblin collision
    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1] and goblin.visible: # man -> above the bottom of rect and below the top and if goblin is not dead
                if man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0]:
                    man.hit()
                    score -= 5
                

    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:  #basically it waits for bullet cool down for 3 frames
        shootloop = 0
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run= False

    #for shooting bullets
    for bullet in bullets:
        if bullet.y - bullet.rad < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.rad > goblin.hitbox[1] and goblin.visible: # bullet -> above the bottom of rect and below the top
            if bullet.x - bullet.rad < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.rad > goblin.hitbox[0]:        
                
                goblin.hit();
                hitSound.play()
                score += 1
                bullets.pop(bullets.index(bullet))      #bullet gayab when goblin shot

        #bullets on blocks
        if bullet.y - bullet.rad < block1.hitbox[1] + block1.hitbox[3] and bullet.y + bullet.rad > block1.hitbox[1] : # bullet -> above the bottom of rect and below the top
            if bullet.x - bullet.rad < block1.hitbox[0] + block1.hitbox[2] and bullet.x + bullet.rad > block1.hitbox[0]:
                bullets.pop(bullets.index(bullet))
                
        if bullet.x >0 and bullet.x < 500:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))      #if bullets out of screen pop bullets that are created
            
    keys = pygame.key.get_pressed()     

    if keys[pygame.K_SPACE] and shootloop == 0:
        bulletSound.play()
        if man.left:
            facing=-1
        else:
            facing=1
            
        if len(bullets)< 5:     # 5 bullets in screen at a time
            bullets.append(projectile(round(man.x + man.w//2),round(man.y + man.h//2), 5, (224,250,244),  facing))

        shootloop = 1   #cooldown bullet as above in mainloop for 3 frames

    #if pressed arrow keys to move        
    if keys[pygame.K_LEFT] and man.x > man.vel :
        if man.hitbox[0] + man.hitbox[2] <= block1.hitbox[0] :
            man.x -= man.vel
            man.y = 410
        if man.collide and man.y==410:
            man.x= block1.hitbox[0]+block1.hitbox[2]+1
            man.y = 410
        if not man.collide:
            man.x -= man.vel
        man.left=True
        man.right=False
        man.standing=False

    elif keys[pygame.K_RIGHT] and man.x <= 500 - man.w - man.vel:
        if man.hitbox[0] >= block1.hitbox[0] + block1.hitbox[2] :
            man.x += man.vel
            man.y = 410
        if man.collide and man.y==410:
            man.x=block1.hitbox[0]-64
            man.y = 410
        if not man.collide:
            man.x += man.vel
        man.left=False
        man.right=True
        man.standing=False

    else:
        man.standing = True
        man.walkCount=0
        
    if not man.isJump:                  #allow jump if not jumping
        if keys[pygame.K_UP]:
            man.isJump=True
            man.left=man.right=False
            man.walkCount=0
        
    else:
        # (10(initial) -10 count up -10 count down)  
        if man.jumpCount>=-10:
           if man.jumpCount>=0:
               man.y -= man.jumpCount**2 * 0.5 *1        #changing y cord while jumpcounts
               man.jumpCount-=1      #positive leap
           if man.jumpCount<0 :     
               man.y += man.jumpCount**2 * 0.5        #changing y cord while jumpcounts
               man.jumpCount-=1
               if man.collide:
                   man.y = block1.hitbox[1] - 64
                   man.isJump= False
                   man.jumpCount=10
                   onBox=True
               else:
                   onBox=False
        elif not onBox:
            man.y=410
            man.isJump= False
            man.jumpCount=10
                           
        else:
            #stop jumping
            man.isJump= False
            man.jumpCount=10

    if man.x == 500 - man.w - man.vel  and not(goblin.visible):
        man.decide(1)
    elif score==-15:
        man.decide(0)
    else:
        pass

    redrawGameWindow()
 

pygame.quit()
