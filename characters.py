import pygame as pg

class Character():
    def __init__(self,screen,sheet,x,y,width,height,scale,frameChange,totalFrames):
        self.x=x
        self.y=y
        self.screen=screen
        self.width=width
        self.height=height
        self.scale=scale

        ## Player States
        self.playerState="MOVING"
        self.flippedX=False
        self.rotatedTo=2 # 1-> Left, 2->Right, -1->Up, -2->Down
        
        ## Player Images/Sprites
        self.spriteSheet=pg.image.load(sheet).convert_alpha()
        self.og_image=pg.Surface((width,height),pg.SRCALPHA).convert_alpha()

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
        return self.image,(self.x,self.y)

    def rotate(self,side):
        if side==1:
            if self.rotatedTo==2:
                self.image=pg.transform.flip(self.og_image,True,False)
            elif self.rotatedTo==-1:
                self.image=pg.transform.rotate(self.og_image,90)
            elif self.rotatedTo==-2:
                self.image=pg.transform.rotate(self.og_image,-90)
            self.rotatedTo=1
        elif side==2:
            if self.rotatedTo==1:
                self.flippedX=True
            elif self.rotatedTo==-1:
                self.image=pg.transform.rotate(self.og_image,-90)
            elif self.rotatedTo==-2:
                self.image=pg.transform.rotate(self.og_image,90)
            self.rotatedTo=2

        elif side==-1:
            if self.rotatedTo==1:
                self.image=pg.transform.rotate(self.og_image,-90)
            elif self.rotatedTo==2:
                self.image=pg.transform.rotate(self.og_image,90)
            elif self.rotatedTo==-2:
                self.image=pg.transform.flip(self.og_image,True,False)
            self.rotatedTo=-1

        elif side==-2:
            if self.rotatedTo==1:
                self.image=pg.transform.rotate(self.og_image,90)
            elif self.rotatedTo==2:
                self.image=pg.transform.rotate(self.og_image,-90)
            elif self.rotatedTo==-1:
                self.image=pg.transform.flip(self.og_image,True,False)
            self.rotatedTo=-2

