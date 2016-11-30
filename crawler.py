from bs4 import BeautifulSoup
import time
import json
import requests
import re
import html

PAUSE_TIME = 3

# Navigation constants
PRODUCT_PAGE_ID = 'productinfoBody'
PRODUCT_TITLE_TAG = 'h3'
PRODUCT_TITLE_CLASS = 'itemTitle'

# Product details constants
PRODUCT_NAME = "productName"
PRODUCT_IMAGE = 'productImage'
PRODUCT_PRICE = 'productPrices'
PRODUCT_DESCRIPTION = 'productDescription'

#Other constants
DUMP_FILE = 'final_dump.json'

class ShopCrawler:
    def __init__(self):
        self.fp = None
        self.page_counter = 0

    def get_page_carefully(self, url):
        url = html.unescape(url)
        time.sleep(PAUSE_TIME)
        page = requests.get(url)
        return BeautifulSoup(page.text, "lxml")

    def parse_product_page(self, url, fields):
        self.page_counter +=1
        product_dict = {'URL' : url}
        page_parsed = self.get_page_carefully(url)
        for field in fields:
            tag = page_parsed.find(id=field)
            if field == PRODUCT_IMAGE:
                img = tag.find("img")
                if img is None:
                    nos = tag.find("noscript")
                    img = nos.find("img")
                product_dict[field] = img["src"]
            else:
                product_dict[field] = tag.text
        return product_dict

    def parse_listing(self, listing_page, fields):
        product_list = []
        product_headers = listing_page.find_all(PRODUCT_TITLE_TAG, class_=PRODUCT_TITLE_CLASS)
        for header in product_headers:
            link = header.find('a')["href"]
            product = self.parse_product_page(link,fields)
            product_list.append(product)
        return product_list

    def crawl_categories(self,category_page, fields):
        body = category_page.find("body")
        if body

    def crawl(self, fields, dump_file):
        self.fp = open(dump_file,'w')
        page_url = r"http://kustomkrafts.com/shop/index.php?main_page=index&cPath=1_23_24"
        parsed_listing = self.get_page_carefully(page_url)
        product_list = self.parse_listing(parsed_listing, fields)
        json.dump(product_list, self.fp, indent=4)
        self.fp.close()



def main():
    fields = [PRODUCT_NAME, PRODUCT_IMAGE, PRODUCT_PRICE, PRODUCT_DESCRIPTION]
    crawler = ShopCrawler()
    crawler.crawl(fields, DUMP_FILE)


if __name__ == "__main__":
    main()
