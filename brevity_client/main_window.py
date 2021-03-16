import sys
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from json import loads
from json.decoder import JSONDecodeError


def serialize_users(msg: str):
	try:
		request = loads(msg)
		if request.get('users'):
			return request.get('users')
		else:
			return None
	except JSONDecodeError:
		return None


class MainWindow(tk.Frame):

	def __init__(self, master, **kwargs):
		# self.send_callback = None
		# self.receive_callback = None
		self.master = master
		self.msg_frame = tk.Frame.__init__(self, master)
		self.my_msg = tk.StringVar()
		self.users_list = tk.Listbox(self.msg_frame, height=15, width=50)
		self.entry_field = tk.Entry(master, textvariable=self.my_msg, width=45)
		self.send_button = tk.Button(master, text='send', command=self.send)
		self.scrollbar = tk.Scrollbar(self.msg_frame)
		self.msg_list = tk.Listbox(self.msg_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
		self.prettify_widgets()
		self.client_socket = socket(AF_INET, SOCK_STREAM)
		self.bufsiz = 1024

	def prettify_widgets(self):
		self.master.protocol('WM_DELETE_WINDOW', self.on_closing)
		self.my_msg.set('Type your name here')

		self.entry_field.bind('<Return>', self.send)
		self.entry_field.pack(side=tk.BOTTOM)

		self.send_button.pack(side=tk.BOTTOM)

		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)

		self.users_list.pack(side=tk.LEFT, fill=tk.BOTH)
		self.users_list.pack()

	def conn(self):
		host = input('Enter host: ')
		if not host:
			print("No host provided. Provide host.")
			sys.exit()

		port = input('Enter port: ')
		if not port:
			port = 33000
		else:
			port = int(port)

		addr = (host, port)

		try:
			self.client_socket.connect(addr)
		except ConnectionRefusedError:
			print("Oops! Couldn't connect to the server.")
			sys.exit()

	def receive(self):
		"""Handles receiving of messages."""
		while True:
			try:
				msg = self.client_socket.recv(self.bufsiz).decode('utf8')

				# get latest list of users
				if serialize_users(msg):
					users = serialize_users(msg).keys()
					self.users_list.delete(0, tk.END)

					for user in users:
						self.users_list.insert(tk.END, user)
				else:
					self.msg_list.insert(tk.END, msg)

			except OSError:  # Possibly client has left the chat.
				break

	def send(self, event=None):  # event is passed by binders.
		"""Handles sending of messages."""
		msg = self.my_msg.get()
		self.my_msg.set('')  # Clears input field.
		self.client_socket.send(bytes(msg, 'utf8'))

	def on_closing(self):
		try:
			self.client_socket.shutdown(1)
			self.client_socket.close()
			self.master.destroy()
			sys.exit()
		except OSError:
			sys.exit()

	def launch(self):
		self.conn()
		receive_thread = Thread(target=self.receive)
		receive_thread.start()
		tk.mainloop()

