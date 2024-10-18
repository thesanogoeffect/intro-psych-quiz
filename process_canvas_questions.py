import re
import llm_extractor as llm
import pandas as pd
import db_operations as db
import pytz
"""WE CANNOT AVOID MANUAL INSPECTION OF THE DATA, BUT WE CAN REDUCE THE AMOUNT OF MANUAL WORK NEEDED
THIS PART IS NOT PIPELINED, BUT A ONE-TIME PREPROCESSING STEP"""

TXT_FILE = "combined_student_generated_halfway_answers_2021-2.txt"
SOURCE_NAME = "21/22_Student_Halfway"

# first, manual preprocessing - deleting stuff like 
# c:\users\dlakens\surfdrive\onderwijs\psychology & technology\tentamen\practice\student generated_halfway_questions_2021\sanlibayrak�a_51250_3474009_assignment 4.txt
# ************************************************************************
# [Error] - File could not be written...

# then manually inspect (?<!\d)\d{7,8}(?!\d|\.) - 7 or 8 digit numbers that are not followed by a digit or a dot


def split_into_chunks(text):
    # Split the text by the pattern
    parts = re.split(r"(\d{7,9}\.)", text)
    
    # Combine the split parts into chunks
    chunks = []
    for i in range(1, len(parts), 2):
        # check that the text part is not empty or very short
        student_id_chapter_dot = parts[i] # 17274273.
        student_id_chapter = student_id_chapter_dot.rstrip(".") # 17274273
        question_content = parts[i + 1]
        if len(question_content) < 70:  # issue a warning if the question content is very short
            print("Found short question content, CHECK MANUALLY:", question_content)
        chunk = student_id_chapter_dot + question_content
        chunks.append(chunk)
    
    return chunks

def process_canvas_questions(txt_file, source_name) ->  pd.DataFrame:
    # Read the text file
    with open(txt_file, "r", encoding="iso-8859-1") as f:
        text = f.read()
        
    chunks = split_into_chunks(text)
    
    chunk_dicts = []
    for chunk in chunks:
        cleaned_dict = llm.canvas_student_q_to_db_ready_dict(chunk)
        if not cleaned_dict:
            print("There is something wrong with this question", chunk)
            continue
        else:
            chunk_dicts.append(cleaned_dict)
    df = pd.DataFrame(chunk_dicts)
    # change student_id to author
    df.rename(columns={"student_id": "author"}, inplace=True)
    df["timestamp"] = pd.Timestamp.now(tz=pytz.timezone("Europe/Amsterdam")).strftime(
        "%m/%d/%Y %H:%M:%S"
    )
    df["source"] = source_name
    return df

def process_canvas_questions_to_db(txt_file : str, source_name : str ) -> None:
    df = process_canvas_questions(txt_file, source_name) # process the questions
    db.process_new_questions(df) # insert the new questions into the database
            


if __name__ == "__main__":
    # Read the text file
    
    process_canvas_questions_to_db(TXT_FILE, SOURCE_NAME)

 

        # now we are pretty much ready to start advanced preprocessing with the LLM model
        # in the end, we want a dataframe to insert into the SQLite database