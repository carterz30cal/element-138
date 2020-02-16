version = "h-1"

import pygame
from pygame import gfxdraw
from random import randint as rint
from glob import glob
import time
# VARIABLES
x = 100
y = 100
palettes = []
palette_index = 0
tilemaps = []
tilemap_index = 0
tilemap_properties = []
mapl = []
tilewidth = 10
px = 50
py = 50
player_sprite = []
screenwidth = 5
ts = 2
# FUNCTIONS
def Init_Palettes():
    files = glob("Mods/*/*.txt")
    for f in files:
        fo = open(f,"r")
        fr = fo.read().split("#")
        if "palette" in fr[0]:
            palettes.append([])
            fr = fr[1].rstrip().split("/")
            pai = len(palettes)-1
            for i in fr:
                cs = i.split(",")
                palettes[pai].append((int(cs[0]),int(cs[1]),int(cs[2])))
        fo.close()
def Init_Tilemaps():
    global player_sprite
    files = glob("Mods/*/*.txt")
    for f in files:
        fo = open(f,"r")
        fr = fo.read().split("#")
        if "tilemap" in fr[0]:
            tilemaps.append([fr[1],[]])
            tilemap_properties.append([])
            fr = fr[2].rstrip().split("/")
            tia = len(tilemaps)-1
            #tilemaps_properties[tia].append(fr[1:])
            for t in fr:
                tilemaps[tia][1].append([])
                tian = len(tilemaps[tia][1])-1
                twave = t.split("~")
                player = False
                tilemap_properties[tia].append([])
                for prop in twave[2:]:
                    tilemap_properties[tia][tian].append(prop)
                    if prop == "player":
                        player = True
                #print(t)
                for tl in twave[0].split(";"):
                    tilemaps[tia][1][tian].append([])
                    tiam = len(tilemaps[tia][1][tian])-1
                    for p in tl.split(","):
                        tilemaps[tia][1][tian][tiam].append(int(p))
                if player:
                    player_sprite = tilemaps[tia][1][tian]
                #print(tilemaps[tia])
        fo.close()
def Init():
    Init_Palettes()
    Init_Tilemaps()
    # create a quick map
    for ix in range(0,x):
        mapl.append([])
        for iy in range(0,y):
            mapl[ix].append(rint(0,4))
    surface = pygame.display.set_mode((x*5,y*5))
    pygame.display.set_caption("element-138 (version %s) " %(version))
    clock = pygame.time.Clock()
def Get_CameraBounds():
    sw = screenwidth
    # returns a tuple of bounds e.g. (0,10,0,10)
    b1 = px-sw
    b2 = px+sw
    b3 = py-sw
    b4 = py+sw
    if b1 < 0:
        b2 += -b1
        b1 = 0
    if b2 > x-1:
        b1 -= b2-(x-1)
        b2 = x-1
    if b3 < 0:
        b4 += -b3
        b3 = 0
    if b4 > y-1:
        b3 -= b4 - (y-1)
        b4 = y-1
    return (b1,b2+1,b3,b4+1)
def Tile_HasProperty(x,y,prop):
    for p in tilemap_properties[tilemap_index][mapl[x][y]]:
        if p.lower() == prop.lower():
            return True
    return False

# GAMEPLAY LOOP
pygame.init()

Init() # init all mods and crap
game = True

movex = 0
movey = 0
movec = 0
movef = 5
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                movex = 1
            elif event.key == pygame.K_a:
                movex = -1
            elif event.key == pygame.K_w:
                movey = -1
            elif event.key == pygame.K_s:
                movey = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                movex = 0
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                movey = 0
    movec += 1
    if movec >= movef and (movex != 0 or movey != 0):
        px += movex
        py += movey
        movec = 0
        if px < 0:
            px -= movex
        elif px >= x:
            px -= movex
        if py < 0:
            py -= movey
        elif py >= y:
            py -= movey
        if Tile_HasProperty(px,py,"impassable"):
            px -= movex
            py -= movey
    bounds = Get_CameraBounds()
    
    
    size = (ts,ts)
    for tx in range(bounds[0],bounds[1]):
        adjx = tx - (bounds[0])
        for ty in range(bounds[2],bounds[3]):
            adjy = ty - (bounds[2])
            for ix in range(0,tilewidth):
                for iy in range(0,tilewidth):
                    c = palettes[palette_index][tilemaps[tilemap_index][1][mapl[tx][ty]][ix][iy]]
                    p = (((adjx*tilewidth)+ix)*ts,((adjy*tilewidth)+iy)*ts)
                    gfxdraw.box(surface,(p,(size)),c)
    locpx = px - bounds[0]
    locpy = py - bounds[2]
    #print(bounds) #bounds readout
    #print("%s-%s - local: %s-%s" %(px,py,locpx,locpy)) #player position readout
    for drox in range(0,tilewidth):
        for droy in range(0,tilewidth):
            if player_sprite[drox][droy] != -1:
                c = palettes[palette_index][player_sprite[drox][droy]]
                p = (((locpx*tilewidth)+drox)*ts,((locpy*tilewidth)+droy)*ts)
                gfxdraw.box(surface,(p,size),c)
    """                                            
    for ix in range(0,x):
        xc = ix//tilewidth
        for iy in range(0,y):
            yc = iy//tilewidth
            c = palettes[0][tilemaps[0][1][mapl[xc][yc]][ix%tilewidth][iy%tilewidth]]
            gfxdraw.box(surface,((ix*2,iy*2),(2,2)),c)
    """
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
print("PROGRAM ENDED")
