# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import sqlite3
from imdbC.items import Movie, Actor, ActorsAndMovies
import ipdb


class ImdbcPipeline:
    def process_item(self, item, spider):
        return item


class SimpleStoragePipeline:
    def open_spider(self, spider):
        self.movie = open("imdb_movie.json", "w")
        self.actor = open("imdb_actor.json", "w")
        self.actor_movie = open("imdb_actor_movie.json", "w")
        # open 1 file for each type
        # connect to db

    def process_item(self, item, spider):
        # if type of item = Movie insert into movie
        if isinstance(item, Movie):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.movie.write(line)
            return item
        elif isinstance(item, Actor):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.actor.write(line)
            return item
        elif isinstance(item, ActorsAndMovies):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.actor_movie.write(line)
            return item

    def close_spider(self, spider):
        self.movie.close()
        self.actor.close()
        self.actor_movie.close()


# class SqlitePipeline:
#     def open_spider(self, spider):
#         # self.movie = open("imdb_movie.json", "r")
#         # self.actor = open("imdb_actor.json", "r")
#         # self.actor_movie = open("imdb_actor_movie.json", "r")
#         self.con = sqlite3.connect("imdb_db")

#         self.cur = self.con.cursor()
#         # ipdb.set_trace()

#         self.create_actors_table()
#         self.create_movies_table()
#         self.create_movie_actors_table()

#     def create_movies_table(self):
#         self.cur.execute("""DROP TABLE IF EXISTS movies""")

#         self.cur.execute(
#             """CREATE TABLE IF NOT EXISTS movies(
#             genre TEXT,
#             date_of_scraping TEXT,
#             directors TEXT,
#             rating TEXT,
#             realease_year TEXT,
#             title TEXT,
#             top_cast TEXT,
#             url TEXT,
#             uid TEXT PRIMARY KEY
#             )
#         """
#         )

#     def create_actors_table(self):

#         self.cur.execute("""DROP TABLE IF EXISTS actors""")

#         # Create ACTORS table if not exists
#         self.cur.execute(
#             """CREATE TABLE IF NOT EXISTS actors(
#             filmography_movie_url TEXT,
#             filmography_movie_title TEXT,
#             name TEXT,
#             uid TEXT PRIMARY KEY)
#         """
#         )

#     def create_movie_actors_table(self):
#         # Drop MOVIE_ACTORS if exists
#         self.cur.execute("""DROP TABLE IF EXISTS movie_actors""")
#         self.cur.execute(
#             """CREATE TABLE IF NOT EXISTS movie_actors(
#             rec_uid INTEGER PRIMARY KEY,
#             actor_uid TEXT,
#             movie_uid TEXT
#             )
#         """
#         )

#     def process_item(self, item, spider):

#         # self.cur.execute(
#         #     """INSERT INTO movies SELECT
#         #     json_extract(value, '$.genre'),
#         #     json_extract(value, '$.date_of_scraping'),
#         #     json_extract(value, '$.directors'),
#         #     json_extract(value, '$.title'),
#         #     json_extract(value, '$.rating'),
#         #     json_extract(value, '$.realease_year'),
#         #     json_extract(value, '$.top_cast'),
#         #     json_extract(value, '$.url'),
#         #     json_extract(value, '$.uid')
#         #     FROM json_each(readfile('imdb_movie.json'))"""
#         # )

#         # self.movie_file = json.load(open("imdb_movie.json"))
#         # columns = [
#         #     "genre",
#         #     "date_of_scraping",
#         #     "directors",
#         #     "title",
#         #     "rating",
#         #     "realease_year",
#         #     "top_cast",
#         #     "url",
#         #     "uid",
#         # ]
#         # for row in self.movie_file:
#         #     keys = tuple(row[c] for c in columns)
#         #     cursor.execute("""INSERT INTO movies values(?,?,?,?,?,?,?,?,?)""", keys)

#         # if isinstance(item, Movie):
#         #     self.cur.executemany(
#         #         """INSERT INTO movies (genre,date_of_scraping,directors,title,rating,realease_year,top_cast,url,uid) VALUES (?,?,?,?,?,?,?,?,?)""",
#         #         [
#         #             (
#         #                 item["genre"],
#         #                 item["date_of_scraping"],
#         #                 item["directors"],
#         #                 item["title"],
#         #                 item["rating"],
#         #                 item["realease_year"],
#         #                 item["top_cast"],
#         #                 item["url"],
#         #                 item["uid"],
#         #                 # item["image_urls"],
#         #                 # item["images"],
#         #             )
#         #         ],
#         #     )

#         # self.con.commit()

#     def close_spider(self, spider):
#         self.con.close()
