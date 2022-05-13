import tkinter as tk
import platform

from SarasaButton import SarasaButton
if platform.platform().startswith('macOS'):
	from tkmacosx import Button, Radiobutton
	is_macos = True
else:
	from tkinter import Button, Radiobutton
	is_macos = False

import serial
import serial.tools.list_ports

from SarasaButton import SarasaButton
from SerialPortSelectDialog import SerialPortSelectDialog
from gencode.change_color import left_forward, right_forward


def set_aspect(content_frame, pad_frame, aspect_ratio):
	"""要素のアスペクト比を固定して拡大・縮小するように設定するメソッド

	Args
		content_frame (tkinter.Frame): アスペクト比を固定する要素
		pad_frame (tkinter.Frame): パディングに用いる要素
		aspect_ratio (float): アスペクト比

	See Also
		https://stackoverflow.com/questions/16523128/resizing-tkinter-frames-with-fixed-aspect-ratio

	"""

	def enforce_aspect_ratio(event):
		desired_width = event.width
		desired_height = int(event.width / aspect_ratio)

		if desired_height > event.height:
			desired_height = event.height
			desired_width = int(event.height * aspect_ratio)

		offset_x = (event.width - desired_width) / 2
		offset_y = (event.height - desired_height) / 2
		if offset_x < 0:
			offset_x = 0
		if offset_y < 0:
			offset_y = 0
		content_frame.place(in_=pad_frame,
		                    x=offset_x,
		                    y=offset_y,
		                    width=desired_width,
		                    height=desired_height)

	pad_frame.bind("<Configure>", enforce_aspect_ratio)


def calc_array_diff(array1, array2, modulo=4):
	"""配列の差分（array2 - array1）を計算する関数"""
	diff_array = []
	for val1, val2 in zip(array1, array2):
		diff_array.append((val2 - val1) % modulo)

	return diff_array


class ShifterGUI(tk.Tk):
	if is_macos:
		size_coef = 1
	else:
		size_coef = 0.1

	# tkf_sarasa
	container_grid_row = 1
	container_grid_cols = (0, 2)
	copy_paste_grid_row = 2
	copy_paste_grid_cols = (0, 2)
	arrow_grid_row = container_grid_row
	arrow_grid_col = 1

	def __init__(self, cube, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.feed_flag = tk.BooleanVar()
		self.sarasa_left = []
		self.sarasa_right = []
		self.clip_board = []

		self.cube = cube
		self.statusmsg = tk.StringVar()
		self.comport = tk.StringVar()
		self.serial = None

		self._initialize()

	def _initialize(self):
		self._initialize_root()
		self._initialize_tkf_sarasa()
		self._initialize_arrow_canvas()
		self._initialize_sarasa_buttons_left()
		self._initialize_sarasa_buttons_right()
		self._initialize_copy_paste()
		self._initialize_sift_rbtn()
		self._initialize_control_btns()
		self._initialize_status_bar()

	def _initialize_root(self):
		self.title('S(h)ift Cubes GUI')
		self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='icon64.png'))

		screenheight = self.winfo_screenheight()
		screenwidth = self.winfo_screenwidth()

		self.geometry(f"{screenwidth//2}x{screenheight//2}")
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=2)
		self.grid_columnconfigure(2, weight=1)

		self._btn_size = int(screenheight // 6 * ShifterGUI.size_coef)
		self._pad_size = self._btn_size // 10

	def _initialize_tkf_sarasa(self):
		tkf_sarasa = tk.Frame(self, pady=10)
		tkf_sarasa.pack(fill=tk.BOTH, expand=True)
		tkf_sarasa.grid_rowconfigure(ShifterGUI.container_grid_row, weight=1)
		tkf_sarasa.grid_columnconfigure(ShifterGUI.container_grid_cols[0], weight=1)
		tkf_sarasa.grid_columnconfigure(ShifterGUI.container_grid_cols[1], weight=1)

		self._tkf_sarasa = tkf_sarasa

	def _initialize_arrow_canvas(self):
		tkf_canvas_container = tk.Frame(self._tkf_sarasa)
		tkf_canvas_container.grid(row=ShifterGUI.arrow_grid_row,
		                          column=ShifterGUI.arrow_grid_col,
		                          sticky="NEWS")
		tkf_canvas_container.grid_columnconfigure(0, weight=1)
		tkf_canvas_container.grid_rowconfigure(0, weight=1)

		### 1.0.1 PADDING CANVAS
		pad_canvas = tk.Frame(tkf_canvas_container, borderwidth=0, width=105, height=50)
		pad_canvas.grid(row=0, column=0, sticky="NEWS", padx=10, pady=10)

		### 1.0.2. CANVAS CONTENT
		tkf_canvas = tk.Frame(tkf_canvas_container)
		canvas = tk.Canvas(tkf_canvas, width=100, height=50)
		canvas.pack(expand=True)
		canvas.create_polygon((10, 15, 10, 35, 70, 35, 70, 45, 100, 25, 70, 5, 70, 15, 10, 15),
		                      fill='DeepSkyBlue3',
		                      outline='black')
		set_aspect(tkf_canvas, pad_canvas, 2.0)

	def _initialize_sarasa_buttons_left(self):
		tkf_sarasa_left_container = tk.Frame(self._tkf_sarasa)
		tkf_sarasa_left_container.grid(row=ShifterGUI.container_grid_row,
		                               column=ShifterGUI.container_grid_cols[0],
		                               sticky="NEWS")
		tkf_sarasa_left_container.grid_columnconfigure(0, weight=1)
		tkf_sarasa_left_container.grid_rowconfigure(0, weight=1)

		### 1.1.1. LEFT PADDING
		pad_frame_left = tk.Frame(tkf_sarasa_left_container, borderwidth=0, width=200, height=200)
		pad_frame_left.grid(row=0, column=0, sticky="NEWS", padx=10, pady=20)

		### 1.1.2. LEFT CONTENT
		tkf_sarasa_left = tk.Frame(tkf_sarasa_left_container, padx=10)

		for i in range(4):
			tkf_sarasa_left.grid_columnconfigure(i, weight=1)
			tkf_sarasa_left.grid_rowconfigure(i, weight=1)

		for i in range(4):
			for j in range(4):
				button_ij = SarasaButton(tkf_sarasa_left, self.cube, width=100, height=100)
				button_ij.grid(row=i, column=j, sticky="NEWS")
				self.sarasa_left.append(button_ij)

		set_aspect(tkf_sarasa_left, pad_frame_left, 1.0 / 1.0)

	def _initialize_sarasa_buttons_right(self):
		tkf_sarasa_right_container = tk.Frame(self._tkf_sarasa)
		tkf_sarasa_right_container.grid(row=ShifterGUI.container_grid_row,
		                                column=ShifterGUI.container_grid_cols[1],
		                                sticky="NEWS")
		tkf_sarasa_right_container.grid_columnconfigure(0, weight=1)
		tkf_sarasa_right_container.grid_rowconfigure(0, weight=1)

		### 1.2.1. RIGHT PADDING
		pad_frame_right = tk.Frame(
		    tkf_sarasa_right_container,
		    borderwidth=0,
		    # background="bisque", # DEBUG
		    width=200,
		    height=200)
		pad_frame_right.grid(row=0, column=0, sticky="NEWS", padx=10, pady=20)

		### 1.2.2. RIGHT CONTENT
		tkf_sarasa_right = tk.Frame(tkf_sarasa_right_container, padx=10)

		for i in range(4):
			tkf_sarasa_right.grid_columnconfigure(i, weight=1)
			tkf_sarasa_right.grid_rowconfigure(i, weight=1)

		for i in range(4):
			for j in range(4):
				button_ij = SarasaButton(tkf_sarasa_right, self.cube, width=100, height=100)
				button_ij.grid(row=i, column=j, sticky="NEWS")
				self.sarasa_right.append(button_ij)

		set_aspect(tkf_sarasa_right, pad_frame_right, 1.0 / 1.0)

	def _initialize_copy_paste(self):

		def copy_to_clip_board(is_left=True):
			if is_left:
				array = self.sarasa_left
			else:
				array = self.sarasa_right

			self.clip_board = []
			for btn in array:
				self.clip_board.append(btn.top_color_index)

		def paste_from_clip_board(is_left=True):
			if is_left:
				array = self.sarasa_left
			else:
				array = self.sarasa_right

			if len(self.clip_board) == len(array):
				for clip, btn in zip(self.clip_board, array):
					btn.top_color_index = clip
					btn.update_button_color()

				self.clip_board = []

		def reset_btn(is_left=True):
			if is_left:
				array = self.sarasa_left
			else:
				array = self.sarasa_right

			for btn in array:
				btn.top_color_index = 0
				btn.update_button_color()

		tkf_left_cp = tk.Frame(self._tkf_sarasa)
		tkf_left_cp.grid(row=ShifterGUI.copy_paste_grid_row,
		                 column=ShifterGUI.copy_paste_grid_cols[0])
		cp_left = Button(tkf_left_cp, command=lambda: copy_to_clip_board(True), text='コピー')
		cp_left.pack(side=tk.LEFT)
		Button(tkf_left_cp, command=lambda: reset_btn(True), text='リセット').pack(side=tk.RIGHT)
		ps_left = Button(tkf_left_cp, command=lambda: paste_from_clip_board(True), text='ペースト')
		ps_left.pack(side=tk.TOP)

		tkf_right_cp = tk.Frame(self._tkf_sarasa)
		tkf_right_cp.grid(row=ShifterGUI.copy_paste_grid_row,
		                  column=ShifterGUI.copy_paste_grid_cols[1])
		cp_right = Button(tkf_right_cp, command=lambda: copy_to_clip_board(False), text='コピー')
		cp_right.pack(side=tk.LEFT)
		Button(tkf_right_cp, command=lambda: reset_btn(False), text='リセット').pack(side=tk.RIGHT)
		ps_right = Button(tkf_right_cp, command=lambda: paste_from_clip_board(False), text='ペースト')
		ps_right.pack(side=tk.TOP)

	def _initialize_sift_rbtn(self):
		self.feed_flag.set(False)

		tkf_sift_position = tk.Frame(self, pady=10)
		tkf_sift_position.pack(side=tk.TOP, expand=False)

		lbl_description = tk.Label(tkf_sift_position, text="ふるいの初期位置")
		lbl_description.pack()

		Radiobutton(tkf_sift_position, text='ひだり', variable=self.feed_flag,
		            value=False).pack(side=tk.LEFT)
		Radiobutton(tkf_sift_position, text='みぎ', variable=self.feed_flag,
		            value=True).pack(side=tk.LEFT)

	def _initialize_control_btns(self):
		tkf_control = tk.Frame(self, pady=5)
		tkf_control.pack(side=tk.TOP, expand=False)

		def send_button_pressed():
			before, after = self.create_sarasa_array()
			diff_array = calc_array_diff(before, after)
			if self.feed_flag.get():
				command, _ = left_forward(diff_array)
			else:
				command, _ = right_forward(diff_array)

			self.send_command(command)

		btn_send = Button(tkf_control,
		                  text='送信',
		                  width=self._btn_size,
		                  height=self._btn_size // 3,
		                  command=send_button_pressed)
		btn_send.pack(side=tk.LEFT)

		def ask_port():
			modal = SerialPortSelectDialog(
			    self, list(map(lambda x: x.device, serial.tools.list_ports.comports())),
			    self.comport.get())
			if modal.result:
				self.comport.set(modal.result)
				self.connect()

		btn_serial = Button(tkf_control,
		                    text='シリアルポート設定',
		                    width=self._btn_size,
		                    height=self._btn_size // 3,
		                    command=ask_port)
		btn_serial.pack(side=tk.LEFT)

	def _initialize_status_bar(self):
		self.comport.set('Not Connected')
		tkf_status_bar = tk.Frame(self, bd=1, relief=tk.SUNKEN)
		tkf_status_bar.pack(side=tk.BOTTOM, fill=tk.X)
		tk.Label(tkf_status_bar, textvariable=self.comport).pack(side=tk.RIGHT)
		tk.Label(tkf_status_bar, text='Comport:').pack(side=tk.RIGHT)
		tk.Label(tkf_status_bar, textvariable=self.statusmsg).pack(side=tk.LEFT)

	def connect(self):
		"""シリアルポートに接続する

		- self.serial が Noneでない場合は，一度切断して再接続する
		- baud rateは9600
		- self.comportに格納されているポートに接続する
		"""
		try:
			if self.serial is not None and self.serial.is_open:
				self.disconnect()

			self.serial = serial.Serial(self.comport.get(), 9600, timeout=2)
			self.statusmsg.set(f'[Info] Successfully connected to {self.comport.get()}')
		except Exception as e:
			self.statusmsg.set(f'[Error] Error occured while connecting to {self.comport.get()}')

	def disconnect(self):
		"""現在接続しているシリアルポートから切断する
		"""
		try:
			self.serial.close()
			self.statusmsg.set('[Info] Successfully disconnected.')
		except Exception as e:
			self.statusmsg.set('[Error] Error occured while disconnecting.')

	def send_command(self, command):
		"""接続されているシリアルポートにコマンドを送信する

		Args
			command List(int): コマンドの配列 
		"""
		send_byte_length = -1
		send_binary = bytes(command)
		if self.serial is not None and self.serial.is_open:
			try:
				send_byte_length = self.serial.write(send_binary)
				self.statusmsg.set(f'[Info] command({(len(command)-1)//4})={command}')
			except serial.serialutil.SerialException as se:
				print('[Error] Send commands failed. Please retry...')
				self.disconnect()
				self.connect()
				send_byte_length = self.serial.write(send_binary)

		return send_byte_length

	def create_sarasa_array(self):
		"""現在のボタンの状態から，それぞれのキューブの回転量を計算する
		"""
		num_before = []
		num_after = []
		for btn_before, btn_after in zip(self.sarasa_left, self.sarasa_right):
			num_before.append(btn_before.top_color_index)
			num_after.append(btn_after.top_color_index)

		return num_before, num_after


if __name__ == '__main__':
	from CubeColor import CubeColor
	from Cube import Cube
	# root = ShifterGUI(Cube([CubeColor.WHITE, CubeColor.BLUE, CubeColor.RED, CubeColor.YELLOW]))
	root = ShifterGUI(Cube([CubeColor.WHITE, CubeColor.BLACK, CubeColor.MAGENDA, CubeColor.GREEN]))
	root.mainloop()