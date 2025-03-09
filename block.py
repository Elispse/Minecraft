def tex_coord(x, y, w=32, h=16):
    """ Return the bounding vertices of the texture square.

    """
    width = 1.0 / w
    height = 1.0 / h
    dx = x * width
    dy = y * height
    return dx, dy, dx + width, dy, dx + width, dy + height, dx, dy + height

def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

#Row 1
STONE = tex_coords((19, 15), (19, 15), (19, 15)) #correct
GRASS_BLOCK = tex_coords((2, 15), (18, 14), (3, 15)) #correct
DIRT = tex_coords((18, 14), (18, 14), (18, 14)) #correct
BRICK = tex_coords((29, 14), (29, 14), (29, 14)) #correct
WOOD_PLANK = tex_coords((21, 14), (21, 14), (21, 14)) # fixed
#Row 2
SAND = tex_coords((5, 14), (5, 14), (5, 14)) #fixed
#Row 5
LAMP = tex_coords((25, 7), (25, 7), (25, 7)) #fixed 
PORTAL = tex_coords((26, 6), (26, 6), (26, 6)) #fixed

