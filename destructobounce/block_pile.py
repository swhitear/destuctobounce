from .block import Block

class BlockPile:
    def __init__(self, config):
        self.blocks = []
        self.row_count = 2
        cols = config.SCREEN_WIDTH // (config.BLOCK_WIDTH + config.BLOCK_PADDING)
        for row in range(self.row_count):
            y = 20 + row * (config.BLOCK_HEIGHT + config.BLOCK_PADDING)
            for col in range(cols):
                x = col * (config.BLOCK_WIDTH + config.BLOCK_PADDING)
                self.blocks.append(Block(x, y, config=config, color=None, max_collisions=abs(self.row_count-row), collision_cost=1))

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