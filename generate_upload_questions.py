from llm_extractor import process_book_text_questions 
from gsheets import download_l1_gsheet_to_df, upload_l1_df_to_gsheet
# matching the following table format in GSheets:
# timestamp	question_title	chapter_id	correct_answer	distractor_1	distractor_2	distractor_3	source	author

# we want different ways to be able to generate questions

# generate from book

def upload_questions_from_book(chapter_id: int, book_text : str) -> None:
    # take in copy pasted text from book, separate questions by | and, 
    df = process_book_text_questions(book_text, chapter_id)

    # upload to GSheets
    upload_l1_df_to_gsheet(df)


# upload_questions_from_book(12, """
# 24. Altruism is a form of prosocial behavior that is motivated by ________.
# a. feeling good about oneself
# b. selfless helping of others
# c. earning a reward
# d. showing bravery to bystanders
# 25. After moving to a new apartment building, research suggests that Sam will be most likely to become
# friends with ________.
# a. his next door neighbor
# b. someone who lives three floors up in the apartment building
# c. someone from across the street
# d. his new postal delivery person
# 26. What trait do both men and women tend to look for in a romantic partner?
# a. sense of humor
# b. social skills
# c. leadership potential
# d. physical attractiveness
# 27. According to the triangular theory of love, what type of love is defined by passion and intimacy but no
# commitment?
# a. consummate love
# b. empty love
# c. romantic love
# d. liking
# 28. According to social exchange theory, humans want to maximize the ________ and minimize the ________
# in relationships.
# a. intimacy; commitment
# b. benefits; costs
# c. costs; benefits
# d. passion; intimacy
# """)