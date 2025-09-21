from destructobounce.wall_block_gen import WallBlockGen
from destructobounce.config import Config
from .test_helper import PygameTestCase

class TestWallBlockGen(PygameTestCase):
    def setUp(self):
        self.config = Config()
        self.wall_gen = WallBlockGen(self.config, row_count=2)

    def test_wall_block_generation(self):
        """Test that wall generator creates correct number of blocks"""
        blocks = self.wall_gen.generate()
        expected_cols = self.config.SCREEN_WIDTH // (self.config.BLOCK_WIDTH + self.config.BLOCK_PADDING)
        expected_blocks = expected_cols * self.wall_gen.row_count
        self.assertEqual(len(blocks), expected_blocks)

    def test_wall_block_positions(self):
        """Test that blocks are positioned correctly"""
        blocks = self.wall_gen.generate()
        
        # Test first row
        first_row = blocks[:self.config.SCREEN_WIDTH // (self.config.BLOCK_WIDTH + self.config.BLOCK_PADDING)]
        for i, block in enumerate(first_row):
            expected_x = i * (self.config.BLOCK_WIDTH + self.config.BLOCK_PADDING)
            self.assertEqual(block.rect.x, expected_x)
            self.assertEqual(block.rect.y, 20)

    def test_wall_block_collision_values(self):
        """Test that blocks have correct collision values based on row"""
        blocks = self.wall_gen.generate()
        cols = self.config.SCREEN_WIDTH // (self.config.BLOCK_WIDTH + self.config.BLOCK_PADDING)
        
        # First row should have max_collisions = 2
        for block in blocks[:cols]:
            self.assertEqual(block.max_collisions, 2)
            
        # Second row should have max_collisions = 1
        for block in blocks[cols:]:
            self.assertEqual(block.max_collisions, 1)