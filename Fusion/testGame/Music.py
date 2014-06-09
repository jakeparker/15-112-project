import pygame
from pygame import mixer
from IO import *

class Music(object):
	def __init__(self, fileName, volume = .2, loop = True):
		self.volume = volume
		self.loop = loop
		mixer.music.load(getFilePath(fileName))
		mixer.music.set_volume(self.volume)
		mixer.music.play(self.loop)

	def stop(self):
		mixer.music.fadeout(500)

	def pause(self):
		mixer.music.pause()

	def play(self):
		mixer.music.unpause()
