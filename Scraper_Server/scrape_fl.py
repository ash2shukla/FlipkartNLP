from requests import get
from bs4 import BeautifulSoup as bs
from pprint import pprint
from PhantomSource import PhantomSource

class ScrapeFL:
    def scrapeJuta(self,string):
        URL_Base = "https://www.flipkart.com"
        URL = "https://www.flipkart.com/search?q=" + string
        soup = bs(get(URL).text)
        rectify = "_2cLu-l"

        all_results = [ {'title':i['title'],'link':URL_Base+i['href'],'pid':self.getPID(i['href'])} for i in soup.findAll('a',{'class':rectify}) ]

        '''all_results = []
        for i in soup.findAll('a',{'class':rectify}):
            dic={}
            dic['title']=i['title']
            dic['href']=i['href']
            all_results.append(dic)
        '''
        print all_results
        for i in all_results:
            pprint(self.scrapeIndividual(get(i['link']).text))

    def scrapeIndividual(self,string):
        URL_Base = "https://www.flipkart.com"
        soup = bs(string)
        in_spec_class = "_2Kp3n6"
        in_spec_name = "HoUsOy"
        key_class = "vmXPri col col-3-12"
        value_class = "sNqDog"
        review_class = "swINJg _3nrCtb"
        retval = {}

        URL_review = soup.find('div',{'class':review_class}).parent['href']

        data =  soup.findAll('div',{'class':in_spec_class})

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
        self.getReviews(URL_Base+URL_review)
        return retval

    def getPID(self,string):
        try:
            start = string.index("pid=")
            end = string.index('&')
            return string[start+4:end]
        except:
            return ''

    def getReviews(self,reviewURL):
        soup = bs(PhantomSource().getSource(reviewURL))
        p_class = "_3v8VuN"
        try:
            p_no =  int(soup.find('span',{'class':p_class}).span.findAll('span')[3].string)
        except:
            p_no = 0
        if reviewURL[reviewURL.index('?')+1:reviewURL.index('?')+5] != 'page':
            parts = reviewURL.split('?')
        else:
            parts = reviewURL.split('?page=1')
        for i in range(1,p_no+1):
            URL = ('?page='+str(i)).join(parts)
            self.getReviewPerPage(URL)

    def getReviewPerPage(self,reviewURL):
        soup = bs(PhantomSource().getSource(reviewURL))
        box_class = "_3DCdKt"
        heading_class = "_2xg6Ul"
        review_class = "qwjRop"
        heading = [i.string for i in soup.findAll('p',{'class':heading_class})]
        review =  [i.div.div.string for i in soup.findAll('div',{'class':review_class})]
        retval = []
        for i,j in zip(heading,review):
                dic ={}
                dic['heading'] = i
                dic['review'] = j
                retval.append(dic)


if __name__ == "__main__":
        ScrapeFL().getReviews('https://www.flipkart.com/pede-milan-loafers/product-reviews/itmegbum8sytnw9c?page=1&pid=SHOEGBUZBNH4CVEY')
