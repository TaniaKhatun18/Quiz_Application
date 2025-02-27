import tkinter as tk
from tkinter import messagebox
import random

# Define the quiz questions and choices
questions = [
    {"question": "Which of the following is the correct way to define a function in Python?",
     "choices": ["def function_name():", "function function_name():", "def function_name[]", "function function_name{}"],
     "answer": "def function_name():"},
    {"question": "What is the output of the following code: `print(2 * 3 + 4)`?",
     "choices": ["10", "14", "12", "8"],
     "answer": "10"},
    {"question": "What keyword is used to handle exceptions in Python?",
     "choices": ["try", "except", "catch", "error"],
     "answer": "except"},
    {"question": "Which of the following is the correct syntax for a list comprehension?",
     "choices": ["[x for x in range(5)]", "[for x in range(5)]", "for x in range(5) [x]", "range(5) [x for x]"],
     "answer": "[x for x in range(5)]"},
    {"question": "Which of the following data types is immutable in Python?",
     "choices": ["List", "Tuple", "Dictionary", "Set"],
     "answer": "Tuple"},
    {"question": "Which method is used to add an element to a set in Python?",
     "choices": ["add()", "insert()", "append()", "push()"],
     "answer": "add()"},
    {"question": "What will be the output of the following code: `print(10 // 3)`?",
     "choices": ["3", "3.0", "3.33", "Error"],
     "answer": "3"},
    {"question": "What is the result of the following code: `x = 2; print(x == 2 and x != 3)`?",
     "choices": ["True", "False", "Error", "None"],
     "answer": "True"},
    {"question": "Which operator is used to raise a number to a power in Python?",
     "choices": ["^", "**", "%%", "//"],
     "answer": "**"},
    {"question": "How do you create an empty dictionary in Python?",
     "choices": ["{}", "[]", "()", "None"],
     "answer": "{}"}
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz Application")
        
        # Set window size and background color
        self.root.geometry("600x600")
        self.root.config(bg="#f0f8ff", bd=5, relief="solid", highlightbackground="black", highlightthickness=2) 
        
        # Initialize score, question index, and user's name
        self.score = 0
        self.question_index = 0
        self.username = ""
        self.timer = 60  # Increased timer to 60 seconds
        self.timer_running = False
        self.selected_answer = None
        self.current_answers = []  # To track selected answers, used to reset quiz
        
        # Shuffle questions initially
        random.shuffle(questions)
        
        # Setup the GUI components
        self.create_widgets()

    def create_widgets(self):
        # Ask for user name before starting the quiz
        self.username_label = tk.Label(self.root, text="Enter your name:", font=("Arial", 14), bg="#f0f8ff") # This is to match the 
        self.username_label.pack(pady=10)
        
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        
        self.start_button = tk.Button(self.root, text="Start Quiz", font=("Arial", 14), bg="#38ACEC", fg="white", command=self.start_quiz)
        self.start_button.pack(pady=20)

    def start_quiz(self):
        # Get the username from the entry widget
        self.username = self.username_entry.get()
        if not self.username:
            messagebox.showerror("Error", "Please enter your name to start the quiz!")
            return
        
        # Clear the username input section
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.start_button.pack_forget()
        
        # Setup the quiz interface
        self.create_quiz_widgets()
        self.load_question()

    def create_quiz_widgets(self):
        # Frame to wrap the question and options (no extra border)
        self.quiz_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.quiz_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Question label with white background
        self.question_label = tk.Label(self.quiz_frame, text="", font=("Arial", 16), width=70, height=1, anchor="w", bg="white")  # White background
        self.question_label.pack(pady=20, padx=20 )
        
        # Choice buttons with rounded ends and updated colors
        self.buttons = []
        for i in range(4):
            btn = tk.Button(self.quiz_frame, text="", width=25, height=2, font=("Arial", 12), bg="#AFDCEC", fg="black", command=lambda i=i: self.check_answer(i), relief="solid", bd=2, highlightthickness=0)
            btn.pack(pady=5, padx=20, fill="x", ipady=5)
            self.buttons.append(btn)
            
            # Adding hover effect for the buttons
            btn.bind("<Enter>", lambda e, btn=btn: btn.config(bg="#82CAFA"))
            btn.bind("<Leave>", lambda e, btn=btn: btn.config(bg="#AFDCEC"))
        
        # Timer label
        self.timer_label = tk.Label(self.quiz_frame, text=f"Time left: {self.timer}", font=("Arial", 12), bg="#f0f8ff")
        self.timer_label.pack(pady=10)

        # Feedback label
        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Arial", 12), bg="#f0f8ff")
        self.feedback_label.pack(pady=5)

        # Score label
        self.score_label = tk.Label(self.quiz_frame, text=f"Score: {self.score}", font=("Arial", 12), bg="#f0f8ff")
        self.score_label.pack(pady=20)

        # Next Button
        self.next_button = tk.Button(self.quiz_frame, text="Next", width=20, height=2, font=("Arial", 12), bg="#38ACEC", fg="white", command=self.next_question, relief="solid", bd=2, highlightthickness=0, state="disabled")
        self.next_button.pack(pady=10)

    def load_question(self):
        """Load the current question and choices."""
        current_question = questions[self.question_index]
        random.shuffle(current_question["choices"])
        
        self.question_label.config(text=f"Question {self.question_index + 1}: {current_question['question']}")
        
        for i, choice in enumerate(current_question["choices"]):
            self.buttons[i].config(text=choice)
        
        # Start the timer for the question if not already running
        if not self.timer_running:
            self.timer_running = True
            self.timer = 60  # Timer set to 60 seconds
            self.update_timer()

    def update_timer(self):
        """Update the timer countdown every second."""
        if self.timer > 0:
            self.timer_label.config(text=f"Time left: {self.timer}")
            self.timer -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.check_answer(-1)  # Automatically check the answer if the timer runs out

    def check_answer(self, choice_index):
        """Check if the chosen answer is correct."""
        correct_answer = questions[self.question_index]["answer"]
        
        # Stop the timer once the answer is selected
        if self.timer_running:
            self.timer_running = False

        # Check if the answer is selected
        if choice_index == -1:
            self.feedback_label.config(text=f"Time's up! The correct answer was: {correct_answer}", fg="red")
        else:
            chosen_answer = self.buttons[choice_index].cget("text")
            if chosen_answer == correct_answer:
                self.score += 1
                self.feedback_label.config(text="Correct!", fg="green")
            else:
                self.feedback_label.config(text=f"Incorrect! The correct answer was: {correct_answer}", fg="red")
        
        # Store the selected answer to avoid it being automatically selected after reset
        self.current_answers.append(chosen_answer)
        
        # Update the score
        self.score_label.config(text=f"Score: {self.score}")
        
        # Disable all buttons after an answer is selected
        for button in self.buttons:
            button.config(state="disabled")
        
        # Enable Next button
        self.next_button.config(state="normal")

    def next_question(self):
        """Load the next question."""
        self.question_index += 1
        if self.question_index < len(questions):
            self.load_question()
            self.enable_buttons()
        else:
            self.end_quiz()

    def enable_buttons(self):
        """Enable the choice buttons again for the next question."""
        for button in self.buttons:
            button.config(state="normal")
        self.feedback_label.config(text="")
        self.next_button.config(state="disabled")
        self.timer_running = False

    def end_quiz(self):
        """End the quiz and display the final score along with the username."""
        messagebox.showinfo("Quiz Over", f"{self.username}, your final score is {self.score} out of {len(questions)}")
        self.root.quit()

# Create the main window (root) and pass it to QuizApp
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
