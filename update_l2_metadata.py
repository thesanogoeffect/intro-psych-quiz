import db_operations as db
import pandas as pd
import llm_extractor as llm
import os
"""provides methods that will be used in pipelines to regularly update the l2 metadata"""


def update_missing_descriptions():
    """Update the l2 metadata with missing descriptions"""
    # get the l2 data
    df = db.load_db_into_df()
    # get the rows with missing descriptions
    missing_descriptions = df[df["description_llm"].isnull()]
    # update the missing descriptions
    for index, row in missing_descriptions.iterrows():
        # get the description
        llm_description = llm.llm_get_description(
            row["question_title"],
            f"A) {row['distractor_1']}\nB) {row['distractor_2']}\nC) {row['distractor_3']}\nD) {row['correct_answer']}",
            row["correct_answer"],
        )
        # update the description
        df.at[index, "description_llm"] = llm_description
    # save the updated data
    db.replace_df_in_db(df)


def update_is_correct():
    """Update the l2 metadata with missing is_correct values"""
    # get the l2 data
    df = db.load_db_into_df()
    # get the rows with missing is_correct values
    missing_is_correct = df[df["is_correct_llm"].isnull()]
    # update the missing is_correct values
    for index, row in missing_is_correct.iterrows():
        # get the is_correct value
        is_correct = llm.llm_get_is_correct(
            row["question_title"],
            f"A) {row['distractor_1']}\nB) {row['distractor_2']}\nC) {row['distractor_3']}\nD) {row['correct_answer']}",
            row["correct_answer"],
        )
        # update the is_correct value
        df.at[index, "is_correct_llm"] = is_correct
    # save the updated data
    db.replace_df_in_db(df)

def make_db_backup():
    """Make a backup of the l2 database"""
    # get the l2 data
    df = db.load_db_into_df()
    # save the data as a csv
    df.to_csv("l2_backup.csv", index=False)

if __name__ == "__main__":
    make_db_backup()
    update_is_correct()
    update_missing_descriptions()