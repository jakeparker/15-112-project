import pygame
import numpy

def load_image(fileName, pathway):
	pathway = '/Users/Jake/CMU/15-112/TermProject/original/' + pathway
	return pygame.image.load(pathway + fileName + '.png')

class Projectile(pygame.sprite.Sprite):
	def __init__(self,main,player,fps=30):
		self.groups = main.LayeredUpdate, main.playerProjectiles
		self._layer = 4
		super(Projectile, self).__init__(self.groups)
		self.pathway = '/sprites/samus/weapons/'
		self.main = main
		self.player = player
		self.screen = main.screen
		self.screen_mask = main.map0_mask
		self.init_sprite(fps)
		self.load_weapons()
		self.load_images()
		self.load_rects()

	def init_sprite(self, fps):
		self.dir = self.player.dir
		self.weapon = self.player.weapon
		self.version = self.getWeaponVersion()
		self.action = 'flight'
		self.delay = 1000/fps
		if (self.weapon == "laser"):
			pts = 5
			self.speed = 7
		elif (self.weapon == "missile"):
			pts = 11
			self.speed = 5
		self.attackPts = pts
		self.weapon_input = '%s_%s_flight_0' % (self.weapon, self.version)
		self.image = load_image(self.weapon_input, self.pathway)
		self.hitmask = pygame.surfarray.array_alpha(self.image)
		self.frame = 0
		self.fired = False
		self.impact = False
		self.last_update = 0
		self.frame = 0

	def getWeaponVersion(self):
		if (self.weapon == 'missile'):
			return 'regular'
		elif (self.weapon == 'laser'):
			return 'power'

	def load_weapons(self):
		laserFire = [ 'laser', 'fire', 2, ['power'] ]
		missileFire = [ 'missile', 'fire', 3, ['regular'] ]
		laserFlight = [ 'laser', 'flight', 2, ['power'] ]
		missileFlight = [ 'missile', 'flight', 2, ['regular'] ]
		laserImpact = [ 'laser', 'impact', 3, ['power'] ]
		missileImpact = [ 'missile', 'impact', 5, ['regular'] ]
		self.moves = [laserFire, missileFire, laserFlight, missileFlight, laserImpact, missileImpact]

	def load_images(self):
		self.images = dict()
		self.frames = dict()
		self.hitmasks = dict()
		for data in self.moves:
			weapon = data[0]
			versions = data[3]
			action = data[1]
			frames = data[2]
			for version in versions:
				for frame in xrange(frames):
					current_sprite = "%s_%s_%s_%s" % (weapon, version, action, frame)
					current_image = load_image(current_sprite, self.pathway)
					current_image = self.rotate_image(current_image)
					current_hitmask = pygame.surfarray.array_alpha(current_image)
					self.images[current_sprite] = current_image
					self.hitmasks[current_sprite] = current_hitmask
					self.frames[current_sprite] = frames


	def rotate_image(self, current_image):
		angle = self.player.angle
		rotationDegrees = eval(angle) - 90
		if (self.dir == 'right'):
			rotationDegrees *= -1
			rotationDegrees += 180
		current_image = pygame.transform.rotate(current_image, rotationDegrees)
		return current_image

	def load_rects(self):
		(cx,cy) = self.getGunPos()
		(width, height) = self.images[self.weapon_input].get_size()
		left = cx - width/2
		top = cy - height/2
		self.rect = pygame.Rect(left, top, width, height)

	def getGunPos(self):
		samus = self.player
		move = samus.move
		dir = samus.dir
		angle = samus.angle
		pos = "self.player.rect.%s%s"

		if (dir == 'left'): sign = -1
		else: sign = 1

		if ((samus.run and samus.jump) or (samus.run and samus.crouch)):
			return None

		if (angle == '45'):
			arg = 'top'
			yAdj = -1
			xAdj = sign
			self.dy = -1
			self.dx = sign
		else:
			if (samus.crouch):
				if (angle == '90'):
					arg = 'mid'
					yAdj = 0
					xAdj = 3*sign
					self.dy = 0
					self.dx = sign
				elif (angle == '135'):
					arg ='bottom'
					yAdj = -2
					xAdj = 2*sign
					self.dy = +1
					self.dx = sign

			else:
				if (angle == '0'):
					arg = 'mid'
					dir = 'top'
					xAdj = 5*sign
					yAdj = 1
					self.dy = -1
					self.dx = 0

				elif (angle == '90'):
					arg = 'mid'
					xAdj = 3*sign
					yAdj = -4
					self.dy = 0
					self.dx = sign
				elif (angle == '135'):
					arg ='mid'
					xAdj = sign
					yAdj = 4
					self.dy = +1
					self.dx = sign
				elif (angle == '180'):
					arg ='top'
					xAdj = 4*sign
					yAdj = 1
					self.dy = +1
					self.dx = 0

		self.dy *= self.speed
		self.dx *= self.speed
		(x,y) = eval(pos%(arg,dir))
		return (x+xAdj, y+yAdj)

	def update(self, current_update):
		timeElapsed = current_update - self.last_update
		if (timeElapsed > self.delay):
			self.updateWeapon()
			self.updateMovement()
			self.last_update = current_update


	def updateWeapon(self):
		weapon = self.weapon
		version = self.version
		action = self.action
		frames = self.frames

		current_image = "%s_%s_%s_0" % (weapon, version, action)
		frames = self.frames[current_image]
		frame = int(self.frame)
		frame += 1
		if (self.action == 'impact'):
			if (frame != 0) and (frame%frames == 0):
				self.main.LayeredUpdate.remove(self)
				
		frame %= frames
		frame = str(frame)
		self.frame = frame
		self.weapon_input = "%s_%s_%s_%s" % (weapon, version, action, frame)
		self.image = self.images[self.weapon_input]
		self.hitmask = self.hitmasks[self.weapon_input]

	def updateMovement(self):
		if (self.dy != 0):
			self.updateVertical()
		if (self.dx != 0):
			self.updateHorizontal()

	def updateVertical(self):
		if (self.dy < 0): dy = -1
		elif (self.dy > 0): dy = +1
		for y in xrange(abs(self.dy)):
			self.rect.centery += dy
			impact = self.checkBoundary()
			if (True in impact):
				self.action = 'impact'
				self.rect.centerx -= dy
				self.dx = 0
				self.dy = 0

	def updateHorizontal(self):
		if (self.dx < 0): dx = -1
		elif (self.dx > 0): dx = +1
		for x in xrange(abs(self.dx)):
			self.rect.centerx += dx
			impact = self.checkBoundary()
			if (True in impact):
				self.action = 'impact'
				self.rect.centerx -= dx
				self.dx = 0
				self.dy = 0

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
		bounds = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright,
		          rect.midleft, rect.midright, rect.midtop, rect.midbottom, leftFloor, midFloor, rightFloor]
		impact = [False for x in xrange(len(bounds))]
		for i in xrange(len(bounds)):
			(x,y) = bounds[i]
			rgb = self.screen_mask[x][y]
			color = (rgb[0], rgb[1], rgb[2])
			if (color == green) or (color == black):
				impact[i] = True
			#elif (color == magenta):
				### do DOOR STUFF ###
			#	impact[i] = True
		return impact

	def death(self):
		self.main.LayeredUpdate.remove(self)
		self.main.playerProjectiles.remove(self)

