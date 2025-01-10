from PIL import Image
from os import listdir,path
from settings import *
from characters import *


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

## Initialization-------------
pg.init()
screen=pg.display.set_mode(SIZE)
pg.display.set_caption("Repac: A Pacman remake")
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

## Loading sprites
bg=load_images("images/bg")
playerCurr=0
player=Character(screen,"sprites/pacman/pacman1.png",playerx,playery,16,16,PLAYER_SCALE,PLAYER_FRAME_CHANGE_RATE,8)

# Some Variables
running=1
clock=pg.time.Clock()

## Resizing images
bg[0]=resize(8,8,bg[0])

while running:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=0
        elif event.type==pg.KEYDOWN:
            if event.key in [pg.K_RIGHT,pg.K_l]:

                playerdx=PLAYER_SPEED
                player.rotate(2)
                playerdy=0

            if event.key in [pg.K_LEFT ,pg.K_h]:
                playerdx=-PLAYER_SPEED
                player.rotate(1)
                playerdy=0

            if event.key in [pg.K_DOWN, pg.K_j]:
                playerdy=PLAYER_SPEED
                player.rotate(-2)
                playerdx=0


            if event.key in [pg.K_UP,pg.K_k]:
                playerdy=-PLAYER_SPEED
                playerdx=0
                player.rotate(-1)
    #Render bg
    screen.blit(bg[0],(0,0))

    #render player
    img,pos=player.update()

    screen.blit(img,pos)

    ## Checking if player is out of bound

    ## Updating player's position
    player.x+=playerdx
    player.y+=playerdy

    #Updating screen
    pg.display.flip()
    clock.tick(FPS)

pg.quit()


