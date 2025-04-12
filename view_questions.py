import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DATABASE_NAME = 'questions.db'

class ViewQuestions(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.label = tk.Label(self, text="View Existing Questions", font=("Arial", 16))
        self.label.pack(pady=10)

        self.category_label = tk.Label(self, text="Select Category:")
        self.category_label.pack(anchor="w", padx=20)
        self.category_var = tk.StringVar(self)
        self.category_choices = ["Analytic Thinking (DS3810)", "Marketing", "Applications Development (DS3850)", "Business Analytics (DS3620)", "Database Management (DS3860)"]
        self.category_var.set(self.category_choices[0])
        self.category_dropdown = ttk.Combobox(self, textvariable=self.category_var, values=self.category_choices, state="readonly")
        self.category_dropdown.pack(anchor="w", padx=20, pady=5)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.populate_question_details)

        self.question_details_text = tk.Text(self, height=15, width=70)
        self.question_details_text.pack(padx=20, pady=10)
        self.question_details_text.config(state=tk.DISABLED) # Make it read-only

        self.populate_question_details()

    def populate_question_details(self, event=None):
        self.question_details_text.config(state=tk.NORMAL)
        self.question_details_text.delete("1.0", tk.END)
        category = self.category_var.get()
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(f"SELECT question_text, option1, option2, option3, option4, correct_answer FROM \"{category}\"")
            questions = cursor.fetchall()
            if questions:
                for q in questions:
                    self.question_details_text.insert(tk.END, f"Question: {q[0]}\n")
                    self.question_details_text.insert(tk.END, f"  Option 1: {q[1]}\n")
                    self.question_details_text.insert(tk.END, f"  Option 2: {q[2]}\n")
                    self.question_details_text.insert(tk.END, f"  Option 3: {q[3]}\n")
                    self.question_details_text.insert(tk.END, f"  Option 4: {q[4]}\n")
                    self.question_details_text.insert(tk.END, f"  Correct Answer: {q[5]}\n\n")
            else:
                self.question_details_text.insert(tk.END, f"No questions found in the '{category}' category.\n")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching questions: {e}")
            self.question_details_text.insert(tk.END, f"Error fetching questions: {e}\n")
        finally:
            self.question_details_text.config(state=tk.DISABLED)
            if conn:
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test View Questions Form")
    view_questions_form = ViewQuestions(root)
    view_questions_form.pack(padx=20, pady=20)
    root.mainloop()