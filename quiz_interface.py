import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

DATABASE_NAME = 'questions.db'

class QuizInterface(tk.Toplevel):  # Inherit from tk.Toplevel
    def __init__(self, master=None):  # Add master argument with a default value
        super().__init__(master)
        self.title("Quiz")
        self.geometry("400x300")
        self.selected_category = None
        self.questions = []
        self.current_question_index = 0
        self.user_answers = {}
        self.feedback_displayed = False
        self.navigation_button = None

        self.display_category_buttons()

    def display_category_buttons(self):
        self.clear_widgets()
        tk.Label(self, text="Select Quiz Category", font=("Arial", 16)).pack(pady=20)

        categories = ["Analytic Thinking (DS3810)", "Marketing", "Applications Development (DS3850)", "Business Analytics (DS3620)", "Database Management (DS3860)"]
        for category in categories:
            category_button = tk.Button(self, text=category, command=lambda cat=category: self.start_quiz(cat))
            category_button.pack(pady=5)

    def start_quiz(self, category):
        self.selected_category = category
        self.questions = self.load_questions()
        self.current_question_index = 0
        self.user_answers = {}
        self.feedback_displayed = False
        self.display_question()

    def load_questions(self):
        conn = None
        questions = []
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(f"SELECT question_text, option1, option2, option3, option4, correct_answer FROM \"{self.selected_category}\"")
            questions = cursor.fetchall()
            random.shuffle(questions)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading questions: {e}")
        finally:
            if conn:
                conn.close()
        return questions

    def display_question(self):
        if not self.questions:
            self.clear_widgets()
            tk.Label(self, text=f"No questions in '{self.selected_category}'.", font=("Arial", 14)).pack(pady=20)
            return

        if self.feedback_displayed:
            return

        self.clear_widgets()

        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            question_text = question_data[0]
            options = list(question_data[1:5])  # Convert the tuple to a list

            # Shuffle the answer choices
            random.shuffle(options)

            tk.Label(self, text=f"Question {self.current_question_index + 1}/{len(self.questions)}", font=("Arial", 12)).pack(pady=5)
            tk.Label(self, text=question_text, wraplength=350, justify='left', font=("Arial", 14)).pack(padx=10, pady=10, anchor='w')

            self.answer_var = tk.StringVar()
            for i, option in enumerate(options):
                rb = ttk.Radiobutton(self, text=option, variable=self.answer_var, value=option)
                rb.pack(padx=20, pady=2, anchor='w')

            # Create the navigation button dynamically
            self.create_navigation_button()
        else:
            self.show_feedback()

    def create_navigation_button(self):
        # Destroy the previous button if it exists
        if self.navigation_button:
            self.navigation_button.destroy()

        if self.current_question_index < len(self.questions) - 1:
            button_text = "Next Question"
            button_command = self.next_question
        else:
            button_text = "Submit Quiz"
            button_command = self.submit_quiz

        self.navigation_button = tk.Button(self, text=button_text, command=button_command)
        self.navigation_button.pack(pady=10)

    def next_question(self):
        selected_answer = self.answer_var.get()
        if selected_answer:
            self.user_answers[self.current_question_index] = selected_answer
            self.current_question_index += 1
            self.display_question()
        else:
            messagebox.showwarning("Warning", "Please select an answer before proceeding.")

    def submit_quiz(self):
        selected_answer = self.answer_var.get()
        if selected_answer:
            self.user_answers[self.current_question_index] = selected_answer
            self.show_feedback()
        else:
            messagebox.showwarning("Warning", "Please select an answer before submitting.")

    def show_feedback(self):
        self.clear_widgets()
        
        # Calculate the correct answers count
        correct_count = 0
        for i, question_data in enumerate(self.questions):
            correct_answer = question_data[5]
            user_answer = self.user_answers.get(i, "Not Answered")
            if user_answer == correct_answer:
                correct_count += 1

        # Display the simplified feedback: only the score
        tk.Label(self, text="Quiz Results", font=("Arial", 16, "bold")).pack(pady=10)
        percentage = (correct_count / len(self.questions)) * 100 if self.questions else 0
        tk.Label(self, text=f"You scored {correct_count}/{len(self.questions)} ({percentage:.2f}%)", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Feedback displayed flag set to True
        self.feedback_displayed = True

        # Add restart and exit buttons
        restart_button = tk.Button(self, text="Restart Quiz", command=self.restart_quiz)
        restart_button.pack(pady=5)
        exit_button = tk.Button(self, text="Exit", command=self.destroy)
        exit_button.pack(pady=5)

    def restart_quiz(self):
        self.selected_category = None
        self.questions = []
        self.current_question_index = 0
        self.user_answers = {}
        self.feedback_displayed = False
        self.display_category_buttons()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    quiz = QuizInterface()
    quiz.mainloop()
