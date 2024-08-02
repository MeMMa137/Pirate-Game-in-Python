class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf=pygame.Surface((TILE_SIZE, TILE_SIZE)), groups=None, z=Z_LAYERS['main'], rotation_angle=0):
		super().__init__(groups)
		self.image = pygame.transform.rotate(surf, rotation_angle)
		self.rect = self.image.get_frect(topleft=pos)
		self.old_rect = self.rect.copy()
		self.z = z
		self.opacity = 255

	def set_opacity(self, value):
		self.opacity = value
		self.image.set_alpha(self.opacity)

	def scale(self, scale_factor):
		width = int(self.image.get_width() * scale_factor)
		height = int(self.image.get_height() * scale_factor)
		self.image = pygame.transform.scale(self.image, (width, height))
		self.rect = self.image.get_frect(topleft=self.rect.topleft)

	def rotate(self, angle):
		self.image = pygame.transform.rotate(self.image, angle)
		self.rect = self.image.get_frect(center=self.rect.center)

class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups, z=Z_LAYERS['main'], animation_speed=ANIMATION_SPEED, loop=True):
		self.frames, self.frame_index = frames, 0
		super().__init__(pos, self.frames[self.frame_index], groups, z)
		self.animation_speed = animation_speed
		self.loop = loop

	def animate(self, dt):
		self.frame_index += self.animation_speed * dt
		if self.loop:
			self.image = self.frames[int(self.frame_index % len(self.frames))]
		else:
			if self.frame_index < len(self.frames):
				self.image = self.frames[int(self.frame_index)]
			else:
				self.kill()

	def set_animation_speed(self, speed):
		self.animation_speed = speed

class Item(AnimatedSprite):
	def __init__(self, item_type, pos, frames, groups, data, collect_sound=None):
		super().__init__(pos, frames, groups)
		self.rect.center = pos
		self.item_type = item_type
		self.data = data
		self.collect_sound = collect_sound

def activate(self):
		if self.item_type == 'gold':
			self.data.coins += 5
		elif self.item_type == 'silver':
			self.data.coins += 1
		elif self.item_type == 'diamond':
			self.data.coins += 20
		elif self.item_type == 'skull':
			self.data.coins += 50
		elif self.item_type == 'potion':
			self.data.health += 1
		if self.collect_sound:
			self.collect_sound.play()

	def update(self, dt):
		super().update(dt)