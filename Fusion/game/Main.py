import pygame, os
from IO import *
import Menu


def Main(width, height):
	os.environ["SDL_VIDEO_CENTERED"] = "1"
	pygame.mixer.pre_init(44100, -16, 2, 512)
	pygame.init()
	pygame.display.set_mode((width, height), pygame.RESIZABLE)
	pygame.display.set_caption("Metroid Fusion")
	pygame.display.set_icon(load_image("mf_icon.png"))
	#pygame.mouse.set_visible(0)


	window = pygame.display.get_surface()
	intro = Menu.Menu(window, width, height)
	intro.run()

if __name__ == "__main__": Main(640, 480)  