from .block_gen import BlockGen
from .block import Block

class WallBlockGen(BlockGen):
    def __init__(self, config, row_count=2):
        super().__init__(config)
        self.row_count = row_count

    def generate(self):
        """Generate a wall of blocks across the screen"""
        blocks = []
        cols = self.config.SCREEN_WIDTH // (self.config.BLOCK_WIDTH + self.config.BLOCK_PADDING)
        
        for row in range(self.row_count):
            y = 20 + row * (self.config.BLOCK_HEIGHT + self.config.BLOCK_PADDING)
            for col in range(cols):
                x = col * (self.config.BLOCK_WIDTH + self.config.BLOCK_PADDING)
                blocks.append(
                    Block(
                        x, y,
                        config=self.config,
                        color=None,
                        max_collisions=abs(self.row_count-row),
                        collision_cost=1
                    )
                )
        return blocks