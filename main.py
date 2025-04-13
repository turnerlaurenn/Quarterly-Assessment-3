import sys
sys.dont_write_bytecode = True

import tkinter as tk
from tkinter import messagebox
from admin_panel import AdminPanel
from quiz_interface import QuizInterface

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Bowl Application")
        self.geometry("400x200")

        self.admin_window = None
        self.quiz_window = None
        self.quiz_active = False  # Flag to track if a quiz is active

        self.create_widgets()

    def create_widgets(self):
        quiz_button = tk.Button(self, text="Start Quiz", command=self.attempt_open_quiz, padx=60, pady=30, font=("Arial", 16))
        quiz_button.pack(pady=(30, 15))

        admin_button = tk.Button(self, text="Admin Interface", command=self.attempt_open_admin_panel, padx=40, pady=20, font=("Arial", 12))
        admin_button.pack(pady=(10, 30))

    def attempt_open_admin_panel(self):
        if self.quiz_active:
            messagebox.showinfo("Quiz in Progress", "Please finish the current quiz before accessing the Admin Interface.")
        else:
            self.open_admin_panel()

    def open_admin_panel(self):
        if not self.admin_window or not tk.Toplevel.winfo_exists(self.admin_window):
            self.admin_window = AdminPanel(self)
        else:
            self.admin_window.lift()

    def attempt_open_quiz(self):
        if self.admin_window and tk.Toplevel.winfo_exists(self.admin_window):
            messagebox.showinfo("Admin Interface Open", "Please close the Admin Interface before starting a quiz.")
        else:
            self.open_quiz_interface()

    def open_quiz_interface(self):
        if not self.quiz_window or not tk.Toplevel.winfo_exists(self.quiz_window):
            self.quiz_window = QuizInterface(self)
            self.quiz_active = True  # Set the flag when the quiz starts
        else:
            self.quiz_window.lift()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()