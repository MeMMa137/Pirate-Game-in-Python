class BossSpawner(Sprite):
    def __init__(self, pos, surf, groups, boss_class, spawn_time, data, z=Z_LAYERS['main']):
        super().__init__(pos, surf, groups, z)
        self.rect.topleft = pos
        self.boss_class = boss_class
        self.spawn_time = spawn_time
        self.data = data
        self.boss_spawned = False
        self.spawn_timer = pygame.time.get_ticks()

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if not self.boss_spawned and current_time - self.spawn_timer >= self.spawn_time:
            self.spawn_boss()
            self.boss_spawned = True

    def spawn_boss(self):
        boss_pos = (self.rect.centerx, self.rect.centery)
        boss = self.boss_class(boss_pos, self.groups, self.data)
        self.groups[0].add(boss)
        self.data.ui.show_boss_spawned()  # Funzione per mostrare l'animazione del boss spawn
