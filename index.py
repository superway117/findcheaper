import os 
import logging 
import wsgiref.handlers 
from google.appengine.ext import webapp 
from google.appengine.ext.webapp import template

from DangdangParser import DangdangParser
from AmazonParser import AmazonParser
from Buy360Parser import Buy360Parser
from IcsonParser import IcsonParser
from NeweggParser import NeweggParser

def doRender(handler, tname='findcheaperbook_result.htm', values={}): 
  temp = os.path.join( 
      os.path.dirname(__file__),  
      'templates/' + tname) 
  if not os.path.isfile(temp): 
    return False 
  
  # Make a copy of the dictionary and add the path 
  newval = dict(values) 
  newval['path'] = tname #handler.request.path 
 
  outstr = template.render(temp, newval) 
  handler.response.out.write(outstr) 
  return True 

class FindCheaperBook(webapp.RequestHandler): 
  def get(self): 
    doRender(self, 'findcheaperbook_result.htm') 
 
  def post(self): 
    product_name = self.request.params["content"]
    if product_name is not None:
       dangdang_parser = DangdangParser("book")
       dangdang_search_list = dangdang_parser.work(product_name)
       
       amazon_parser = AmazonParser("book")
       amazon_search_list = amazon_parser.work(product_name)
       
       doRender(self, 'findcheaperbook_result.htm',{"amazon_search_list":amazon_search_list,"dangdang_search_list":dangdang_search_list}) 
    else:
       self.response.out.write("请输入有效数据") 

class FindCheaperAll(webapp.RequestHandler): 
  def get(self): 
    doRender(self, 'findcheaperall_result.htm') 
 
  def post(self): 
    product_name = self.request.params["content"]
    if product_name is not None:
       dangdang_parser = DangdangParser("all")
       dangdang_search_list = dangdang_parser.work(product_name)
       
       amazon_parser = AmazonParser("all")
       amazon_search_list = amazon_parser.work(product_name)
       
       buy360_parser = Buy360Parser("all")
       buy360_search_list = buy360_parser.work(product_name)
       
       icson_parser = IcsonParser("all")
       icson_search_list = icson_parser.work(product_name)
       
       newegg_parser = NeweggParser("all")
       newegg_search_list = newegg_parser.work(product_name)
       
       doRender(self, 'findcheaperall_result.htm',{"amazon_search_list":amazon_search_list,\
            "dangdang_search_list":dangdang_search_list,\
            "buy360_search_list":buy360_search_list,\
            "icson_search_list":icson_search_list,\
            "newegg_search_list": newegg_search_list,\
            }) 
    else:
       self.response.out.write("请输入有效数据")        
       
class FindCheaperDigital(webapp.RequestHandler):
  def get(self): 
    doRender(self, 'findcheaperdigital_result.htm') 
 
  def post(self): 
    product_name = self.request.params["content"]
    if product_name is not None:
       amazon_parser = AmazonParser("digital")
       amazon_search_list = amazon_parser.work(product_name)
       
       buy360_parser = Buy360Parser("digital")
       buy360_search_list = buy360_parser.work(product_name)
       
       icson_parser = IcsonParser("digital")
       icson_search_list = icson_parser.work(product_name)
       
       newegg_parser = NeweggParser("digital")
       newegg_search_list = newegg_parser.work(product_name)
       
       doRender(self, 'findcheaperdigital_result.htm',{"amazon_search_list":amazon_search_list,\
                    "buy360_search_list":buy360_search_list,\
                    "icson_search_list": icson_search_list,\
                    "newegg_search_list": newegg_search_list,\
                    }) 
    else:
       self.response.out.write("请输入有效数据")        
              
class MainHandler(webapp.RequestHandler): 
 
  def get(self): 
    path = self.request.path 
    if doRender(self,path) :  
      return 
    if doRender(self,'index.htm') :  
      return 
    self.response.out.write('Error - unable to find index.htm') 
 
def main(): 
  urlmap = [
       ('/findcheaperbook', FindCheaperBook),
       ('/findcheaperdigital', FindCheaperDigital),
       ('/findcheaperall', FindCheaperAll),
       ('/.*', MainHandler)]

  application = webapp.WSGIApplication(urlmap,debug=True) 

  wsgiref.handlers.CGIHandler().run(application) 
 
if __name__ == '__main__': 
  main()

