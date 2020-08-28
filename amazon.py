# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Request
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    #start_urls = ['http://amazon.com/']
    def start_requests(self):
        self.driver = webdriver.Chrome('F:/chromedriver')
        self.driver.get('http://amazon.com/')
        self.driver.maximize_window()

        amazonkeyword=input("Enter Search Keyword: ")

        Search=self.driver.find_element_by_xpath('//*[@type="text"]').send_keys(amazonkeyword,'\ue007')

        response = Selector(text=self.driver.page_source)
        URLs = response.xpath('//*[@class="a-link-normal a-text-normal"]//@href').extract()
        for Url in URLs:
            absolute_URL="https://www.amazon.com"+Url
            yield Request(absolute_URL, callback=self.parse_products, meta={'Link':absolute_URL})

        while True:
            try:
                print("---------------------------------------------Next Page---------------------------------------------")
                #response = Selector(text=self.driver.page_source)
                next=self.driver.find_element_by_xpath('//*[@class="a-last"]')
                sleep(5)
                next.click()
                sleep(5)
            
                response = Selector(text=self.driver.page_source)
                URLs = response.xpath('//*[@class="a-link-normal a-text-normal"]//@href').extract()
                for Url in URLs:
                    absolute_URL="https://www.amazon.com"+Url
                    yield Request(absolute_URL, callback=self.parse_products, meta={'Link':absolute_URL})

            except NoSuchElementException:
                print('No more pages to load.')
                self.driver.quit()

    def parse_products(self,response):
        Brand_Name=response.xpath('//*[@id="bylineInfo"]//text()').extract_first().strip()
        Product_Title=response.xpath('//span[@id="productTitle"]//text()').extract_first().strip()
        Product_Price=response.xpath('//*[@id="priceblock_ourprice"]//text()').extract_first()
        Rating=response.xpath('//*[@class="a-icon a-icon-star a-star-4-5"]//text()').extract_first()
        Number_of_ratings=response. xpath('//*[@id="acrCustomerReviewText"]//text()').extract_first()
        Qty_Flavor=response.xpath('//*[@type="button"]//*[@class="a-size-base"]//text()').extract()
        absolute_URL = response.meta['Link']
        #Serve_style=response.xpath().extract()


        yield{'Brand_Name':Brand_Name,
            'Product_Title':Product_Title,
            'Product_Price':Product_Price,
            'Rating':Rating,
            'Number_of_ratings':Number_of_ratings,
            'Qty/Flavor':Qty_Flavor,
            'Link':absolute_URL}
