
import pygame
import numpy
from samus import *
from background import *


				# scrolling/sprites/
# nettori
	# awaken 0-13
	# green 0-4
	# green/purple/red_beam_top 0-33
	# green/purple/red_beam_bottom 0-33

# buds (nettori/buds/)
	# bud_left/right_closed 0-2
	# bud_left/right_opened 0-1

# flowers (nettori/flowers/)
	# flower_closed/opened 0-3

# spores (nettori/spores/)
	# spore 0-3

# beams (nettori/beams/)
	# beam 0-1

class Nettori(pygame.sprite.Sprite):
	def __init__(self, main, fps = 5):
		self.groups = main.LayeredUpdate, main.enemyGroup
		self._layer = 2
		super(Nettori, self).__init__(self.groups)
		self.main = main
		self.main.nettori = self
		self.screen = main.screen
		self.screen_mask = main.map0_mask
		self.pathway = "sprites/nettori/"
		self.init_attributes()
		self.init_sprite(fps)
		self.init_plants()

	def init_attributes(self):
		self.healthPts = 500
		self.attackPts = 35

	def damaged(self, weapon, amount):
		if (weapon == "missile"):
			self.image = self.damaged_image
			self.healthPts -= amount

	def init_sprite(self, fps):
		self.delay = 1000/fps
		self.topFired = False
		self.bottomFired = False
		self.delay = 1000/fps
		self.counter = 0
		self.last_update = 0
		self.state = 'awaken'
		self.damaged_image = load_image("damaged_image", self.pathway)
		self.initial_state = "awaken_None_None_0"
		self.current_state = "awaken_None_None_0"
		self.positions = ["top", "bottom"]
		self.position = "top"
		self.beamAttack = False
		self.weapon = None
		self.position = None
		self.frame = 0
		self.left = 782
		self.top = 1600
		groups = self.main.LayeredUpdate
		layer = 1
		self.room = Room(self.main, None, groups, layer, "nettori_room", self.left, self.top)
		self.load_states()
		self.load_images()
		self.load_rects()

	def init_plants(self):
		topLeft = (self.left, self.top)
		flowers = [ (32, 312), (112, 312), (192, 312) ]
			# spore -> y: self.rect.top - self.rect.height/3
			# 		-> x: self.rect.mid +- 4
		buds = [ (58, 216, 'right'), (188, 194, 'left') ]
			# right spore -> x,y + 11
			# left spore  -> x,y +6, +11
		self.flowers = []
		for (left, top) in flowers:
			flower = Flower(self.main, self, left, top)
			self.flowers.append(flower)

		self.buds = []	
		for (left, top, dir) in buds:
			bud = Bud(self.main, self, left, top, dir)
			self.buds.append(bud)
			

	def load_states(self):
		awaken = [ 'awaken',[7],  [None], [[None]] ]
		yellow = [ 'yellow', [4], [None], [[None]] ]
		green = [ 'green', [4, 33], [None, 'beam'], [[None], ['top', 'bottom']] ]
		purple = [ 'purple', [4, 33], [None, 'beam'], [[None], ['top', 'bottom']] ]
		red = [ 'red', [4, 33], [None, 'beam'], [[None], ['top', 'bottom']] ]
		states = [awaken, yellow, green, purple, red]
		self.states = dict()
		self.keys = []
		for state in states:
			key = state[0]
			self.keys.append(key)
			self.states[key] = state

	def load_images(self):
		self.images = dict()
		self.hitmasks = dict()
		self.frames = dict()
		for key in self.keys:
			attributes = self.states[key]
			state = attributes[0]
			for index in xrange(len(attributes[1])):
				frames = attributes[1][index]
				weapon = attributes[2][index]
				positions = attributes[3][index]
				for position in positions:
					for frame in xrange(frames+1):
						self.load_sprite_image(state, weapon, position, frame, frames)

	def load_sprite_image(self, state, weapon, position, frame, frames):
		current_image = "%s_%s_%s_%d" % (state, weapon, position, frame)
		current_sprite = load_image(current_image, self.pathway)
		current_hitmask = pygame.surfarray.array_alpha(current_sprite)
		self.images[current_image] = current_sprite
		self.hitmasks[current_image] = current_hitmask
		self.frames[current_image] = frames

	def load_rects(self):
		(xPos, yPos) = (223, 226) # xy position relative to topleft of 'nettori_room.png'
		self.rect = self.images[self.initial_state].get_rect()
		self.rect.topleft = (self.left+xPos, self.top+yPos)
		self.initialRect = self.rect

	def update(self, current_update):
		timeElapsed = current_update - self.last_update
		if (timeElapsed > self.delay):
			self.updateHealth()
			self.updateWeapon()
			self.updateState()
			self.last_update = current_update

	def updateHealth(self):
		hitPts = self.healthPts
		if (450 > hitPts) and (hitPts > 400):
			self.state = 'yellow'
			self.budsAttack()
		elif (400 > hitPts) and (hitPts > 300):
			self.state = 'green'
			self.flowersAttack()
		elif (300 > hitPts) and (hitPts > 200):
			self.state = 'purple'
			self.budsDie()
			self.beamAttack = True
		elif (200 > hitPts) and (hitPts > 100):
			self.state = 'red'
			self.flowersDie()
		elif (hitPts <= 0):
			self.death()

	def budsAttack(self):
		for bud in self.buds:
			bud.attack = True

	def flowersAttack(self):
		for flower in self.flowers:
			flower.attack = True

	def budsDie(self):
		for bud in self.buds:
			bud.death()

	def flowersDie(self):
		for flower in self.flowers:
			flower.death()

	def death(self):
		self.main.LayeredUpdate.remove(self)
		self.main.enemyGroup.remove(self)

	def updateWeapon(self):
		if (self.beamAttack):
			if (self.weapon == None):
				self.weapon = "beam"
				self.position = self.positions[0]
			else:
				if (self.frame % self.frames[self.current_state] == 0):
					# last frame is the firing frame
					self.counter += 1
					self.counter %= 2
					self.position = self.positions[self.counter]
					beam = Beam(self.main)

	def updateState(self):
		self.frame += 1
		past_state = "%s_%s_%s_%d" % (self.state, self.weapon, self.position, 0)
		self.frame %= self.frames[past_state]
		self.current_state = "%s_%s_%s_%d" % (self.state, self.weapon, self.position, self.frame)
		self.image = self.images[self.current_state]
		self.hitmask = self.hitmasks[self.current_state]

class Beam(pygame.sprite.Sprite):
	def __init__(self, main, fps=30):
		self.groups = main.LayeredUpdate, main.enemyProjectiles
		self._layer = 4
		super(Beam, self).__init__(self.groups)
		self.main = main
		self.screen = main.screen
		self.screen_mask = main.map0_mask
		self.nettori = main.nettori
		self.pathway = self.nettori.pathway + "beams/"
		self.init_sprite(fps)

	def init_sprite(self, fps):
		self.delay = 1000/fps
		self.last_update = 0
		self.dx = -7
		self.attackPts = 12
		self.frame = 0
		self.frames = 1
		self.weapon = "beam"
		self.current_state = "beam_0"
		self.image = load_image(self.current_state, self.pathway)
		self.load_images()
		self.load_rects()

	def load_images(self):
		self.images = dict()
		self.hitmasks = dict()
		(self.frames, self.weapon) = (1, 'beam')
		for frame in xrange(self.frames+1):
			current_image = "%s_%s" % (self.weapon, frame)
			current_sprite = load_image(current_image, self.pathway)
			current_hitmask = pygame.surfarray.array_alpha(current_sprite)
			self.images[current_image] = current_sprite
			self.hitmasks[current_image] = current_hitmask

	def load_rects(self):
		(left, top) = (self.nettori.left, self.nettori.top)
		self.rect = self.image.get_rect()
		if (self.nettori.position == "top"): self.topAdj = 270 + top
		else: self.topAdj = 243 + top
		self.leftAdj = 227 + left
		self.rect.left += self.leftAdj
		self.rect.top += self.topAdj


	def death(self):
		self.main.LayeredUpdate.remove(self)
		self.main.enemyProjectiles.remove(self)

	def update(self, current_update):
		timeElapsed = current_update - self.last_update
		if (timeElapsed > self.delay):
			self.updateState()
			self.updateHorizontal()
			self.last_update = current_update

	def updateHorizontal(self):
		if (self.dx < 0): dx = -1
		elif (self.dx > 0): dx = +1
		for x in xrange(abs(self.dx)):
			self.rect.centerx += dx
			impact = self.checkBoundary()
			if impact == True:
				self.rect.centerx += dx
				self.dx = 0
				self.death()

	def updateState(self):
		self.frame += 1
		self.frame %= self.frames
		self.current_state = "%s_%d" % (self.weapon, self.frame)
		self.image = self.images[self.current_state]
		self.hitmask = self.hitmasks[self.current_state]

	def checkBoundary(self):
		black = (0,0,0)         # out of bounds
		green = (0,249,0)       # wall segment
		cyan = (0,253,255)      # playable area
		blue = (4,51,255)       # overlay
		magenta = (255,64,255)  # door lock
		purple = (148,33,146)  # door passage
		orange = (255,147,0)    # elevator pad

		rect = self.rect
		(width, height) = (rect.width, rect.height)
		bounds = [rect.topleft]
		impact = [False for x in xrange(len(bounds))]
		for i in xrange(len(bounds)):
			(x,y) = bounds[i]
			rgb = self.screen_mask[x][y]
			color = (rgb[0], rgb[1], rgb[2])
			if (color == green) or (color == black):
				return True
		return False

class Flower(pygame.sprite.Sprite):
	def __init__(self, main, nettori, left, top, fps=5):
		self.groups = main.LayeredUpdate, main.enemyGroup
		self._layer = 2
		super(Flower, self).__init__(self.groups)
		self.main = main
		self.screen = main.screen
		self.screen_mask = main.map0_mask
		self.nettori = nettori
		self.pathway = self.nettori.pathway + "flowers/"
		self.init_sprite(left, top, fps)

	def init_sprite(self, left, top, fps):
		self.delay = 1000/fps
		self.last_update = 0
		self.current_state = "flower_closed_0"
		self.plant = "flower"
		self.state = "closed"
		self.states = ["closed", "opened"]
		self.damaged_image = load_image("damaged_image", self.pathway)
		self.counter = 0
		self.attack = False
		self.dead = False
		self.healthPts = 0
		self.attackPts = 1
		self.frames = 3
		self.frame = 0
		self.load_images()
		self.load_rects(left, top)

	def load_images(self):
		attributes = [[ 'flower', ['closed', 'opened'], 3]]
		self.images = dict()
		self.hitmasks = dict()
		for attribute in attributes:
			plant = attribute[0]
			states = attribute[1]
			frames = attribute[2]
			for state in states:
				for frame in xrange(frames+1):
					self.load_sprite_image(plant, state, frame, frames)

	def load_sprite_image(self, plant, state, frame, frames):
		current_image = "%s_%s_%s" % (plant, state, frame)
		current_sprite = load_image(current_image, self.pathway)
		current_hitmask = pygame.surfarray.array_alpha(current_sprite)
		self.images[current_image] = current_sprite
		self.hitmasks[current_image] = current_hitmask

	def load_rects(self, left, top):
		image = self.images[self.current_state]
		self.rect = image.get_rect()
		roomLeft = self.nettori.left
		roomTop = self.nettori.top
		self.rect.left += (roomLeft + left)
		self.rect.top += (roomTop + top)

	def damaged(self, weapon, amount):
		self.healthPts += amount
		# negetive damage?

	def update(self, current_update):
		timeElapsed = current_update - self.last_update
		if (timeElapsed > self.delay):
			self.updateState()
			if (self.dead == True):
				self.main.LayeredUpdate.remove(self)
				self.main.enemyGroup.remove(self)
			if (self.attack == True):
				if (self.current_state == "flower_opened_2"):
					self.doAttack()
			self.last_update = current_update

	def updateState(self):
		self.frame += 1
		if (self.attack == False):
			self.frame %= self.frames
		elif (self.frame % self.frames == 0):
			self.frame = 0
			self.counter += 1
			self.counter %= 2
			self.state = self.states[self.counter]

		self.current_state = "%s_%s_%d" % (self.plant, self.state, self.frame)
		self.image = self.images[self.current_state]
		self.hitmask = self.hitmasks[self.current_state]

	def doAttack(self):
		dy = -8
		(dxA, dxB) = (-2, +2)
		(left, top) = (self.rect.left, self.rect.top)
		(leftA, topA) = (left+19, top+2)
		(leftB, topB) = (left+29, top+1)
		sporeA = Spore(self.main, dxA, dy, leftA, topA)
		sporeB = Spore(self.main, dxB, dy, leftB, topB)

	def death(self):
		self.image = self.damaged_image
		self.dead = True

class Bud(pygame.sprite.Sprite):
	def __init__(self, main, nettori, left, top, dir, fps=5):
		self.groups = main.LayeredUpdate, main.enemyGroup
		self._layer = 2
		super(Bud, self).__init__(self.groups)
		self.main = main
		self.screen = main.screen
		self.screen_mask = main.map0_mask
		self.nettori = nettori
		self.pathway = self.nettori.pathway + "buds/"
		self.init_sprite(left, top, dir, fps)

	def init_sprite(self, left, top, dir, fps):
		self.dir = dir
		self.delay = 1000/fps
		self.healthPts = 0
		self.attackPts = 5
		self.last_update = 0
		self.current_state = "bud_" + self.dir + "_closed_0" 
		self.damaged_image = load_image("damaged_image", self.pathway)
		self.plant = "bud"
		self.state = "closed"
		self.counter = 0
		self.states = ["closed", "opened"]
		self.attack = False
		self.dead = False
		self.frame = 0
		self.load_images()
		self.load_rects(left, top)

	def load_images(self):
		attributes = [[ 'bud', ['left', 'right'], ['closed', 'opened']]]
		self.frameDict = dict()
		self.frameDict['closed'] = 2
		self.frameDict['opened'] = 1
		self.images = dict()
		self.hitmasks = dict()
		for attribute in attributes:
			plant = attribute[0]
			dirs = attribute[1]
			states = attribute[2]
			for state in states:
				frames = self.frameDict[state]
				for dir in dirs:
					for frame in xrange(frames+1):
						self.load_sprite_image(plant, dir, state, frame, frames)

	def load_sprite_image(self, plant, dir, state, frame, frames):
		current_image = "%s_%s_%s_%s" % (plant, dir, state, frame)
		current_sprite = load_image(current_image, self.pathway)
		current_hitmask = pygame.surfarray.array_alpha(current_sprite)
		self.images[current_image] = current_sprite
		self.hitmasks[current_image] = current_hitmask

	def load_rects(self, left, top):
		image = self.images[self.current_state]
		self.rect = image.get_rect()
		roomLeft = self.nettori.left
		roomTop = self.nettori.top
		self.rect.left += (roomLeft + left)
		self.rect.top += (roomTop + top)

	def damaged(self, weapon, amount):
		self.healthPts += amount
		# negetive damage?

	def update(self, current_update):
		timeElapsed = current_update - self.last_update
		if (timeElapsed > self.delay):
			self.updateState()
			if (self.dead == True):
				self.main.LayeredUpdate.remove(self)
				self.main.enemyGroup.remove(self)
			if (self.attack == True):
				if (self.current_state == "bud_" +self.dir+ "_opened_0"):
					self.doAttack()
			self.last_update = current_update

	def updateState(self):
		self.frame += 1
		if (self.attack == False):
			self.frame %= self.frameDict[self.state]+1
		elif (self.frame % (self.frameDict[self.state]+1) == 0):
			self.frame = 0
			self.counter += 1
			self.counter %= 2
			self.state = self.states[self.counter]

		self.current_state = "%s_%s_%s_%d" % (self.plant, self.dir, self.state, self.frame)
		self.image = self.images[self.current_state]
		self.hitmask = self.hitmasks[self.current_state]

	def doAttack(self):
		dy = +2
		if (self.dir == 'left'):
			dx = -2
			(left, top) = (self.rect.left+9, self.rect.top+11)
		elif (self.dir == 'right'):
			dx = +2
			(left, top) = (self.rect.left+10, self.rect.top+12)
		spore = Spore(self.main, dx, dy, left, top)

	def death(self):
		self.image = self.damaged_image
		self.dead = True

class Spore(pygame.sprite.Sprite):
	def __init__(self, main, dx, dy, left, top, fps=30):
		self.groups = main.LayeredUpdate, main.enemyProjectiles
		self._layer = 4
		super(Spore, self).__init__(self.groups)
		self.dx = dx
		self.dy = dy
		self.gravity = 1
		self.main = main
		self.screen = main.screen
		self.screen_mask = main.map0_mask
		self.nettori = main.nettori
		self.pathway = self.nettori.pathway + "spores/"
		self.init_sprite(left, top, fps)

	def init_sprite(self, left, top, fps):
		self.delay = 1000/fps
		self.last_update = 0
		self.attackPts = 5
		self.current_state = "spore_0"
		self.image = load_image(self.current_state, self.pathway)
		self.hitmask = pygame.surfarray.array_alpha(self.image)
		self.weapon = "spore"
		self.frames = 3
		self.frame = 0
		self.load_images()
		self.load_rects(left, top)

	def load_images(self):
		self.images = dict()
		self.hitmasks = dict()
		for frame in xrange(self.frames+1):
			current_image = "%s_%s" % (self.weapon, frame)
			current_sprite = load_image(current_image, self.pathway)
			current_hitmask = pygame.surfarray.array_alpha(current_sprite)
			self.images[current_image] = current_sprite
			self.hitmasks[current_image] = current_hitmask

	def load_rects(self, leftAdj, topAdj):
		self.rect = self.image.get_rect() ## ADJUST RECT TO INITIAL POS
		self.rect.left += leftAdj
		self.rect.top += topAdj

	def update(self, current_update):
		timeElapsed = current_update - self.last_update
		if (timeElapsed > self.delay):
			self.updateState()
			self.updateMovement()
			self.last_update = current_update

	def updateMovement(self):
		if (self.dx != 0):
			self.updateHorizontal()
		self.updateVertical()

	def updateHorizontal(self):
		if (self.dx < 0): dx = -1
		elif (self.dx > 0): dx = +1
		for x in xrange(abs(self.dx)):
			self.rect.centerx += dx
			impact = self.checkBoundary()
			if (impact == True):
				self.rect.centerx -= dx
				self.dx = 0
				self.dy = 0
				self.death()

	def updateVertical(self):
		if (self.dy < 0): dy = -1
		elif (self.dy >= 0): dy = +1
		self.dy += self.gravity
		for y in xrange(abs(self.dy)):
			self.rect.centery += dy
			impact = self.checkBoundary()
			if (impact == True):
				self.rect.centerx -= dy
				self.dx = 0
				self.dy = 0
				self.death()

	def updateState(self):
		self.frame += 1
		self.frame %= self.frames
		self.current_state = "%s_%d" % (self.weapon, self.frame)
		self.image = self.images[self.current_state]
		self.hitmask = self.hitmasks[self.current_state]

	def checkBoundary(self):
		black = (0,0,0)         # out of bounds
		green = (0,249,0)       # wall segment
		cyan = (0,253,255)      # playable area
		blue = (4,51,255)       # overlay
		magenta = (255,64,255)  # door lock
		purple = (148,33,146)  # door passage
		orange = (255,147,0)    # elevator pad

		rect = self.rect
		(width, height) = (rect.width, rect.height)
		(xFloor,yFloor) = rect.midbottom
		leftFloor = (xFloor-width/2, yFloor+1)
		midFloor = (xFloor, yFloor+1)
		rightFloor = (xFloor+width/2, yFloor+1)
		bounds = [rect.midleft, rect.midright, rect.midtop, rect.midbottom]
		impact = [False for x in xrange(len(bounds))]
		for i in xrange(len(bounds)):
			(x,y) = bounds[i]
			rgb = self.screen_mask[x][y]
			color = (rgb[0], rgb[1], rgb[2])
			if (color == green) or (color == black):
				return True
		return False

	def death(self):
		self.main.LayeredUpdate.remove(self)
		self.main.enemyProjectiles.remove(self)

