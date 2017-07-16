from selenium import webdriver

class PhantomSource:
    def getSource(self,URL):
        driver = webdriver.PhantomJS()
        driver.get(URL)
        retval = driver.page_source
        driver.quit()
        return retval
