from CubeColor import CubeColor

class Cube:
	"""S(h)ift Cubes で用いられるキューブの色情報を表すクラス
	"""
	def __init__(self, colors):
		"""Cubeクラスのコンストラクタ

		Args:
			colors List(CubeColor): キューブに使われている4つの色
		"""
		if len(colors) != 4:
			self = None
			raise ValueError(f"The length of `colors` must be 4. Currently it is {len(colors)}.")
		else:
			self.colors = []
			for i, color in enumerate(colors):
				if type(color) != CubeColor:
					raise ValueError(f"The type of the list item must be `CubeColor`. (type(colors[{i}])={type(color)})")

				self.colors.append(color)
