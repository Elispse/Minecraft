import block
from EventDispatcher import BLOCK_CHANGED

class Inventory:
    def __init__(self, dispatcher, *args, **kwargs):
        self.hotbar = [block.PORTAL, block.STONE, block.SPRUCE_WOOD_PLANK, block.BIRCH_WOOD_PLANK, block.JUNGLE_WOOD_PLANK, block.ACACIA_WOOD_PLANK, block.DARK_OAK_WOOD_PLANK]
        self.index = 0
        self.dispatcher = dispatcher

    def set_index(self, index):
        """Set the selected slot index and notify listeners."""
        self.index = index
        self.dispatcher.dispatch_event(BLOCK_CHANGED)

    def get_selected_block(self):
        """Get the block in the currently selected slot."""
        self.dispatcher.dispatch_event(BLOCK_CHANGED)
        return self.hotbar[self.index]