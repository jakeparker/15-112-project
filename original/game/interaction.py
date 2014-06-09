import pygame
from placeholders import *
from nettori import *


#  --> returns new Rect cropped to be inside arg Rect, if rects dont overlap, returns 0
# .contains(Rect) --> test if Rect is inside another Rect (returns bool)
# .collidepoint(x,y) --> test if arg point is inside a Rect
# .colliderect(Rect) --> test if two Rects overlap
# .collidelist(list) --> returns index of first collision of rect with rects in list, else empty list

def isRectImpact(spriteA, spriteB):
	return spriteA.rect.colliderect(spriteB)

def isPixelImpact(spriteA, spriteB):
	rectA = spriteA.rect
	rectB = spriteB.rect
	# rectangle intersection of A and B
	rectAB = rectA.clip(rectB)
	# topleft AB > topleft A
	# get topleft of rectAB w/ respect to rectA's topleft
	(leftA, topA) = (rectAB.left-rectA.left, rectAB.top-rectA.top)
	# get topleft of rectAB w/ respect to rectB's topleft
	(leftB, topB) = (rectAB.left-rectB.left, rectAB.top-rectB.top)
	# get hitmasks from sprite classes
	(hitmaskA, hitmaskB) = (spriteA.hitmask, spriteB.hitmask)
	(widthAB, heightAB) = (rectAB.width, rectAB.height)
	# range by y,x and check each (x,y) pixel value for equality
	for i in xrange(heightAB):
		for j in xrange(widthAB):
			# must use coordinates that are releative to each sprite's Rect
			pixelA = hitmaskA[leftA+j][topA+i]
			pixelB = hitmaskB[leftB+j][topB+i]
			# array2d used for hitmask, so each pixel either 0 (transparent) or 1
			# 1&0 = 0, 1&1=1....
			if (pixelA & pixelB):
				return True # impact
	return False # no impact detected

# pygame.sprite.Sprite() --> built in pygame class for sprite objects
# pygame.sprite.Group() --> built in container for pygame.sprite.Sprite instances
# pygame.sprite.LayeredUpdates() --> subclass of sprite.Group() which includes a draw by layer hierarchy
# pygame.sprite.Group.sprites() --> returns list of sprites in the group


def isGroupImpact(spriteA, group):
	# group != list of sprites
	# group == pygame.sprite.Group()
	impacts = []
	isImpact = False
	spriteGroup = group.sprites()
	for spriteB in spriteGroup:
		# first check if rects collide, only then check hitmask
		if (isRectImpact(spriteA, spriteB) == True):
			if (isPixelImpact(spriteA, spriteB) == True):
				impacts.append(spriteB)
				isImpact = True
	return (isImpact, impacts)


def isListImpact(spriteA, spriteList):
	impacts = []
	isImpact = False
	for spriteB in spriteList:
		# first check if rects collide, only then check hitmask
		if (isRectImpact(spriteA, spriteB) == True):
			if (isPixelImpact(spriteA, spriteB) == True):
				impacts.append(spriteB)
				isImpact = True
	return (isImpact, impacts)
  
# LayeredUpdate,  enemyGroup,  enemyProjectiles,  playerProjectiles

# interfaceGroup,  elevatorGroup

class Interaction(object):
	def __init__(self, main):
		self.main = main
		self.enemies = main.enemyGroup
		self.player = main.player
		self.enemyWeapons = main.enemyProjectiles
		self.playerWeapons = main.playerProjectiles
		self.rooms = main.rooms

	def update(self):
		# check for collisions, for all groups / sprites that require hitmask
		self.checkPixelImpact()
		# check for collisions, for all groups / sprites that require rect
		self.checkRectImpact()
		# handle boss spawning, and player confinement
		self.checkForSpawn()

	def checkPixelImpact(self):
		if (len(self.enemies.sprites()) != 0):
			self.checkForPlayerDamage()
		if (len(self.playerWeapons.sprites()) != 0):
			self.checkForEnemyDamage()

	def checkForPlayerDamage(self):
	    characterImpact = isGroupImpact(self.player, self.enemies)
	    weaponImpact = isGroupImpact(self.player, self.enemyWeapons)
	    if (characterImpact[0] == True):
	    	damage = 0
	    	for enemy in characterImpact[1]:
	    		damage += enemy.attackPts
	    	self.player.damaged(None, damage)
	    if (weaponImpact[0] == True):
	    	damage = 0
	    	for weapon in weaponImpact[1]:
	    		damage += weapon.attackPts
	    		weapon.death()
	    	self.player.damaged(None, damage)

	def checkForEnemyDamage(self):
		for playerWeapon in self.playerWeapons:
			weapon = playerWeapon.weapon
			weaponImpact = isGroupImpact(playerWeapon, self.enemies)
			if (weaponImpact[0] == True):
				playerWeapon.death()
				damage = playerWeapon.attackPts
				for enemy in weaponImpact[1]:
					enemy.damaged(weapon, damage)

	def checkRectImpact(self):
		self.checkForHatchActivation()
		#self.checkForElevatorActivation()

	def checkForHatchActivation(self):
		for playerWeapon in self.playerWeapons:
			for i in xrange(len(self.main.left_hatches)):
				left_hatch = self.main.left_hatches[i]
				right_hatch = self.main.right_hatches[i]
				if (isRectImpact(playerWeapon, left_hatch)):
					left_hatch.opened = True
					right_hatch.opened = True
					playerWeapon.death()
				elif (isRectImpact(playerWeapon, right_hatch)):
					left_hatch.opened = True
					right_hatch.opened = True
					playerWeapon.death()
		for i in xrange(len(self.main.left_hatches)):
			left_hatch = self.main.left_hatches[i]
			right_hatch = self.main.right_hatches[i]
			if (isRectImpact(self.player, left_hatch)):
				left_hatch.opened = False
				time = pygame.time.get_ticks()
				left_hatch.update(time)
			elif (isRectImpact(self.player, right_hatch)):
				right_hatch.opened = False
				time = pygame.time.get_ticks()
				right_hatch.update(time)

	def checkForElevatorActivation(self):
		for elevator in self.main.elevators:
			if (isRectImpact(self.player, elevator)):
				self.player.elevator = True
				elevator.running = True
				return None

	def checkForSpawn(self):
		for bossTuple in self.main.bossSpawns:
			spawn = bossTuple[0]
			isSpawned = bossTuple[1]
			if (isSpawned == False):
				if (isRectImpact(self.player, spawn)):
					bossClass = bossTuple[2]
					bossTuple[1] = True
					eval(bossClass)
					return None
