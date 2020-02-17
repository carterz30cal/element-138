version = "h-1"

import pygame
from pygame import gfxdraw
from random import randint as rint
from random import choice
from glob import glob
from math import floor
import time
import noise

# VARIABLES
screenx = 1000
screeny = 500
x = 100
y = 100
palettes = []
palette_index = 0
tilemaps = []
tilemap_index = 0
tilemap_properties = []
worldgens = []
mapl = []
tilewidth = 10
px = 50
py = 50
player_sprite = []
screenwidth = 5
ts = 4
surface = None
clock = None
perlinfreq = 32
font_index = -1
font_file = "Core/tilemap_text.txt"
font_size = 3
# FUNCTIONS
def String_ToIndexes(string):
    global font_index
    if font_index == -1:
        Init_Tilemap(font_file)
        font_index = len(tilemaps)-1
    indexes = Get_IndexFromNames(string,font_index)
    return indexes
def Text(text,colour,posx,posy):
    indexes = String_ToIndexes(text)
    csx = int(floor(posx))
    for i in range(len(indexes)):
        if indexes[i] == -1:
            csx += 2*font_size
        else:
            tile = tilemaps[font_index][1][indexes[i]]
            sx = 12
            lpx = -1
            for ky in range(10):
                for kx in range(10):
                    if tile[kx][ky] != -1:
                        if kx < sx:
                            sx = kx
                        elif kx > lpx:
                            lpx = kx
                        gfxdraw.box(surface,((csx+(kx*font_size),posy+(ky*font_size)),(font_size,font_size)),colour)
            ad = 2
            if lpx-sx == 0:
                ad = 3
            csx += ((lpx-sx)+ad)*font_size
def Init_Palettes():
    files = glob("Mods/*/*.txt")
    for f in files:
        fo = open(f,"r")
        fr = fo.read().split("#")
        if "palette" in fr[0].lower():
            palettes.append([f,[]])
            fr = fr[1].rstrip().split("/")
            pai = len(palettes)-1
            for i in fr:
                cs = i.split(",")
                palettes[pai][1].append((int(cs[0]),int(cs[1]),int(cs[2])))
        fo.close()
def Init_Tilemaps():
    global player_sprite
    files = glob("Mods/*/*.txt")
    for f in files:
        fo = open(f,"r")
        fr = fo.read().split("#")
        fo.close()
        if "tilemap" in fr[0].lower():
            tilemaps.append([fr[1],[]])
            tilemap_properties.append([])
            fr = fr[2].rstrip().split("`")
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
def Init_Tilemap(file):
    global player_sprite,palette_index
    fo = open("Mods/" + file,"r")
    fr = fo.read().split("#")
    fo.close()
    index = -1
    for p in range(len(palettes)):
        if palettes[p][0] == fr[1]:
            index = p
    if index == -1:
        pass #Init_Palette(). Shouldn't ever actually occur unless file is in a weird place or subfolder.
    palette_index = index
    tilemaps.append([fr[1],[]])
    tilemap_properties.append([])
    fr = fr[2].rstrip().split("`")
    tia = len(tilemaps)-1
    for t in fr:
        tilemaps[tia][1].append([])
        tian = len(tilemaps[tia][1])-1
        twave = t.split("~")
        player = False
        tilemap_properties[tia].append([])
        for prop in twave[1:]:
            tilemap_properties[tia][tian].append(prop)
            if prop == "player":
                player = True
        for tl in twave[0].split(";"):
            tilemaps[tia][1][tian].append([])
            tiam = len(tilemaps[tia][1][tian])-1
            for p in tl.split(","):
                tilemaps[tia][1][tian][tiam].append(int(p))
        if player:
            player_sprite = tilemaps[tia][1][tian]
def Init_Worldgens():
    files = glob("Mods/*/*.txt")
    for f in files:
        fo = open(f,"r")
        fr = fo.read().split("#")
        fo.close()
        if "worldgen" in fr[0].lower():
            worldgens.append([fr[1],fr[2:]])
def Init():
    global surface,clock
    Init_Palettes()
    Init_Worldgens()
    # map generation
    WorldGen_Generate(0)
    surface = pygame.display.set_mode((screenx,screeny))
    pygame.display.set_caption("element-138 (version %s) " %(version))
    clock = pygame.time.Clock()
def WorldGen_DoorPos(roomsize):
    dx = rint(1,roomsize[0]-1)
    dy = rint(1,roomsize[1]-1)
    if dy < roomsize[1]-dy:
        dy = 0
    else:
        dy = roomsize[1]-1
    if dx == dy:
        return WorldGen_DoorPos(roomsize)
    elif dx == roomsize[0]-1 and dy == 0:
        return WorldGen_DoorPos(roomsize)
    elif dx == 0 and dy == roomsize[1]-1:
        return WorldGen_DoorPos(roomsize)
    elif dx == roomsize[0]-1 and dy == roomsize[1]-1:
        return WorldGen_DoorPos(roomsize)
    else:
        return (dx,dy)
    
def WorldGen_Generate(index):
    global tilemap_index,mapl
    wg = worldgens[index][1]
    Init_Tilemap(wg[0].split(":")[1])
    tilemap_index = len(tilemaps)-1
    checks = []
    octaves = 4
    buildings = 10
    building_wall = 0
    building_floor = 0
    building_door = 0
    buildingmap = []
    for prop in wg[1:]:
        pros = prop.lower().split(":")
        if pros[0] == "fill":
            checks.append([(0,1),Get_IndexFromName(pros[1])])
        elif pros[0] == "perlin":
            rage = pros[1].split(",")
            checks.append([(float(rage[0]),float(rage[1])),Get_IndexFromNames(pros[2].split(","))])
        elif pros[0] == "octaves":
            octaves = int(pros[1])
        elif pros[0] == "building_count":
            buildings = int(pros[1])
        elif pros[0] == "building_wall":
            building_wall = Get_IndexFromName(pros[1])
        elif pros[0] == "building_floor":
            building_floor = Get_IndexFromNames(pros[1].split(","))
        elif pros[0] == "building_door":
            building_door = Get_IndexFromName(pros[1])
    for wx in range(x):
        mapl.append([])
        buildingmap.append([])
        for wy in range(y):
            n = noise._perlin.noise2(float(wx)/perlinfreq,float(wy)/perlinfreq,octaves)
            n = (n+1)/2
            #print(n)
            for c in checks:
                if n >= c[0][0] and n < c[0][1]:
                    #print(c[1])
                    mapl[wx].append(choice(c[1]))
                    buildingmap[wx].append(False)
                    break
    attempts = 0
    while buildings > 0 and attempts < 1000:
        attempts += 1
        rx = rint(0,x-10)
        ry = rint(0,y-10)
        sizex = rint(5,10)
        sizey = rint(5,10)
        build = False
        if not Tile_HasProperty(rx,ry,"impassable") and not buildingmap[rx][ry]:
            build = True
            for testx in range(rx,rx+sizex):
                for testy in range(ry,ry+sizey):
                    if buildingmap[testx][testy]:
                        build = False
        if build:
            doorpos = WorldGen_DoorPos((sizex,sizey))
            #print("made a building")
            buildings -= 1
            for buildx in range(rx,rx+sizex):
                locx = buildx-rx
                for buildy in range(ry,ry+sizey):
                    locy = buildy-ry
                    buildingmap[buildx][buildy] = True
                    if locx == doorpos[0] and locy == doorpos[1]:
                        #print("yuuuup got here dx-%s dy-%s" %(doorpos[0],doorpos[1]))
                        mapl[buildx][buildy] = building_door
                    elif locx == 0 or locx == sizex-1 or locy == 0 or locy == sizey-1:
                        mapl[buildx][buildy] = building_wall
                    else:
                        mapl[buildx][buildy] = choice(building_floor)
def Get_IndexFromName(name,index=tilemap_index):
    for t in range(len(tilemap_properties[index])):
        if tilemap_properties[index][t][0].lower() == name:
            return t
def Get_IndexFromNames(names,index=tilemap_index):
    indexes = []
    for name in names:
        if name == " ":
            indexes.append(-1)
            continue
        for t in range(len(tilemap_properties[index])):
            if tilemap_properties[index][t][0].lower() == name:
                indexes.append(t)
                break
    return indexes
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
                    c = palettes[palette_index][1][tilemaps[tilemap_index][1][mapl[tx][ty]][ix][iy]]
                    p = (((adjx*tilewidth)+ix)*ts,((adjy*tilewidth)+iy)*ts)
                    gfxdraw.box(surface,(p,(size)),c)
    locpx = px - bounds[0]
    locpy = py - bounds[2]
    #print(bounds) #bounds readout
    #print("%s-%s - local: %s-%s" %(px,py,locpx,locpy)) #player position readout
    for drox in range(0,tilewidth):
        for droy in range(0,tilewidth):
            if player_sprite[drox][droy] != -1:
                c = palettes[palette_index][1][player_sprite[drox][droy]]
                p = (((locpx*tilewidth)+drox)*ts,((locpy*tilewidth)+droy)*ts)
                gfxdraw.box(surface,(p,size),c)
    Text("hello there my name is carter",(255,255,255),ts*(screenwidth+0.5)*tilewidth*2,0)
    pygame.display.flip() # actually update the surface
    clock.tick(60) # cap the framerate (not usually necessary :/)
pygame.quit()
print("bye bye")
