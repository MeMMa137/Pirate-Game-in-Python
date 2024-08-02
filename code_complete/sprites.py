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


class MovingSprite(AnimatedSprite):
	def __init__(self, frames, groups, start_pos, end_pos, move_dir, speed, flip=False, bounce=False):
		super().__init__(start_pos, frames, groups)
		if move_dir == 'x':
			self.rect.midleft = start_pos
		else:
			self.rect.midtop = start_pos

		self.start_pos = start_pos
		self.end_pos = end_pos
		self.speed = speed
		self.direction = vector(1, 0) if move_dir == 'x' else vector(0, 1)
		self.move_dir = move_dir
		self.flip = flip
		self.bounce = bounce
		self.reverse = {'x': False, 'y': False}

	def check_border(self):
		if self.move_dir == 'x':
			if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
				self.direction.x = -1
				self.rect.right = self.end_pos[0]
			if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
				self.direction.x = 1
				self.rect.left = self.start_pos[0]
			self.reverse['x'] = True if self.direction.x < 0 else False
		else:
			if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
				self.direction.y = -1
				self.rect.bottom = self.end_pos[1]
			if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
				self.direction.y = 1
				self.rect.top = self.start_pos[1]
			self.reverse['y'] = True if self.direction.y > 0 else False

	def update(self, dt):
		self.old_rect = self.rect.copy()
		self.rect.topleft += self.direction * self.speed * dt
		self.check_border()
		self.animate(dt)
		if self.flip:
			self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])
		if self.bounce:
			self.rect.topleft -= self.direction * self.speed * dt


class Spike(Sprite):
	def __init__(self, pos, surf, groups, radius, speed, start_angle, end_angle, z=Z_LAYERS['main'],
				 color_change=False):
		self.center = pos
		self.radius = radius
		self.speed = speed
		self.start_angle = start_angle
		self.end_angle = end_angle
		self.angle = self.start_angle
		self.direction = 1
		self.full_circle = True if self.end_angle == -1 else False
		self.color_change = color_change
		super().__init__(self.calculate_position(), surf, groups, z)

		def calculate_position(self):
			y = self.center[1] + sin(radians(self.angle)) * self.radius
			x = self.center[0] + cos(radians(self.angle)) * self.radius
			return (x, y)

		def update(self, dt):
			self.angle += self.direction * self.speed * dt
			if not self.full_circle:
				if self.angle >= self.end_angle:
					self.direction = -1
				if self.angle < self.start_angle:
					self.direction = 1
			self.rect.center = self.calculate_position()
			if self.color_change:
				color = (255 * abs(sin(radians(self.angle))), 255 * abs(cos(radians(self.angle))), 255)
				self.image.fill(color, special_flags=pygame.BLEND_RGB_ADD)