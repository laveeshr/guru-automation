# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class linksItem(scrapy.Item):
    #define the fields for collecting links
    pid = scrapy.Field()
    link = scrapy.Field()

class GurujobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    p_link = scrapy.Field()
    p_title = scrapy.Field()
    p_skills = scrapy.Field()
    p_date = scrapy.Field()
    p_expiry = scrapy.Field()
    p_quotes = scrapy.Field()
    p_desc = scrapy.Field()
    p_budget = scrapy.Field()
    p_exposure = scrapy.Field()
    p_employer = scrapy.Field()
    emp_link = scrapy.Field()
    emp_country = scrapy.Field()
    emp_budget = scrapy.Field()
    emp_feedback = scrapy.Field()
    emp_date = scrapy.Field()
    emp_jobs = scrapy.Field()
    emp_paid = scrapy.Field()
    emp_paid_percent = scrapy.Field()
    emp_invoices = scrapy.Field()
    emp_invoices_percent = scrapy.Field()
    emp_invoices_out = scrapy.Field()
    emp_lag = scrapy.Field()
    emp_img = scrapy.Field()
    p_time = scrapy.Field()
    pass

    # ["Project ID", "Project Link", "Project Title", "Skills", "Posted Date", "Expiry Date", "Quotes", "Description",
    #  "Budget", "Exposure",
    #  "Employer", "Employer URL", "Country", "Budget Spend", "Employer Feedback (out of 10)", "Member Since",
    #  "Jobs Posted", "Jobs Paid",
    #  "Jobs Percent Paid", "Invoices Paid", "Invoice Percent Paid", "Invoices Outstanding", "Average Pay Time Lag",
    #  "Image URL", "Project Updated Time"]

class QuotesItem(scrapy.Item):

    pid = scrapy.Field()
    fl_name = scrapy.Field()
    fl_hired = scrapy.Field()
    fl_link = scrapy.Field()
    fl_city = scrapy.Field()
    fl_country = scrapy.Field()
    fl_budget = scrapy.Field()
    fl_feedback = scrapy.Field()
    fl_date = scrapy.Field()
    fl_data = scrapy.Field()
    fl_skill_tech = scrapy.Field()
    fl_skill_time = scrapy.Field()
    fl_skill_creative = scrapy.Field()
    fl_skill_comm = scrapy.Field()
    fl_star_5 = scrapy.Field()
    fl_star_4 = scrapy.Field()
    fl_star_3 = scrapy.Field()
    fl_star_2 = scrapy.Field()
    fl_time = scrapy.Field()
    pass

    # ["Project ID", "Freelancer", "Hired", "Freelancer URL", "Location City", "Location Country", "Budget (year)",
    #  "Feedback", "Bid submit date", "Misc Data",
    #  "Skill Ratings- Technical", "Skill Ratings- Timeliness", "Skill Ratings- Creativity",
    #  "Skill Ratings- Communication", "Star Ratings - 5 stars",
    #  "Star Ratings - 4 stars", "Star Ratings - 3 stars", "Star Ratings - 2 stars", "Quotes Updated Time"]
