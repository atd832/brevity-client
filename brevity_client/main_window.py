import sys
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Frame):

	def __init__(self, master, **kwargs):
		self.master = master
		self.msg_frame = tk.Frame.__init__(self, master)
		self.my_msg = tk.StringVar()
		self.entry_field = tk.Entry(master, textvariable=self.my_msg, width=45)
		self.send_button = ttk.Button(master, text='send', command=self.send)
		self.scrollbar = tk.Scrollbar(self.msg_frame)
		self.msg_list = tk.Listbox(self.msg_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
		self.prettify_widgets()
		self.msg_client_socket = socket(AF_INET, SOCK_STREAM)
		self.bufsiz = 1024
		self.host = ''

	def prettify_widgets(self):
		self.master.protocol('WM_DELETE_WINDOW', self.on_closing)
		self.my_msg.set('Type your name here')

		self.entry_field.bind('<Return>', self.send)
		self.entry_field.pack(side=tk.BOTTOM)

		self.send_button.pack(side=tk.BOTTOM)

		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)

	def conn(self):
		self.host = input('Enter host: ')
		if not self.host:
			print("No host provided. Provide host.")
			sys.exit()

		port = input('Enter port: ')
		if not port:
			port = 33000
		else:
			port = int(port)

		addr = (self.host, port)

		try:
			self.msg_client_socket.connect(addr)
		except ConnectionRefusedError:
			print("Oops! Couldn't connect to the server.")
			sys.exit()

	def receive_msg(self):
		"""Handles receiving of messages."""
		while True:
			try:
				msg = self.msg_client_socket.recv(self.bufsiz).decode('utf8')
				self.msg_list.insert(tk.END, msg)
			except OSError:
				break

	def send(self, event=None):
		"""Handles sending of messages."""
		msg = self.my_msg.get()
		self.my_msg.set('')  # Clears input field.
		self.msg_client_socket.send(bytes(msg, 'utf8'))

	def on_closing(self):
		try:
			self.msg_client_socket.shutdown(1)
			self.msg_client_socket.close()
			self.master.destroy()
			sys.exit()
		except OSError:
			sys.exit()

	def launch(self):
		self.conn()
		receive_msg_thread = Thread(target=self.receive_msg)
		receive_msg_thread.start()

		tk.mainloop()

