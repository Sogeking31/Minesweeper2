import pygame
from settings import Settings
from pygame.sprite import Sprite

class Sensor(Sprite):
	def __init__(self, mn_game):
		super().__init__()
		from settings import Settings
		self.screen = mn_game.screen
		self.screen_rect = self.screen.get_rect()

	def create_sensor(self, square):
		self.rect = pygame.Rect((0, 0), (64, 64))
		self.rect.center = square.rect.center

