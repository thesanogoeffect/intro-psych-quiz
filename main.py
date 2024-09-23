from QuestionManager import QuestionManager
import streamlit as st
import pandas as pd
import time
import random as rd

# Initialize the QuestionManager
qm = QuestionManager("Halfway Answers 2021-2_cleaned.parquet")


def radio_on_change():
    print("Radio changed")
    st.session_state.answered = True


# Function to display a question and capture user response
def handle_question(question: pd.Series):
    st.write(f"**Question ID:** {question.name}")
    st.write(f"**Chapter:** {question['chapter']}")
    st.write(f"**Title:** {question['question_title']}")
    options = list(question["options"])
    correct_answer = str(question["correct_answer"])

    # Randomize the order of the multiple-choice options
    randomized_options = rd.sample(options, len(options))

    # Display multiple-choice options
    user_answer = st.radio(
        "Choose your answer:",
        options=randomized_options,
        key=f"q{question.name}",
        index=None,
        on_change=radio_on_change,
    )

    if st.session_state.answered:
        if user_answer == correct_answer:
            st.write("Correct!")
            st.session_state["total_correct"] += 1
        else:
            st.write("Incorrect! The correct answer was:", correct_answer)
        st.session_state["total_answered"] += 1


# Streamlit app layout
st.title("Intro to Psychology Mid-term Quiz")
st.write(
    "Made by Jakub Werner, cleaned data from D. Lakens' post https://canvas.tue.nl/courses/27884/discussion_topics/255128"
)

st.session_state["total_answered"] = 0
st.session_state["total_correct"] = 0
st.session_state["seen_questions"] = set()
st.session_state["answered"] = False


# Get a random question from the QuestionManager
question = qm.get_random_question()

# Display the current question
handle_question(question)


st.markdown("---")  # Separator between questions
