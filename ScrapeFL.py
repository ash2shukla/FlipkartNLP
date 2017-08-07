from requests import get
from bs4 import BeautifulSoup as bs
from pprint import pprint
from PhantomSource import PhantomSource
from toDB import toDB

class ScrapeFL:
    URL_Base = "https://www.flipkart.com"
    def __init__(self):
        self.toDB = toDB()

    def getPID(self,string):
        try:
            start = string.index("pid=")
            end = string.index('&')
            return string[start+4:end]
        except:
            return ''

    def scrapeProduct(self,string):
        URL = "https://www.flipkart.com/search?q=" + string
        soup = bs(get(URL).text)
        p_class = "_3v8VuN"
        try:
            p_no =  int(soup.find('span',{'class':p_class}).span.contents[1].split(' ')[3].replace(',',''))
        except:
            p_no = 0
        print "Pages Found = "+str(p_no)
        for i in range(p_no+1):
            data = self.extractProductNames(URL+"&page="+str(i+1))
            print '\n'.join([str(data.index(j)) + ". "+j['title'] for j in data])
            print "More results ? press enter. Else give index of your product."
            inp = raw_input()
            if ( inp == ''):
                continue
            else:
                data  = self.scrapeIndividual(data[int(inp)])
                break
        self.toDB.insertSpecs(data[0])
        for i in data[1]:
            self.toDB.insertReviews(i)


    def extractProductNames(self,URL_product):
        rectify = "_2cLu-l"
        soup = bs(get(URL_product).text)
        all_results = [ {'title':i['title'],'link':self.URL_Base+i['href'],'pid':self.getPID(i['href'])} for i in soup.findAll('a',{'class':rectify}) ]
        if all_results == []:
            total = "col _2-gKeQ"
            title = "_3wU53n"
            link = "_1UoZlX"
            all_results = [{'title':i.find('div',{'class':title}).string,'link':self.URL_Base+i.find('a',{'class':link})['href'],'pid':self.getPID(i.find('a',{'class':link})['href'])} for i in soup.findAll('div',{'class':total})]
        print all_results
        return all_results

    def scrapeIndividual(self,Object_individual):
        soup = bs(get(Object_individual['link']).text)
        PID = Object_individual['pid']
        P_name = Object_individual['title']
        in_spec_class = "_2Kp3n6"
        in_spec_name = "HoUsOy"
        key_class = "vmXPri col col-3-12"
        value_class = "sNqDog"
        review_class = "swINJg _3nrCtb"
        rating_class = "_1i0wk8"
        retval = {}

        URL_review = soup.find('div',{'class':review_class}).parent['href']

        data =  soup.findAll('div',{'class':in_spec_class})
        try:
            rating = soup.find('div',{'class':rating_class}).string
        except:
            rating = 0

        for i in data:
            try:
                sub_name = i.find('div',{'class':in_spec_name}).contents[0]
            except:
                sub_name = 'base_info'+str(data.index(i))
            dic = {}

            all_keys = [j.contents[0] for j in i.findAll('div',{'class':key_class})]
            all_values = [j.contents[0] for j in i.findAll('li',{'class':value_class})]

            for j,k in zip(all_keys,all_values):
                dic[j]=k
            retval[sub_name] = dic
        retval['title'] =P_name
        retval['PID'] = PID
        retval['rating'] = rating

        return [retval,self.getReviews(self.URL_Base+URL_review,PID)]


    def getReviews(self,reviewURL,PID):
        retval = []
        soup = bs(PhantomSource().getSource(reviewURL))
        p_class = "_3v8VuN"
        try:
            p_no =  int(soup.find('span',{'class':p_class}).span.contents[1].split(' ')[3].replace(',',''))
        except:
            p_no = 0
        if reviewURL[reviewURL.index('?')+1:reviewURL.index('?')+5] != 'page':
            parts = reviewURL.split('?')
        else:
            parts = reviewURL.split('?page=1')

        print("Pages Found "+str(p_no))
        if(p_no > 10 ):
            print("How many pages to scrape ?")
            p_no = input()

        for i in range(p_no):
            URL = ('?page='+str(i+1)+"&").join(parts)
            print("Getting Reviews Of Page "+str(i+1))
            retval += self.getReviewPerPage(URL,PID)
        print("Reviewing Done")
        return retval

    def getReviewPerPage(self,reviewURL,PID):
        soup = bs(PhantomSource().getSource(reviewURL))
        box_class = "_3DCdKt"
        heading_class = "_2xg6Ul"
        review_class = "qwjRop"
        span_class = "_1_BQL8"

        blocks = soup.findAll('div',{'class':box_class})
        heading = [ i.find('p',{'class':heading_class}).string for i in blocks ]
        review =  [ i.find('div',{'class':review_class}).div.div.string for i in blocks ]
        thumbs_up = [ i.findAll('span',{'class':span_class})[0].string for i in blocks ]
        thumbs_down = [ i.findAll('span',{'class':span_class})[1].string for i in blocks ]

        retval = []

        for i,j,k,m in zip(heading,review,thumbs_up,thumbs_down):
                dic ={}
                dic['heading'] = i
                dic['review'] = j
                dic['PID'] = PID
                dic['up'] = k
                dic['down'] = m
                retval.append(dic)
        return retval

if __name__ == "__main__":
        ScrapeFL().scrapeProduct('mobile')
