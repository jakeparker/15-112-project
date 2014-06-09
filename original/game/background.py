import pygame
from samus import *


def load_doors(main):
	for index in xrange(len(main.doors)):
		door = main.doors[index]
		main.doors[index] = Door(door, main)

def load_hatches(main):
	for index in xrange(len(main.left_hatches)):
		left_hatch = main.left_hatches[index]
		right_hatch = main.right_hatches[index]
		main.left_hatches[index] = Hatch(left_hatch, main, 'left', 'closed')
		main.right_hatches[index] = Hatch(right_hatch, main, 'right','closed')

def load_overlays(main):
	for index in xrange(5):
		overlay = main.overlays[index]
		main.overlays[index] = Overlay(overlay, main)

def load_brokenDoors(main):
	for index in xrange(len(main.brokenDoors)):
		brokenDoor = main.brokenDoors[index]
		main.brokenDoors[index] = Overlay(brokenDoor, main, "brokenDoor0")

def load_background(main):
	load_overlays(main)
	load_brokenDoors(main)
	load_hatches(main)
	load_doors(main)


class Background(pygame.sprite.Sprite):
	def __init__(self, rect, main, image, groups, layer=5):
		self.groups = groups
		self._layer = layer
		super(Background, self).__init__(self.groups)
		self.pathway = "/sprites/bg/"
		if (image != None):
			self.name = image
			self.image = load_image(image, self.pathway)
			self.hitmask = pygame.surfarray.array_alpha(self.image)
		else:
			(self.image, self.hitmask) = (None, None)

		self.main = main
		self.rect = rect

	def update(self, current_update):
		pass

	def draw(self):
		self.main.map0.blit(self.image, self.rect)

class Door(Background):
	def __init__(self, rect, main, image='door'):
		groups = main.LayeredUpdate
		super(Door, self).__init__(rect, main, image, groups)

class Hatch(pygame.sprite.Sprite):
	def __init__(self, rect, main, dir, state='closed', body='hatch', fps=5):
		self.groups = main.LayeredUpdate
		self._layer = 4
		super(Hatch, self).__init__(self.groups)
		self.delay = 1000/fps
		self.dir = dir
		self.main = main
		self.body = body
		self.state = state
		self.opened = False
		self.frames = dict()
		self.last_update = 0
		self.frames['opened'] = 2
		self.frames["closed"] = 1
		self.frame = 0
		self.pathway = "/sprites/bg/"
		self.opened_mask = load_image("opened_mask", self.pathway)
		self.closed_mask = load_image("closed_mask", self.pathway)
		self.name = "%s_%s_%s_%d" % (self.dir, self.body, self.state, self.frame)
		self.image = load_image(self.name, self.pathway)
		self.hitmask = pygame.surfarray.array_alpha(self.image)
		self.rect = rect
		self.map0_mask = self.main.map0_mask

	def update(self, current_update):
		timeElapsed = current_update - self.last_update
		if (timeElapsed > self.delay):
			self.updateState()
			self.last_update = current_update

	def updateState(self):
		self.frame += 1
		self.frame %= self.frames[self.state]
		if self.opened == True:
			self.state = 'opened'
			self.frame = 0
			self.name = "%s_%s_%s_%d" % (self.dir, self.body, self.state, self.frame)
			self.image = load_image(self.name, self.pathway)
		else:
			self.state = "closed"
			self.frame = 0
			self.name = "%s_%s_%s_%d" % (self.dir, self.body, self.state, self.frame)
			self.image = load_image(self.name, self.pathway)
			

class Room(Background):
	def __init__(self, main, rect, groups, layer, image=None, left=None, top=None, width=None, height=None):
		if (groups == None):
			groups = main.LayeredUpdate
		if (layer == None):
			layer = 1
		super(Room, self).__init__(rect, main, image, groups, layer)
		if (rect == None):
			self.rect = self.image.get_rect()
			if (left != None):
				self.rect.left = left
			if (top != None):
				self.rect.top = top
			if (width != None):
				self.rect.width = width
			if (height != None):
				self.rect.height = height

class Overlay(Background):
	def __init__(self, rect, main, image='overlay'):
		groups = main.LayeredUpdate
		super(Overlay, self).__init__(rect, main, image, groups)

class Elevator(object):
	def __init__(self):
		pass