import unittest
from destructobounce.block import Block
from destructobounce.block_gen import BlockGen
from destructobounce.block_pile import BlockPile
from destructobounce.config import Config
from destructobounce.wall_block_gen import WallBlockGen
from .test_helper import PygameTestCase

class TestBlockPile(PygameTestCase):
    def setUp(self):
        self.config = Config()
        
    def test_custom_generator(self):
        """Test that BlockPile accepts custom generator"""
        block_pile = BlockPile(self.config, TestGenerator(self.config))
        self.assertEqual(len(block_pile.blocks), 1)
        block_pile = BlockPile(self.config, TestGenerator2(self.config))
        self.assertEqual(len(block_pile.blocks), 2)

    def test_block_pile_update(self):
        """Test that update removes defunct blocks"""
        self.default_instance()
        initial_count = len(self.block_pile.blocks)
        
        # Make some blocks defunct
        for block in list(self.block_pile.blocks)[:3]:
            for _ in range(block.max_collisions):
                block.collide(1)
        
        self.block_pile.update()
        
        # Should have 3 fewer blocks
        self.assertEqual(len(self.block_pile.blocks), initial_count - 3)
        # All remaining blocks should be active
        self.assertTrue(all(block.is_active() for block in self.block_pile))

    def test_block_pile_draw(self):
        """Test that drawing doesn't raise exceptions"""
        import pygame
        surface = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        self.default_instance()
        try:
            self.block_pile.draw(surface)
        except Exception as e:
            self.fail(f"Drawing block pile raised an exception: {e}")

    def test_block_pile_iteration(self):
        """Test that BlockPile supports iteration"""
        self.default_instance()
        blocks = list(self.block_pile)
        self.assertEqual(len(blocks), len(self.block_pile.blocks))
        for block in self.block_pile:
            self.assertIn(block, self.block_pile.blocks)

    def default_instance(self):
        self.test_gen = WallBlockGen(self.config, row_count=2)
        self.block_pile = BlockPile(self.config, self.test_gen)
    
class TestGenerator(BlockGen):
    def generate(self):
        return [Block(0, 0, self.config)]  # Single block

class TestGenerator2(BlockGen):
    def generate(self):
        return [Block(0, 0, self.config), Block(0, 0, self.config)]  # Two block

if __name__ == '__main__':
    unittest.main()