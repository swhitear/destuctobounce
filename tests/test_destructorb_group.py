from destructobounce.destructorb_group import DestructorbGroup
from destructobounce.destructorb import Destructorb
from destructobounce.config import Config
from .test_helper import PygameTestCase

class TestDestructorbGroup(PygameTestCase):
    def setUp(self):
        self.config = Config()
        self.group = DestructorbGroup(self.config)

    def test_group_initialization(self):
        """Test that a new group starts empty"""
        self.assertEqual(len(list(self.group)), 0)

    def test_add_orb(self):
        """Test that orbs can be added to the group"""
        orb = Destructorb((100, 100), self.config)
        self.group.add(orb)
        self.assertEqual(len(list(self.group)), 1)

    def test_new_orb(self):
        """Test that new_orb creates and adds an orb with correct parameters"""
        orb = self.group.new_orb(
            x=100,
            y=200,
            dx=0.5,
            dy=-0.5
        )
        
        self.assertEqual(orb.x, 100)
        self.assertEqual(orb.y, 200)
        self.assertEqual(len(list(self.group)), 1)
        self.assertTrue(orb in self.group)

    def test_update_removes_defunct_orbs(self):
        """Test that update removes orbs that are defunct"""
        # Add an orb and make it defunct
        orb = Destructorb((100, 100), self.config, max_collisions=1)
        self.group.add(orb)
        orb.collide(1)  # Make it defunct
        
        # Update should remove defunct orbs
        self.group.update()
        self.assertEqual(len(list(self.group)), 0)

    def test_multiple_orbs(self):
        """Test that multiple orbs can be managed"""
        # Add several orbs
        positions = [(100, 100), (200, 200), (300, 300)]
        for pos in positions:
            self.group.new_orb(pos[0], pos[1], 0, -1)

        self.assertEqual(len(list(self.group)), len(positions))

    def test_draw_group(self):
        """Test that drawing the group doesn't raise exceptions"""
        import pygame
        surface = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        
        # Add a few orbs
        self.group.new_orb(100, 100, 0, -1)
        self.group.new_orb(200, 200, 1, 0)
        
        try:
            self.group.draw(surface)
        except Exception as e:
            self.fail(f"Drawing group raised an exception: {e}")

    def test_iteration(self):
        """Test that the group can be iterated over"""
        # Add some orbs
        orbs = [
            self.group.new_orb(100, 100, 0, -1),
            self.group.new_orb(200, 200, 1, 0),
            self.group.new_orb(300, 300, -1, 0)
        ]
        
        # Test iteration
        for i, orb in enumerate(self.group):
            self.assertEqual(orb, orbs[i])

    def test_orb_speed_direction(self):
        """Test that new orbs are created with correct speed and direction"""
        dx, dy = 0.6, -0.8  # Normalized direction vector
        orb = self.group.new_orb(100, 100, dx, dy)
        
        # Check that speed components are proportional to direction
        self.assertAlmostEqual(abs(orb.speed_x / orb.speed_y), abs(dx / dy))

    def test_batch_update(self):
        """Test that updating the group updates all orbs"""
        orbs = [
            self.group.new_orb(100, 100, 1, 0),
            self.group.new_orb(200, 200, 0, 1),
            self.group.new_orb(300, 300, -1, 0)
        ]
        
        initial_positions = [(orb.x, orb.y) for orb in orbs]
        self.group.update()
        
        # Verify all orbs have moved
        for orb, (initial_x, initial_y) in zip(orbs, initial_positions):
            self.assertNotEqual((orb.x, orb.y), (initial_x, initial_y))