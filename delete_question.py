import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DATABASE_NAME = 'questions.db'

class DeleteQuestion(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.label = tk.Label(self, text="Delete Existing Question", font=("Arial", 16))
        self.label.pack(pady=10)

        self.category_label = tk.Label(self, text="Select Category:")
        self.category_label.pack(anchor="w", padx=20)
        self.category_var = tk.StringVar(self)
        self.category_choices = ["", "Analytic Thinking (DS3810)", "Marketing", "Applications Development (DS3850)", "Business Analytics (DS3620)", "Database Management (DS3860)"]
        self.category_var.set(self.category_choices[0])
        self.category_dropdown = ttk.Combobox(self, textvariable=self.category_var, values=self.category_choices, state="readonly")
        self.category_dropdown.pack(anchor="w", padx=20, pady=5)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.populate_question_list)

        self.question_list_label = tk.Label(self, text="Select Question to Delete:")
        self.question_list_label.pack(anchor="w", padx=20)
        self.question_list_scrollbar = tk.Scrollbar(self)
        self.question_list = tk.Listbox(self, width=60, yscrollcommand=self.question_list_scrollbar.set)
        self.question_list.pack(anchor="w", padx=20, pady=5)
        self.question_list_scrollbar.config(command=self.question_list.yview)
        self.question_list_scrollbar.pack(side="right", fill="y")

        self.delete_button = tk.Button(self, text="Delete Selected Question", command=self.delete_selected_question, state=tk.DISABLED)
        self.delete_button.pack(pady=20)

        self.populate_question_list()

    def populate_question_list(self, event=None):
        self.question_list.delete(0, tk.END)
        category = self.category_var.get()
        if not category:
            self.delete_button.config(state=tk.DISABLED)
            return
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(f"SELECT rowid, question_text FROM \"{category}\"")
            questions = cursor.fetchall()
            for rowid, text in questions:
                self.question_list.insert(tk.END, f"ID: {rowid} - {text[:50]}...") # Show a preview of the question
            if questions:
                self.delete_button.config(state=tk.NORMAL)
            else:
                self.delete_button.config(state=tk.DISABLED)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching questions: {e}")
            self.delete_button.config(state=tk.DISABLED)
        finally:
            if conn:
                conn.close()

    def delete_selected_question(self):
        selected_index = self.question_list.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a question to delete.")
            return

        selected_question = self.question_list.get(selected_index[0])
        try:
            question_id = selected_question.split(" - ")[0].split(": ")[1]
        except IndexError:
            messagebox.showerror("Error", "Could not parse question ID.")
            return
        category = self.category_var.get()

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete question ID {question_id} from {category}?"):
            conn = None
            try:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM \"{category}\" WHERE rowid = ?", (question_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Question ID {question_id} deleted successfully from {category}.")
                self.populate_question_list() # Refresh the list after deletion
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error deleting question: {e}")
                if conn:
                    conn.rollback()
            finally:
                if conn:
                    conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Delete Question Form")
    delete_question_form = DeleteQuestion(root)
    delete_question_form.pack(padx=20, pady=20)
    root.mainloop()