from destructobounce.block import Block
from destructobounce.config import Config
from .test_helper import PygameTestCase

class TestBlock(PygameTestCase):
    def setUp(self):
        self.config = Config()
        self.x = 100
        self.y = 100
        self.block = Block(self.x, self.y, self.config)

    def test_block_initialization(self):
        """Test that a block is created with correct initial values"""
        self.assertEqual(self.block.rect.x, self.x)
        self.assertEqual(self.block.rect.y, self.y)
        self.assertEqual(self.block.rect.width, self.config.BLOCK_WIDTH)
        self.assertEqual(self.block.rect.height, self.config.BLOCK_HEIGHT)
        self.assertEqual(self.block.color, self.config.COLOR_GREY)
        self.assertEqual(self.block.collisions, 0)
        self.assertTrue(self.block.is_active())

    def test_block_collision_counting(self):
        """Test that collisions are counted correctly"""
        self.block.collide(1)
        self.assertEqual(self.block.collisions, 1)
        self.block.collide(1)
        self.assertEqual(self.block.collisions, 2)

    def test_block_becomes_defunct_at_max_collisions(self):
        """Test that block becomes defunct when collisions reach max_collisions"""
        max_collisions = 3
        block = Block(self.x, self.y, self.config, max_collisions=max_collisions)
        
        # Block should be active before reaching max collisions
        for i in range(max_collisions - 1):
            block.collide(1)
            self.assertTrue(block.is_active())
            
        # Block should become defunct after reaching max collisions
        block.collide(1)
        self.assertFalse(block.is_active())

    def test_block_collision_cost(self):
        """Test that collision cost affects collision count correctly"""
        block = Block(self.x, self.y, self.config, max_collisions=6, collision_cost=2)
        block.collide(block.collision_cost)
        self.assertEqual(block.collisions, 2)
        self.assertTrue(block.is_active())
        
        block.collide(block.collision_cost)
        self.assertEqual(block.collisions, 4)
        self.assertTrue(block.is_active())
        
        block.collide(block.collision_cost)
        self.assertEqual(block.collisions, 6)
        self.assertFalse(block.is_active())

    def test_draw_active_block(self):
        """Test that drawing an active block doesn't raise exceptions"""
        import pygame
        surface = pygame.Surface((200, 200))
        try:
            self.block.draw(surface)
        except Exception as e:
            self.fail(f"Drawing active block raised an exception: {e}")

    def test_draw_defunct_block(self):
        """Test that drawing a defunct block doesn't raise exceptions"""
        import pygame
        surface = pygame.Surface((200, 200))
        self.block.collisions = self.block.max_collisions  # Make block defunct
        try:
            self.block.draw(surface)
        except Exception as e:
            self.fail(f"Drawing defunct block raised an exception: {e}")