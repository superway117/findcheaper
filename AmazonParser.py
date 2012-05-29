from BeautifulSoup import BeautifulSoup, SoupStrainer
from webparser import WebParser

class AmazonParser(WebParser):
    def __init__(self, product_class):
        WebParser.__init__(self,"Amazon",product_class)
        
    def produce_url(self,product_name):
        if self.product_class == "book":
            return "http://www.amazon.cn/mn/searchApp?ix=sunray&pageletid=headsearch&searchType=&keywords=" \
                +product_name+"&Go.x=0&Go.y=0&searchKind=keyword&bestSaleNum=3"
        else:
            return "http://www.amazon.cn/mn/searchApp?ix=sunray&pageletid=headsearch&searchType=&keywords=" \
                +product_name+"&Go.x=13&Go.y=7&bestSaleNum=0"
            
    def parser(self,page):
        result_list=[]
        links = SoupStrainer('div', attrs={"id" : "product-content"})
        product_list = BeautifulSoup(page.content,parseOnlyThese=links)
        for product in product_list:
            search_item ={}
            try:
                product_title_tag = product.find('div',attrs={"class" : "ProductTitle"})
            except AttributeError:
                continue
            try:
                product_name = product_title_tag.a.string
                search_item["name"]=product_name
            except AttributeError:
                continue
            if self.product_class == "book":
                try:   
                    product_author = product_title_tag.find('span',attrs={"class" : "author"})
                    search_item["author"]=product_author.string.strip()
                except AttributeError:
                    pass
                try:
                    product_company_tag = product.find('div',attrs={"class" : "Company"})
                    search_item["company"]=product_company_tag.span.string.strip()
                except AttributeError:
                    pass
            try:   
                product_url = product_title_tag.a['href']
                search_item["url"]=product_url.strip()
            except AttributeError:
                pass

            try:
                product_price_tag = product.find('div',attrs={"class" : "PriceArea"})
                cur_price_tag = product_price_tag.find('span',attrs={"class" : "OurPrice"})
                cur_price= cur_price_tag.string
                search_item["current_price"]=u"￥"+cur_price
            except AttributeError:
                pass
            try:
                strike_price_tag = product_price_tag.find('strike')
                origin_price = strike_price_tag.string[1:]
                search_item["origin_price"]=u"￥"+origin_price
            except AttributeError:
                pass
            result_list.append(search_item)
        return result_list
        
if __name__ == '__main__': 
  main()