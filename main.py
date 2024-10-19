# main.py

import tkinter as tk
from modules.app import AoK

if __name__ == "__main__":
    root = tk.Tk()
    app = AoK(root)
    root.mainloop()