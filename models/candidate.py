from utils.mongo import get_mongo_collection
import bcrypt

class Candidate:
    def __init__(self, data):
        self.username = data["username"]
        self.email = data["email"]
        self.password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
        self.status = "Pending"
        self.test_results = None
        self.interview_scheduled = False

    def save(self):
        collection = get_mongo_collection("candidates")
        collection.insert_one(self.__dict__)

    @staticmethod
    def find_by_email(email):
        collection = get_mongo_collection("candidates")
        return collection.find_one({"email": email})

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)