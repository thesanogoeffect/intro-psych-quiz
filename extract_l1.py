from gsheets import download_l1_gsheet_to_df
import pandas as pd
import sqlite3
from db_operations import create_table, process_new_questions


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


# Step 1: Download the data from the Google Sheet
df = download_l1_gsheet_to_df()

# Step 2: Load current snapshot, if it exists
try:
    snapshot_df = pd.read_csv("l1_latest_snapshot.csv", index_col=0)  # Load snapshot with index
except FileNotFoundError:
    snapshot_df = None

# Step 3: Compare DataFrames and get new rows
if snapshot_df is not None:
    # If there's a snapshot, compare and filter new rows
    new_rows_df = df[~df.index.isin(snapshot_df.index)]
else:
    # If no snapshot exists, assume all rows are new
    new_rows_df = df

# Step 4: Save the DataFrame as a new snapshot, including the index
df.to_csv("l1_latest_snapshot.csv", index=True)

# Step 5: Create the table if it doesn't exist
create_table()

# Step 6: Insert new data into the SQLite database
if not new_rows_df.empty:
    process_new_questions(new_rows_df)
