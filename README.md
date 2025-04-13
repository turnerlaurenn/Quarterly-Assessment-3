## Description

This application provides an administrative interface for managing quiz data and a quiz-taking interface for users. It is built using Python’s Tkinter GUI toolkit and supports functionality for viewing, adding, deleting, modifying, and taking quizzes from a SQLite database.

## Features

### Admin Interface

* **User Authentication:** Admin access is restricted via password protection.
* **Question Management:**
  * **View Questions:** Display all stored questions.
  * **Add Question:** Input new questions into the database.
  * **Delete Question:** Remove existing questions.
  * **Modify Question:** Edit question content or answers.
* **Window Isolation:** The admin panel and quiz interface cannot be accessed simultaneously.
* **Scrollable Views:** Admin windows utilize scrollable canvases for better layout and accessibility.

### Quiz Interface

* **Category Selection:** Users choose from multiple quiz categories.
* **Question Navigation:** Navigate forward and backward between questions before submission.
* **Answer Tracking:** Selected answers are remembered when navigating.
* **Score Feedback:** Upon completion, users receive a score summary showing correct answers and percentage.
* **Incorrect Answer Review:** After viewing the results, users are asked if they’d like to review questions they got wrong. If they choose to review:
  * The interface displays each incorrect question, the user’s answer, and the correct answer.
  * Navigation buttons allow users to move back and forth through incorrect responses.
  * The quiz score remains visible at the top during review for reference.

## Technical Details

* **Language:** Python 3.x
* **GUI Library:** Tkinter
* **Database:** SQLite (`questions.db`)
* **Admin Password:** Hardcoded as `easyadmin123`.

## Question Class

* **Purpose:** Encapsulates the data and logic related to a single quiz question.
* **Defined In:** `question_class.py`
* **Structure:**
  * `question_text` – The main question string.
  * `options` – A list containing four possible answers.
  * `correct_answer` – The correct option string.
* **Usage:**
  * During quiz loading, each row from the database is converted into a `Question` instance.
  * These instances are stored in a list and used throughout the quiz for display, answer checking, and review.
  * Includes an `is_correct(answer)` method that checks whether a user's answer is correct.

## File Structure

* `main.py` - Launches the admin interface.
* `admin_panel.py` - Contains the admin dashboard with options to view, add, delete, and modify questions.
* `view_questions.py` - Displays all questions by category.
* `add_question.py` - Adds new questions to a category.
* `delete_question.py` - Removes questions.
* `modify_question.py` - Edits questions.
* `quiz_interface.py` - Handles quiz logic and user interaction.

## How to Run the Application

1. Make sure Python is installed on your system.
2. Place all Python files (`main.py`, `quiz_interface.py`, etc.) in the same directory.
3. Run the application using `python main.py` in the terminal.
4. To enter the admin section, log in using the admin password.
5. To take a quiz, launch `quiz_interface.py` separately with `python quiz_interface.py`.
