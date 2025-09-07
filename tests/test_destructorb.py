from destructobounce.destructorb import Destructorb
from destructobounce.config import Config
from .test_helper import PygameTestCase

class TestDestructorb(PygameTestCase):
    def setUp(self):
        self.config = Config()
        self.pos = (400, 500)  # Starting position
        self.orb = Destructorb(
            self.pos, 
            self.config,
            max_collisions=3
        )

    def test_destructorb_initialization(self):
        """Test that a destructorb is created with correct initial values"""
        self.assertEqual(self.orb.x, self.pos[0])
        self.assertEqual(self.orb.y, self.pos[1])
        self.assertEqual(self.orb.radius, self.config.ORB_RADIUS)
        self.assertEqual(self.orb.color, self.config.COLOR_WHITE)
        self.assertTrue(self.orb.is_active())
        self.assertEqual(self.orb.collisions, 0)

    def test_destructorb_collision_counting(self):
        """Test that collisions are counted correctly"""
        self.assertEqual(self.orb.collisions, 0)
        
        # Single collision with default cost
        self.orb.collide(1)
        self.assertEqual(self.orb.collisions, 1)
        self.assertTrue(self.orb.is_active())

        # Multiple collisions accumulate
        self.orb.collide(1)
        self.assertEqual(self.orb.collisions, 2)
        self.assertTrue(self.orb.is_active())

    def test_destructorb_variable_collision_cost(self):
        """Test that collision costs are summed correctly"""
        self.assertEqual(self.orb.collisions, 0)
        
        # Test different collision costs
        self.orb.collide(2)  # Cost of 2
        self.assertEqual(self.orb.collisions, 2)
        
        self.orb.collide(3)  # Additional cost of 3
        self.assertEqual(self.orb.collisions, 5)

    def test_destructorb_max_collisions(self):
        """Test that destructorb deactivates after max collisions"""
        orb = Destructorb(
            self.pos, 
            self.config,
            max_collisions=6
        )
        
        # Test progressive collisions
        orb.collide(2)  # Cost of 2
        self.assertEqual(orb.collisions, 2)
        self.assertTrue(orb.is_active())
        
        orb.collide(3)  # Additional cost of 3
        self.assertEqual(orb.collisions, 5)
        self.assertTrue(orb.is_active())
        
        orb.collide(1)  # Final cost of 1, should deactivate
        self.assertEqual(orb.collisions, 6)
        self.assertFalse(orb.is_active())

    def test_destructorb_boundary_movement(self):
        """Test that the destructorb bounces off screen boundaries without counting collisions"""
        initial_collisions = self.orb.collisions
        
        # Test left boundary
        self.orb.x = self.orb.radius
        self.orb.speed_x = -5
        self.orb.update()
        self.assertTrue(self.orb.speed_x > 0)  # Should have reversed direction
        self.assertEqual(self.orb.collisions, initial_collisions)  # Collisions shouldn't change

        # Test right boundary
        self.orb.x = self.config.SCREEN_WIDTH - self.orb.radius
        self.orb.speed_x = 5
        self.orb.update()
        self.assertTrue(self.orb.speed_x < 0)
        self.assertEqual(self.orb.collisions, initial_collisions)

        # Test top boundary
        self.orb.y = self.orb.radius
        self.orb.speed_y = -5
        self.orb.update()
        self.assertTrue(self.orb.speed_y > 0)
        self.assertEqual(self.orb.collisions, initial_collisions)

    def test_draw_destructorb(self):
        """Test that drawing the destructorb doesn't raise exceptions"""
        import pygame
        surface = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        try:
            self.orb.draw(surface)
        except Exception as e:
            self.fail(f"Drawing destructorb raised an exception: {e}")

    def test_rect_updates_with_position(self):
        """Test that the rect attribute updates correctly with position"""
        self.orb.x = 100
        self.orb.y = 100
        self.orb.update_rect()  # Use update_rect instead of update
        self.assertEqual(self.orb.rect.center, (100, 100))

    def test_movement_with_speed(self):
        """Test that speed correctly affects position over multiple updates"""
        self.orb.x = 100
        self.orb.y = 100
        self.orb.speed_x = 5
        self.orb.speed_y = -3
        
        # Track movement over multiple updates
        expected_positions = [
            (105, 97),   # First update
            (110, 94),   # Second update
            (115, 91)    # Third update
        ]
        
        for expected_x, expected_y in expected_positions:
            self.orb.update()
            self.assertEqual(self.orb.x, expected_x)
            self.assertEqual(self.orb.y, expected_y)

    def test_boundary_bounce_preserves_speed_magnitude(self):
        """Test that bouncing preserves the magnitude of speed"""
        # Test horizontal bounce
        self.orb.x = self.config.SCREEN_WIDTH - self.orb.radius
        self.orb.speed_x = 5
        initial_speed = abs(self.orb.speed_x)
        self.orb.update()
        self.assertEqual(abs(self.orb.speed_x), initial_speed)
        
        # Test vertical bounce
        self.orb.y = self.orb.radius
        self.orb.speed_y = -5
        initial_speed = abs(self.orb.speed_y)
        self.orb.update()
        self.assertEqual(abs(self.orb.speed_y), initial_speed)

    def test_bottom_screen_deactivation(self):
        """Test that moving below screen deactivates the orb"""
        self.orb.y = self.config.SCREEN_HEIGHT - self.orb.radius
        self.orb.speed_y = 5
        self.assertTrue(self.orb.is_active())
        
        # Move past bottom edge
        self.orb.update()
        self.assertFalse(self.orb.is_active())

    def test_diagonal_boundary_bounce(self):
        """Test that the orb bounces correctly when hitting corners"""
        self.orb.x = self.orb.radius
        self.orb.y = self.orb.radius
        self.orb.speed_x = -5
        self.orb.speed_y = -5
        
        # Should bounce off both top and left boundaries
        self.orb.update()
        self.assertTrue(self.orb.speed_x > 0)
        self.assertTrue(self.orb.speed_y > 0)

    def test_continuous_movement_within_bounds(self):
        """Test that normal movement within boundaries works as expected"""
        start_x = self.config.SCREEN_WIDTH // 2
        start_y = self.config.SCREEN_HEIGHT // 2
        self.orb.x = start_x
        self.orb.y = start_y
        self.orb.speed_x = 3
        self.orb.speed_y = 4
        
        # Movement should continue normally when within bounds
        for _ in range(5):
            prev_x = self.orb.x
            prev_y = self.orb.y
            self.orb.update()
            self.assertEqual(self.orb.x, prev_x + self.orb.speed_x)
            self.assertEqual(self.orb.y, prev_y + self.orb.speed_y)