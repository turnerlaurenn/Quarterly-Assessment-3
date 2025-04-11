import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DATABASE_NAME = 'questions.db'

class ModifyQuestion(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.label = tk.Label(self, text="Modify Existing Question", font=("Arial", 16))
        self.label.pack(pady=10)

        self.category_label = tk.Label(self, text="Select Category:")
        self.category_label.pack(anchor="w", padx=20)
        self.category_var = tk.StringVar(self)
        self.category_choices = ["Analytic Thinking (DS3810)", "Marketing", "Applications Development (DS3850)", "Business Analytics (DS3620)", "Database Management (DS3860)"]
        self.category_var.set(self.category_choices[0])
        self.category_dropdown = ttk.Combobox(self, textvariable=self.category_var, values=self.category_choices)
        self.category_dropdown.pack(anchor="w", padx=20, pady=5)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.populate_question_list)

        self.question_list_label = tk.Label(self, text="Select Question to Modify:")
        self.question_list_label.pack(anchor="w", padx=20)
        self.question_list_scrollbar = tk.Scrollbar(self)
        self.question_list = tk.Listbox(self, width=60, yscrollcommand=self.question_list_scrollbar.set)
        self.question_list.pack(anchor="w", padx=20, pady=5)
        self.question_list_scrollbar.config(command=self.question_list.yview)
        self.question_list_scrollbar.pack(side="right", fill="y")
        self.question_list.bind('<<ListboxSelect>>', self.load_question_details)

        self.question_text_label = tk.Label(self, text="Question Text:")
        self.question_text_label.pack(anchor="w", padx=20, pady=10)
        self.question_text_entry = tk.Text(self, height=3, width=50)
        self.question_text_entry.pack(anchor="w", padx=20, pady=5)

        self.option_labels = []
        self.option_entries = []
        for i in range(4):
            label = tk.Label(self, text=f"Option {i+1}:")
            label.pack(anchor="w", padx=30)
            entry = tk.Entry(self, width=40)
            entry.pack(anchor="w", padx=30, pady=2)
            self.option_labels.append(label)
            self.option_entries.append(entry)

        self.correct_answer_label = tk.Label(self, text="Correct Answer (enter option number 1-4):")
        self.correct_answer_label.pack(anchor="w", padx=20)
        self.correct_answer_entry = tk.Entry(self, width=5)
        self.correct_answer_entry.pack(anchor="w", padx=20, pady=5)

        self.save_button = tk.Button(self, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=20)
        self.save_button.config(state=tk.DISABLED) # Initially disabled until a question is selected

        self.selected_question_id = None

        self.populate_question_list()

    def populate_question_list(self, event=None):
        self.question_list.delete(0, tk.END)
        category = self.category_var.get()
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(f"SELECT rowid, question_text FROM {category}")
            questions = cursor.fetchall()
            for rowid, text in questions:
                self.question_list.insert(tk.END, f"ID: {rowid} - {text[:50]}...")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching questions: {e}")
        finally:
            if conn:
                conn.close()
            self.clear_details()
            self.save_button.config(state=tk.DISABLED)
            self.selected_question_id = None

    def load_question_details(self, event):
        selected_index = self.question_list.curselection()
        if selected_index:
            selected_question_str = self.question_list.get(selected_index[0])
            try:
                self.selected_question_id = int(selected_question_str.split(" - ")[0].split(": ")[1])
            except ValueError:
                messagebox.showerror("Error", "Could not parse question ID.")
                return

            category = self.category_var.get()
            conn = None
            try:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                cursor.execute(f"SELECT question_text, option1, option2, option3, option4, correct_answer FROM {category} WHERE rowid = ?", (self.selected_question_id,))
                question_details = cursor.fetchone()
                if question_details:
                    self.question_text_entry.delete("1.0", tk.END)
                    self.question_text_entry.insert(tk.END, question_details[0])
                    for i in range(4):
                        self.option_entries[i].delete(0, tk.END)
                        self.option_entries[i].insert(0, question_details[i+1])

                    correct_answer = question_details[5]
                    try:
                        correct_index = question_details[1:5].index(correct_answer) + 1
                        self.correct_answer_entry.delete(0, tk.END)
                        self.correct_answer_entry.insert(0, str(correct_index))
                        self.save_button.config(state=tk.NORMAL)
                    except ValueError:
                        messagebox.showerror("Error", "Correct answer not found in options.")
                        self.save_button.config(state=tk.DISABLED)
                else:
                    self.clear_details()
                    self.save_button.config(state=tk.DISABLED)
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error fetching question details: {e}")
            finally:
                if conn:
                    conn.close()
        else:
            self.clear_details()
            self.save_button.config(state=tk.DISABLED)
            self.selected_question_id = None

    def save_changes(self):
        if self.selected_question_id is None:
            messagebox.showerror("Error", "No question selected to modify.")
            return

        category = self.category_var.get()
        question_text = self.question_text_entry.get("1.0", tk.END).strip()
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
            sql = f"""UPDATE {category} SET question_text = ?, option1 = ?, option2 = ?, option3 = ?, option4 = ?, correct_answer = ?
                      WHERE rowid = ?"""
            cursor.execute(sql, (question_text, options[0], options[1], options[2], options[3], correct_answer, self.selected_question_id))
            conn.commit()
            messagebox.showinfo("Success", f"Question ID {self.selected_question_id} updated successfully in {category}!")
            self.populate_question_list() # Refresh the list
            self.clear_details()
            self.save_button.config(state=tk.DISABLED)
            self.selected_question_id = None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error updating question: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def clear_details(self):
        self.question_text_entry.delete("1.0", tk.END)
        for entry in self.option_entries:
            entry.delete(0, tk.END)
        self.correct_answer_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Modify Question Form")
    modify_question_form = ModifyQuestion(root)
    modify_question_form.pack(padx=20, pady=20)
    root.mainloop()