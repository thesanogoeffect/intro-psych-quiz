# connect to Firestore when we need to touch the live data

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

COLLECTION_NAME = "questions"
client = firestore.client()

new_question = {
    "times_asked": 0,
    "times_answered_correct": 0,
    "times_skipped": 0,
    "times_flagged": 0,
    "times_answered": 0,
    "times_upvoted": 0,
    "times_downvoted": 0,
}


# get a question by id
def get_question_by_id(question_id: int) -> dict:
    doc_ref = client.collection(COLLECTION_NAME).document(str(question_id))
    return doc_ref.get().to_dict()


def create_question(question_id: int) -> None:
    doc_ref = client.collection(COLLECTION_NAME).document(str(question_id))
    question_contents = new_question.copy()
    question_contents["question_id"] = question_id
    doc_ref.set(question_contents)
    # set question_id as the document id
    # also set the question_id in the document


def delete_question(question_id: int) -> None:
    doc_ref = client.collection(COLLECTION_NAME).document(str(question_id))
    doc_ref.delete()


def delete_all_questions():
    questions = client.collection(COLLECTION_NAME).stream()
    for question in questions:
        question.reference.delete()


if __name__ == "__main__":
    delete_all_questions()
