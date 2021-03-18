"""Script for Tkinter chat_window chat client."""
import tkinter as tk
from brevity_client.main_window import MainWindow


chat_window = tk.Tk()
chat_window.title('brevity')
chat_window.configure(bg='grey')

app = MainWindow(chat_window)
app.launch()
