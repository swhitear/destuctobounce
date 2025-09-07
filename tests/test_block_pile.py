import unittest
import pygame
from destructobounce.block_pile import BlockPile
from destructobounce.config import Config
from .test_helper import PygameTestCase

class TestBlockPile(PygameTestCase):
    def setUp(self):
        self.config = Config()
        self.block_pile = BlockPile(self.config)

    def test_block_pile_creation(self):
        # Test that the block pile is created with the correct number of blocks
        expected_cols = self.config.SCREEN_WIDTH // (self.config.BLOCK_WIDTH + self.config.BLOCK_PADDING)
        expected_blocks = 2 * expected_cols  # Two rows
        self.assertEqual(len(self.block_pile.blocks), expected_blocks)

    def test_block_pile_blocks_have_correct_attributes(self):
        # Test that each block in the pile has the correct attributes
        for block in self.block_pile:
            self.assertEqual(block.rect.width, self.config.BLOCK_WIDTH)
            self.assertEqual(block.rect.height, self.config.BLOCK_HEIGHT)

    def test_block_pile_draw(self):
        # Test that the draw method does not raise an exception
        try:
            import pygame
            surface = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            self.block_pile.draw(surface)
        except Exception as e:
            self.fail(f"draw() raised an exception: {e}")

    def test_update_removes_defunct_blocks(self):
        """Test that update removes blocks that are defunct"""
        initial_count = len(self.block_pile.blocks)
        target_blocks = self.block_pile.blocks[:3]  # Get first three blocks
        
        # Make these blocks defunct
        for block in target_blocks:
            block.collide(block.max_collisions)
            
        self.block_pile.update()
        
        # Check that exactly three blocks were removed
        self.assertEqual(len(self.block_pile.blocks), initial_count - 3)
        # Verify those specific blocks are gone
        for block in target_blocks:
            self.assertNotIn(block, self.block_pile.blocks)

    def test_update_keeps_active_blocks(self):
        """Test that update retains blocks that are still active"""
        initial_blocks = list(self.block_pile.blocks)
        
        # Make only some blocks defunct
        for block in initial_blocks[:2]:
            block.collide(block.max_collisions)
            
        self.block_pile.update()
        
        # Check that active blocks remain
        for block in initial_blocks[2:]:
            self.assertIn(block, self.block_pile.blocks)

    def test_update_with_partial_damage(self):
        """Test that update doesn't remove blocks that are damaged but not defunct"""
        initial_count = len(self.block_pile.blocks)
        
        # Damage but don't destroy some blocks
        for block in self.block_pile.blocks[:3]:
            block.collide(block.max_collisions - 1)  # One hit away from defunct
            
        self.block_pile.update()
        
        # Should still have all blocks
        self.assertEqual(len(self.block_pile.blocks), initial_count)

    def test_update_empty_pile(self):
        """Test that update handles an empty block pile correctly"""
        # Clear all blocks
        self.block_pile.blocks = []
        
        # Should not raise any exceptions
        try:
            self.block_pile.update()
            self.assertEqual(len(self.block_pile.blocks), 0)
        except Exception as e:
            self.fail(f"update() raised an exception with empty pile: {e}")

    def test_blocks_update_called(self):
        """Test that update calls update on each block"""
        # Create a block pile with a test block that tracks update calls
        class TestBlock:
            def __init__(self):
                self.update_called = False
                self.active = True
            
            def update(self):
                self.update_called = True
                
            def is_active(self):
                return self.active

        test_block = TestBlock()
        self.block_pile.blocks = [test_block]
        
        self.block_pile.update()
        self.assertTrue(test_block.update_called)

if __name__ == '__main__':
    unittest.main()