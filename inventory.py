import block

class Inventory:
    def __init__(self, *args, **kwargs):
        self.hotbar = [block.WOOD_PLANK, block.DIRT, block.GRASS_BLOCK, block.SAND, block.PORTAL, block.LAMP]
        
        self.block = self.hotbar[0]