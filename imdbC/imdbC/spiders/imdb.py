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
            item = Movie()
            # category_items = response.xpath(
            #     "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div/a[1]"
            # )
            # category_list = []
            # for category in category_items:
            #     category_list.append(
            #         category.xpath(
            #             ".//ul[@class='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap baseAlt']/li[@class='ipc-inline-list__item ipc-chip__text']/text()"
            #         ).get()
            #     )
            # item["category"] = category_list
            # item["category"] = response.xpath("").getall()
            item["date_of_scraping"] = str(date.today())
            item["directors"] = response.xpath(
                "//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/text()"
            ).get()
            item["title"] = response.xpath(
                "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/h1/text()"
            ).get()
            item["rating"] = response.xpath(
                "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]/text()"
            ).get()
            item["realease_year"] = response.xpath(
                "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div/ul/li[1]/span/text()"
            ).get()
            # item["top_cast"] = response.xpath("").getall()
            item["url"] = response.url
            uid = response.url
            item["uid"] = uid[27 : len(uid) - 1]

            meta = dict(item=item)
            print(meta)
