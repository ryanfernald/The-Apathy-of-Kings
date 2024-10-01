import tkinter as tk
import platform

class AoK:
    def __init__(self, master):
        self.master = master
        master.title("The Apathy of Kings")


if __name__ == "__main__":
    root = tk.Tk()
    app = AoK(root)
    root.mainloop()