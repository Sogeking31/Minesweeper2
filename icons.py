import pygame
from pygame.sprite import Sprite 

class ICONS(Sprite):
	def __init__(self, mn_game, symbol):
		super().__init__()
		self.screen = mn_game.screen
		self.screen_rect = self.screen.get_rect()

		self.image = pygame.image.load(f'images/{symbol}.bmp')
		self.rect = self.image.get_rect()