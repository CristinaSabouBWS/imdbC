import scrapy
import re
import json
from imdbC.items import Movie
from datetime import date


class ImdbPySpider(scrapy.Spider):
    name = "imdb.py"
    allowed_domains = ["www.imdb.com"]
    start_urls = [
        "https://www.imdb.com/user/ur24609396/watchlist",
    ]

    def parse(self, response):
        pattern = re.compile(r"[^t]const.{3}tt\d{7}")
        import ipdb

        # ipdb.set_trace()
        arr = re.findall(pattern, response.text)
        arr = [x.replace('"const":"', "https://www.imdb.com/title/") for x in arr]
        for link in arr:
            yield scrapy.Request(url=link, callback=self.parse_movie)

    def parse_movie(self, response):
        movie_items = response.xpath("//*[@id='__next']/main/div/section[1]")
        for item in movie_items:
            # to handdle: special char in names, different page layout: category, year, director or year and director nulll
            item = Movie()
            item["category"] = response.xpath(
                "//div[@class='sc-16ede01-8 hXeKyz sc-910a7330-11 GYbFb']//li[@class='ipc-inline-list__item ipc-chip__text']/text()"
            ).getall()
            item["date_of_scraping"] = str(date.today())
            item["directors"] = response.xpath(
                "//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/text()"
            ).getall()
            item["title"] = response.xpath(
                "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/h1/text()"
            ).get()
            item["rating"] = response.xpath(
                "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]/text()"
            ).get()
            item["realease_year"] = response.xpath(
                "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div/ul/li[1]/span/text()"
            ).get()
            item["top_cast"] = response.xpath("//div[@class='sc-18baf029-7 eVsQmt']//a/text()").getall()
            item["url"] = response.url
            uid = response.url
            item["uid"] = uid[27 : len(uid) - 1]
            yield item
        # in progress
        # pattern = re.compile(r"[^t]const.{3}nm\d{7}")
        # # ipdb.set_trace()
        # arr = re.findall(pattern, response.text)
        # arr = [x.replace('"const":"', "https://www.imdb.com/title/") for x in arr]
        # for link in arr:
        #     yield scrapy.Request(url=link, callback=self.parse_movie)
