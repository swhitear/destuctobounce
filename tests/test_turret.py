from destructobounce.turret import Turret
from destructobounce.config import Config
from .test_helper import PygameTestCase
import math

class TestTurret(PygameTestCase):
    def setUp(self):
        self.config = Config()
        self.turret = Turret(self.config)

    def test_turret_initialization(self):
        """Test that turret is created with correct initial values"""
        # Should start at center bottom of screen
        expected_x = (self.config.SCREEN_WIDTH - self.turret.width) // 2
        expected_y = self.config.SCREEN_HEIGHT - self.turret.height - 30
        
        self.assertEqual(self.turret.x, expected_x)
        self.assertEqual(self.turret.y, expected_y)
        self.assertEqual(self.turret.pivot_angle, 90)  # Should start pointing up

    def test_movement_left(self):
        """Test that turret moves left correctly"""
        initial_x = self.turret.x
        dt = 0.1  # 100ms
        self.turret.move(Turret.LEFT, dt)
        self.assertTrue(self.turret.x < initial_x)

    def test_movement_right(self):
        """Test that turret moves right correctly"""
        initial_x = self.turret.x
        dt = 0.1  # 100ms
        self.turret.move(Turret.RIGHT, dt)
        self.assertTrue(self.turret.x > initial_x)

    def test_movement_speed(self):
        """Test that movement speed is correct"""
        initial_x = self.turret.x
        dt = 1.0  # 1 second
        self.turret.move(Turret.RIGHT, dt)
        distance = self.turret.x - initial_x
        self.assertEqual(distance, self.turret.speed)

    def test_pivot_left(self):
        """Test that turret pivots left correctly"""
        initial_angle = self.turret.pivot_angle
        self.turret.pivot(Turret.PIVOT_LEFT)
        self.assertTrue(self.turret.pivot_angle > initial_angle)

    def test_pivot_right(self):
        """Test that turret pivots right correctly"""
        initial_angle = self.turret.pivot_angle
        self.turret.pivot(Turret.PIVOT_RIGHT)
        self.assertTrue(self.turret.pivot_angle < initial_angle)

    def test_pivot_angle_limits(self):
        """Test that turret pivot angle stays within limits"""
        # Test left limit
        for _ in range(100):  # More than enough to reach limit
            self.turret.pivot(Turret.PIVOT_LEFT)
        self.assertEqual(self.turret.pivot_angle, self.turret.max_angle)

        # Reset angle
        self.turret.pivot_angle = 90

        # Test right limit
        for _ in range(100):  # More than enough to reach limit
            self.turret.pivot(Turret.PIVOT_RIGHT)
        self.assertEqual(self.turret.pivot_angle, self.turret.min_angle)

    def test_screen_boundary_clamping(self):
        """Test that turret stays within screen boundaries"""
        # Test left boundary
        self.turret.rect.x = -50
        self.turret.clamp_to_screen(self.config.SCREEN_WIDTH)
        self.assertEqual(self.turret.x, 0)

        # Test right boundary
        self.turret.rect.x = self.config.SCREEN_WIDTH + 50
        self.turret.clamp_to_screen(self.config.SCREEN_WIDTH)
        self.assertEqual(self.turret.x + self.turret.width, self.config.SCREEN_WIDTH)

    def test_fire_location(self):
        """Test that fire location is correctly calculated"""
        fire_x, fire_y = self.turret.fire_location()
        expected_x = self.turret.x + self.turret.width // 2
        expected_y = self.turret.y
        self.assertEqual(fire_x, expected_x)
        self.assertEqual(fire_y, expected_y)

    def test_fire_direction(self):
        """Test that fire direction is correctly calculated"""
        # Test straight up (90 degrees)
        self.turret.pivot_angle = 90
        dx, dy = self.turret.fire_direction()
        self.assertAlmostEqual(dx, 0)
        self.assertAlmostEqual(dy, -1)

        # Test 45 degrees
        self.turret.pivot_angle = 45
        dx, dy = self.turret.fire_direction()
        self.assertAlmostEqual(dx, math.cos(math.radians(45)))
        self.assertAlmostEqual(dy, -math.sin(math.radians(45)))

    def test_draw(self):
        """Test that drawing the turret doesn't raise exceptions"""
        import pygame
        surface = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        try:
            self.turret.draw(surface)
        except Exception as e:
            self.fail(f"Drawing turret raised an exception: {e}")