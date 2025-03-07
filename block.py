def tex_coord(x, y, n=16):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

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
GRASS = tex_coords((0, 15), (2, 15), (3, 15))
STONE = tex_coords((1, 15), (1, 15), (1, 15))
DIRT = tex_coords((2, 15), (2, 15), (2, 15))
BRICK = tex_coords((7, 15), (7, 15), (7, 15))
WOOD_PLANK = tex_coords((4, 15), (4, 15), (4, 15))
#Row 2
SAND = tex_coords((2, 14), (2, 14), (2, 14))
#Row 5
LAMP = tex_coords((12, 11), (12, 11), (12, 11))
PORTAL = tex_coords((13, 11), (13, 11), (13, 11))