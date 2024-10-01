from QuestionManager import QuestionManager
import streamlit as st
import pandas as pd
import random as rd

# Initialize the QuestionManager
qm = QuestionManager("Halfway Answers 2021-2_cleaned.parquet")
st.set_page_config(page_title="ITP Mid-term Quiz", page_icon="🧠")

def handle_user_input(question: pd.Series, correct_answer: str, radio_key: str):
    user_answer = st.session_state[radio_key]
    st.session_state["seen_questions"].add(int(question.name))
    st.session_state["total_answered"] += 1

    # Check if the answer is correct
    if user_answer == correct_answer:
        st.session_state["total_correct"] += 1
        feedback_message = f"Correct! The answer was: {correct_answer}"
    else:
        feedback_message = f"Incorrect. The correct answer was: {correct_answer}"

    # Update feedback message in session state
    st.session_state["feedback_message"] = feedback_message

    # Load a new question
    st.session_state["current_question"] = qm.get_random_question(seen_questions=st.session_state["seen_questions"], chapters=selected_chapters)

    # Reset radio button selection
    st.session_state[radio_key] = None

def handle_chapter_change():
    st.session_state["seen_questions"].clear()
    st.session_state["current_question"] = qm.get_random_question(seen_questions=st.session_state["seen_questions"], chapters=selected_chapters)

def handle_question(question: pd.Series):
    st.write(f"**QID:** {question.name}")
    st.write(f"**Chapter:** {question['chapter']}")
    
    # Larger, centered title
    st.markdown(f"<h2 style='text-align: center; font-size: 22px;'>{question['question_title']}</h2>", unsafe_allow_html=True)

    options = list(question["options"])
    correct_answer = str(question["correct_answer"])

    # Randomize the order of the multiple-choice options
    randomized_options = rd.sample(options, len(options))

    # Generate a unique key for the radio button
    radio_key = f"q_{question.name}"

    # Display multiple-choice options
    st.radio(
        "Choose one:",
        options=randomized_options,
        key=radio_key,
        index=None,
        on_change=handle_user_input,
        args=(question, correct_answer, radio_key),
    )

# Streamlit app layout
st.title("Intro to Psychology Mid-term Quiz")

# Enable the user to check the chapters they want to see
max_chapters = [1, 2, 3, 4, 5, 6]
with st.expander("Filter Chapters?"):
    # By default all enabled, multiselect
    selected_chapters = st.multiselect("Select the chapters you want to see", max_chapters, default=max_chapters, on_change=handle_chapter_change)

# Initialize session state variables
if "total_answered" not in st.session_state:
    st.session_state["total_answered"] = 0
if "total_correct" not in st.session_state:
    st.session_state["total_correct"] = 0
if "seen_questions" not in st.session_state:
    st.session_state["seen_questions"] = set()
if "feedback_message" not in st.session_state:
    st.session_state["feedback_message"] = ""
if "current_question" not in st.session_state:
    st.session_state["current_question"] = qm.get_random_question(seen_questions=st.session_state["seen_questions"], chapters=selected_chapters)

# Display feedback message
if st.session_state["feedback_message"]:
    if "Correct!" in st.session_state["feedback_message"]:
        st.success(st.session_state["feedback_message"])
    else:
        st.warning(st.session_state["feedback_message"])

# Display the current question
question = st.session_state["current_question"]
handle_question(question)

st.write(f"**Total answered:** {st.session_state['total_answered']}")
st.write(f"**Total correct:** {st.session_state['total_correct']}")

st.markdown("<br><hr><br>", unsafe_allow_html=True)  # Separator between questions with spacing
# Footer
st.write(
    "Made by Jakub W., cleaned data from prof. D. Lakens' post https://canvas.tue.nl/courses/27884/discussion_topics/255128. Special thanks to Anton B."
)
st.write(
    "Want to help make it better? Found a problem in the questions? Visit here, but PLEASE KEEP THE FORMATTING!: (https://docs.google.com/document/d/14OcbX4qMwhRGgL2HfmaO_qIqZKjJfzWfvDCaZ8Kxpaw/edit?usp=sharing"
)

# GitHub link
st.write(
    "Or check out the project on https://github.com/thesanogoeffect/IntroPsychQuiz"
)
