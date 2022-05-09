import tkinter as tk
import platform
if platform.platform().startswith('macOS'):
	from tkmacosx import Button
else:
	from tkinter import Button


class SerialPortSelectDialog(tk.Toplevel):
	"""シリアルポート選択画面（tkinter.Toplevelを継承）
	"""
	def __init__(self, master, portlist, connected_port,  *args, **kwargs):
		"""SerialPortSelectDialogのコンストラクタ

		Args
			master: 親要素
			portlist: ポートのリスト
			connected_port: 現在接続されているポート
		"""
		super().__init__(master, *args, **kwargs)

		self.title('シリアルポートの選択')
		self.geometry('500x200')
		self._initialize(portlist, connected_port)

		self.result = None

		self.wait_visibility()
		self.grab_set()
		self.wait_window(self)
		
	def _initialize(self, portlist, connected_port):
		"""初期化関数

		Args
			portlist List: ポートのリスト
			connected_port: 現在接続されているポート
		"""
		# main frame
		tkf_main = tk.Frame(self)
		tkf_main.pack(fill=tk.BOTH, expand=True)

		# Connect button
		self.select_btn = Button(tkf_main, text='接続', command=self._connect)
		self.select_btn.pack(side=tk.BOTTOM, pady=10)

		# Serialport list
		self.listbox = tk.Listbox(
			tkf_main,
			selectmode=tk.SINGLE
		)
		self.listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
		for i, port in enumerate(portlist):
			self.listbox.insert(i, str(port))
			if connected_port == port:
				self.listbox.select_set(i)

	def validate(self):
		"""選択されたポート（Listboxの要素）を有効化する関数

		有効化された場合：選択した要素は，親要素（master）に返される
		有効化されない場合：親要素（master）には，`None`が返される．
		"""
		tmp = self.listbox.curselection()
		if len(tmp) == 0:
			self.result = None
		else:
			self.result = self.listbox.get(tmp[0])
		
		return self.result
	
	def _connect(self):
		"""「接続」ボタンが押されたときのコールバック関数
		"""
		self.validate()
		if self.result is not None:
			self.destroy()
	

