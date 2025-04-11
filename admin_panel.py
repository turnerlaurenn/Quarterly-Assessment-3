import tkinter as tk
from tkinter import simpledialog, messagebox

# Import the files for the admin actions
from view_questions import ViewQuestions
from add_question import AddQuestion
from delete_question import DeleteQuestion
from modify_question import ModifyQuestion

ADMIN_PASSWORD = "easyadmin123"  # Replace with a more secure method

class AdminPanel(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Admin Interface")
        self.geometry("400x300")

        self.master_frame = tk.Frame(self)
        self.master_frame.pack(fill="both", expand=True)

        self.current_view = None
        self.show_login()

    def show_login(self):
        self.clear_view()
        login_frame = tk.Frame(self.master_frame)
        login_frame.pack(pady=50)

        password_label = tk.Label(login_frame, text="Enter Admin Password:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.pack(pady=5)
        login_button = tk.Button(login_frame, text="Login", command=self.authenticate)
        login_button.pack(pady=10)

    def authenticate(self):
        password = self.password_entry.get()
        if password == ADMIN_PASSWORD:
            self.show_admin_actions()
        else:
            messagebox.showerror("Error", "Incorrect Password")
            self.password_entry.delete(0, tk.END)

    def show_admin_actions(self):
        self.clear_view()
        actions_frame = tk.Frame(self.master_frame)
        actions_frame.pack(pady=20)

        view_button = tk.Button(actions_frame, text="View Questions", command=self.open_view_questions, padx=20, pady=10)
        view_button.pack(pady=5)
        add_button = tk.Button(actions_frame, text="Add Question", command=self.open_add_question, padx=20, pady=10)
        add_button.pack(pady=5)
        delete_button = tk.Button(actions_frame, text="Delete Question", command=self.open_delete_question, padx=20, pady=10)
        delete_button.pack(pady=5)
        modify_button = tk.Button(actions_frame, text="Modify Question", command=self.open_modify_question, padx=20, pady=10)
        modify_button.pack(pady=5)

    def open_view_questions(self):
        self.clear_view()
        self.current_view = ViewQuestions(self.master_frame)
        self.current_view.pack(fill="both", expand=True)

    def open_add_question(self):
        self.clear_view()
        self.current_view = AddQuestion(self.master_frame)
        self.current_view.pack(fill="both", expand=True)

    def open_delete_question(self):
        self.clear_view()
        self.current_view = DeleteQuestion(self.master_frame)
        self.current_view.pack(fill="both", expand=True)

    def open_modify_question(self):
        self.clear_view()
        self.current_view = ModifyQuestion(self.master_frame)
        self.current_view.pack(fill="both", expand=True)

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

if __name__ == "__main__":
    # This block is for testing admin_panel.py directly
    root = tk.Tk()
    root.title("Test Main Window (for Admin Panel)")
    admin_app = AdminPanel(root)
    root.mainloop()