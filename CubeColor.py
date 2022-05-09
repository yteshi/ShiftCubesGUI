from enum import Enum
from tkinter import ttk

class CubeColor(Enum):
	"""キューブに使われる色を定義した列挙体
	"""
	RED="#FF0000"
	GREEN="#00FF00"
	BLUE="#0000FF"
	YELLOW="#FFFF00"
	CYAN="#00FFFF"
	MAGENDA="#FF00FF"
	BLACK="#000000"
	WHITE="#FFFFFF"

	def __str__(self):
		return self.value