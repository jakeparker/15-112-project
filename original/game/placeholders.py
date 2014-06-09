
import pygame
import numpy

def load_image(fileName, pathway):
	pathway = '/Users/Jake/CMU/15-112/TermProject/original' + pathway
	return pygame.image.load(pathway + fileName + '.png')

class SA_X(pygame.sprite.Sprite):
	def __init__(self, main, fps=15):
		self.groups = main.LayeredUpdate, main.enemyGroup
		self._layer = 2
		super(SA_X, self).__init__(self.groups)
		self.main = main
		self.screen = main.screen
		self.state = "sa-x_death_4"
		self.pathway = "/sprites/sa-x_mutant/"
		self.image = load_image(self.state, self.pathway)
		self.load_rects()
		self.hitmask = pygame.surfarray.array_alpha(self.image)
		self.init_attributes()

	def init_attributes(self):
		self.healthPts = 500
		self.attackPts = 0

	def load_rects(self):
		self.rect = self.image.get_rect()
		self.rect.left += 2052
		self.rect.top += 392

	def damaged(self, weapon, amount):
		self.healthPts -= amount

	def updateHealth(self):
		if (self.healthPts <= 0):
			self.main.LayeredUpdate.remove(self)
			self.main.enemyGroup.remove(self)


class Mecha_Ridley(pygame.sprite.Sprite):
	def __init__(self, main, fps=15):
		self.groups = main.LayeredUpdate, main.enemyGroup
		self._layer = 2
		super(Mecha_Ridley, self).__init__(self.groups)
		self.main = main
		self.screen = main.screen
		self.state = "claw_0"

		self.pathway = "/sprites/mecha-ridley/"
		self.image = load_image(self.state, self.pathway)
		self.load_rects()
		self.hitmask = pygame.surfarray.array_alpha(self.image)
		self.init_attributes()

	def init_attributes(self):
		self.healthPts = 500
		self.attackPts = 0

	def load_rects(self):
		self.rect = self.image.get_rect()
		self.rect.left += 2533
		self.rect.top += 188

	def damaged(self, weapon, amount):
		self.healthPts -= amount

	def updateHealth(self):
		if (self.healthPts <= 0):
			self.main.LayeredUpdate.remove(self)
			self.main.enemyGroup.remove(self)


class Omega_Metroid(pygame.sprite.Sprite):
	def __init__(self, main, fps=15):
		self.groups = main.LayeredUpdate, main.enemyGroup
		self._layer = 2
		super(Omega_Metroid, self).__init__(self.groups)
		self.main = main
		self.screen = main.screen
		self.state = "placeholder"
		self.pathway = "/sprites/omega_metroid/"
		self.image = load_image(self.state, self.pathway)
		self.load_rects()
		self.hitmask = pygame.surfarray.array_alpha(self.image)
		self.init_attributes()

	def init_attributes(self):
		self.healthPts = 500
		self.attackPts = 0

	def load_rects(self):
		self.rect = self.image.get_rect()
		self.rect.left += 3091
		self.rect.top += 375

	def damaged(self, weapon, amount):
		self.healthPts -= amount

	def updateHealth(self):
		if (self.healthPts <= 0):
			self.main.LayeredUpdate.remove(self)
			self.main.enemyGroup.remove(self)


class Neo_Ridley(pygame.sprite.Sprite):
	def __init__(self, main, fps=15):
		self.groups = main.LayeredUpdate, main.enemyGroup
		self._layer = 2
		super(Neo_Ridley, self).__init__(self.groups)
		self.main = main
		self.screen = main.screen
		self.state = "placeholder"
		self.pathway = "/sprites/ridley-x"
		self.image = load_image(self.state, self.pathway)
		self.load_rects()
		self.hitmask = pygame.surfarray.array_alpha(self.image)
		self.init_attributes()

	def init_attributes(self):
		self.healthPts = 500
		self.attackPts = 0

	def load_rects(self):
		self.rect = self.image.get_rect()
		self.rect.left += 9
		self.rect.top += 1821

	def damaged(self, weapon, amount):
		self.healthPts -= amount

	def updateHealth(self):
		if (self.healthPts <= 0):
			self.main.LayeredUpdate.remove(self)
			self.main.enemyGroup.remove(self)