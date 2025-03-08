import block

class Inventory:
    def __init__(self, *args, **kwargs):
        self.hotbar = [block.DIRT, block.GRASS_BLOCK, block.SAND, block.DIRT, block.PORTAL, block.LAMP]
        
        self.block = self.hotbar[0]