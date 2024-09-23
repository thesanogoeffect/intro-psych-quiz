"""Module for the parsing of the question/answer .txt files"""

import pandas as pd
import re


class TxtProcessor:
    def __init__(self, path):
        self.path = path
        self.df = None
        self.process()

    def process(self):
        with open(self.path, "r", encoding='utf-8-sig') as file:
            text = file.read()
            split_text = text.split("\n\n")
            # now we have question on the even indexes and answers on the odd indexes
            questions = split_text[::2]
            answers = split_text[1::2]

            question_data = []
            for question, answers in zip(questions, answers):
                q_dict = {}
                # ['17274271. What was Gestalt Psychology a response to?',
                split = question.split(".")
                q_id = question.split(".")[0].strip()
                q_dict["question_title"] = " ".join(split[1:]).strip()
                q_chapter = q_id[-1]
                q_dict["ID"] = int(q_id)
                q_dict["chapter"] = int(q_chapter)

                # now parse the answer data
                # 'A) Behaviorism\n*B) Structuralism\nC) Cognitive Psychology\nD) Humanistic Psychology'
                correct_answer = None
                answer_options = []
                parsed_answers = answers.split("\n")
                for answer in parsed_answers:
                    if "*" in answer:
                        correct_answer = answer.strip()[3:].strip()
                        answer_options.append(answer.strip()[3:].strip())
                    else:
                        answer_options.append(answer.strip()[2:].strip())
                q_dict["correct_answer"] = correct_answer
                q_dict["options"] = answer_options
                question_data.append(q_dict)
            self.df = pd.DataFrame(question_data)
            self.df.set_index("ID", inplace=True)
            # drop all rows that have the same index
            self.df = self.df[~self.df.index.duplicated(keep=False)]


if __name__ == "__main__":
    txt = TxtProcessor("cleaned_questions.txt")
    txt.df.to_parquet("Halfway Answers 2021-2_cleaned.parquet")
