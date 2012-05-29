from BeautifulSoup import BeautifulSoup, SoupStrainer
from webparser import WebParser

class DangdangParser(WebParser):
    def __init__(self, product_class):
        WebParser.__init__(self,"DangDang",product_class)
        
    def produce_url(self,product_name):
        return "http://search.book.dangdang.com/search.aspx?key=" \
            +product_name+"&catalog=01"
            
    def parser(self,page):
        result_list=[]
        links = SoupStrainer('div', attrs={"class" : "list_r_list"})
        product_list = BeautifulSoup(page.content,parseOnlyThese=links,fromEncoding="GB18030")
        for product in product_list:
            search_item ={}
            try:
                product_context = product.find('span',attrs={"class" : "list_r_list_book"})
                product_name = product_context.img['alt']
                search_item["name"]=product_name.strip()
                product_url = "http://search.book.dangdang.com/"+product_context.a['href']
                search_item["url"]=product_url.strip()
            except AttributeError:
                continue
            try:
                product_current_price = product.find('span',attrs={"class" : "red"})
                search_item["current_price"]=product_current_price     
            except AttributeError:
                pass
            try:
                product_origin_price = product.find('span',attrs={"class" : "del"})
                search_item["origin_price"]=product_origin_price     
            except AttributeError:
                pass
            if self.product_class == "book":
                try:
                    product_author = product.find('h4',attrs={"class" : "list_r_list_h4"})
                    search_item["author"]=product_author.a.string 
                except AttributeError:
                    pass
                try:
                    product_company_condition = '出版社'.decode("utf-8")
                    product_company = product.find('a',attrs={"name" : product_company_condition})
                    search_item["company"]=product_company.string 
                except AttributeError:
                    pass    
            result_list.append(search_item)
        return result_list
if __name__ == '__main__': 
  main()