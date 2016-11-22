import scrapy, sys
import MySQLdb

sys.path.insert(0, '../')

class guruJobs(scrapy.Spider):
    name = "parse_guru"

    def start_requests(self):
        from general_utils_lib import account_creation as AC
        from selenium.webdriver.support.ui import WebDriverWait

        urls = [
            'http://www.guru.com/d/jobs/pg/9/'
        ]

        driver = AC.initialize_tor()#driver()
        driver_wait = WebDriverWait(driver, 20)

        login_dets = dict()
        AC.login_as_worker(driver, driver_wait, login_dets)

        db = MySQLdb.connect("localhost", "root", "", "guru_crawler")
        cursor = db.cursor()

        meta = {"driver": driver, "driver_wait": driver_wait, "db": db, "cursor": cursor}

        yield scrapy.Request(url=urls[0], callback=self.parse, meta=meta)

    def parse(self, response):
        import get_quotes

        job_links = response.xpath(".//li[@class='serviceItem clearfix']/div[@class='clearfix']/div[@class='serviceHeader clearfix']/h2/a[not(@href='#')]/@href").extract()
        for i in range(0, len(job_links)):
            job_links[i] = response.urljoin(job_links[i])

        driver = response.meta["driver"]
        driver_wait = response.meta["driver_wait"]
        db = response.meta["db"]
        cursor = response.meta["cursor"]

        get_quotes.get_all_data(job_links, driver, driver_wait, cursor, db)


        next_page = response.xpath(".//ul[@id='ctl00_guB_ulpaginate']/li[last()]/a/@href").extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            meta = {"driver" : driver, "driver_wait" : driver_wait, "db" : db, "cursor" : cursor}
            yield scrapy.Request(url=next_page, callback=self.parse, meta=meta)
        else:
            driver.close()
            db.close()

