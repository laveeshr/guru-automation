# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class GurujobsPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='', host='localhost', db='guru_crawler')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if spider.name == 'getLinks':
            try:
                self.cursor.execute(
                    "REPLACE INTO project_links(PID, PLINK)"
                    " VALUES (%s, %s)", (item['pid'], item['link']))
                self.conn.commit()

            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                pass
            #return item
