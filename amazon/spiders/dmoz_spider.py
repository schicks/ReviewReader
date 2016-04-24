import scrapy
from scrapy.selector import Selector

import scrapy


class AmazonItem(scrapy.Item):
    review = scrapy.Field()
    help = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()

class DmozSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com", "www.amazon.com"]
    start_urls = [
            #"http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_1?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=1",
            #"http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_2?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=2",
            #"http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_3?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=3",
            #"http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_4?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=4",
            "http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_5?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=5",
            #"http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_6?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=6",
            #"http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_7?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=7",
            #"http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_8?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=8",
            #"http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_9?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=9",
            #"http://www.amazon.com/gp/product-reviews/0743273567/ref=undefined_10?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=01NZGSG23R6S39WZMZ4X&pf_rd_t=101&pf_rd_p=2261201562&pf_rd_i=283155&pageNumber=10",

    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            item=AmazonItem()
            item['review']=response.xpath('//div[@class="a-row review-data"]').extract()
            item['help']=response.xpath('//span[@class="a-size-small a-color-secondary review-votes"]').extract()
            item['date']=response.xpath('//span[@class="a-size-base a-color-secondary review-date"]').extract()
            item['title'] = response.xpath('//a[@class="a-size-base a-link-normal review-title a-color-base a-text-bold"]').extract()

            text_file = open("Output.txt", "w")
            text_file.write(str(item['review']))
            text_file.write(str(item['help']))
            text_file.write(str(item['date']))
            text_file.write(str(item['title']))
            text_file.close()
