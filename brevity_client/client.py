"""Script for Tkinter chat_window chat client."""

import sys
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

IP = '10.0.0.246'  # my windows machine

HOST = input('Enter host: ')
if not HOST:
    HOST = IP
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)

try:
    client_socket.connect(ADDR)
except ConnectionRefusedError:
    print("Oops! Couldn't connect to the server.")
    sys.exit()


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode('utf8')

            # get latest list of users
            if str(msg).split(' ')[0] == 'USERS':
                users = str(msg).split(' ')[1:]
                # TODO: users should have their own statuses updated on infinite loop
                users_list.delete(0, tkinter.END)
                for user in users:
                    users_list.insert(tkinter.END, user)
            else:
                msg_list.insert(tkinter.END, msg)

        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set('')  # Clears input field.
    client_socket.send(bytes(msg, 'utf8'))
    if msg == '{quit}':
        # https://code.activestate.com/recipes/408997-when-to-not-just-use-socketclose/
        client_socket.shutdown(1)
        client_socket.close()
        chat_window.destroy()
        sys.exit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set('{quit}')
    send()


chat_window = tkinter.Tk()
chat_window.title('brevity')
chat_window.configure(bg='grey')

messages_frame = tkinter.Frame(chat_window)

my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set('Type your name here')
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
users_list = tkinter.Listbox(messages_frame, height=15, width=50)
users_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
users_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(chat_window, textvariable=my_msg, width=45)
entry_field.bind('<Return>', send)
entry_field.pack()

send_button = tkinter.Button(chat_window, text='send', command=send)
send_button.pack()

chat_window.protocol('WM_DELETE_WINDOW', on_closing)

# TODO:
# another thread for retrieving user data?
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts chat_window execution.

# how do i see all users in chat from server

