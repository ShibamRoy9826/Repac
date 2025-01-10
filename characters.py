import pygame as pg

class Character():
    def __init__(self,screen,sheet,x,y,width,height,scale,frameChange,totalFrames):
        self.x=x
        self.y=y
        self.screen=screen
        self.width=width
        self.height=height
        self.scale=scale
        self.angle=0
        self.flippedX=False

        ## Player States
        self.playerState="MOVING"
        self.rotatedTo=2 # 1-> Left, 2->Right, -1->Up, -2->Down
        
        ## Player Images/Sprites
        self.spriteSheet=pg.image.load(sheet).convert_alpha()
        self.og_image=pg.Surface((width,height),pg.SRCALPHA).convert_alpha()
        self.rect=pg.Rect(x,y,width*scale,height*scale)

        ## Counters for animations
        self.spriteIndex=0
        self.frameCounter=0
        self.frameChangeRate=frameChange
        self.totalSpriteFrames=totalFrames

        ## Bliting sprite
        # self.image.blit(self.spriteSheet,(x,y),(0,0,16,16))
        # self.image.set_colorkey((0,0,0))

    def update(self):
        self.frameCounter+=1
        if self.frameCounter>=self.frameChangeRate:
            self.spriteIndex=(self.spriteIndex+1)%self.totalSpriteFrames
            self.frameCounter=0
            if self.spriteIndex>=self.totalSpriteFrames:
                self.spriteIndex=0
            self.image=self.og_image.fill((0,0,0,0))
            self.og_image.blit(self.spriteSheet,(0,0),(self.spriteIndex*self.width,0,self.width,self.height))

        self.image=pg.transform.scale(self.og_image,(self.width*self.scale,self.height*self.scale))
        self.rect.x=self.x
        self.rect.y=self.y

    def rotate(self,angle):
        self.angle=angle
    def flip(self,flipBool):
        self.flippedX = flipBool
    def render(self,surf):
        self.image=pg.transform.scale(pg.transform.flip(pg.transform.rotate(self.og_image,self.angle),self.flippedX,False),(self.width*self.scale,self.height*self.scale))
        surf.blit(self.image,(self.x,self.y))
