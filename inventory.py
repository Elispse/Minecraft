import block

class Inventory:
    def __init__(self, *args, **kwargs):
        self.hotbar = [block.BRICK, block.GRASS, block.SAND, block.DIRT]
        
        self.block = self.hotbar[0]