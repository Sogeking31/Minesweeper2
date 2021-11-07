import pygame
import sys
from random import sample

from settings import Settings
from square import Square
from line import Line
from icons import ICONS
from sensor import Sensor
from button import Button

class Minesweeper:
	def __init__(self):
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width, 
			self.settings.screen_height))
		self.screen_rect = self.screen.get_rect()

		background = Square(self)
		self.square = Square(self)
		self.line = Line(self)
		self.sensor = Sensor(self)
		self.bg_square = Square(self)
		self.button = Button(self)

		self.bg_squares = pygame.sprite.Group()
		self.squares = pygame.sprite.Group()
		self.mines = pygame.sprite.Group()
		self.lines = pygame.sprite.Group()
		self.clicked_squares = pygame.sprite.Group()

		self.ones = pygame.sprite.Group()
		self.twos = pygame.sprite.Group()
		self.threes = pygame.sprite.Group()
		self.fours = pygame.sprite.Group()
		self.fives = pygame.sprite.Group()
		self.sixs = pygame.sprite.Group()
		self.sevens = pygame.sprite.Group()
		self.eights = pygame.sprite.Group()
		self.zeros = pygame.sprite.Group()

		self.sensors = pygame.sprite.Group()
		self.flags = pygame.sprite.Group()
		self.false_mines = pygame.sprite.Group()
		self.exploded_mines = pygame.sprite.Group()

		self.start_time= 0
		self.stop_time= '0'
		self._create_background()

		self.game_active = False
		self.show_menu = True
		self.show_won = False

	def _run_game(self): 
	# game loop
		while True:
			clock = pygame.time.Clock()
			clock.tick(20)

			self._check_events()	
			self._update_screen()

	def _show_number_ofmines(self):
		""" shows how many mines remaining in the top left corner"""
		self.width, self.height = 100, 35
		self.box_color = (32, 32, 32)
		self.digits_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		self.box_rect = pygame.Rect(0, 0, self.width, self.height)
		self.box_rect.center = (self.settings.screen_width - 100, 37.5)

		self.number_ofmines = str( self.settings.num_mines
		 -len(self.flags.sprites()))
		self.msg = self.font.render(self.number_ofmines, True, self.digits_color,
			self.timer_color)
		self.msg_rect = self.msg.get_rect()
		self.msg_rect.center = self.box_rect.center

	def _timer(self):
		""" place a timer in the top right corner"""
		self.width, self.height = 100, 35
		self.timer_color = (32, 32, 32)
		self.digits_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		self.timer_rect = pygame.Rect(0, 0, self.width, self.height)
		self.timer_rect.center = (100, 37.5)

		if self.game_active:
			self.time = str((pygame.time.get_ticks()-self.start_time)//1000)
			#start the timer when the game starts
		else:
			self.time =str(self.stop_time)
			#freeze the timer when game won or gameover
		self.digits = self.font.render(self.time, True, self.digits_color,
		self.timer_color)
		self.digits_rect = self.digits.get_rect()
		self.digits_rect.center = self.timer_rect.center


	def _start_game(self): # start the game
		""" creating function that starts the game when called"""
		self.show_menu = False
		self.settings.reset_groups(self)
		self.screen = pygame.display.set_mode((self.settings.screen_width, 
			self.settings.screen_height))
		self._create_map()
		self._create_background()

		self.game_active = True # making game active again
		self.game_over = False

	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit()
				elif event.key == pygame.K_r:
					self._start_game()
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
				# recognize mouse left click
				mouse_pos = pygame.mouse.get_pos()
				self._check_mouse_left(mouse_pos)
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
				#recognize mouse right click
				mouse_pos = pygame.mouse.get_pos()
				self._check_mouse_right(mouse_pos)

	def _check_mouse_right(self, mouse_pos):
		""" putting a flag when right clicking only if game active and the
		 square was not clicked before"""
		if self.game_active:
			# getting clicked square position and check if it still in square group
			for square in self.squares.sprites(): 
				square_clicked = square.rect.collidepoint(mouse_pos)
				if square_clicked: 
					for flag in self.flags.sprites(): 
						#if square already flagged remove flag
						flag_clicked = flag.rect.collidepoint(mouse_pos)
						if flag_clicked:
							self.flags.remove(flag)
							return
					flag = ICONS(self, 'flag')
					flag.rect.center = square.rect.center
					self.flags.add(flag)
				

	def _create_map(self):
		squares = Square(self)
		# making game bounderies

		bg_square_l = 32 #making square
		#length based on bounday and number of coloumns

		for coloumn_num in range(self.settings.num_coloumns):
			for row_num in range(self.settings.num_rows):
				self._create_square(bg_square_l, coloumn_num, row_num)
		# checking numbers of rows and column needed in setting folder

	def _create_square(self, bg_square_l, coloumn_num, row_num):
		self.bg_square = Square(self) #backgrounds squares only for better visiual
		self.square = Square(self)
		#square position
		bg_x = bg_square_l * coloumn_num + 20 
		bg_y = bg_square_l * row_num + 75
		square_l = bg_square_l - 2
		x = bg_x + 1
		y = bg_y + 1
		self.bg_square.rect = pygame.Rect(bg_x, bg_y, bg_square_l, bg_square_l)
		self.square.rect = pygame.Rect(x, y, square_l, square_l)

		self.bg_squares.add(self.bg_square)
		self.squares.add(self.square)

	def _create_background(self):
		""" the background shown after the square getting clicked"""
		self.background = Square(self)
		background_width = self.settings.screen_width - 40
		background_height = self.settings.screen_height - 95
		background_x = 20
		background_y = 75
		self.background.rect = pygame.Rect(background_x, background_y,
		 background_width, background_height)


	def _create_mines(self):
		""" posion the mines randomly behind the squares"""
		mines_pos=[]
		mines_pos.extend( sample(self.squares.sprites(), self.settings.num_mines))
		# chosong x numbers of squares randomly and add them to mines list
		for mine_pos in mines_pos: #placing a mine behind each chosen square
			mine = ICONS(self, 'mine')
			mine.rect.center = mine_pos.rect.center
			self.mines.add(mine) #add mines to mines group

	def _create_lines(self):
		# making lines in background for better visiual
		space = 32

		for row_num in range(self.settings.num_rows + 1):
			h_start_pos = (20, (space * row_num) + 75)
			h_end_pos = (self.settings.screen_width - 20, (space * row_num) +  75)
			self.line.draw_line(h_start_pos, h_end_pos)

		for coloumn_num in range(self.settings.num_coloumns + 1):
			v_start_pos = ((space * coloumn_num) + 20, 75)
			v_end_pos = ((space * coloumn_num) + 20, self.settings.screen_height - 20)
			self.line.draw_line(v_start_pos, v_end_pos)

	def _detect_mines(self):
		""" placing an invisible square sensor around each empty square that count the number 
		of mines around that square"""
		for square in self.squares.sprites():
			if not pygame.sprite.spritecollideany(square, self.mines):
				self.sensor = pygame.Rect((0, 0), (64, 64))

				self.sensor.center =square.rect.center
				surrounding_squares = self.sensor.collidelistall(self.mines.sprites())
				num_surr = len(surrounding_squares)

				self._create_numbers(square, num_surr)
				#calling create number method with the correct number

	def _create_numbers(self, square, num_surr):
		""" place number icon behind the square and add it to the group of that number"""
		if num_surr == 1:
			one = ICONS(self, 'one_')
			one.rect.center = square.rect.center
			self.ones.add(one)
		elif num_surr == 2:
			two = ICONS(self, 'two_')
			two.rect.center = square.rect.center
			self.twos.add(two)
		elif num_surr == 3:
			three = ICONS(self, 'three_')
			three.rect.center = square.rect.center
			self.threes.add(three)
		elif num_surr == 4:
			four = ICONS(self, 'four_')
			four.rect.center = square.rect.center
			self.fours.add(four)
		elif num_surr == 5:
			five = ICONS(self, 'five_')
			five.rect.center = square.rect.center
			self.fives.add(five)
		elif num_surr == 6:
			six = ICONS(self, 'six_')
			six.rect.center = square.rect.center
			self.sixs.add(six)
		elif num_surr == 7:
			seven = ICONS(self, 'seven_')
			seven.rect.center = square.rect.center
			self.sevens.add(seven)
		elif num_surr == 8:
			eight = ICONS(self, 'eight_')
			eight.rect.center = square.rect.center
			self.eights.add(eight)
		elif num_surr == 0:
			self.zeros.add(square) 

	def _show_surrounding(self, number, number_clicked):
		""" the function auto-click all squares that surrounds the number
		that was clicked, only works if the the number of flags around
		that number equals the number itself"""
		self.sensor = Sensor(self) 
		self.sensor.create_sensor(number_clicked) 
		num_offlags = pygame.sprite.spritecollide(self.sensor, self.flags, False)
		if not pygame.sprite.spritecollideany(number_clicked, self.squares):
			if len(num_offlags) == number:
				surr_squares = pygame.sprite.spritecollide(self.sensor,
				 self.squares, False)
				for surr_square in surr_squares:
					if not pygame.sprite.spritecollideany(surr_square,
					 self.flags):
						self.squares.remove(surr_square)

	def _check_mouse_left(self, mouse_pos):
		"""this function check if the gane is active or not when
		left-click then act accordingly"""
		if self.game_active:
			self._active_left(mouse_pos)
		elif self.game_active == False:
			self._inactive_left(mouse_pos)

	def _active_left(self, mouse_pos):
		for flag in self.flags.sprites():
			#when a flag is clicked
			flag_clicked = flag.rect.collidepoint(mouse_pos)
			if flag_clicked:
				return()
		
		for mine in self.mines.sprites():
			# when mine clicked the game is over and all mines become visible
			mine_clicked = mine.rect.collidepoint(mouse_pos)
			if mine_clicked:
				exploded_mine = ICONS(self, 'exploded_mine')
				exploded_mine.rect.center = mine.rect.center
				self.exploded_mines.add(exploded_mine)
				self._game_over()
				
		# when a number is clicked
		for one in self.ones.sprites():
			one_clicked = one.rect.collidepoint(mouse_pos)
			if one_clicked:
				self._show_surrounding(1, one)
		for two in self.twos.sprites():
			two_clicked = two.rect.collidepoint(mouse_pos)
			if two_clicked:
				self._show_surrounding(2, two)
		for three in self.threes.sprites():
			three_clicked = three.rect.collidepoint(mouse_pos)
			if three_clicked:
				self._show_surrounding(3, three)
		for four in self.fours.sprites():
			four_clicked = four.rect.collidepoint(mouse_pos)
			if four_clicked:
				self._show_surrounding(4, four)
		for five in self.fives.sprites():
			five_clicked = five.rect.collidepoint(mouse_pos)
			if five_clicked:
				self._show_surrounding(5, five)
		for six in self.sixs.sprites():
			six_clicked = six.rect.collidepoint(mouse_pos)
			if six_clicked:
				self._show_surrounding(6, six)
		for seven in self.sevens.sprites():
			seven_clicked = seven.rect.collidepoint(mouse_pos)
			if seven_clicked:
				self._show_surrounding(7, seven)
				
		for square in self.squares.sprites():
		#when a square is clicked
			square_clicked = square.rect.collidepoint(mouse_pos)
			if square_clicked:
				self.squares.remove(square) # remove the clicked square from square group
				if len(self.squares.sprites()) == (self.settings.num_rows *
				 self.settings.num_coloumns - 1):
					self.start_time = pygame.time.get_ticks()
					# calling create mine methode only after clicking the first square to prevent
					# losing at the start
					self._create_mines()
					self._detect_mines()
					 # calling create number method here because the mines were created after
					 # clicking the square
					self.sensor = pygame.Rect((0, 0), (64, 64))
					self.sensor.center =square.rect.center
					surrounding_squares = self.sensor.collidelistall(self.mines.sprites())
					num_surr = len(surrounding_squares)
					self._create_numbers(square, num_surr)

	def _game_won(self, time):
		""" when game won show game won msg and make it inactive
		and record the time"""
		self.game_active = False
		self.stop_time = self.time

		self.wn_image = self.font.render(f'You won! time: {time}s', True,
		 (0,153,0))
		self.wn_image_rect = self.wn_image.get_rect()
		self.wn_image_rect.center = (self.settings.screen_width/2, 
		 self.settings.screen_height/2)
		self.show_won = True

	def _inactive_left(self, mouse_pos):
		if self.show_menu == False:
		# show the menu after losing/winning
			if self.screen_rect.collidepoint(mouse_pos):
				self.settings.reset_groups(self)
				self.settings.apply_expert()
				self._create_background()
				self.screen = pygame.display.set_mode((self.settings.screen_width, 
			self.settings.screen_height))
				self.show_won = False
				self.show_menu = True
				return()

		if self.show_menu:
		#start the game with the chosen diffcaulty
			if self.button.rect_main.collidepoint(mouse_pos):
				self.settings.apply_normal()
				self._start_game()
				
			elif self.button.rect_ez.collidepoint(mouse_pos):
				self.settings.apply_easy()
				self._start_game()

			elif self.button.rect_hd.collidepoint(mouse_pos):
				self.settings.apply_expert()
				self._start_game()

	def _update_squares(self):
		""" this method solve some errors in the game and add some functions"""

		# when a square with a zero surrounding mines all surrounding squares
		# will be licked (removed) automatically
		for zero in self.zeros.sprites():
			if zero not in self.squares: #checking if "zero" squares are clicked
				self.sensor = Sensor(self) 
				self.sensor.create_sensor(zero) #sensor placed here only for using it in
				#sprit collide function to remove the squares
				empty_squares = pygame.sprite.spritecollide(self.sensor,
				 self.squares, False)
				for empty_square in empty_squares:
					if not pygame.sprite.spritecollideany(empty_square, self.flags):
						self.squares.remove(empty_square)

		for mine in self.mines.sprites():
		# when mine are auto-clicked the game does not end, this line solve this problem
			if not pygame.sprite.spritecollideany(mine, self.squares):
				if not pygame.sprite.spritecollideany(mine, self.flags):
					self._game_over()

		for bg_square in self.bg_squares.sprites(): #make sure the background squares
		# are removed too when a square is clicked
			if not pygame.sprite.spritecollideany(bg_square, self.squares):
				self.bg_squares.remove(bg_square)

	def _game_over(self):
		""" show all mines after losing, make game inactive"""
		pygame.sprite.groupcollide(self.mines, self.squares, False, True)
		for flag in self.flags.sprites():
			if not pygame.sprite.spritecollideany(flag, self.mines):
				false_mine = ICONS(self, 'false_mine')
				false_mine.rect.center = flag.rect.center
				self.false_mines.add(false_mine)
		self.stop_time = self.time
		self.game_over = True
		self.game_active= False

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""

		self.screen.fill(self.settings.bg_color)

		self.background.screen.fill(self.background.background_color,
		 self.background.rect)

		self._timer()
		self._show_number_ofmines()

		self.screen.fill(self.timer_color, self.timer_rect)
		if len(self.squares.sprites()) <= (self.settings.num_rows *
			self.settings.num_coloumns - 1) :
			self.screen.blit(self.digits, self.digits_rect)

		self.screen.fill(self.box_color, self.box_rect)
		self.screen.blit(self.msg, self.msg_rect)

		self.ones.draw(self.screen)
		self.twos.draw(self.screen)
		self.threes.draw(self.screen)
		self.fours.draw(self.screen)
		self.fives.draw(self.screen)
		self.sixs.draw(self.screen)
		self.sevens.draw(self.screen)
		self.eights.draw(self.screen)

		self.mines.draw(self.screen)

		self._create_lines()
		self._update_squares()

		for bg_square in self.bg_squares.sprites():
			bg_square.screen.fill(bg_square.bg_square_color,
				 bg_square.rect)

		for square in self.squares.sprites():
			square.screen.fill(square.square_color,square.rect)

		self.flags.draw(self.screen)
		self.false_mines.draw(self.screen)
		self.exploded_mines.draw(self.screen)
		
		if self.show_menu:
			self.button.draw_button()
		if self.show_won:
			self.screen.blit(self.wn_image, self.wn_image_rect)

		if (len(self.squares.sprites()) == self.settings.num_mines
		 and self.game_over == False):
			self._game_won(self.time) 

		pygame.display.flip()

if __name__== '__main__':
	# Make a game instance, and run the game.
	mn = Minesweeper()
	mn._run_game()
