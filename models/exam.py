from utils.mongo import get_mongo_collection

class Exam:
    @staticmethod
    def get_questions():
        """
        Fetch coding test questions from the database.
        """
        collection = get_mongo_collection("coding_tests")
        questions = list(collection.find({}, {"_id": 0, "question": 1, "options": 1}))
        return questions

    @staticmethod
    def submit_answers(candidate_id, answers):
        """
        Submit coding test answers to the database.
        """
        collection = get_mongo_collection("coding_tests")
        result = collection.update_one(
            {"candidate_id": candidate_id},
            {"$set": {"answers": answers, "status": "submitted"}},
            upsert=True
        )
        return result.acknowledged