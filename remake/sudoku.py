from tkinter import *
from tkinter.font import Font
from functools import partial

class GameGrid(Tk):
	def __init__(self):
		super(GameGrid, self).__init__()
		
		self.board_width, self.board_height = (9, 9)
		self.outer_border_width, self.inner_border_width = (5, 2)
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

		self.title('Sudoku')
		self.config(background=self.background)
		self.iconbitmap('./assets/logo.ico')

		self.setupWidget()
		self.placeWidget()
		self.setupEvent()

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
					font=Font(size=28, weight="bold"),
					cursor="arrow"
				) for _ in range(self.board_width)
			] for _ in range(self.board_height)
		]

		self.button_container = Frame(self)
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
					ipady=10, 
					padx=(self.outer_border_width, 0) if not x%3 else (self.inner_border_width, self.outer_border_width if (x+1) == self.board_width else 0), 
					pady=(self.outer_border_width, 0) if not y%3 else (self.inner_border_width, self.outer_border_width if (y+1) == self.board_height else 0)
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

	def onCellMouseLeaveCallback(self, y, x, e):
		e.widget.configure(disabledbackground=self.foreground if self.current_selected_cell == (y, x) else self.background)

	def onCellMouseEnterCallback(self, y, x, e):
		e.widget.configure(disabledbackground=self.foreground if self.current_selected_cell == (y, x) else self.hover_background)

	def selectCellCallback(self, y, x, e):
		if self.current_selected_cell:
			_y, _x = self.current_selected_cell
			self.grid[_y][_x].config(disabledbackground=self.background, disabledforeground=self.foreground)
		self.grid[y][x].config(disabledbackground=self.selected_background, disabledforeground=self.selected_foreground)
		self.current_selected_cell = (y, x)

	def insertNumberCallback(self, n, e):
		if self.current_selected_cell:
			y, x = self.current_selected_cell
			cell = self.grid[y][x]
			cell.config(state='normal')
			cell.delete(0, 'end')
			cell.insert(0, str(n))
			cell.config(state='disabled')

	def clearCellCallback(self, e):
		if self.current_selected_cell:
			y, x = self.current_selected_cell
			cell = self.grid[y][x]
			cell.config(state='normal')
			cell.delete(0, 'end')
			cell.config(state='disabled')

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

root = GameGrid()
root.mainloop()