import sys
sys.dont_write_bytecode = True

import tkinter as tk
from tkinter import simpledialog, messagebox

# Import the files for the admin actions
from view_questions import ViewQuestions
from add_question import AddQuestion
from delete_question import DeleteQuestion
from modify_question import ModifyQuestion

ADMIN_PASSWORD = "easyadmin123" 

class AdminPanel(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Admin Interface")
        self.geometry("600x400")

        self.master_frame = tk.Frame(self)
        self.master_frame.pack(fill="both", expand=True)

        self.current_view = None
        self.login_frame = None
        self.actions_frame = None
        self.scrollable_canvas = None
        self.scrollbar = None

        self.show_login()

    def show_login(self):
        self.clear_view()
        self.login_frame = tk.Frame(self.master_frame)
        self.login_frame.pack(pady=50)

        password_label = tk.Label(self.login_frame, text="Enter Admin Password:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)
        login_button = tk.Button(self.login_frame, text="Login", command=self.authenticate)
        login_button.pack(pady=10)
        self.current_view = self.login_frame

    def authenticate(self):
        password = self.password_entry.get()
        if password == ADMIN_PASSWORD:
            self.show_admin_actions()
        else:
            messagebox.showerror("Error", "Incorrect Password")
            self.password_entry.delete(0, tk.END)

    def show_admin_actions(self):
        self.clear_view()
        self.actions_frame = tk.Frame(self.master_frame)
        self.actions_frame.pack(pady=20)

        view_button = tk.Button(self.actions_frame, text="View Questions", command=self.open_view_questions, padx=20, pady=10)
        view_button.pack(pady=5)
        add_button = tk.Button(self.actions_frame, text="Add Question", command=self.open_add_question, padx=20, pady=10)
        add_button.pack(pady=5)
        delete_button = tk.Button(self.actions_frame, text="Delete Question", command=self.open_delete_question, padx=20, pady=10)
        delete_button.pack(pady=5)
        modify_button = tk.Button(self.actions_frame, text="Modify Question", command=self.open_modify_question, padx=20, pady=10)
        modify_button.pack(pady=5)

        self.current_view = self.actions_frame

    def open_view_questions(self):
        self.load_scrollable_view(ViewQuestions)

    def open_add_question(self):
        self.load_scrollable_view(AddQuestion)

    def open_delete_question(self):
        self.load_scrollable_view(DeleteQuestion)

    def open_modify_question(self):
        self.load_scrollable_view(ModifyQuestion)

    def load_scrollable_view(self, ViewClass):
        self.clear_view()

        canvas = tk.Canvas(self.master_frame)
        scrollbar = tk.Scrollbar(self.master_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add content
        self.current_view = ViewClass(scrollable_frame)
        self.current_view.pack(fill="both", expand=True)

        back_button = tk.Button(scrollable_frame, text="Back", command=self.show_admin_actions)
        back_button.pack(pady=10)

        # Bind mousewheel scrolling
        self.bind_mousewheel(canvas)

        self.scrollable_canvas = canvas
        self.scrollbar = scrollbar

    def bind_mousewheel(self, widget):
        def on_mousewheel(event):
            # Determine the direction of the mousewheel event
            if event.delta > 0:
                self.scrollable_canvas.yview_scroll(-1, "units")
            else:
                self.scrollable_canvas.yview_scroll(1, "units")

        # Bind the mousewheel event to the canvas
        widget.bind_all("<MouseWheel>", on_mousewheel)

    def clear_view(self):
        for widget in self.master_frame.winfo_children():
            widget.destroy()
        self.current_view = None
        self.login_frame = None
        self.actions_frame = None
        self.scrollable_canvas = None
        self.scrollbar = None

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Prevent extra empty window
    admin_app = AdminPanel(root)
    admin_app.mainloop()
