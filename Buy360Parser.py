from BeautifulSoup import BeautifulSoup, SoupStrainer
from webparser import WebParser

class Buy360Parser(WebParser):
    def __init__(self, product_class):
        WebParser.__init__(self,"360Buy",product_class)
        
    def produce_url(self,product_name):
        return "http://search.360buy.com/Search?keyword=" \
            +product_name
            
    def parser(self,page):
        result_list=[]
        page1=unicode(page.content,'gbk','ignore').encode('utf-8','ignore')
        links = SoupStrainer('div', attrs={"class" : "Product_List_S7"})
        product_list_start = BeautifulSoup(page1,parseOnlyThese=links)
        
        try:
            #product_list_start = soup.find('div',attrs={"class" : "Product_List_S7"})
            product_list = product_list_start.findAll('dl')
        except AttributeError:
            return result_list
        for product in product_list:
            search_item ={}
            try:
                product_title_tag = product.find('dd',attrs={"class" : "p_Name"})
                if product_title_tag.a.string == None:
                    product_name =product_title_tag.a.contents[0].string
                    if product_title_tag.a.font.string != None:
                        product_name+=product_title_tag.a.font.string
                        try:
                            product_name+=product_title_tag.a.contents[2].string
                        except IndexError:
                            continue
                else:
                    product_name =product_title_tag.a.string
                product_url = product_title_tag.a['href']
                search_item["name"]=product_name
                search_item["url"]=product_url.strip()
            except AttributeError:
                continue
            try:
                product_price_tag = product.find('dd',attrs={"class" : "p_Price"})
                search_item["current_price"]=u"￥"+product_price_tag.strong.string[1:]
            except AttributeError:
                pass
            result_list.append(search_item)
        return result_list
        
if __name__ == '__main__': 
  main()