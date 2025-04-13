import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

DATABASE_NAME = 'questions.db'

class QuizInterface(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Quiz")
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", self.on_quiz_closing)
        self.quiz_started = False
        self.selected_category = None
        self.questions = []
        self.current_question_index = 0
        self.user_answers = {}
        self.feedback_displayed = False
        self.navigation_button = None
        self.back_button = None

        self.display_category_buttons()

    def display_category_buttons(self):
        self.clear_widgets()
        tk.Label(self, text="Select Quiz Category", font=("Arial", 16)).pack(pady=20)

        categories = [
            "Analytic Thinking (DS3810)",
            "Marketing",
            "Applications Development (DS3850)",
            "Business Analytics (DS3620)",
            "Database Management (DS3860)"
        ]
        for category in categories:
            category_button = tk.Button(self, text=category, command=lambda cat=category: self.start_quiz(cat))
            category_button.pack(pady=5)

    def start_quiz(self, category):
        self.quiz_started = True
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
            options = list(question_data[1:5])
            correct_answer = question_data[5]

            random.shuffle(options)

            tk.Label(self, text=f"Question {self.current_question_index + 1}/{len(self.questions)}", font=("Arial", 12)).pack(pady=5)
            tk.Label(self, text=question_text, wraplength=350, justify='left', font=("Arial", 14)).pack(padx=10, pady=10, anchor='w')

            self.answer_var = tk.StringVar()

            # Restore saved answer if it exists
            saved_answer = self.user_answers.get(self.current_question_index)
            if saved_answer:
                self.answer_var.set(saved_answer)

            for i, option in enumerate(options):
                option_frame = tk.Frame(self)
                option_frame.pack(fill="x", padx=20, pady=5, anchor="w")

                rb = ttk.Radiobutton(option_frame, variable=self.answer_var, value=option)
                rb.pack(side="left")

                lbl = tk.Label(
                    option_frame,
                    text=option,
                    wraplength=300,
                    justify="left",
                    anchor="w",
                    font=("Arial", 12)
                )
                lbl.pack(side="left", padx=10, fill="x")

                lbl.bind("<Button-1>", lambda e, opt=option: self.answer_var.set(opt))




            self.create_navigation_buttons()
        else:
            self.show_feedback()


    def create_navigation_buttons(self):
        if self.navigation_button:
            self.navigation_button.destroy()
        if self.back_button:
            self.back_button.destroy()

        navigation_frame = tk.Frame(self)
        navigation_frame.pack(pady=10)

        if self.current_question_index > 0:
            self.back_button = tk.Button(navigation_frame, text="Back", command=self.previous_question)
            self.back_button.pack(side="left", padx=10)

        if self.current_question_index < len(self.questions) - 1:
            button_text = "Next Question"
            button_command = self.next_question
        else:
            button_text = "Submit Quiz"
            button_command = self.submit_quiz

        self.navigation_button = tk.Button(navigation_frame, text=button_text, command=button_command)
        self.navigation_button.pack(side="right", padx=10)

    def previous_question(self):
        if self.current_question_index > 0:
            self.user_answers[self.current_question_index] = self.answer_var.get()
            self.current_question_index -= 1
            self.display_question()

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

        correct_count = 0
        self.incorrect_questions = []

        for i, question_data in enumerate(self.questions):
            correct_answer = question_data[5]
            user_answer = self.user_answers.get(i, "Not Answered")
            if user_answer == correct_answer:
                 correct_count += 1
            else:
                self.incorrect_questions.append((i, question_data, user_answer))

        self.score_summary = f"You scored {correct_count}/{len(self.questions)} ({(correct_count / len(self.questions)) * 100:.2f}%)"
                
        tk.Label(self, text="Quiz Results", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self, text=self.score_summary, font=("Arial", 14, "bold")).pack(pady=10)

        self.feedback_displayed = True

        if self.incorrect_questions:
            review_button = tk.Button(self, text="Review Incorrect Answers", command=self.start_review)
            review_button.pack(pady=5)

        back_button = tk.Button(self, text="Back to Categories", command=self.restart_quiz)
        back_button.pack(pady=5)

        exit_button = tk.Button(self, text="Exit", command=self.on_quiz_closing)
        exit_button.pack(pady=5)

    def start_review(self):
        self.current_review_index = 0  # Initialize the review index
        self.display_review_question()

    def display_review_question(self):
        self.clear_widgets()

        if self.current_review_index < len(self.incorrect_questions):
            i, question_data, user_answer = self.incorrect_questions[self.current_review_index]
            question_text = question_data[0]
            correct_answer = question_data[5]

            # Score label
            tk.Label(self, text=f"{self.score_summary}", font=("Arial", 12, "bold")).pack(pady=5)

            # Question label
            tk.Label(self, text=f"Reviewing Question {self.current_review_index + 1}/{len(self.incorrect_questions)}",
                    font=("Arial", 11)).pack(pady=5)
            tk.Label(self, text=question_text, wraplength=350, justify='left',
                    font=("Arial", 13)).pack(padx=10, pady=10, anchor='w')

            # User's answer
            tk.Label(self, text=f"Your Answer: {user_answer}", fg="red",
                    font=("Arial", 12)).pack(pady=3)

            # Correct answer
            tk.Label(self, text=f"Correct Answer: {correct_answer}", fg="green",
                    font=("Arial", 12)).pack(pady=3)

            # Navigation buttons
            nav_frame = tk.Frame(self)
            nav_frame.pack(pady=10)

            if self.current_review_index > 0:
                back_btn = tk.Button(nav_frame, text="Back", command=self.review_previous_question)
                back_btn.pack(side="left", padx=10)

            if self.current_review_index < len(self.incorrect_questions) - 1:
                next_btn = tk.Button(nav_frame, text="Next", command=self.review_next_question)
                next_btn.pack(side="right", padx=10)
            else:
                done_btn = tk.Button(nav_frame, text="Done Reviewing", command=self.restart_quiz)
                done_btn.pack(side="right", padx=10)

    def review_next_question(self):
        self.current_review_index += 1
        self.display_review_question()

    def review_previous_question(self):
        if self.current_review_index > 0:
            self.current_review_index -= 1
            self.display_review_question()

    def show_review_mode(self):
        self.clear_widgets()
        self.review_mode = True
        self.current_question_index = 0

        self.score_label = tk.Label(self, text=f"Your Score: {self.score}", font=("Arial", 10, "bold"))
        self.score_label.pack(pady=5)

        self.display_review_question()

    def prev_review(self):
        if self.review_index > 0:
            self.review_index -= 1
            self.display_review_question()

    def next_review(self):
        if self.review_index < len(self.incorrect_questions) - 1:
            self.review_index += 1
            self.display_review_question()

    def restart_quiz(self):
        self.quiz_started = False
        self.selected_category = None
        self.questions = []
        self.current_question_index = 0
        self.user_answers = {}
        self.feedback_displayed = False
        self.display_category_buttons()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def on_quiz_closing(self):
        if self.quiz_started and not self.feedback_displayed:
            if messagebox.askyesno("Exit Quiz", "Are you sure you want to exit the quiz?"):
                self.destroy()
                if self.master:
                    self.master.quiz_active = False
        else:
            self.destroy()
            if self.master:
                self.master.quiz_active = False

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    quiz = QuizInterface(root)
    root.mainloop()