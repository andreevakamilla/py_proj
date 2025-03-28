import tkinter as tk
from app import CalorieTrackerApp

def main():
    root = tk.Tk()
    app = CalorieTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

main()