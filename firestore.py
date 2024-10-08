# connect to Firestore when we need to touch the live data

# columns: difficulty_score_sum, quality_score_sum, seen_times, times_flagged_as_incorrect, times_flagged_as_misleading, times_flagged_other_problem, times_rated_difficulty, times_rated_quality, total_answered, total_answered_correct
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

COLLECTION_NAME = "questions"
client = firestore.client()

new_question = {
    "difficulty_score_sum": 0,
    "quality_score_sum": 0,
    "seen_times": 0,
    "times_flagged_as_incorrect": 0,
    "times_flagged_as_misleading": 0,
    "times_flagged_other_problem": 0,
    "times_rated_difficulty": 0,
    "times_rated_quality": 0,
    "total_answered": 0,
    "total_answered_correct": 0,
    "total_times_skipped": 0,
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

# if __name__ == "__main__":
#     delete_all_questions()