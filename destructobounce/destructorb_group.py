from destructobounce.destructorb import Destructorb

class DestructorbGroup:
    def __init__(self, config):
        self.orbs = []
        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT
        self.config = config

    def add(self, orb):
        self.orbs.append(orb)

    def new_orb(self, x, y, dx, dy):
        orb = Destructorb(
            (x, y),
            self.config
        )
        orb.speed_x = dx * abs(orb.speed_y)
        orb.speed_y = dy * abs(orb.speed_y)
        self.add(orb)
        return orb

    def update(self):
        for orb in self.orbs:
            orb.update()
        self.orbs = [o for o in self.orbs if o.is_active()]

    def draw(self, surface):
        for orb in self.orbs:
            orb.draw(surface)

    def __iter__(self):
        return iter(self.orbs)