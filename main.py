from PIL import Image
from os import listdir,path
from settings import *
from characters import *
from random import choice

## Setting initial speed to 0 and position to (20,20)
playerdx=0
playerdy=0

# Functions ######
def load_images(loc):
    allRes=[]
    for i in listdir(loc):
        j=pg.image.load(path.join(loc,i)).convert_alpha()
        allRes.append(j)
    return allRes

def resize(multiplierx,multipliery,image):
    w,h=image.get_rect().width,image.get_rect().height
    return pg.transform.scale(image,(w*multiplierx,h*multipliery))

def readLevel(fl,scale):
    blocks=[]
    dots=[]
    xCount=60
    yCount=60
    xCountMax=WIDTH-2*LEFT_BOUND
    yCountMax=HEIGHT-2*UPPER_BOUND
    with open(fl,"r") as f:
        lines=f.readlines()
        img1=pg.image.load("images/tiles/GrassHorizontal.png").convert_alpha()
        img2=pg.image.load("images/tiles/GrassVertical.png").convert_alpha()
        for indj,i in enumerate(lines):
            for ind,block in enumerate(i):
                if block=="=":
                    blocks.append((48*ind+xCount,48*indj+yCount,48*ind+xCount+TILE_SIZE,48*indj+yCount+TILE_SIZE))
                elif block==".":
                    dots.append((48*ind+xCount+20,48*indj+yCount+20))
    return blocks,dots




## Initialization-------------
pg.init()
screen=pg.display.set_mode(SIZE)
pg.display.set_caption("Repac: A Pacman remake")
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

## Loading sprites
bg=load_images("images/bg")
playerCurr=0
player=Character("sprites/pacman/pacman1.png",playerx,playery,16,16,PLAYER_SCALE,PLAYER_FRAME_CHANGE_RATE,8)
ghostRed=Character("sprites/ghosts/red.png",red_ghostx,red_ghosty,16,16,PLAYER_SCALE,GHOST_FRAME_CHANGE_RATE,4)
ghostRed_dx=0
ghostRed_dy=GHOST_SPEED

## Load audio
pg.mixer.music.load("audio/bg.mp3")
pg.mixer.music.play(loops=-1)

eatFruit=pg.mixer.Sound("audio/eatfruit.wav")
eatFruit.set_volume(0.3)

## Making boundaries
invisibleBlocks=[]
BoundTop=pg.Rect(0,0,WIDTH,UPPER_BOUND)
BoundBottom=pg.Rect(0,LOWER_BOUND,WIDTH,UPPER_BOUND)
BoundLeft1=pg.Rect(0,0,LEFT_BOUND,(HEIGHT/2)-12*CHAR_SIZE)
BoundRight1=pg.Rect(WIDTH-UPPER_BOUND,0,RIGHT_BOUND,(HEIGHT/2)-12*CHAR_SIZE)
BoundLeft2=pg.Rect(0,(HEIGHT/2)+2.5*CHAR_SIZE,LEFT_BOUND,(HEIGHT/2)-12*CHAR_SIZE)
BoundRight2=pg.Rect(WIDTH-UPPER_BOUND,(HEIGHT/2)+2.5*CHAR_SIZE,RIGHT_BOUND,(HEIGHT/2)-12*CHAR_SIZE)
invisibleBlocks.extend([BoundTop,BoundBottom,BoundLeft1,BoundRight1,BoundLeft2,BoundRight2])

# Some Variables
running=1
points=0
clock=pg.time.Clock()

## Resizing images
bg[0]=resize(8,8,bg[0])


blocks,dots=readLevel("levels/lvl1.txt",CHAR_SIZE)
blockObjs=[]
for i in blocks:
    b=Block(i[0],i[1],TILE_SIZE,TILE_SIZE,1)
    blockObjs.append(b)
bugLastFrame=False
renderBlocks=True

ghostChangeDirection=False
ghostAllSpeeds=[(0,GHOST_SPEED),(GHOST_SPEED,0),(-GHOST_SPEED,0),(0,-GHOST_SPEED)]
ghostSpeeds=[(0,GHOST_SPEED),(GHOST_SPEED,0),(-GHOST_SPEED,0),(0,-GHOST_SPEED)]

while running:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=0
        elif event.type==pg.KEYDOWN:
            if event.key in [pg.K_RIGHT,pg.K_l]:
                playerdx=PLAYER_SPEED
                player.flip(False)
                player.rotate(0)
                playerdy=0

            if event.key in [pg.K_LEFT ,pg.K_h]:
                playerdx=-PLAYER_SPEED

                player.rotate(0)
                player.flip(True)
                playerdy=0

            if event.key in [pg.K_DOWN, pg.K_j]:
                playerdy=PLAYER_SPEED
                player.rotate(-90)
                playerdx=0

            if event.key in [pg.K_UP,pg.K_k]:
                playerdy=-PLAYER_SPEED
                playerdx=0
                player.rotate(90)

    #Render bg
    screen.blit(bg[0],(0,0))

    #render player
    player.update()
    player.render(screen)

    #render ghosts
    ghostRed.update()
    ghostRed.render(screen)

    for block in blockObjs:
        block.render(screen)
        if player.rect.colliderect(block.rect):
            playerdx=0
            playerdy=0

            if player.x<=block.x:
                player.x-=REPULSION

            if player.x>=block.x:
                player.x+=REPULSION


            if player.y<=block.y:
                player.y-=REPULSION

            if player.y>=block.y:
                player.y+=REPULSION

        if ghostRed.rect.colliderect(block.rect):
            ghostRed_dx=0
            ghostRed_dy=0
            options=[]
        
            if ghostRed.x<=block.x:
                options.append((-GHOST_SPEED,0))

            elif ghostRed.x>=block.x:
                options.append((GHOST_SPEED,0))

            elif ghostRed.y<=block.y:
                options.append((0,-GHOST_SPEED))

            elif ghostRed.y>=block.y:
                options.append((0,GHOST_SPEED))

            c=choice(options)
            ghostRed_dx=c[0]
            ghostRed_dy=c[1]

    for block in invisibleBlocks:
        if player.rect.colliderect(block):
            playerdx=0
            playerdy=0

            if player.x<=block.x:
                player.x-=REPULSION

            if player.x>=block.x:
                player.x+=REPULSION

            if player.y<=block.y:
                player.y-=REPULSION

            if player.y>=block.y:
                player.y+=REPULSION

        if ghostRed.rect.colliderect(block):
            ghostRed_dx=0
            ghostRed_dy=0
        
            if ghostRed.x<=block.x:
                ghostRed.x-=REPULSION
                ghostRed_dx=-GHOST_SPEED

            elif ghostRed.x>=block.x:
                ghostRed.x+=REPULSION
                ghostRed_dx=+GHOST_SPEED

            elif ghostRed.y<=block.y:
                ghostRed.y-=REPULSION
                ghostRed_dy=-GHOST_SPEED

            elif ghostRed.y>=block.y:
                ghostRed.y+=REPULSION
                ghostRed_dy=+GHOST_SPEED


    # for i in blocks:
    #     im=pg.Rect(i[0],i[1],TILE_SIZE,TILE_SIZE)
    #     pg.draw.rect(screen,(64,128,20),im)
    #     if player.rect.colliderect(im):
    #         playerdx=0
    #         playerdy=0
    #
    #         if player.x<=i[0]:
    #             player.x-=REPULSION
    #
    #         if player.x>=i[0]:
    #             player.x+=REPULSION
    #
    #
    #         if player.y<=i[1]:
    #             player.y-=REPULSION
    #
    #         if player.y>=i[1]:
    #             player.y+=REPULSION
    #
    #     if ghostRed.rect.colliderect(im):
    #         options=[]
    #         ## To Continue
    #         ghostRed_dx=0
    #         ghostRed_dy=0


    for j in dots:
        dotRect=pg.Rect(j[0],j[1],8,8)
        pg.draw.rect(screen,(255,0,0),dotRect)
        if player.rect.colliderect(dotRect):
            points+=500
            eatFruit.play()

            dots.remove(j)
            print(points)


    ## Checking if player is out of bound
    # pg.draw.rect(screen,(255,255,255),BoundLeft2)
    # pg.draw.rect(screen,(255,255,255),BoundRight2)

    ## Updating player's position

    # if player.rect.colliderect(BoundTop) and playerdy<0:
    #     playerdy=0
    #
    # elif player.rect.colliderect(BoundBottom) and playerdy>0:
    #     playerdy=0
    #
    # if player.rect.colliderect(BoundLeft1) and playerdx<0:
    #     playerdx=0
    # elif player.rect.colliderect(BoundRight1) and playerdx>0:
    #     playerdx=0
    #
    # if player.rect.colliderect(BoundLeft2) and playerdx<0:
    #     playerdx=0
    # elif player.rect.colliderect(BoundRight2) and playerdx>0:
    #     playerdx=0
    #

    ## Teleportation
    if player.x< -player.width:
        player.x=WIDTH-2

    if player.x>WIDTH+player.width:
        player.x=2

    if ghostRed.x< -ghostRed.width:
        ghostRed.x=WIDTH-2

    if ghostRed.x>WIDTH+ghostRed.width:
        ghostRed.x=2
    
    ## Moving player
    player.x+=playerdx
    player.y+=playerdy

    ## Moving Ghost(red)

    ghostRed.x+=ghostRed_dx
    ghostRed.y+=ghostRed_dy

    # if player.rect.colliderect(BoundBottom):
    #     print("Collision!!!")

    #Updating screen
    pg.display.flip()
    clock.tick(FPS)

pg.quit()


