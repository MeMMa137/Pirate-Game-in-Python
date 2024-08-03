class Companion(AnimatedSprite):
    def __init__(self, pos, frames, groups, player, speed=150, follow_distance=50, z=Z_LAYERS['main']):
        super().__init__(pos, frames, groups, z)
        self.player = player
        self.speed = speed
        self.follow_distance = follow_distance
        self.state = 'idle'

    def follow_player(self, dt):
        distance = self.player.rect.center - self.rect.center
        distance_length = distance.length()

        if distance_length > self.follow_distance:
            self.state = 'move'
            direction = distance.normalize()
            self.rect.center += direction * self.speed * dt
        else:
            self.state = 'idle'

    def attack_nearby_enemies(self):
        for sprite in self.groups[0]:
            if isinstance(sprite, Enemy) and self.rect.colliderect(sprite.rect):
                sprite.health -= 1
                self.ui.show_companion_attack(sprite)

    def get_state(self):
        if self.state == 'move':
            self.image = self.frames['move'][int(self.frame_index % len(self.frames['move']))]
        else:
            self.image = self.frames['idle'][int(self.frame_index % len(self.frames['idle']))]

    def update(self, dt):
        self.follow_player(dt)
        self.attack_nearby_enemies()
        self.get_state()
        self.animate(dt)