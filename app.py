import streamlit as st
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
]

# Shuffle questions randomly
random.shuffle(questions)

# Streamlit app layout
st.title("🧠 Python Quiz Application")
st.write("Test your Python knowledge with this quiz!")

# Session State for tracking progress
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "completed" not in st.session_state:
    st.session_state.completed = False

# Display current question
if not st.session_state.completed and st.session_state.question_index < len(questions):
    current_question = questions[st.session_state.question_index]

    st.subheader(f"Question {st.session_state.question_index + 1}:")
    st.write(current_question["question"])

    # Shuffle answer choices
    choices = current_question["choices"]
    random.shuffle(choices)

    selected_answer = st.radio("Choose your answer:", choices)

    if st.button("Submit Answer"):
        if selected_answer == current_question["answer"]:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect! The correct answer was: {current_question['answer']}")

        # Move to the next question
        st.session_state.question_index += 1

# Show Final Score
if st.session_state.question_index >= len(questions):
    st.session_state.completed = True
    st.write("🎉 **Quiz Completed!** 🎉")
    st.write(f"Your final score: **{st.session_state.score} / {len(questions)}**")

    # Restart Quiz
    if st.button("Restart Quiz"):
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.completed = False
        st.rerun()
