import block
from EventDispatcher import BLOCK_CHANGED

class Inventory:
    def __init__(self, dispatcher, *args, **kwargs):
        self.hotbar = [block.STONE, block.SPRUCE_WOOD_PLANK, block.BIRCH_WOOD_PLANK, block.JUNGLE_WOOD_PLANK, block.ACACIA_WOOD_PLANK, block.DARK_OAK_WOOD_PLANK]
        self.dispatcher = dispatcher
        self.block = self.hotbar[0]
    
    def change_block(self):
        self.dispatcher.dispatch_event(BLOCK_CHANGED)