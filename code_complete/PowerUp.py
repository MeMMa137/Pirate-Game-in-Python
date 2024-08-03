class Powerup(Sprite):
    def __init__(self, pos, power_type, surf, groups, data, z=Z_LAYERS['main']):
        super().__init__(pos, surf, groups, z)
        self.power_type = power_type
        self.data = data

    def activate(self):
        if self.power_type == 'speed':
            self.data.speed += 1
        elif self.power_type == 'strength':
            self.data.strength += 1
        elif self.power_type == 'shield':
            self.data.shield += 1
        elif self.power_type == 'health':
            self.data.health += 1

    def update(self, dt):
        if self.rect.colliderect(self.data.player.rect):
            self.activate()
            self.kill()
