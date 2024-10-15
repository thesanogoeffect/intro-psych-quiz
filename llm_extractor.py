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
        
        Output format (valid JSON): {{
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
    


def process_book_text_questions(book_text: str, chapter_id:int) -> pd.DataFrame:
    book_text = add_separator_to_book_text(book_text)
    questions = book_text.split("|")
    questions = [extract_dict_from_question_text(question) for question in questions]
    df = pd.DataFrame(questions)
    df["source"] = "Book"
    df["chapter_id"] = chapter_id
    df["author"] = ""
    df["timestamp"] = pd.Timestamp.now(tz=pytz.timezone('Europe/Amsterdam')).strftime('%m/%d/%Y %H:%M:%S')
    df = df[["timestamp", "question_title", "chapter_id", "correct_answer", "distractor_1", "distractor_2", "distractor_3", "source", "author"]]
    return df

