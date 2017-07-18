from __future__ import division
from pymongo import MongoClient
from textblob import TextBlob
from math import log,exp

class Analyse:
    def __init__(self,PID):
        self.client = MongoClient("mongodb://192.168.0.11:27017").FlipNLP.Product_Reviews
        self.info = MongoClient("mongodb://192.168.0.11:27017").FlipNLP.Product_Info
        self.PID = PID

    def getRating(self):
        return float(list(self.info.find({'PID':self.PID}))[0]['rating'])

    def _sigmoidal(self,value):
        retval = ( 1 + exp(-value))**-1
        return retval

    def _sentimentFactor(self,up,down):
        try:
            normalize = log(int(up)-int(down),10)
            return self._sigmoidal(normalize)
        except:
            return 0

    def averageSentiment(self):
        retval = []
        for i in self.client.find({'PID':self.PID}):
            try:
                string  =  str(i['heading'])+' '+str(i['review'])
                sentiment = TextBlob(string).sentiment.polarity
                factor = self._sentimentFactor(i['up'],i['down'])
                retval.append(sentiment + sentiment*factor)
            except:
                pass
        return sum(retval)/len(retval)

    def predictRating(self):
        at_10 = self.averageSentiment()
        to_5 = at_10*5
        rating = self.getRating()
        if rating == 0:
            return to_5
        else:
            return (to_5+rating)/2


if __name__ == "__main__":
    print Analyse('SHOEREHEFXTHEBJN').predictRating()
