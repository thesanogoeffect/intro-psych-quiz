import langchain
import dotenv
import pytz
import pandas as pd
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# timestamp	question_title	chapter_id	correct_answer	distractor_1	distractor_2	distractor_3	source	author	student_id

dotenv.load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()


# for the first function, we want to create a df of questions in the following format
def extract_dict_from_question_text(text: str) -> dict:
    system_template = """
        Extract the following details from the input Psychology question text:
        - Question title
        - Correct answer
        - Three distractors

        Similar to the following example:
        {{
            "question_title": "________ is most well-known for proposing his hierarchy of needs.",
            "correct_answer": "Abraham Maslow",
            "distractor_1": "Carl Rogers",
            "distractor_2": "B.F. Skinner",
            "distractor_3": "Ivan Pavlov"
        }}
        
        Input text: "{text}"
        
        Output format: {{
            "question_title": "<question_title>",
            "correct_answer": "<correct_answer>",
            "distractor_1": "<distractor_1>",
            "distractor_2": "<distractor_2>",
            "distractor_3": "<distractor_3>"
        }}
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )
    chain = prompt_template | model | parser

    input_dict = {"text": text}

    # Get the string output
    question_str = chain.invoke(input_dict)

    # Attempt to parse the string output to a dictionary
    try:
        question_dict = json.loads(question_str)
    except json.JSONDecodeError:
        # Handle JSON parsing error
        question_dict = {}

    return question_dict


# print(extract_dict_from_question_text("""Based on your reading, which theorist would have been most likely to agree with this statement: Perceptual
# phenomena are best understood as a combination of their components.
# a. William James
# b. Max Wertheimer
# c. Carl Rogers
# d. Noam Chomsky"""))


def add_separator_to_book_text(book_text: str) -> str:
    system_template = """
        Add a separator to the input book text to separate all of the questions. Also remove any trailing whitespace and the numbers at the beginning of each question, otherwise keep them as they are.
        
        example:
        Input:
        1. Which of the following was mentioned as a skill to which psychology students would be exposed?
        a. critical thinking
        b. use of the scientific method
        c. critical evaluation of sources of information
        d. all of the above
        2. Before psychology became a recognized academic discipline, matters of the mind were undertaken by
        those in ________.
        a. biology
        b. chemistry
        c. philosophy
        d. physics
        3. In the scientific method, a hypothesis is a(n) ________.
        a. observation
        b. measurement
        c. test
        d. proposed explanation

        Output:
        Which of the following was mentioned as a skill to which psychology students would be exposed?
        a. critical thinking
        b. use of the scientific method
        c. critical evaluation of sources of information
        d. all of the above
        |Before psychology became a recognized academic discipline, matters of the mind were undertaken by
        those in ________.
        a. biology
        b. chemistry
        c. philosophy
        d. physics
        |3. In the scientific method, a hypothesis is a(n) ________.
        a. observation
        b. measurement
        c. test
        d. proposed explanation
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )
    chain = prompt_template | model | parser

    input_dict = {"text": book_text}

    # Get the string output

    question_str = chain.invoke(input_dict)

    return question_str


def process_book_text_questions(book_text: str, chapter_id: int) -> pd.DataFrame:
    book_text = add_separator_to_book_text(book_text)
    questions = book_text.split("|")
    questions = [extract_dict_from_question_text(question) for question in questions]
    df = pd.DataFrame(questions)
    df["source"] = "Book"
    df["chapter_id"] = chapter_id
    df["author"] = ""
    df["timestamp"] = pd.Timestamp.now(tz=pytz.timezone("Europe/Amsterdam")).strftime(
        "%m/%d/%Y %H:%M:%S"
    )
    df = df[
        [
            "timestamp",
            "question_title",
            "chapter_id",
            "correct_answer",
            "distractor_1",
            "distractor_2",
            "distractor_3",
            "source",
            "author",
        ]
    ]
    return df


def canvas_student_q_raw_to_dict(text: str):

    # now, we can also process the student-made questions
    system_template = """
            You will see a student-made question from the Intro to Psychology course at TU/e, which uses the OpenStax Psychology 2e textbook. I have provided an example.
            The 7-to-9 digit number at the beginning followed by the dot is the student_id.
            Make any fields, that are missing or cannot be inferred, as an empty string. Do not alter the submissions themselves in any way except for handling non-unicode characters, it is very important to keep them authentic!
            The students marked the correct answer with an asterisk (*). It doesn't matter if the marked correct answer is wrong. The output should be only be a dictionary starting with {{ and ending with }}
            
            Example Input 1:

            17535923. A ____ uses X-rays to create a cross-section of your body.
            A) EEG
            B) MRI
            C) PET scan
            *D) CT scan

            Example Output 1:
            {{
                "question_title": "A ____ uses X-rays to create a cross-section of your body.",
                "student_id": "17535923",
                "correct_answer": "D",
                "distractor_1": "EEG",
                "distractor_2": "MRI",
                "distractor_3": "PET scan"}}
            
            Example Input 2:
            1739026. What is the correct defintion of a cone?

            A) Specialized photoreceptor that works well in low light conditions
            *B) Specialized photoreceptor that works best in bright light conditions and detects color
            C) -
            D) -

            Example Output 2:
            {{
                "question_title": "What is the correct defintion of a cone?",
                "student_id": "1739026",
                "correct_answer": "B",
                "distractor_1": "Specialized photoreceptor that works well in low light conditions",
                "distractor_2": "",
                "distractor_3": ""}}
            
        """
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )
    chain = prompt_template | model | parser

    input_dict = {"text": text}

    # Get the string output

    question_str = chain.invoke(input_dict)

    return question_str


def canvas_student_q_organized_to_raw_dict(text: str) -> dict:
    system_template = """
        Extract the following details from the organized student-made question text:
        - Question title
        - Student ID
        - Marked Correct Answer
        - Answer A
        - Answer B
        - Answer C
        - Answer D

        Similar to the following example:
        {{
            "question_title": "A ____ uses X-rays to create a cross-section of your body.",
            "student_id": "17535923",
            "marked_correct_answer": "D",
            "answer_a": "EEG",
            "answer_b": "MRI",
            "answer_c": "PET scan",
            "answer_d": "CT scan"
        }}
        
        Input text: "{text}"
        
        Output format: {{
            "question_title": "<question_title>",
            "student_id": "<student_id>",
            "marked_correct_answer": "<marked_correct_answer>",
            "answer_a": "<answer_a>",
            "answer_b": "<answer_b>",
            "answer_c": "<answer_c>",
            "answer_d": "<answer_d>"
        }}
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )
    chain = prompt_template | model | parser

    input_dict = {"text": text}

    # Get the string output
    question_str = chain.invoke(input_dict)

    # Attempt to parse the string output to a dictionary
    try:
        question_dict = json.loads(question_str)
    except json.JSONDecodeError:
        # Handle JSON parsing error
        question_dict = {}

    return question_dict


def llm_get_chapter(question_title: str, answers: str) -> int:
    # we can use the model to get the chapter of the question
    system_template = """
        Given the question title and answers, predict the chapter number in the OpenStax Psychology 2e textbook that the student-made question belongs to. Just for recap, the OpenStax Psychology 2e textbook has 16 chapters. Try to think critically about the question and its content.
        You can definitely rule out the chapters that are not in the exam, which are 11, 13, 15 and 16.

1 - Introduction to Psychology

1.1 What Is Psychology?
1.2 History of Psychology
1.3 Contemporary Psychology
1.4 Careers in Psychology
2 - Psychological Research

2.1 Why Is Research Important?
2.2 Approaches to Research
2.3 Analyzing Findings
2.4 Ethics
3 - Biopsychology

3.1 Human Genetics
3.2 Cells of the Nervous System
3.3 Parts of the Nervous System
3.4 The Brain and Spinal Cord
3.5 The Endocrine System
4 - States of Consciousness

4.1 What Is Consciousness?
4.2 Sleep and Why We Sleep
4.3 Stages of Sleep
4.4 Sleep Problems and Disorders
4.5 Substance Use and Abuse
4.6 Other States of Consciousness
5 - Sensation and Perception

5.1 Sensation versus Perception
5.2 Waves and Wavelengths
5.3 Vision
5.4 Hearing
5.5 The Other Senses
5.6 Gestalt Principles of Perception
6 - Learning

6.1 What Is Learning?
6.2 Classical Conditioning
6.3 Operant Conditioning
6.4 Observational Learning (Modeling)
7 - Thinking and Intelligence

7.1 What Is Cognition?
7.2 Language
7.3 Problem Solving
7.4 What Are Intelligence and Creativity?
7.5 Measures of Intelligence
7.6 The Source of Intelligence
8 - Memory

8.1 How Memory Functions
8.2 Parts of the Brain Involved with Memory
8.3 Problems with Memory
8.4 Ways to Enhance Memory
9 - Lifespan Development

9.1 What Is Lifespan Development?
9.2 Lifespan Theories
9.3 Stages of Development
9.4 Death and Dying
10 - Emotion and Motivation

10.1 Motivation
10.2 Hunger and Eating
10.3 Sexual Behavior
10.4 Emotion
11 - Personality

11.1 What Is Personality?
11.2 Freud and the Psychodynamic Perspective
11.3 Neo-Freudians: Adler, Erikson, Jung, and Horney
11.4 Learning Approaches
11.5 Humanistic Approaches
11.6 Biological Approaches
11.7 Trait Theorists
11.8 Cultural Understandings of Personality
11.9 Personality Assessment
12 - Social Psychology

12.1 What Is Social Psychology?
12.2 Self-presentation
12.3 Attitudes and Persuasion
12.4 Conformity, Compliance, and Obedience
12.5 Prejudice and Discrimination
12.6 Aggression
12.7 Prosocial Behavior
13 - Industrial-Organizational Psychology

13.1 What Is Industrial and Organizational Psychology?
13.2 Industrial Psychology: Selecting and Evaluating Employees
13.3 Organizational Psychology: The Social Dimension of Work
13.4 Human Factors Psychology and Workplace Design
14 - Stress, Lifestyle, and Health

14.1 What Is Stress?
14.2 Stressors
14.3 Stress and Illness
14.4 Regulation of Stress
14.5 The Pursuit of Happiness
15 - Psychological Disorders

15.1 What Are Psychological Disorders?
15.2 Diagnosing and Classifying Psychological Disorders
15.3 Perspectives on Psychological Disorders
15.4 Anxiety Disorders
15.5 Obsessive-Compulsive and Related Disorders
15.6 Posttraumatic Stress Disorder
15.7 Mood and Related Disorders
15.8 Schizophrenia
15.9 Dissociative Disorders
15.10 Disorders in Childhood
15.11 Personality Disorders
16 - Therapy and Treatment

16.1 Mental Health Treatment: Past and Present
16.2 Types of Treatment
16.3 Treatment Modalities
16.4 Substance-Related and Addictive Disorders: A Special Case
16.5 The Sociocultural Model and Therapy Utilization
        
        Input:
        Question title: "{question_title}"
        Answers: "{answers}"
        
        Output (single int from 1 to 16):

    """
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{question_title}\n{answers}")]
    )
    chain = prompt_template | model | parser

    input_dict = {
        "question_title": question_title,
        "answers": answers,
    }

    # Get the string output
    chapter_str = chain.invoke(input_dict)

    # Attempt to parse the string output to an integer
    try:
        chapter = int(chapter_str)
    except ValueError:
        # Handle ValueError
        print("Error: Could not parse chapter number.")
        chapter = 0

    return chapter


def llm_get_description(question_title: str, answers: str, correct_answer: str) -> str:
    # we can use the model to get the description of the question
    system_template = """
        Given the following question and answers from the OpenStax Psychology 2e textbook, give a very brief explanation. The description should be in basic HTML with <p> tags for paragraphs and <b> tags for bold text. 
        It should explain why the answer is correct and why the distractors are incorrect, if possible - but don't use the letters A to D nor the order of the options (e.g. avoid "both A and B" or "neither A nor B", but also "first option" or "last option"),
          as they will be randomized!!! Instead just mention the answers directly, or abbreviate them if neccessary. A good description should be informative and concise. Keep in mind
          that freshmen Psychology students are the target audience. Make it flow and be readable.

        Input:
        Question title: "{question_title}"
        Answers: "{answers}"
        Correct answer: "{correct_answer}"

        Output format (valid HTML):
        <div> DESCRIPTION </div>
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("user", "{question_title}\n{answers}\n{correct_answer}"),
        ]
    )
    chain = prompt_template | model | parser

    input_dict = {
        "question_title": question_title,
        "answers": answers,
        "correct_answer": correct_answer,
    }

    # Get the string output
    description_str = chain.invoke(input_dict)

    return description_str


def llm_get_sensible(question_title: str, answers: str, correct_answer: str) -> bool:
    system_template = """
        Given the following question and answers from the OpenStax Psychology 2e textbook, predict whether the question is sensible ("YES") or not ("NO"). A sensible question is one that
        can be understood, is relevant, and is not very misleading. It's fine if the grammar is wrong, the answer is incorrect or the question is incomplete. Just
        focus on the question itself.

        Input:
        Question title: "{question_title}"
        Answers: "{answers}"
        Correct answer: "{correct_answer}"

        Output: "YES" or "NO"
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("user", "{question_title}\n{answers}\n{correct_answer}"),
        ]
    )
    chain = prompt_template | model | parser

    input_dict = {
        "question_title": question_title,
        "answers": answers,
        "correct_answer": correct_answer,
    }

    # Get the string output
    # Attempt to parse the string output to a boolean
    try:
        sensible = chain.invoke(input_dict) == "YES"
    except ValueError:
        # Handle ValueError
        print("Error: Could not parse sensible value.")
        sensible = False


    print("sensible", sensible)

    return sensible


def llm_get_correct(question_title: str, answers: str, correct_answer: str) -> bool:
    system_template = """
        Given the following student-made question and answers from the OpenStax Psychology 2e textbook, predict whether the question can be considered as correct ("YES") or not ("NO"). A correct question is one that
        has a correct answer and the distractors are all incorrect. It's fine if the grammar is wrong, the question is incomplete or the question is misleading. Just
        focus on the question itself. Keep in mind that they are Psychology freshmen, so be lenient. Not perfect or not specific enough is fine. Confusing rods and cones is not.

        Input:
        Question title: "{question_title}"
        Answers: "{answers}"
        Correct answer: "{correct_answer}"

        Output: "YES" or "NO"
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("user", "{question_title}\n{answers}\n{correct_answer}"),
        ]
    )
    chain = prompt_template | model | parser

    input_dict = {
        "question_title": question_title,
        "answers": answers,
        "correct_answer": correct_answer,
    }

    # Get the string output
    # Attempt to parse the string output to a boolean
    try:
        correct = chain.invoke(input_dict) == "YES"
    except ValueError:
        # Handle ValueError
        print("Error: Could not parse correct value.")
        correct = False

    return correct


def llm_adjust_question(
    question_title: str,
    marked_correct_answer: str,
    answer_1: str,
    answer_2: str,
    answer_3: str,
    answer_4: str,
) -> dict:
    # we can use the model to adjust the question
    model = ChatOpenAI(model="gpt-4o")  # we use a larger model for this task
    system_template = """
        Given the following student-made question and answers from the OpenStax Psychology 2e textbook, adjust the question to make it more correct, sensible, not misleading, grammatical, complete. You can alter the question title, correct answer, distractors or anything else you see fit, but
        do so only if it's really needed, try to keep it as authentic as possible. Simple or low quality questions are okay. As long as it's sensible, not seriously misleading or obviously wrong.
        It's perfectly fine if you return the original, if deemed good enough. If one of the distractors is lazily made or missing, feel free to replace it with a better one. I want you to be relatively lenient, as they are freshmen Psychology students.
        Where you do make changes, try to follow the material in the OpenStax Psychology 2e textbook.
        Change the correct answer only if it's wrong - if it's reasonably correct, it's fine. It doesn't have to be perfect or super specific.  Your task is not to make the question perfect, but to make it better.
        The rules don't apply for grammar, spelling, punctuation, formatting etc. - you don't have to be lenient. Also ensure that the answers have the same case-style.
        The answers will be randomized, so make sure they don't rely on "A to D" nor the order of the options (e.g. avoid "both A and B" or "neither A nor B"), also replace "all of the above" and similar with other non-position-based options ("all other answers except...").

        Input:
        {{
            "question_title": "{question_title}",
            "marked_correct_answer": "{marked_correct_answer}",
            "answer_a": "{answer_a}",
            "answer_b": "{answer_b}",
            "answer_c": "{answer_c}",
            "answer_d": "{answer_d}"
        }}

        Output format:
        {{
            "question_title": "<question_title>",
            "correct_answer": "<correct_answer>",
            "distractor_1": "<distractor_1>",
            "distractor_2": "<distractor_2>",
            "distractor_3": "<distractor_3>"
        }}
    """

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{question_title}\n{marked_correct_answer}\n{answer_a}\n{answer_b}\n{answer_c}\n{answer_d}")]
    )
    chain = prompt_template | model | parser

    input_dict = {
        "question_title": question_title,
        "marked_correct_answer": marked_correct_answer,
        "answer_a": answer_1,
        "answer_b": answer_2,
        "answer_c": answer_3,
        "answer_d": answer_4,
    }

    # Get the string output
    question_str = chain.invoke(input_dict)
    print("got the question", question_str)


    # Attempt to parse the string output to a dictionary
    try:
        question_dict = json.loads(question_str)
    except json.JSONDecodeError:
        print("Error: Could not parse question.")
        # Handle JSON parsing error
        question_dict = {}


    return question_dict


def get_student_id_chapter(canvas_student_id_composite: str):
    # try to get the chapter from the student id, depends on whether they have submitted it correctly, return a tuple of the student id and the chapter
    CORRECT_COMPOSITE_LENGTH = 8
    if len(canvas_student_id_composite) == CORRECT_COMPOSITE_LENGTH:
        return (canvas_student_id_composite[:7], canvas_student_id_composite[7])
    else:
        return (canvas_student_id_composite, None)


def canvas_student_q_to_db_ready_dict(original_text: str) -> dict:
    raw_dict = canvas_student_q_organized_to_raw_dict(original_text)
    # try
    student_id, chapter = None, None
    try:
        student_id, chapter = get_student_id_chapter(raw_dict["student_id"])
    except ValueError:
        print("Error: Could not parse student_id.")
    if student_id is None:
        raise ValueError("Could not parse student_id")
    if chapter is None:
        chapter = llm_get_chapter(
            raw_dict["question_title"],
            f"A) {raw_dict['answer_a']}\nB) {raw_dict['answer_b']}\nC) {raw_dict['answer_c']}\nD) {raw_dict['answer_d']}",
        )

    if not llm_get_sensible(
        raw_dict["question_title"],
        f"A) {raw_dict['answer_a']}\nB) {raw_dict['answer_b']}\nC) {raw_dict['answer_c']}\nD) {raw_dict['answer_d']}",
        raw_dict["marked_correct_answer"],
    ):
        return {}
    adjusted_dict = llm_adjust_question(
        raw_dict["question_title"],
        raw_dict["marked_correct_answer"],
        raw_dict["answer_a"],
        raw_dict["answer_b"],
        raw_dict["answer_c"],
        raw_dict["answer_d"],
    )
    print("the dict", adjusted_dict)
    llm_description = llm_get_description(
        adjusted_dict["question_title"],
        f"A) {adjusted_dict['distractor_1']}\nB) {adjusted_dict['distractor_2']}\nC) {adjusted_dict['distractor_3']}\nD) {adjusted_dict['correct_answer']}",
        adjusted_dict["correct_answer"],
    )
    adjusted_dict["student_id"] = student_id
    adjusted_dict["chapter_id"] = chapter
    adjusted_dict["description_llm"] = llm_description
    print(llm_description)

    print(raw_dict)

    return adjusted_dict


if __name__ == "__main__":
    raw_dict = canvas_student_q_to_db_ready_dict(  # step 1, we get the dict
        """07677714. Fill in the blanks: when you fall asleep, the brain frequency patterns will (1) and the amplitude will (2)
    
            A) (1) = increase, (2) = increase
            B) (1) = decrease, (2) = decrease
            *C) (1) = decrease, (2) = increase
            D) (1) = increase, (2) = decrease
            """
    )
    raw_dict2 = canvas_student_q_to_db_ready_dict(  # step 1, we get the dict
        """
        08123451. If a parent tries to stop a child from misbehaving by scolding them, which teaching method is applied by the parent?

        A) Positive reinforcement
        *B) Positive punishment
        C) Negative reinforcement
        D) Negative punishment
        """
    )

    raw_dict3 = canvas_student_q_to_db_ready_dict(  # step 1, we get the dict
        """
                17304445. What sort of pain is felt immediately when suffering an injury?

        A) tonic pain
        *B) phasic pain
        C) phantom pain
        D) You won't feel the pain.
        """
    )
    raw_dict4 = canvas_student_q_to_db_ready_dict(  # step 1, we get the dict
        """
        08123455. Imagine someone getting struck in the head by an arrow. The arrow penatrates Wernicke's area, causing its functions to cease.
What would happen if this person were to engage in a conversation with someone else?

A) He cannot understand what is said to him, nor can he talk back
B) He can engage in a normal conversation, but he cannot identify the face of the other person.
*C) He cannot understand what is said to him, but he could talk back.
D) He is completely paralyzed.

        """
    )

    raw_dict5 = canvas_student_q_to_db_ready_dict(  # step 1, we get the dict
        """
        08123455. Imagine someone getting struck in the head by an arrow. The arrow penatrates Wernicke's area, causing its functions to cease.
What would happen if this person were to engage in a conversation with someone else?

A) He cannot understand what is said to him, nor can he talk back
B) He can engage in a normal conversation, but he cannot identify the face of the other person.
*C) He cannot understand what is said to him, but he could talk back.
D) He is completely paralyzed.

        """
    )

    raw_dict6 = canvas_student_q_to_db_ready_dict(  # step 1, we get the dict
        """
        07677712. In a research, the researchers look back at the events of the second world war and its effects. What kind of research is this?

A) longitudinal research
B) cross-sectional research
*C) Archival research.
D) experiment
    """
    )
