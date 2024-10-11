from gsheets import download_l1_gsheet_to_df
import pandas as pd
import sqlite3
from firestore import create_question, delete_question

# add new columns in addition to l2, keeping in mind that the live data exists in Firestore

# LLM features are suffixed with "_llm"
# is_sensible_llm - boolean
# is_grammatical_llm - boolean
# is_relevant_chapter_llm - boolean 
# is_complete_llm - boolean
# is_correct_llm - boolean
# is_misleading_llm - boolean

# now do the same for human annotations
# is_sensible_human - boolean
# is_grammatical_human - boolean
# is_relevant_chapter_human - boolean
# is_complete_human - boolean
# is_correct_human - boolean
# is_misleading_human - boolean

# now add quality and difficulty scores
# quality_score - float (0-1) 0 is worst, 1 is best
# difficulty_score - float (0-1) 0 is easiest, 1 is hardest

# also there is a possiblity that this question is a spin-off of another question or llm generated
# spinoff_id - integer (id of the original question)
# is_llm_generated - boolean
# revision - integer (incremented every time the question is edited)


def create_table():
    # connect to l1 SQLite database
    conn = sqlite3.connect("l2.db")
    # create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS l2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        question_title TEXT NOT NULL,
        chapter_id INTEGER NOT NULL,
        correct_answer TEXT NOT NULL,
        distractor_1 TEXT NOT NULL,
        distractor_2 TEXT NOT NULL,
        distractor_3 TEXT NOT NULL,
        source TEXT,
        author TEXT,
        student_id TEXT,
        is_sensible_llm BOOLEAN,
        is_grammatical_llm BOOLEAN,
        is_relevant_chapter_llm BOOLEAN,
        is_complete_llm BOOLEAN,
        is_correct_llm BOOLEAN,
        is_misleading_llm BOOLEAN,
        is_sensible_human BOOLEAN,
        is_grammatical_human BOOLEAN,
        is_relevant_chapter_human BOOLEAN,
        is_complete_human BOOLEAN,
        is_correct_human BOOLEAN,
        is_misleading_human BOOLEAN,
        quality_score_llm FLOAT,
        difficulty_score_llm FLOAT,
        is_spinoff BOOLEAN,
        spinoff_id INTEGER,
        is_llm_generated BOOLEAN

    );
    """
    conn.execute(create_table_query)
    conn.close()

def dump_df_to_db(df : pd.DataFrame):
    conn = sqlite3.connect("l2.db")
    df.to_sql('l2', conn, if_exists='append', index=False)
    conn.close()

def delete_question(question_id: int) -> None:
    conn = sqlite3.connect("l2.db")
    delete_query = f"DELETE FROM l2 WHERE id = {question_id}"
    # also delete from Firestore
    delete_question(question_id)
    conn.execute(delete_query)
    conn.close()


def process_new_questions(df: pd.DataFrame):
    # Insert new data into the SQLite database
    if not df.empty:
        dump_df_to_db(df)
    # for each new question, create a new document in Firestore
    # retrieve the ids of the new questions
    new_row_count = len(df)
    try:
        conn = sqlite3.connect("l2.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM l2 ORDER BY id DESC LIMIT {new_row_count}")
        new_question_ids = cursor.fetchall()
        for question_id in new_question_ids:
            create_question(question_id[0])
        conn.close()
    except Exception as e:
        print(e)
        return
    

def load_db_into_df():
    conn = sqlite3.connect("l2.db")
    df = pd.read_sql_query("SELECT * FROM l2", conn)
    conn.close()
    return df


# if __name__ == "__main__":
# # try load only db into df
#     df =load_db_into_df()
#     print(df)
    

