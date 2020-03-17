from pygame import gfxdraw
# element-138 rendering library
version = "h-1"
# screen data (surface,pixel_size)
def Load_Tilemap(tilemap):
    pass
def Draw(screen,tile,palette,x,y):
    size = screen[1]
    ps = screen[1]
    for ix in range(len(tile)):
        for iy in range(len(tile[ix])):
            c = palette[1][tile[ix][iy]]
            if not c == -1:
                pos = ((x+ix)*ps,(y+iy)*ps)
                gfxdraw.box(screen[0],(pos,(size)
def Get_IndexFromTilemap(names,tilemap):
    indexes = []
    for name in names:
        if name == " ":
            indexes.append(-1)
            continue
        for t in range(len(tilemap)):
            if tilemap_properties[index][t][0].lower() == name:
                indexes.append(t)
                break
    return indexes
def String_ToIndexes(string):
    return 
def Text(screen,text,tilemap,colour,posx,posy):
    indexes = 
    return total_length
def Bar(screen,sx,sy,ex,h,colour,progress):
    pass
