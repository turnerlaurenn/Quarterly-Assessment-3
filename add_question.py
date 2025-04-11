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

        self.create_widgets()

    def create_widgets(self):
        # Category selection
        self.category_label = tk.Label(self, text="Category:")
        self.category_label.pack(anchor="w", padx=20)
        self.category_var = tk.StringVar(self)
        self.category_choices = ["Analytic Thinking (DS3810)", "Marketing", "Applications Development (DS3850)", "Business Analytics (DS3620)", "Database Management (DS3860)"]
        self.category_var.set(self.category_choices[0])  # Set a default value
        self.category_dropdown = ttk.Combobox(self, textvariable=self.category_var, values=self.category_choices)
        self.category_dropdown.pack(anchor="w", padx=20, pady=5)

        # Question text
        self.question_label = tk.Label(self, text="Question Text:")
        self.question_label.pack(anchor="w", padx=20)
        self.question_entry = tk.Text(self, height=3, width=50)
        self.question_entry.pack(anchor="w", padx=20, pady=5)

        # Options
        self.options_label = tk.Label(self, text="Options:")
        self.options_label.pack(anchor="w", padx=20)
        self.option_entries = []
        for i in range(4):
            label = tk.Label(self, text=f"Option {i+1}:")
            label.pack(anchor="w", padx=30)
            entry = tk.Entry(self, width=40)
            entry.pack(anchor="w", padx=30, pady=2)
            self.option_entries.append(entry)

        # Correct answer
        self.correct_answer_label = tk.Label(self, text="Correct Answer (enter option number 1-4):")
        self.correct_answer_label.pack(anchor="w", padx=20)
        self.correct_answer_entry = tk.Entry(self, width=5)
        self.correct_answer_entry.pack(anchor="w", padx=20, pady=5)

        # Save button
        self.save_button = tk.Button(self, text="Save Question", command=self.save_question)
        self.save_button.pack(pady=20)

    def save_question(self):
        category = self.category_var.get()
        question_text = self.question_entry.get("1.0", tk.END).strip()
        options = [entry.get().strip() for entry in self.option_entries]
        correct_answer_index = self.correct_answer_entry.get().strip()

        if not all([category, question_text, all(options), correct_answer_index]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not correct_answer_index.isdigit() or not 1 <= int(correct_answer_index) <= 4:
            messagebox.showerror("Error", "Correct answer must be a number between 1 and 4.")
            return

        correct_answer = options[int(correct_answer_index) - 1]

        conn = None
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            sql = f"""INSERT INTO {category} (question_text, option1, option2, option3, option4, correct_answer)
                      VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (question_text, options[0], options[1], options[2], options[3], correct_answer))
            conn.commit()
            messagebox.showinfo("Success", "Question added successfully!")
            self.clear_form()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding question: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def clear_form(self):
        self.question_entry.delete("1.0", tk.END)
        for entry in self.option_entries:
            entry.delete(0, tk.END)
        self.correct_answer_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Add Question Form")
    add_question_form = AddQuestion(root)
    add_question_form.pack(padx=20, pady=20)
    root.mainloop()