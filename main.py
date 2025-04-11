import tkinter as tk
from admin_panel import AdminPanel
from quiz_interface import QuizInterface

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Bowl Application")
        self.geometry("300x150") 

        self.admin_window = None
        self.quiz_window = None  

        self.create_widgets()

    def create_widgets(self):
        admin_button = tk.Button(self, text="Admin Interface", command=self.open_admin_panel, padx=20, pady=10)
        admin_button.pack(pady=15)

        quiz_button = tk.Button(self, text="Start Quiz", command=self.open_quiz_interface, padx=20, pady=10) 
        quiz_button.pack(pady=15)

    def open_admin_panel(self):
        if not self.admin_window or not tk.Toplevel.winfo_exists(self.admin_window):
            self.admin_window = tk.Toplevel(self)
            admin_panel = AdminPanel(self.admin_window)
        else:
            self.admin_window.lift() # Bring existing window to front

    def open_quiz_interface(self):  
        if not self.quiz_window or not tk.Toplevel.winfo_exists(self.quiz_window):
            self.quiz_window = tk.Toplevel(self)
            quiz_interface = QuizInterface(self.quiz_window)  
        else:
            self.quiz_window.lift()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()