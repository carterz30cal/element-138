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
tilemaps = []
tilemaps_properties = []
mapl = []
tilewidth = 10
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
    files = glob("Mods/*/*.txt")
    for f in files:
        fo = open(f,"r")
        fr = fo.read().split("#")
        if "tilemap" in fr[0]:
            tilemaps.append([fr[1],[]])
            tilemaps_properties.append([])
            fr = fr[2].rstrip().split("/").split("~")
            tia = len(tilemaps)-1
            tilemaps_properties[tia].append(fr[1:])
            for t in fr[0]:
                tilemaps[tia][1].append([])
                tian = len(tilemaps[tia][1])-1
                for tl in t.split(";"):
                    tilemaps[tia][1][tian].append([])
                    tiam = len(tilemaps[tia][1][tian])-1
                    for p in tl.rstrip().split(","):
                        tilemaps[tia][1][tian][tiam].append(int(p))
            print(tilemaps[tia])
        fo.close()
def Init():
    Init_Palettes()
    Init_Tilemaps()
    # create a quick map
    for ix in range(0,x):
        mapl.append([])
        for iy in range(0,y):
            mapl[ix].append(rint(0,2))


# GAMEPLAY LOOP
pygame.init()
surface = pygame.display.set_mode((x*5,y*5))
pygame.display.set_caption("carter's game version " + version)
clock = pygame.time.Clock()
Init() # init all mods and crap
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    for ix in range(0,x):
        xc = ix//tilewidth
        for iy in range(0,y):
            yc = iy//tilewidth
            c = palettes[0][tilemaps[0][1][mapl[xc][yc]][iy%tilewidth][ix%tilewidth]]
            gfxdraw.box(surface,((ix*2,iy*2),(2,2)),c)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
print("PROGRAM ENDED")
