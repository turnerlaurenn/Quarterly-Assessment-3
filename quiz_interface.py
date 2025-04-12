import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

DATABASE_NAME = 'questions.db'

class QuizInterface(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Quiz")
        self.geometry("400x300")

        self.category_choices = ["Analytic Thinking (DS3810)", "Marketing", "Applications Development (DS3850)", "Business Analytics (DS3620)", "Database Management (DS3860)"]
        self.category_buttons = {}

        for category in self.category_choices:
            button = tk.Button(self, text=category, command=lambda cat=category: self.start_quiz(cat), padx=20, pady=10)
            self.category_buttons[category] = button
            button.pack(pady=5)

        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.user_answers = {}
        self.answer_var = tk.StringVar()

        self.question_label = tk.Label(self, text="", wraplength=380, justify="left")
        self.question_label.pack(pady=10, padx=10)

        self.option_radiobuttons = []
        for i in range(4):
            rb = tk.Radiobutton(self, text="", variable=self.answer_var, value="", anchor="w", padx=20)
            self.option_radiobuttons.append(rb)
            rb.pack()

        self.submit_button = tk.Button(self, text="Submit Answer", command=self.submit_answer, state=tk.DISABLED)
        self.submit_button.pack(pady=10)

        self.next_button = tk.Button(self, text="Next Question", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=5)

        # Initially hide question elements
        self.question_label.pack_forget()
        for rb in self.option_radiobuttons:
            rb.pack_forget()
        self.submit_button.pack_forget()
        self.next_button.pack_forget()

    def start_quiz(self, selected_category):
        # Hide category buttons
        for button in self.category_buttons.values():
            button.pack_forget()

        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.user_answers = {}
        self.answer_var.set(None) # Clear previous selection
        self.clear_options()
        self.question_label.config(text="Loading questions...")
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)

        # Show question elements
        self.question_label.pack(pady=10, padx=10)
        for rb in self.option_radiobuttons:
            rb.pack()
        self.submit_button.pack(pady=10)
        self.next_button.pack(pady=5)

        conn = None
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(f"SELECT question_text, option1, option2, option3, option4, correct_answer FROM '{selected_category}' ORDER BY RANDOM()") # Fetch in random order
            fetched_questions = cursor.fetchall()
            if fetched_questions:
                for q in fetched_questions:
                    question_data = {
                        "text": q[0],
                        "options": [q[1], q[2], q[3], q[4]],
                        "correct_answer": q[5]
                    }
                    self.questions.append(question_data)
                self.display_question()
            else:
                self.question_label.config(text=f"No questions available in the '{selected_category}' category.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching questions: {e}")
            self.question_label.config(text="Error loading questions.")
        finally:
            if conn:
                conn.close()

    def display_question(self):
        if self.current_question_index < len(self.questions):
            self.clear_options()
            question_data = self.questions[self.current_question_index]
            self.question_label.config(text=f"Q{self.current_question_index + 1}: {question_data['text']}")

            # Shuffle options to prevent correct answer always being in the same position
            shuffled_options = list(question_data['options'])
            random.shuffle(shuffled_options)

            for i, option in enumerate(shuffled_options):
                self.option_radiobuttons[i].config(text=option, value=option, state=tk.NORMAL)
                self.option_radiobuttons[i].deselect() # Ensure no option is pre-selected

            self.answer_var.set(None) # Reset answer selection
            self.submit_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)
        else:
            self.show_results()

    def submit_answer(self):
        selected_answer = self.answer_var.get()
        if not selected_answer:
            messagebox.showerror("Error", "Please select an answer.")
            return

        correct_answer = self.questions[self.current_question_index]['correct_answer']
        self.user_answers[self.current_question_index] = selected_answer

        # Disable radio buttons after submission
        for rb in self.option_radiobuttons:
            rb.config(state=tk.DISABLED)

        if selected_answer == correct_answer:
            self.score += 1

        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question_index += 1
        self.display_question()

    def show_results(self):
        self.clear_widgets()
        result_label = tk.Label(self, text=f"Quiz Finished!\nYour final score is: {self.score}/{len(self.questions)}", font=("Arial", 14))
        result_label.pack(pady=20)

        close_button = tk.Button(self, text="Close Quiz", command=self.destroy)
        close_button.pack(pady=10)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_options(self):
        for rb in self.option_radiobuttons:
            rb.config(text="", value="", state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Quiz Interface")
    quiz_app = QuizInterface(root)
    root.mainloop()