from db_operations import load_db_into_df
# running scripts to transform the l2 (sqlite) into a cherrypicked selection (l3) based on heuristic rules (such as sensible, grammatical, relevant chapter, complete, correct, misleading and quality/difficulty scores)


# in L3, we want less features again. the final features are:
# id INTEGER PRIMARY KEY AUTOINCREMENT,
        # id INTEGER PRIMARY KEY AUTOINCREMENT,
        # timestamp TEXT NOT NULL,
        # question_title TEXT NOT NULL,
        # chapter_id INTEGER NOT NULL,
        # correct_answer TEXT NOT NULL,
        # distractor_1 TEXT NOT NULL,
        # distractor_2 TEXT NOT NULL,
        # distractor_3 TEXT NOT NULL,
        # source TEXT,
        # author TEXT,
        # chapter_id_llm BOOLEAN,
        # description_llm TEXT,
        # is_correct_llm BOOLEAN,
        # quality_score_llm INTEGER,
        # is_spinoff BOOLEAN,
        # spinoff_id INTEGER,

# at first, we just export all questions from L2, later we will add heuristics to filter out the best questions and discard duplicates
# it's ok to have l3 only .csv, .json, no need for a database
def create_l3():
    # get the l2 data
    df = load_db_into_df()
    # keep only the columns we want
    df = df[["id", "timestamp", "question_title", "chapter_id", "correct_answer", "distractor_1", "distractor_2", "distractor_3", "source", "author", "description_llm"]]
    # save the l2 data as l3
    df.to_csv("l3.csv", index=False)
    # now also save it as json
    df.to_json("l3.json", orient="records")

if __name__ == "__main__":
    create_l3()

