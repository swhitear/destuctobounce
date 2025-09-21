from destructobounce.block_gen import BlockGen
class BlockPile:
    def __init__(self, config, block_gen:BlockGen=None):
        self.block_gen = block_gen
        self.blocks = self.block_gen.generate()

    def update(self):
        """Update all blocks and remove defunct ones"""
        for block in self.blocks:
            block.update()
        # Remove defunct blocks
        self.blocks = [block for block in self.blocks if block.is_active()]

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)

    def __iter__(self):
        return iter(self.blocks)