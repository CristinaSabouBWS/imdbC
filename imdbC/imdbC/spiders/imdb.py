import scrapy
import re
import json
from imdbC.items import Movie, Actor, ActorsAndMovies
from datetime import date
import ipdb


class ImdbPySpider(scrapy.Spider):
    name = "imdb.py"
    allowed_domains = ["www.imdb.com", "m.media-amazon.com"]
    start_urls = [
        "https://www.imdb.com/user/ur24609396/watchlist",
    ]

    def parse(self, response):
        pattern = re.compile(r"[^t]const.{3}tt\d{7}")

        arr = re.findall(pattern, response.text)
        arr = [x.replace('"const":"', "https://www.imdb.com/title/") for x in arr]
        for link in arr:
            yield scrapy.Request(url=link, callback=self.parse_movie)

    def parse_movie(self, response):

        # to handdle: special char in names, different page layout: category, year, director or year and director nulll
        movie = Movie()
        movie["genre"] = response.xpath(
            "//div[@class='sc-16ede01-8 hXeKyz sc-910a7330-11 GYbFb']//li[@class='ipc-inline-list__item ipc-chip__text']/text()"
        ).getall()
        if movie["genre"] == []:
            movie["genre"] = "n/a"
        movie["date_of_scraping"] = str(date.today())
        movie["directors"] = response.xpath(
            "//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/text()"
        ).getall()
        movie["title"] = response.xpath(
            "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/h1/text()"
        ).get()
        movie["rating"] = response.xpath(
            "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]/text()"
        ).get()
        movie["realease_year"] = response.xpath(
            "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div/ul/li[1]/span/text()"
        ).get()
        movie["top_cast"] = response.xpath("//div[@class='sc-18baf029-7 eVsQmt']//a/text()").getall()
        movie["url"] = response.url
        uid = response.url
        movie["uid"] = uid[27 : len(uid) - 1]
        movie["image_urls"] = response.xpath(
            "//div[@class='ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img']/img[@class='ipc-image']/@src"
        ).getall()

        yield movie

        pattern = re.compile(r"characters.{1}nm\d{7}")
        arr = re.findall(pattern, response.text)
        url_actor_base = "https://www.imdb.com/name/"
        actor_url_set = set([x.replace("characters/", "") for x in arr])
        for link in actor_url_set:
            yield scrapy.Request(url=url_actor_base + link, callback=self.parse_actor)
            actor_movie = ActorsAndMovies()
            actor_movie["actor_uid"] = link
            actor_movie["movie_uid"] = movie["uid"]
            yield actor_movie

    def parse_actor(self, response):
        actor_items = response.xpath("//*[@id='content-2-wide']")
        for actor in actor_items:
            actor = Actor()
            actor["name"] = response.xpath("//h1/span[@class='itemprop']/text()").get()
            uid = response.url
            actor["uid"] = uid[26 : len(uid) - 1]

            arr = response.xpath("//div[@class='filmo-category-section']/div[contains(@id,'act')]/b/a/@href").getall()
            movie_url_base = "https://www.imdb.com"

            for x in range(0, len(arr)):
                arr[x] = movie_url_base + arr[x]
            actor["filmography_movie_url"] = arr
            actor["filmography_movie_title"] = response.xpath(
                "//div[@class='filmo-category-section']/div[contains(@id,'act')]/b/a/text()"
            ).getall()
            yield actor
