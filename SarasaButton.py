import platform
if platform.platform().startswith('macOS'):
	import tkmacosx as tk
else:
	import tkinter as tk

from Cube import Cube

class SarasaButton(tk.Button):
	"""GUIに使われるボタン（tkinter.Buttonを継承）
	"""
	def __init__(self, parent, cube, *args, **kwargs):
		"""SarasaButtonのコンストラクタ
		
		Args
			parent: ボタンの親要素
			cube (Cube): そのボタンのキューブの色の設定
			*args: *argsは親クラス（tkinter.Button）のコンストラクタにそのまま渡される．
			**kwargs: **kwargsは親クラス（tkinter.Button）のコンストラクタにそのまま渡される．
		"""
		if type(cube) != Cube:
			self.cube = None
			raise ValueError(f"check type of `cube`. it must be `Cube`")
		else:
			self.cube = cube

		self.top_color_index = 0
		super().__init__(parent, *args, **kwargs)
		self.bind('<Button-1>', self.left_click)
		self.bind('<Button-2>', self.right_click)
		self.update_button_color()
		
	def next_color(self, inverse=False):
		"""ボタンの次の状態の色に設定する

		注意：ボタンの色を更新するためには，
		このメソッドで色を設定した後に，
		`update_button_color`を呼ぶ必要がある．
		"""
		if inverse:
			self.top_color_index -= 1
		else:
			self.top_color_index += 1
		
		self.top_color_index %= 4
	
	def get_top_color(self):
		"""現在の表示色を取得する

		Returns
			Cube: 現在の色
		"""
		return self.cube.colors[self.top_color_index]

	def update_button_color(self):
		"""ボタンの色を更新する．
		"""
		self.config(bg=str(self.get_top_color()))
	
	def left_click(self, event):
		"""ボタンが押されたときのコールバック関数

		次の色に設定（`next_color`）し，ボタンの色を更新（`update_button_color`）する．
		"""
		self.next_color()
		self.update_button_color()

	def right_click(self, event):
		"""右クリックされたときのコールバック関数

		`command`メソッドと逆の色にする
		"""
		self.next_color(inverse=True)
		self.update_button_color()	

	