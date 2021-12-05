# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class ExamplaImagePipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("mobile_tb.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""drop table if exists mobile_tb""")
        self.curr.execute(""" create table mobile_tb(
                        title text,
                        price integer,
                        image_urls text,
                        discount varchar
                        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into mobile_tb values (?,?,?,?)""",(
                    item['title'],
                    item['price'],
                    item['image_urls'][0],
                    item['discount']
                    ))
        self.conn.commit()
