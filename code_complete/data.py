class Data:
	def __init__(self, ui):
		self.ui = ui
		self._coins = 0
		self._health = 5
		self.ui.create_hearts(self._health)
		self.unlocked_level = 0
		self.current_level = 0
		self.inventory = {}
		self._experience = 0
		self._level = 1
		self._weapon = None

	@property
	def coins(self):
		return self._coins

	@coins.setter
	def coins(self, value):
		self._coins = value
		if self.coins >= 100:
			self.coins -= 100
			self.health += 1
		self.ui.show_coins(self.coins)

	@property
	def health(self):
		return self._health

	@health.setter
	def health(self, value):
		self._health = value
		self.ui.create_hearts(value)

	@property
	def experience(self):
		return self._experience

	@experience.setter
	def experience(self, value):
		self._experience = value
		if self._experience >= 100:
			self._experience -= 100
			self.level += 1
		self.ui.show_experience(self._experience)

	@property
	def level(self):
		return self._level

	@level.setter
	def level(self, value):
		self._level = value
		self.ui.show_level(self._level)

	@property
	def weapon(self):
		return self._weapon

	@weapon.setter
	def weapon(self, value):
		self._weapon = value
		self.ui.show_weapon(self._weapon)

	def add_to_inventory(self, item, quantity=1):
		if item in self.inventory:
			self.inventory[item] += quantity
		else:
			self.inventory[item] = quantity
		self.ui.update_inventory(self.inventory)

	def attack(self, target):
		if self.weapon:
			damage = self.weapon.damage
			target.health -= damage
			self.ui.show_attack(self.weapon, damage)
		else:
			self.ui.show_no_weapon()
