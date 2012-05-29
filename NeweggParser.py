from BeautifulSoup import BeautifulSoup, SoupStrainer
from webparser import WebParser
class NeweggParser(WebParser):
    def __init__(self, product_class):
        WebParser.__init__(self,"newegg",product_class)
        
    def produce_url(self,product_name):
        return "http://www.newegg.com.cn/Product/ProductSearchAdvanced.aspx?keyWord=" \
                +product_name
            
    def parser(self,page):
        result_list=[]
        links = SoupStrainer('dd', attrs={"class" : "info"})
        product_list = BeautifulSoup(page.content,parseOnlyThese=links)

        for product in product_list:
            search_item ={}
            try:
                product_title_tag = product.find('ul',attrs={"class": "parameter"})
           
                search_item["url"]=product.h3.a['href']
                search_item["name"]=product.h3.a.contents[0].string
            except AttributeError:
                continue
            try:
                product_price_tag = product.find('ul',attrs={"class" : "price"})
                search_item["origin_price"]=product_price_tag.find('del').string
                search_item["current_price"]=product_price_tag.find('strong').string
         
                
            except AttributeError:
                pass
            result_list.append(search_item)

        return result_list
        
if __name__ == '__main__': 
  main()