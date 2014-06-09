import pygame
import numpy
from main import *

def load_image(fileName):
	pathway = '/Users/Jake/CMU/15-112/TermProject/original/sprites/bg/'
	return pygame.image.load(pathway + fileName + '.png')

def main(width, height, scaleBy):
	print "title running"
	title = True
	pygame.init()
	screen = pygame.display.set_mode((width*scaleBy, height*scaleBy-2))
	pygame.display.set_caption("Metroid Fusion")
	title_screen = load_image("splash_screen")
	title_array = pygame.surfarray.array2d(title_screen)
 
	# numpy array scaling method based on:
	# http://osdir.com/ml/python.pygame/2001-12/msg00000.html
	n = scaleBy
	if (title_array.shape[0] >= title_array.shape[1]):
		scaled = numpy.repeat(numpy.repeat(title_array,n,1), n,0)
	else:
		scaled = numpy.repeat(numpy.repeat(title_array, n,0), n,1)

	print scaled.shape
	print screen.get_size()
	print title_screen.get_size()
	pygame.surfarray.blit_array(screen, scaled)

	while title:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_r):
					title = False
					game = Game()
					game.run(width, height, scaleBy)
		pygame.display.flip()


if __name__ == "__main__":
	print "title"
	main(240*2, 160*2, 2)