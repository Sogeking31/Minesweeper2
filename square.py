import pygame
from settings import Settings
from pygame.sprite import Sprite

class Square(Sprite):
	def __init__(self, mn_game):
		super().__init__()
		from settings import Settings
		self.screen = mn_game.screen
		self.screen_rect = self.screen.get_rect()
		
		self.settings = mn_game.settings
		self.bg_square_color = (0, 51, 102)
		self.square_color = (102, 178, 255)
		self.background_color = (204, 229, 255)



	def create_squares(self, x, y, l):
		self.rect = pygame.Rect(x, y, l, l)
		self.rect = pygame.Rect(x, y, l, l)
	
		