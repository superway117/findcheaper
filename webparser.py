import os 
import urllib2
import logging 

from google.appengine.api import urlfetch

class WebParser:
    def __init__(self, webname,product_class):
        self.product_class = product_class
        self.webname = webname
    
    def produce_url(self,product_name):
        return None
      
    def fetch(self, product_name):
        url = self.produce_url(product_name.strip().encode("gb2312"))
        logging.debug('search %s in %s' % (product_name,self.webname))
        #try three times to fetch html page
        for index in range(0,5):
            try:
                page = urlfetch.fetch(url=url,allow_truncated=True,deadline=10)
                if page.status_code != 200:
                    return None
                return page
            except urlfetch.DownloadError:
                logging.debug('%s catch %s DownloadError %d' % (self.webname,product_name,index))
                if index == 4:
                    return None
    
    def parser(self,page):
        return []
    
    def work(self, product_name):
        page = self.fetch(product_name)
        
        if page != None:
            return self.parser(page)
        else:
            logging.debug('%s fetch failure' % (self.webname))
            return []
        
if __name__ == '__main__': 
  main()
        
