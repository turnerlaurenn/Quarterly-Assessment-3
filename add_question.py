import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DATABASE_NAME = 'questions.db'

class AddQuestion(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.label = tk.Label(self, text="Add New Question", font=("Arial", 16))
        self.label.pack(pady=10)

        self.category_label = tk.Label(self, text="Select Category:")
        self.category_label.pack(anchor="w", padx=20)
        self.category_var = tk.StringVar(self)
        self.category_choices = ["", "Analytic Thinking (DS3810)", "Marketing", "Applications Development (DS3850)", "Business Analytics (DS3620)", "Database Management (DS3860)"]
        self.category_var.set(self.category_choices[0])
        self.category_dropdown = ttk.Combobox(self, textvariable=self.category_var, values=self.category_choices, state="readonly") # Make it readonly
        self.category_dropdown.pack(anchor="w", padx=20, pady=5)

        self.question_text_label = tk.Label(self, text="Question Text:")
        self.question_text_label.pack(anchor="w", padx=20, pady=10)
        self.question_text_entry = tk.Text(self, height=3, width=50, wrap=tk.WORD) # Use tk.Text with word wrapping
        self.question_text_entry.pack(anchor="w", padx=20, pady=5)
        self.question_text_entry.bind("<KeyRelease>", self.check_enable_add_button)
        self.question_text_entry.bind("<FocusOut>", self.check_enable_add_button)

        self.option1_label = tk.Label(self, text="Option 1:")
        self.option1_label.pack(anchor="w", padx=30)
        self.option1_entry = tk.Entry(self, width=40)
        self.option1_entry.pack(anchor="w", padx=30, pady=2)
        self.option1_entry.bind("<KeyRelease>", self.check_enable_add_button)
        self.option1_entry.bind("<FocusOut>", self.check_enable_add_button)

        self.option2_label = tk.Label(self, text="Option 2:")
        self.option2_label.pack(anchor="w", padx=30)
        self.option2_entry = tk.Entry(self, width=40)
        self.option2_entry.pack(anchor="w", padx=30, pady=2)
        self.option2_entry.bind("<KeyRelease>", self.check_enable_add_button)
        self.option2_entry.bind("<FocusOut>", self.check_enable_add_button)

        self.option3_label = tk.Label(self, text="Option 3:")
        self.option3_label.pack(anchor="w", padx=30)
        self.option3_entry = tk.Entry(self, width=40)
        self.option3_entry.pack(anchor="w", padx=30, pady=2)
        self.option3_entry.bind("<KeyRelease>", self.check_enable_add_button)
        self.option3_entry.bind("<FocusOut>", self.check_enable_add_button)

        self.option4_label = tk.Label(self, text="Option 4:")
        self.option4_label.pack(anchor="w", padx=30)
        self.option4_entry = tk.Entry(self, width=40)
        self.option4_entry.pack(anchor="w", padx=30, pady=2)
        self.option4_entry.bind("<KeyRelease>", self.check_enable_add_button)
        self.option4_entry.bind("<FocusOut>", self.check_enable_add_button)

        self.correct_answer_label = tk.Label(self, text="Correct Answer (enter text of the correct option):")
        self.correct_answer_label.pack(anchor="w", padx=20)
        self.correct_answer_entry = tk.Entry(self, width=40)
        self.correct_answer_entry.pack(anchor="w", padx=20, pady=5)
        self.correct_answer_entry.bind("<KeyRelease>", self.check_enable_add_button)
        self.correct_answer_entry.bind("<FocusOut>", self.check_enable_add_button)

        self.add_button = tk.Button(self, text="Add Question", command=self.add_new_question, state=tk.DISABLED) # Initially disabled
        self.add_button.pack(pady=20)

        # Bind the Combobox selection event
        self.category_dropdown.bind("<<ComboboxSelected>>", self.create_table_if_not_exists)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.check_enable_add_button)

    def check_enable_add_button(self, event=None):
        category_selected = self.category_var.get() != ""
        question_text_filled = self.question_text_entry.get("1.0", tk.END).strip() != ""
        option1_filled = self.option1_entry.get().strip() != ""
        option2_filled = self.option2_entry.get().strip() != ""
        option3_filled = self.option3_entry.get().strip() != ""
        option4_filled = self.option4_entry.get().strip() != ""
        correct_answer_filled = self.correct_answer_entry.get().strip() != ""

        if (category_selected and question_text_filled and option1_filled and
                option2_filled and option3_filled and option4_filled and correct_answer_filled):
            self.add_button.config(state=tk.NORMAL)
        else:
            self.add_button.config(state=tk.DISABLED)

    def create_table_if_not_exists(self, event=None):
        category = self.category_var.get()
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{category}' (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                question_text TEXT NOT NULL,
                                option1 TEXT NOT NULL,
                                option2 TEXT NOT NULL,
                                option3 TEXT NOT NULL,
                                option4 TEXT NOT NULL,
                                correct_answer TEXT NOT NULL
                            )""")
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error creating table: {e}")
        finally:
            if conn:
                conn.close()

    def add_new_question(self):
        category = self.category_var.get()
        question_text = self.question_text_entry.get("1.0", tk.END).strip()
        option1 = self.option1_entry.get().strip()
        option2 = self.option2_entry.get().strip()
        option3 = self.option3_entry.get().strip()
        option4 = self.option4_entry.get().strip()
        correct_answer = self.correct_answer_entry.get().strip()

        if not category:
            messagebox.showerror("Error", "Please select a category first.")
            return
        if not all([question_text, option1, option2, option3, option4, correct_answer]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        conn = None
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO '{category}' (question_text, option1, option2, option3, option4, correct_answer) VALUES (?, ?, ?, ?, ?, ?)",
                           (question_text, option1, option2, option3, option4, correct_answer))
            conn.commit()
            messagebox.showinfo("Success", "Question added successfully!")
            self.question_text_entry.delete("1.0", tk.END)
            self.option1_entry.delete(0, tk.END)
            self.option2_entry.delete(0, tk.END)
            self.option3_entry.delete(0, tk.END)
            self.option4_entry.delete(0, tk.END)
            self.correct_answer_entry.delete(0, tk.END)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding question: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Add New Question Form")
    add_question_form = AddQuestion(root)
    add_question_form.pack(padx=20, pady=20)
    root.mainloop()