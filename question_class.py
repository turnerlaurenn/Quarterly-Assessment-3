class Question:
    def __init__(self, question_text, option1, option2, option3, option4, correct_answer):
        self.question_text = question_text
        self.options = [option1, option2, option3, option4]
        self.correct_answer = correct_answer

    def is_correct(self, user_answer):
        return user_answer == self.correct_answer