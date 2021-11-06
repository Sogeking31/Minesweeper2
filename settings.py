class Settings:
	def __init__(self):
		self.num_rows = 16
		self.num_coloumns = 30

		self.screen_width = self.num_coloumns * 32 + 40
		self.screen_height = self.num_rows * 32 + 95
		self.bg_color = (230, 230, 230)

		self.square_boarder = 10

		self.num_mines = 99

	def apply_easy(self):
		self.num_rows = 9
		self.num_coloumns = 9
		self.num_mines = 10
		self.screen_width = self.num_coloumns * 32 + 40
		self.screen_height = self.num_rows * 32 + 95

	def apply_normal(self):
		self.num_rows = 16
		self.num_coloumns = 16
		self.num_mines = 40
		self.screen_width = self.num_coloumns * 32 + 40
		self.screen_height = self.num_rows * 32 + 95

	def apply_expert(self):
		self.num_rows = 16
		self.num_coloumns = 30
		self.num_mines = 99
		self.screen_width = self.num_coloumns * 32 + 40
		self.screen_height = self.num_rows * 32 + 95

	def reset_groups(self, mn_game):
		mn_game.bg_squares.empty()
		mn_game.squares.empty()
		mn_game.mines.empty()
		mn_game.clicked_squares.empty()
		mn_game.ones.empty()
		mn_game.twos.empty()
		mn_game.threes.empty()
		mn_game.fours.empty()
		mn_game.fives.empty()
		mn_game.sixs.empty()
		mn_game.sevens.empty()
		mn_game.eights.empty()
		mn_game.zeros.empty()
		mn_game.sensors.empty()
		mn_game.flags.empty()
		mn_game.false_mines.empty()
		mn_game.exploded_mines.empty()