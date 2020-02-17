import pygame
from pygame import gfxdraw
from glob import glob

version = "h-2"
game = True
mouseDown = False
ftiles = []
tile = []
tindex = 0
tfile = ""
tpalette = []
palette = ""
editing = False
eColour = 1

def Import_Palette(palette):
    global tpalette
    fo = open(palette,"r")
    fr = fo.read().split("#")[1].split("/")
    #print(fr)
    fo.close()
    tpalette = []
    for i in fr:
        #print(i)
        cs = i.split(",")
        tpalette.append((int(cs[0]),int(cs[1]),int(cs[2])))
def Save():
    print("SAVING...")
    #print(ftiles)
    f = open(tfile,"r")
    prev = f.read()
    f.close()
    try:
        f = open(tfile,"w")
        if tindex != -1:
            sti = "\n"
            for sx in range(tilewidth):
                sti = sti + str(tile[0][sx][0]).replace("\n","")
                for sy in range(1,tilewidth):
                    sti = sti + "," + str(tile[0][sx][sy]).replace("\n","")
                if sx != tilewidth-1:
                    sti = sti + ";\n"
            s = "\n"
            for p in tile[1:]:
                s = s + "~" + p
            sti = sti + s
            ftiles[tindex] = sti
        data = ftiles[0]
        for p in ftiles[1:]:
            #print(p)
            data = data + "`" + p
        dataf = "tilemap#%s#%s" % (palette.rstrip(),data)
        #print(dataf)
        f.write(dataf)
        f.close()
        print("SAVED SUCCESSFULLY")
    except Exception:
        f.close()
        f = open(tfile,"w")
        f.write(prev)
        f.close()
        print("SAVE FAILED, RESTORED PREVIOUS FILE CONTENTS")
def Select():
    global editing,tile,tindex,palette,tile,tfile,tpalette,ftiles
    files = glob("Mods/*/*.txt")
    tfiles = []
    for f in files:
        fio = open(f,"r")
        fior = fio.read().replace("\n","").split("#")[0]
        fio.close()
        if "tilemap" in fior.lower():
            tfiles.append(f)
    print("-- tilemaps (%d)" % len(tfiles))
    for t in range(len(tfiles)):
        print(str(t+1) + " - " + tfiles[t])
    t = int(input("Select a file (or type 0 to make a new file): "))
    filer = ""
    if t == -1:
        tfile = input("Please make a new file (with folder path): ")
        file = open(tfile,"w")
        palette = input("File path for palette: ")
        Import_Palette(palette)
        file.write("tilemap#" + palette)
        file.close()
        file = open(tfile,"r")
        filer = file.read()
    else:
        tfile = tfiles[t-1]
        file = open(tfiles[t-1],"r")
        filer = file.read()
        palette = filer.split("#")[1]
        #print(palette)
        Import_Palette(palette)
        ftiles = filer.split("#")[2].split("`")
    print("-- tiles (%d) --" % len(ftiles))
    for ti in range(len(ftiles)):
        print(str(ti+1) + " - " + ftiles[ti].split("~")[1])
    tindex = int(input("Select a tile or type 0 to make a new one"))-1
    if tindex == -1:
        name = input("name yo tile: ")
        start = input("fill with (index): ")
        comma = start + ","
        semi = start + ";"
        tile = ((((comma)*(tilewidth-1))+semi)*(tilewidth-1) + ((comma)*(tilewidth-1))+start) + "~%s" % name
        inp = "yeet"
        while inp != "-1":
            inp = input("add property (or type -1 to finish)")
            if inp == "-1":
                pass
            else:
                tile = tile + "~" + inp
        tile = tile.split("~")
        tile[0] = tile[0].split(";")
        nt = []
        for o in tile[0]:
            nt.append(o.split(","))
        tile[0] = nt
        ftiles.append(tile)
        print(tile)
        tindex = len(ftiles)-1
    else:
        tile = ftiles[tindex].split("~")
        tile[0] = tile[0].split(";")
        nt = []
        for o in tile[0]:
            nt.append(o.split(","))
        tile[0] = nt
    editing = True

tilewidth = 10
x = 200
y = 100
pygame.init()
clock = pygame.time.Clock()
WHITE = (255,255,255)
BLACK = (0,0,0)
Select()
surface = pygame.display.set_mode((x*5,y*5))
pygame.display.set_caption("tilemap editor version " + version)
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                eColour += 1
                if eColour == len(tpalette):
                    eColour = 0
                elif eColour == -1:
                    eColour = 0
            elif event.key == pygame.K_q:
                eColour -= 1
                if eColour == -1:
                    eColour = len(tpalette)-1
            elif event.key == pygame.K_s:
                Save()
            elif event.key == pygame.K_a:
                #abort with save
                Save()
                editing = False
            elif event.key == pygame.K_TAB:
                #abort without save
                editing = False
            elif event.key == pygame.K_DELETE:
                print(ftiles.pop(tindex))
                tindex = -1
                Save()
                editing = False
            elif event.key == pygame.K_t:
                eColour = -1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
    if mouseDown:
        mx,my = pygame.mouse.get_pos()
        if mx < tilewidth*25 and my < tilewidth*25:
            tile[0][mx//25][my//25] = eColour
    if editing:
        for ix in range(len(tile[0])):
            for iy in range(len(tile[0][ix])):
                #print("%s-%s" % (ix,iy))
                c = int(tile[0][ix][iy])
                if c == -1:
                    gfxdraw.box(surface,((ix*25,iy*25),(12,12)),WHITE)
                    gfxdraw.box(surface,((ix*25+13,iy*25+13),(13,13)),WHITE)
                    gfxdraw.box(surface,((ix*25+13,iy*25),(12,12)),BLACK)
                    gfxdraw.box(surface,((ix*25,iy*25+13),(13,13)),BLACK)
                else:
                    c = tpalette[c]
                    gfxdraw.box(surface,((ix*25,iy*25),(25,25)),c)
        for ix in range(11):
            gfxdraw.box(surface,((ix*25,0),(2,250)),(255,0,0))
        for iy in range(11):
            gfxdraw.box(surface,((0,iy*25),(250,2)),(255,0,0))
        if eColour == -1:
            gfxdraw.box(surface,((x*5-25,0),(12,12)),WHITE)
            gfxdraw.box(surface,((x*5-25+13,13),(13,13)),WHITE)
            gfxdraw.box(surface,((x*5-25+13,0),(12,12)),BLACK)
            gfxdraw.box(surface,((x*5-25,13),(13,13)),BLACK)
        else:
            gfxdraw.box(surface,((x*5-25,0),(25,25)),tpalette[eColour])
    else:
        Select()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
print("PROGRAM ENDED")
