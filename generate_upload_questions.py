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


upload_questions_from_book(14, """
17. Which of the following is not one of the presumed components of happiness?
a. using our talents to help improve the lives of others
b. learning new skills
c. regular pleasurable experiences
d. identifying and using our talents to enrich our lives
18. Researchers have identified a number of factors that are related to happiness. Which of the following is
not one of them?
a. age
b. annual income up to $75,000
c. physical attractiveness
d. marriage
19. How does positive affect differ from optimism?
a. Optimism is more scientific than positive affect.
b. Positive affect is more scientific than optimism.
c. Positive affect involves feeling states, whereas optimism involves expectations.
d. Optimism involves feeling states, whereas positive affect involves expectations.
20. Carson enjoys writing mystery novels, and has even managed to publish some of his work. When he’s
writing, Carson becomes extremely focused on his work; in fact, he becomes so absorbed that that he
often loses track of time, often staying up well past 3 a.m. Carson’s experience best illustrates the concept
of ________.
a. happiness set point
b. adaptation
c. positive affect
d. flow
""")