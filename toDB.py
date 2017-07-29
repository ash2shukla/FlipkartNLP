from pymongo import MongoClient

class toDB:
    def __init__(self):
        try:
            URL = "mongodb://127.0.0.1:27017"
            self.client = MongoClient(URL)
            self.FlipNLP = self.client.FlipNLP
        except:
            print "Could not maintain a connection with Database"
            exit(0)

    def insertReviews(self,JSON):
        self.FlipNLP.Product_Reviews.insert(JSON)

    def insertSpecs(self,JSON):
        self.FlipNLP.Product_Info.insert(JSON)
