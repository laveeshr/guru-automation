# -*- coding: utf-8 -*-
import scrapy, re
from guruJobs.items import linksItem

class GetlinksSpider(scrapy.Spider):
    name = "getLinks"
    #allowed_domains = ["http://www.guru.com/d/jobs/c/web-software-it/"]
    start_urls = (
        'http://www.guru.com/d/jobs/c/web-software-it//',
    )

    def parse(self, response):
        item = linksItem()

        job_links = response.xpath(".//li[@class='serviceItem clearfix']/div[@class='clearfix']/div[@class='serviceHeader clearfix']/h2/a[not(@href='#')]/@href").extract()

        for job_link in job_links:
            job_link = response.urljoin(job_link)
            pid = re.findall("^.*?\/(\d+)&[.]*", job_link)[0]
            item["pid"] = pid
            item["link"] = job_link
            yield item

        next_page = response.xpath(".//ul[@id='ctl00_guB_ulpaginate']/li[last()]/a/@href").extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
