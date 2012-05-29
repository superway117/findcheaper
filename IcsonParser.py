from BeautifulSoup import BeautifulSoup, SoupStrainer
from webparser import WebParser
class IcsonParser(WebParser):
    def __init__(self, product_class):
        WebParser.__init__(self,"Icson",product_class)
        
    def produce_url(self,product_name):
        return "http://www.icson.com/Items/ItemQuery.aspx?Type=All&Key=" \
                +product_name+"&Cat=0"
            
    def parser(self,page):
        result_list=[]
        links = SoupStrainer('div', attrs={"class" : "fl_page_li"})
        product_list = BeautifulSoup(page.content,parseOnlyThese=links)

        for product in product_list:
            search_item ={}
            try:
                product_title_tag = product.find('a',attrs={"target": "_blank"})
            except AttributeError:
                continue
            try:
                product_name = product_title_tag.contents[0].string
                url =product_title_tag['href']
                search_item["url"]=url.replace("..","http://www.icson.com")
                search_item["name"]=product_name
            except AttributeError:
                continue
            try:
                product_price_tag = product.find('span',attrs={"class" : "color_f60"})
                cur_price= product_price_tag.string
                search_item["current_price"]=cur_price
            except AttributeError:
                pass
            result_list.append(search_item)

        return result_list
        
if __name__ == '__main__': 
  main()