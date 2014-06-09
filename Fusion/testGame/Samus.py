import pygame, sys
from collections import defaultdict
from pygame.locals import *
from Music import Music
from IO import *

class Samus(object):
	def __init__(self, game):
		self.game = game
		self.controls = game.controls
		self.window = game.window
		self.screen = game.screen
		self.load_attributes()

	def load_attributes(self):
		self.load_dirs()

	def load_dirs(self):
		self.up = False
		self.down = False
		self.right = False
		self.left = False
		self.slant = False
		self.fire = False
		self.fire = False
		self.mode = False
		self.jump = False

	def keyEvent(self):
		pass