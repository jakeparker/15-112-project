import pygame, os
from pygame.locals import *
from os.path import abspath, normpath, dirname, exists, join, getsize


#currentDir =  normpath(join(os.getcwd(), dirname(__file__)))
currentDir = abspath(dirname(__file__))
fusionDir = normpath(join(currentDir, '..'))
dataDir = normpath(join(currentDir, '..', 'data'))


def getFilePath(fileName, path=fusionDir):
	for root, dirs, files in os.walk(path):
		if fileName in files:
			return join(root, fileName)

	raise SystemExit, "unable to locate %s" % fileName


def load_file(fileName, mode='r'):
	try:
		path = getFilePath(fileName)
		return open(path, mode)
	except:
		raise SystemExit, "unable to open %s" % path

def load_image(fileName):
	try:
		path = getFilePath(fileName)
		return pygame.image.load(path)
	except:
		raise SystemExit, "unable to load %s" % fileName


def load_sound(fileName, volume=0.5):
	try:
		path = getFilePath(fileName)
		sound = pygame.mixer.Sound(path)
		sound.set_volume(volume)
		return sound
	except:
		raise SystemExit, "unable to load %s" %(fileName)

def play_music(fileName, volume=0.5, loop=-1):
	try:
		path = getFilePath(fileName)
		pygame.mixer.music.load(path)
		pygame.mixer.music.set_volume(volume)
		pygame.mixer.music.play(loop)
	except:
		raise SystemExit, "unable to load %s" % fileName
