class Trap(Sprite):
    def __init__(self, pos, trap_type, surf, groups, data, z=Z_LAYERS['main']):
        super().__init__(pos, surf, groups, z)
        self.trap_type = trap_type
        self.data = data
        self.active = False

    def activate(self):
        if self.trap_type == 'spike':
            self.data.health -= 2
        elif self.trap_type == 'fire':
            self.data.health -= 3
        elif self.trap_type == 'poison':
            self.data.health -= 1
            self.data.poisoned = True

    def update(self, dt):
        if self.rect.colliderect(self.data.player.rect):
            if not self.active:
                self.activate()
                self.active = True
