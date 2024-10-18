import re
"""WE CANNOT AVOID MANUAL INSPECTION OF THE DATA, BUT WE CAN REDUCE THE AMOUNT OF MANUAL WORK NEEDED
THIS PART IS NOT PIPELINED, BUT A ONE-TIME PREPROCESSING STEP"""

TXT_FILE = "combined_student_generated_halfway_answers_2021-2.txt"

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


if __name__ == "__main__":
    # Read the text file
    with open(TXT_FILE, "r", encoding="iso-8859-1") as f:
        text = f.read()
        
        chunks = split_into_chunks(text)
        # just to make sure, print the last chunk and compare to the original txt
        print(chunks[-1])

        # now we are pretty much ready to start advanced preprocessing with the LLM model
        # in the end, we want a dataframe to insert into the SQLite database