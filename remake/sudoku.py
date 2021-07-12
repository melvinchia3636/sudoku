from tkinter import *
from tkinter.font import Font
from functools import partial
import requests
from fake_useragent import UserAgent as ua

class GameGrid(Tk):
	def __init__(self):
		super(GameGrid, self).__init__()
		
		self.board_width, self.board_height = (9, 9)
		self.region_width, self.region_height = (3, 3)
		self.outer_border_width, self.inner_border_width = (5, 2)
		self.font_size = 28
		self.height_add = 10

		self.background = "#f6f5f7"
		self.foreground = "#4450ff"
		self.hover_background = "#D8D8D8"
		self.hover_foreground = "#4450ff"
		self.selected_background = "#4450ff"
		self.selected_foreground = "#FFFFFF"

		self.new_icon = PhotoImage(file="assets/new.png")
		self.check_icon = PhotoImage(file="assets/check.png")
		self.file_icon = PhotoImage(file="assets/file.png")
		self.hint_icon = PhotoImage(file="assets/hint.png")
		self.edit_icon = PhotoImage(file="assets/edit.png")
		self.play_icon = PhotoImage(file="assets/play.png")
		self.replay_icon = PhotoImage(file="assets/replay.png")
		self.settings_icon = PhotoImage(file="assets/settings.png")

		self.current_selected_cell = None
		self.current_highlight_cells = []
		self.current_board = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
		self.current_board_editable_map = [[True for _ in range(self.board_width)] for _ in range(self.board_height)]

		self.title('Sudoku')
		self.config(background=self.background)
		self.iconbitmap('./assets/logo.ico')

		self.setupWidget()
		self.placeWidget()
		self.setupEvent()
		self.generateBoard()

	def setupWidget(self):
		self.grid_container = Frame(self, bg=self.foreground)
		self.grid = [
			[
				Entry(
					self.grid_container, 
					width=3, 
					justify="center", 
					relief="flat",
					bg=self.background,
					disabledbackground=self.background,
					disabledforeground=self.foreground,
					state="disabled",
					font=Font(size=self.font_size, weight="bold"),
					cursor="arrow"
				) for _ in range(self.board_width)
			] for _ in range(self.board_height)
		]

		self.button_container = Frame(self, bg=self.background)
		self.new_button = Button(self.button_container, image=self.new_icon, relief="flat", bg=self.background)
		self.check_button = Button(self.button_container, image=self.check_icon, relief="flat", bg=self.background)
		self.file_button = Button(self.button_container, image=self.file_icon, relief="flat", bg=self.background)
		self.edit_button = Button(self.button_container, image=self.edit_icon, relief="flat", bg=self.background)
		self.hint_button = Button(self.button_container, image=self.hint_icon, relief="flat", bg=self.background)
		self.play_button = Button(self.button_container, image=self.play_icon, relief="flat", bg=self.background)
		self.replay_button = Button(self.button_container, image=self.replay_icon, relief="flat", bg=self.background)
		self.settings_button = Button(self.button_container, image=self.settings_icon, relief="flat", bg=self.background)

	def placeWidget(self):
		self.grid_container.pack(padx=(20, 0), pady=20, side="left")
		[
			[
				self.grid[y][x].grid(
					row=y, 
					column=x, 
					ipady=self.height_add, 
					padx=(self.outer_border_width, 0) if not x%self.region_width else (self.inner_border_width, self.outer_border_width if (x+1) == self.board_width else 0), 
					pady=(self.outer_border_width, 0) if not y%self.region_height else (self.inner_border_width, self.outer_border_width if (y+1) == self.board_height else 0)
				) for x in range(self.board_width)
			] for y in range(self.board_height)
		]

		self.button_container.pack(side="left", padx=(10, 20))
		self.new_button.pack(pady=10)
		self.play_button.pack(pady=10)
		self.replay_button.pack(pady=10)
		self.hint_button.pack(pady=10)
		self.edit_button.pack(pady=10)
		self.check_button.pack(pady=10)
		self.file_button.pack(pady=10)
		self.settings_button.pack(pady=10)

	def writeCell(self, y, x, i):
		cell = self.grid[y][x]
		cell.config(state='normal')
		cell.delete(0, 'end')
		cell.insert(0, str(i))
		cell.config(state='disabled')

	def updateBoard(self, run="ingame"):
		if run == "ingame":
			for y in range(self.board_height):
				for x in range(self.board_width):
					cell_content = self.grid[y][x].get()
					if not cell_content or not cell_content.isdigit(): num = 0
					else: num = int(cell_content)
					self.current_board[y][x] = num

		elif run == "new":
			for y in range(self.board_height):
				for x in range(self.board_width):
					num = self.current_board[y][x]
					self.writeCell(y, x, num if num else "")
		else: return

	def updateHighlight(self):
		if self.current_selected_cell:
			_y, _x = self.current_selected_cell
			current_selected_cell = self.grid[_y][_x].get()
			if not current_selected_cell or not current_selected_cell.isdigit(): 
				self.current_highlight_cells = []
				return
			else: current_selected_num = int(current_selected_cell)

			for y in range(self.board_height):
				for x in range(self.board_width):
					cell = (y, x)
					cell_content = self.grid[y][x].get()
					if not cell_content or not cell_content.isdigit(): continue
					else: num = int(cell_content)

					if num == current_selected_num:
						if cell not in self.current_highlight_cells:
							if num == current_selected_num and cell:
								self.current_highlight_cells.append(cell)
					else:
						if cell in self.current_highlight_cells:
							self.current_highlight_cells.remove(cell)

	def renderHighlight(self):
		for y in range(self.board_height):
			for x in range(self.board_width):
				cell = (y, x)
				if cell in self.current_highlight_cells or cell == self.current_selected_cell:
					self.grid[y][x].config(disabledbackground=self.selected_background, disabledforeground=self.selected_foreground)
				else:
					self.grid[y][x].config(disabledbackground=self.background, disabledforeground=self.foreground)

	def onCellMouseLeaveCallback(self, y, x, e):
		if self.current_selected_cell == (y, x) or (y, x) in self.current_highlight_cells:
			e.widget.configure(disabledbackground=self.selected_background, disabledforeground=self.selected_foreground)
		else:
			e.widget.config(disabledbackground=self.background, disabledforeground=self.foreground)

	def onCellMouseEnterCallback(self, y, x, e):
		if self.current_selected_cell != (y, x) and (y, x) not in self.current_highlight_cells:
			e.widget.configure(disabledbackground=self.hover_background, disabledforeground=self.hover_foreground)

	def selectCellCallback(self, y, x, e):
		self.current_selected_cell = (y, x)

		self.updateHighlight()
		self.renderHighlight()

	def insertNumberCallback(self, n, e):
		if self.current_selected_cell:
			y, x = self.current_selected_cell
			if self.current_board_editable_map[y][x]:
				self.writeCell(y, x, n)

				self.updateBoard()
				self.updateHighlight()
				self.renderHighlight()

	def clearCellCallback(self, e):
		if self.current_selected_cell:
			y, x = self.current_selected_cell
			if self.current_board_editable_map[y][x]:
				self.writeCell(y, x, "")

				self.updateBoard()
				self.updateHighlight()
				self.renderHighlight()

	def setupEvent(self): 
		[
			[
				[
					self.grid[y][x].bind('<Enter>', partial(self.onCellMouseEnterCallback, y, x)),
					self.grid[y][x].bind('<Leave>', partial(self.onCellMouseLeaveCallback, y, x)),
					self.grid[y][x].bind('<Button-1>', partial(self.selectCellCallback, y, x)),
				]
				for x in range(self.board_width)
			] for y in range(self.board_height)
		]
		[self.bind(str(i), partial(self.insertNumberCallback, i)) for i in range(1, 10)],
		self.bind('<BackSpace>', self.clearCellCallback)

	def generateEditableMap(self):
		editable_map = []
		for y in range(self.board_height):
			editable_map.append([])
			for x in range(self.board_width):
				if self.current_board[y][x]: is_editable = False
				else: is_editable = True
				editable_map[-1].append(is_editable)

		self.current_board_editable_map = editable_map

	def generateBoard(self):
		request_headers = {
			'x-requested-with': 'XMLHttpRequest', 
			'user-agent': ua().random
		}
		response = requests.get('https://sudoku.com/api/level/hard', headers=request_headers).json()
		if response:
			raw_data = response["mission"]
			board = [[int(j) for j in raw_data[i:i+self.board_width]] for i in range(0, self.board_width*self.board_height, self.board_height)]
			
			if len(board[0]) == self.board_width and len(board) == self.board_height:
				self.current_board = board
				self.updateBoard(run="new")
				self.generateEditableMap()
			else:
				raise RuntimeError('Sudoku board size doesn\'t match')
		else:
			raise RuntimeError('Sudoku board fetching failed')

root = GameGrid()
root.mainloop()