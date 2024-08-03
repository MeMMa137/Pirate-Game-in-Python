class Portal(Sprite):
    def __init__(self, pos, destination, surf, groups, data, z=Z_LAYERS['main']):
        super().__init__(pos, surf, groups, z)
        self.destination = destination
        self.data = data

    def activate(self):
        self.data.player_pos = self.destination

    def update(self, dt):
        if self.rect.colliderect(self.data.player.rect):
            self.activate()
