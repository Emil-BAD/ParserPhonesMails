import scrapy
from urllib.parse import urlparse
import re


class SiteSpider(scrapy.Spider):
    name = "site"
    
    def __init__(self, start_url: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not start_url:
            raise ValueError("start_url обязателен")
        
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc] #разбиваем url на части и ограничеваем по домену

    def parse(self, response): 
        emails = [e.replace("mailto:", "") for e in response.css('a[href^="mailto:"]::attr(href)').getall()] #поиск почт в ссылках
        phones = [p.replace("tel:", "") for p in response.css('a[href^="tel:"]::attr(href)').getall()] #поиск телефонов в ссылках
        
        emails += re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text) #поиск почт в тексте через регулярные выражения
        phones += re.findall(r'\+?\d[\d\s\-\(\)]{5,}\d', response.text) #поиск телефонов в тексте через регулярные выражения
        #убираем повторения
        emails = list(set(emails))
        phones = list(set(phones))
        
        yield {
            "url": response.url,
            "emails": emails,
            "phones": phones
            }
        for href in response.css("a::attr(href)").getall(): #разбор переход ссылок домена
            if not href.startswith(("mailto:", "tel:")): #исключение перехода по почтам и телефонам
                yield response.follow(href, callback=self.parse)
