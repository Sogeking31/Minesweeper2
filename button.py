import pygame.font
from settings import Settings

class Button:

	def __init__(self, mn_game):
		"""initilize button attributes."""
		self.settings = Settings()
		self.screen = mn_game.screen
		self.screen_rect = self.screen.get_rect()

		# set the dimension and properties of the button.
		self.width, self.height = 150, 50
		self.button_color = (0, 153, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 40)

		#build the button's rect object and center it.
		self.rect_main = pygame.Rect(0, 0, self.width, self.height)
		self.rect_main.center = (500, 350)

		self.rect_ez = pygame.Rect(0, 0, self.width, self.height)
		self.rect_ez.center = (300, 350)

		self.rect_hd = pygame.Rect(0, 0, self.width, self.height)
		self.rect_hd.center = (700, 350)

		#the button message needs to be prepped only once.
		self._prep_msg()
		self._prep_ez()
		self._prep_hd()

	def _prep_msg(self):
		"""turn msg into a rendered image and center text on the button."""
		self.msg_image = self.font.render('normal', True, self.text_color,
			self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect_main.center

	def _prep_ez(self):
		"""turn msg into a rendered image and center text on the button."""
		self.ez_image = self.font.render('easy', True, self.text_color,
			self.button_color)
		self.ez_image_rect = self.ez_image.get_rect()
		self.ez_image_rect.center = self.rect_ez.center

	def _prep_hd(self):
		"""turn msg into a rendered image and center text on the button."""
		self.hd_image = self.font.render('hard', True, self.text_color,
			self.button_color)
		self.hd_image_rect = self.hd_image.get_rect()
		self.hd_image_rect.center = self.rect_hd.center

	def _prep_wn(self, time):
		"""turn msg into a rendered image and center text on the button."""
		self.wn_image = self.font.render(f'You Won ! time:{time}', True, self.text_color,
			self.button_color)
		self.wn_image_rect = self.wn_image.get_rect()
		self.rect_wn.center = (self.settings.screen_width/2, 
		 self.settings.screen_height/2)
		self.wn_image_rect.center = self.rect_wn.center


	def draw_button(self):
		# draw blank button and then draw message.
		self.screen.fill(self.button_color, self.rect_main)
		self.screen.blit(self.msg_image, self.msg_image_rect)
		self.screen.fill(self.button_color, self.rect_ez)
		self.screen.blit(self.ez_image, self.ez_image_rect)
		self.screen.fill(self.button_color, self.rect_hd)
		self.screen.blit(self.hd_image, self.hd_image_rect)

	def draw_wn(self):
		self.screen.fill(self.button_color, self.rect_wn)
		self.screen.blit(self.wn_image, self.wn_image_rect)