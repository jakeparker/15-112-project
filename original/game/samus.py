import pygame
import numpy
import sys
from samus_weapons import *


def load_image(fileName, pathway):
	pathway = '/Users/Jake/CMU/15-112/TermProject/original/' + pathway
	return pygame.image.load(pathway + fileName + '.png')

class Samus(pygame.sprite.Sprite):
	def __init__(self, main, health, cx, cy, fps=30):
		self.groups = main.LayeredUpdate
		self._layer = 3
		super(Samus, self).__init__(self.groups)
		self.main = main
		self.screen = main.screen
		self.screen_mask = main.map0_mask
		self.init_sprite(health, fps)
		self.init_move(cx, cy)
		self.load_moves()
		self.load_images()
		self.load_rects(cx, cy)

	def init_sprite(self, health, fps):
		self.projectiles = []
		self.fired = False
		self.wallJump = False
		self.elevator = False
		self.switch = False
		self.rightSwitch = False
		self.leftSwitch = False
		self.delay = 1000/fps
		self.triggerDelay = 300
		self.last_weapon_update = 0
		self.last_update = 0
		self.healthPts = health
		self.attackPts = 0
		self.frame = 0
		self.pathway = '/sprites/samus/fusion_suit/'
		self.damaged_image = load_image("damaged_image", self.pathway)
		self.weapons = ['missile', 'laser']
		self.weaponIndex = 0
		self.sprite_input = 'stand_right_laser_90_0'
		self.move = 'stand'
		self.dir = 'right'
		self.weapon = 'laser'
		self.angle = '90'
		self.frame = '0'

	def damaged(self, weapon,  amount):
		self.image = self.damaged_image
		self.healthPts -= amount

	def init_move(self, cx, cy):
		self.stand = True
		self.run = False
		self.land = False
		self.jump = False
		self.spin = False
		self.crouch = False
		self.morph = False
		self.dx = 3
		self.dy = 0
		self.maxJump = -12
		self.gravity = 1
		

	def load_moves(self):
		# move_dir_weapon_angle_num                              # stand, crouch, jump, land, run, morph, spin
		# stand:  4 frames + fire   0, 45, 90, 135               # left, right
		# crouch: 2 frames + fire      45, 90, 135               # missile, laser, empty
		# jump:   4 frames + 180     0, 45, 90, 135, 180         # 0, 45, 90, 135, 180
		# land:   1 frame            0, 45, 90, 135
		# run:    10 frames              45, 90, 135       weapon -/-> empty
		# morph:  10 frame        90            weapon --> empty
		# spin:   9 frames        90            weapon --> empty
		self.dirs = ['left', 'right']
		stand =  [ 'stand', [3, 'fire'], [['0', '45', '90', '135'], ['0', '45', '90', '135']], [['missile', 'laser'], ['missile', 'laser'] ]]
		crouch = [ 'crouch', [1, 'fire'], [['45', '90', '135'], ['45', '90', '135']], [['missile', 'laser'],['missile', 'laser']] ]
		jump =   [ 'jump', [4,1], [['0', '45', '90', '135'], ['180']], [['missile', 'laser'],['missile', 'laser']] ]
		land =   [ 'land', 1, ['0', '45', '90', '135'], ['missile', 'laser'] ]
		run =    [ 'run', [10,10], [['45', '90', '135'],['90']], [['missile', 'laser'], ['missile', 'empty']] ]
		morph =  [ 'morph', 9, ['none'], ['empty'] ]
		spin =   [ 'spin', 8, ['none'], ['empty'] ]

		moves = [stand, crouch, jump, land, run, morph, spin]
		self.moves = dict()
		self.keys = []
		for move in moves:
			key = move[0]
			self.keys.append(key)
			self.moves[key] = move


	def load_images(self):
		self.images = dict()
		self.hitmasks = dict()
		self.frames = dict()
		for key in self.keys:
			moveData = self.moves[key]
			if (type(moveData[1]) == list):
				self.load_dual_move(moveData)
			else:
				self.load_single_move(moveData)

	def load_dual_move(self, moveData):
		move = moveData[0]
		for index in xrange(0,2):
			frames = moveData[1][index]
			angles = moveData[2][index]
			weapons = moveData[3][index]
			self.load_sprite(move, angles, weapons, frames)

	def load_single_move(self, moveData):
		move = moveData[0]
		frames = moveData[1]
		angles = moveData[2]
		weapons = moveData[3]
		self.load_sprite(move, angles, weapons, frames)

	def load_sprite(self, move, angles, weapons, frames):
		for dir in self.dirs:
			for angle in angles:
				for weapon in weapons:
					if (type(frames) == str):
						frame = frames
						#frames = 1
						self.load_sprite_image(move, dir, angle, weapon, frame, 1)
					else:
						for frame in xrange(frames):
							self.load_sprite_image(move, dir, angle, weapon, frame, frames)

	def load_sprite_image(self, move, dir, angle, weapon, frame, frames):
		current_image = "%s_%s_%s_%s_%s" % (move, dir, weapon, angle, frame)
		current_sprite = load_image(current_image, self.pathway)
		current_hitmask = pygame.surfarray.array_alpha(current_sprite)
		if frame == 'fire':
			frames = frame
		self.images[current_image] = current_sprite
		self.hitmasks[current_image] = current_hitmask
		self.frames[current_image] = frames

	def load_rects(self, cx, cy):
		(width, height) = self.images[self.sprite_input].get_size()
		left = cx - width/2
		top = cy - height/2
		self.rect = pygame.Rect(left, top, width, height)

	def keyEvent(self, event):
		self.switch = False
		#self.wallJump = False
		self.checkMovement(event)
		self.checkAngles()
		self.checkLook(event)
		self.checkWeapon(event, pygame.time.get_ticks())

	def checkMovement(self, event):
		isPressed = pygame.key.get_pressed()
		if isPressed[pygame.K_COMMA]:
			if (self.run == True) and (self.crouch == True):
				self.run = True
			elif (self.run == True):
				self.run = False
				self.stand = True
			else:
				self.run = True
				self.stand = False

		if isPressed[pygame.K_PERIOD]:
			if (self.crouch == False) and (self.run == False):
				self.crouch = True
				self.stand = False
				self.run = False
			elif (self.crouch) and (self.run):
				self.run = False
			else:
				self.crouch = False
				self.stand = True
				self.run = False


		if isPressed[pygame.K_SLASH]:
				if (self.jump == False):
					self.stand = False
					self.jump = True
					self.dy = self.maxJump

	def checkAngles(self):
		if (self.crouch):
			if (self.angle == '0'):
				self.angle = '45'
			elif (self.angle == '180'):
				self.angle = '90'
		elif (self.run) or (self.land):
			if (self.angle == '0'):
				self.angle = '45'
			elif (self.angle == '180'):
				self.angle = '90'
		elif (self.stand):
			if (self.angle == '180'):
				self.angle = '90'

	def checkLook(self, event):
		if (event.key == pygame.K_w):
			if (self.jump) or (self.stand):
				self.angle = "0"
		elif (event.key == pygame.K_s):
			if (self.jump):
				self.angle = "180"
		elif (event.key == pygame.K_a):
			if (self.dir == "left"):
				self.angle = "90"
			else:
				self.dir = "left"
				self.dx *= -1
				self.leftSwitch = True
		elif (event.key == pygame.K_d):
			if (self.dir == "right"):
				self.angle = "90"
			else:
				self.dir = "right"
				self.dx *= -1
				self.rightSwitch = True

		isPressed = pygame.key.get_pressed()
		if isPressed[pygame.K_w] and isPressed[pygame.K_a]:
			self.angle = "45"
		elif isPressed[pygame.K_w] and isPressed[pygame.K_d]:
			self.angle = "45"
		elif isPressed[pygame.K_s] and isPressed[pygame.K_a]:
			self.angle = "135"
		elif isPressed[pygame.K_s] and isPressed[pygame.K_d]:
			self.angle = "135"

	def checkWeapon(self, event, current_update):
		if (event.key == pygame.K_SPACE):
			if not(self.run and self.jump):
				if not (self.run and self.crouch):
					timeElapsed = current_update - self.last_weapon_update
					if (timeElapsed > self.triggerDelay):
						self.last_weapon_update = current_update
						self.fired = True
		if (event.key == pygame.K_f):
			self.weaponIndex += 1
			self.weaponIndex %= len(self.weapons)
			self.weapon = self.weapons[self.weaponIndex]

	def doJump(self):
		if (self.dy < 0): ddy = -1
		else: ddy = +1
		self.dy += self.gravity
		for y in xrange(abs(self.dy)):
			self.rect.centery += ddy
			impact = self.checkBoundary()
			(topLeft,topRight,bottomLeft,bottomRight,midLeft,midRight,midTop,midBottom,midFloor) = (0,1,2,3,4,5,6,7,9)

			if (True in impact):
				if (impact[topLeft] or impact[midTop] or impact[topRight]):
					ddy *= -1
					self.rect.centery += ddy
					self.dy = 0
				elif (impact[midBottom]):
					self.rect.centery -= ddy
					self.stand = True
					self.jump = False
		if (self.run == True):
			if (self.dx < 0): ddx = -1
			elif (self.dx > 0): ddx = +1
			else: ddx = 0
			for x in xrange(abs(self.dx)):
				self.rect.centerx += ddx
				impact = self.checkBoundary()
				(midLeft,midRight,midBottom,leftFloor, midFloor, rightFloor) = (4,5,7,8,9,10)
				if (True in impact):
					if (impact[midLeft]==True) or (impact[midRight]==True):
						self.rect.centerx -= ddx
						self.wallJump = True
					if (impact[leftFloor] or impact[midFloor] or impact[rightFloor]):
						self.jump = False
	def doRun(self):
		if (self.dx < 0): ddx = -1
		elif (self.dx > 0): ddx = +1
		else: ddx = 0
		for x in xrange(abs(self.dx)):
			self.rect.centerx += ddx
			impact = self.checkBoundary()
			(topLeft,topRight,bottomLeft,bottomRight,midLeft,midRight,midTop,midBottom,leftFloor,midFloor,rightFloor) = (0,1,2,3,4,5,6,7,8,9,10)
			if (True in impact):
				if (impact[midLeft]==True) or (impact[midRight]==True):
					self.rect.centerx -= ddx

	def doFall(self):
		if not((self.crouch) and (self.run)):
			self.move = 'jump'
			self.frame = '2'
		self.dy += self.gravity
		for y in xrange(abs(self.dy)):
			impact = self.checkBoundary()
			(midLeft, midRight,midBottom,leftFloor,midFloor,rightFloor) = (4,5,7,8,9,10)
			self.rect.centery += 1
			if (True in impact):
				if (impact[midFloor]):
					self.rect.centery -= 1
				elif (impact[leftFloor]): # and not(impact[midLeft]):
					self.rect.centery -= 1
				elif (impact[rightFloor]): # and not(impact[midRight]):
					self.rect.centery -= 1

	def checkBoundary(self):
		black = (0, 0, 0)
		green = (0, 249, 0)
		cyan = (0, 253, 255)
		blue = (4,51,255)
		orange = (255,147,0)    # elevator

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
			if (color == orange):
				if (self.elevator == False):
					self.dy = -5
					self.elevator = True
				else:
					self.dy = 0
		return impact

	def checkStep(self):
		impact = self.checkBoundary()
		(topLeft,topRight,bottomLeft,bottomRight,midLeft,midRight,midTop,midBottom,midFloor) = (0,1,2,3,4,5,6,7,9)
		if (True in impact):
			if (impact[midFloor]) and (impact[midBottom]):
				if (impact[bottomLeft] or impact[bottomRight]):
					self.rect.centery -= 1
					return self.checkStep()
			elif (impact[midFloor]) and not(impact[midBottom]):
				return None

	def checkWall(self):
		impact = self.checkBoundary()
		(topLeft,topRight,bottomLeft,bottomRight,midLeft,midRight,midTop,midBottom,midFloor) = (0,1,2,3,4,5,6,7,9)
		if (True in impact):
			if (impact[midLeft]):
				self.rect.centerx += 1
				self.checkWall()
			elif (impact[midRight]):
				self.rect.centerx -= 1
				self.checkWall()
			else:
				return None

	def checkFloor(self):
		impact = self.checkBoundary()
		(topLeft,topRight,bottomLeft,bottomRight,midLeft,midRight,midTop,midBottom,leftFloor, midFloor, rightFloor) = (0,1,2,3,4,5,6,7,8,9,10)
		if (impact[midFloor]==False):
			if (self.dx<0) and (impact[leftFloor]==False):
				self.doFall()
			elif (self.dx>0) and (impact[rightFloor]==False):
				self.doFall()
			elif (self.dx == 0):
				self.doFall()
		else:
			self.elevator = False

	def checkTrigger(self):
		if (self.fired == True):
			self.projectiles.append(Projectile(self.main, self))

	def update(self, current_update):
		timeElapsed = current_update - self.last_update
		if (timeElapsed > self.delay):
			self.checkHealth()
			self.checkFireRate()
			self.checkTrigger()
			self.updateMove()
			if (self.jump == False):
				self.checkFloor()
			self.updatePlayerMovement()
			self.updateSpriteMovement(current_update)
			self.correctPosition()
			self.last_update = current_update
			self.checkStep()
			self.checkWall()

	def checkHealth(self):
		if (self.healthPts <= 0):
			self.death()

	def checkFireRate(self):
		if (self.weapon == "laser"):
			self.triggerDelay = 300
		else:
			self.triggerDelay = 550

	def updateMove(self):
		if (self.run) and (self.jump) and not(self.crouch):
			self.move = 'spin'
			if (self.wallJump):
				self.dy = -15
				self.wallJump = False
		elif (self.jump) and (self.run) and (self.crouch):
			self.move = 'morph'
			self.wallJump = False
		else:
			if (self.crouch) and (self.run):
				self.move = 'morph'
			elif (self.run):
				self.move = 'run'
			elif (self.crouch):
				self.move = 'crouch'
			elif (self.jump):
				self.move = 'jump'
				self.wallJump = False
			elif (self.stand):
				self.move = 'stand'
			else:
				self.move = 'stand'

	def updatePlayerMovement(self):
		if (self.jump):
			self.doJump()

		elif (self.run):
			self.doRun()

	def updateSpriteMovement(self, current_update):
		move = self.move
		dir = self.dir
		if ((move != 'jump') and (move != 'spin')):
			if (self.angle == '180'):
				self.angle = '90'
		if (move == 'spin') or (move == 'morph'):
			angle = 'none'
			weapon = 'empty'
		else:
			angle = self.angle
			weapon = self.weapon
		if (self.fired == True):
			self.fired = False

			if (self.run==False):
				if (self.jump == False):
					if (self.stand) or (self.crouch):
						frame = 'fire'
					else:
						frame = self.updateFrame(move, dir, weapon, angle)

				else:
					frame = self.updateFrame(move, dir, weapon, angle)
			else:
				frame = self.updateFrame(move, dir, weapon, angle)
		else:
			frame = self.updateFrame(move, dir, weapon, angle)
		if (frame == 'fire') and (self.move == "jump"):
			frame = 0
		self.sprite_input = "%s_%s_%s_%s_%s" % (move, dir, weapon, angle, frame)
		self.image = self.images[self.sprite_input]
		self.hitmask = self.hitmasks[self.sprite_input]

	def updateFrame(self, move, dir, weapon, angle):
		if (self.frame == 'fire') and (self.move == "jump"):
			self.frame = 0
		current_image = "%s_%s_%s_%s_0" % (move, dir, weapon, angle)
		frames = self.frames[current_image]
		frame = int(self.frame)
		if (self.jump) and not(self.run):
			if (self.frame < self.frames):
				self.frame += 1
		else:
			frame += 1
		frame %= frames
		frame = str(frame)
		self.frame = frame
		return frame

	def correctPosition(self):
		(width, height) = self.image.get_size()
		dx = width - self.rect.width
		dy = height - self.rect.height
		self.rect.top -= dy
		self.rect.width = width
		self.rect.height = height
		if (self.move == 'stand') or (self.move == 'crouch'):
			if (self.dir == 'left'):
				self.rect.left -= dx
			if (self.rightSwitch == True):
				self.rect.left += width/3
				self.rightSwitch = False
			elif (self.leftSwitch == True):
				self.rect.left -= width/3
				self.leftSwitch = False
		elif (self.move == 'run'):
			if (self.dir == 'right'):
				self.rect.centerx -= dx

	def death(self):
		self.main.running = False
