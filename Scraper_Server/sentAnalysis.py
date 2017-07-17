from __future__ import division
from pymongo import MongoClient
from textblob import TextBlob


class Analyse:
    def __init__(self,PID):
        self.client = MongoClient("mongodb://192.168.0.11:27017").FlipNLP.Product_Reviews
        self.PID = PID

    def averageSentiment(self):
        retval = []
        for i in self.client.find({'PID':self.PID}):
            try:
                string  =  str(i['heading'])+' '+str(i['review'])
                retval.append(TextBlob(string).sentiment.polarity)
            except:
                pass
        return sum(retval)/len(retval)

if __name__ == "__main__":
    print Analyse('SHOEREHEDQDUHCHU').averageSentiment()
