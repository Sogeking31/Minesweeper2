import pygame
from pygame.sprite import Sprite
from settings import Settings

class Line(Sprite):
	def __init__(self, mn_game):
		super().__init__()
		self.settings = Settings()
		self.screen = mn_game.screen
		self.screen_rect = self.screen.get_rect()
		self.line_color = (0, 25, 51)

	def draw_line(self, start_pos, end_pos):
		self.line = pygame.draw.line(self.screen, self.line_color, start_pos, end_pos, 1)

