import block

class Inventory:
    def __init__(self, *args, **kwargs):
        self.hotbar = [block.BRICK, block.GRASS, block.SAND, block.DIRT, block.PORTAL, block.LAMP]
        
        self.block = self.hotbar[5]