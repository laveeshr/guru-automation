import urllib2, json, requests, csv, re, time, sys
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from general_utils_lib import account_creation as AC
from MySQLdb import escape_string
import get_project_links

reload(sys)
sys.setdefaultencoding('utf-8')

def get_time_string(str):
    time = ""
    if "hr" in str :
        time = datetime.today() - timedelta(hours=int(str.replace("hrs", "").replace("hr", "").strip()))
    elif "min" in str :
        time = datetime.today() - timedelta(minutes=int(str.replace("mins", "").replace("min", "").strip()))
    elif "day" in str :
        time = datetime.today() - timedelta(days=int(str.replace("days", "").replace("day", "").strip()))

    if time:
        return time.strftime('%m-%d-%Y %H:%M:%S')
    else :
        return str


def get_date_string(str):
    time = ""
    if "today" in str.lower():
        time = datetime.today()
    elif "tomorrow" in str.lower():
        time = datetime.today() + timedelta(days=1)
    elif "yesterday" in str.lower():
        time = datetime.today() - timedelta(days=1)

    if time :
        return time.strftime("%b %d, %Y")
    else:
        return str

def get_string_from_soup_array(arr):
    val_arr = list()
    for val in arr:
        val_arr.append(val.text.strip())

    return ", ".join(val_arr)

def get_employee_dets(emp_id):
    from general_utils_lib import read_files as RF

    employee_dets = {"emp_url": emp_id}
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"}
    resp = requests.get(url=emp_id, headers=header)

    soup = BeautifulSoup(resp.content, "html.parser")

    location = soup.find("span", {"id": "ucempstats_lblLocation"}).text
    member_since = datetime.strptime(soup.find("span", {"id" : "ucempstats_lblMemberSince"}).text, "%d-%b-%Y").strftime('%m-%d-%Y %H:%M:%S')
    spent = soup.find("span", {"id" : "ucempstats_lblDollarsSpent"}).text
    feedback = soup.find("span", {"id" : "ucempstats_lblFeedbackImg"}).find("img")
    feedback = get_ratings_from_img(feedback.get("src")) if feedback else "No Feedback"
    jobs_posted = soup.find("span", {"id" : "ucempstats_lblProjectsPosted"}).text
    jobs_paid = soup.find("span", {"id" : "ucempstats_lblProjectsPaid"}).text
    jobs_paid_percent = jobs_paid.split(" [")[1].replace("]", "")
    jobs_paid = jobs_paid.split(" [")[0]
    invoices_paid = soup.find("span", {"id" : "ucempstats_lblInvoicesPaid"}).text
    if len(invoices_paid.split(" [")) > 1:
        invoices_paid_percent = invoices_paid.split(" [")[1].replace("]", "")
    else:
        invoices_paid_percent = 0
    invoices_paid = invoices_paid.split(" [")[0]
    invoices_out = soup.find("span", {"id" : "ucempstats_lblInvoicesOutstanding"}).text
    avg_lag = soup.find("span", {"id" : "ucempstats_lblAvgPayTimeLag"}).text

    employee_dets["location"] = location
    employee_dets["member_since"] = member_since
    employee_dets["budget_spent"] = RF.get_numbers(spent)[0]
    employee_dets["feedback"] = feedback
    employee_dets["jobs_posted"] = jobs_posted
    employee_dets["jobs_paid"] = jobs_paid
    employee_dets["jobs_paid_percent"] = RF.get_numbers(jobs_paid_percent)[0]
    employee_dets["invoices_paid"] = invoices_paid
    employee_dets["invoices_paid_percent"] = RF.get_numbers(str(invoices_paid_percent))[0]
    employee_dets["invoices_out"] = invoices_out
    employee_dets["avg_pag_lag"] = RF.get_numbers(avg_lag)[0]

    return employee_dets

def get_project_details(soup):
    from general_utils_lib import read_files as RF

    get_date = lambda date: datetime.strptime(date, "%Y-%m-%d-%H-%M-%S").strftime('%m-%d-%Y %H:%M:%S')
    project_dets = dict()

    project_dets["title"] = escape_string(soup.find("h1", {"id": "ctl00_guB_hTitleAndAddtoWatchSec"}).text.strip())
    project_dets["quotes"] = soup.find("span", {"id" : "snpProposalCount"}).text.strip()
    project_dets["budget"] = escape_string(get_string_from_soup_array(soup.find("div", {"class": "budget"}).find_all("li")))
    project_dets["exposure"] = escape_string(get_string_from_soup_array(soup.find("div", {"class": "exposure"}).find_all("li")))
    project_dets["skills"] = escape_string(get_string_from_soup_array(soup.find('ul', {"id" : "ctl00_guB_ucProjectDetail_ulSkills"}).find_all("li")))
    project_dets["job_desc"] = escape_string(soup.find("section", {"class" : "section_desc jobDetail-section"}).find("pre").text.strip())
    project_dets["submit_date"] = get_date(soup.find("span", {"class" : "dt-style1"}).get("data-date"))
    project_dets["expiry_date"] = get_date(soup.find("span", {"class" : "dt-style6"}).get("data-date"))
    project_dets["img"] = escape_string(soup.find("div", {"id" : "ctl00_guB_dvEmployerImage"}).find("img").get("src"))
    project_dets["default_img"] = (project_dets["img"] == "https://img-guru.com/images/defaultemp.png")

    return project_dets




def get_and_set_quotes(url, pid, driver, driver_wait, cursor, db):
    from general_utils_lib import read_files as RF

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    project_details = get_project_details(soup)

    emp_id = soup.find("section", {"id": "empStats"}).find_all("a")[0].get("href").replace("javascript:feedback_popup('","http://www.guru.com").replace("')", "")
    employee_dets = get_employee_dets(emp_id)
    emp_name = soup.find("h3", {"class" : "identityName"}).find("a").text
    employee_dets["name"] = emp_name

    if int(project_details["quotes"]) <= 0:
        return {"employer" : employee_dets, "project" : project_details}

    assert_page = {"name": ".//ul[@id='modalApplicants']/li[1]", "type": AC.constants.BY_XPATH}
    elem_dets = {"name": "anchrTotalProposalHeader", "click": 1}
    AC.check_and_click_el(driver_wait, elem_dets, assert_page)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    quotes_modal = soup.find_all("ul", {"id" : "modalApplicants"})[0]

    fl_hired = soup.find("span", {"id" : "spnMAwardedCount"}).text.strip()
    hired_fls = list()
    if int(fl_hired) > 0:

        assert_page = {"name": ".//ul[@id='modalApplicants']/li[1]", "type": AC.constants.BY_XPATH}
        elem_dets = {"name": "liAwardedProposal", "click": 1}
        AC.check_and_click_el(driver_wait, elem_dets, assert_page)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        hired_modal = soup.find_all("ul", {"id" : "modalApplicants"})[0]
        for hired in hired_modal.find_all("li", {"class" : "clearfix"}):
            fl_link = hired.find("strong").find("a").get("href")
            hired_fls.append(fl_link)

    get_feedback = lambda feedback, prop: feedback[prop] if prop in feedback else "No Feedback"

    for item in quotes_modal.find_all("li", {"class" : "clearfix"}):

        fl_name = item.find("strong").find("a")
        fl_link = escape_string(fl_name.get("href"))
        fl_hired = "Yes" if (fl_link in hired_fls) else "No"
        fl_data = item.find_all("p", {"class": "subtext"})
        fl_loc_bud = fl_data[0].span.previous_sibling.strip()
        fl_loc = fl_loc_bud.split("-")[0].strip()
        fl_loc_country = escape_string(fl_loc.split(",")[-1].strip())
        fl_loc_city = escape_string(fl_loc.replace(fl_loc_country, "").strip().strip(","))
        fl_bud = RF.get_numbers(escape_string(fl_loc_bud.split("-")[-1].replace("(year)", "").strip()))[0]
        fl_feedback = item.find("img", {"title": "Feedback Rating"})
        fl_ratings = get_ratings_from_img(fl_feedback.get("src")) if fl_feedback else "No Feedback"
        fl_misc = escape_string(fl_data[1].text.strip())
        fl_submit = item.find("div", {"class": "dt-style1"}).span.get("title").replace("p.m.", "pm").replace("a.m.", "am")
        fl_date = datetime.strptime(fl_submit, "%b %d, %Y at %H:%M %p").strftime('%m-%d-%Y %H:%M:%S')
        fl_skills_and_stars = {"skills": "No Feedback", "stars": "No Feedback"}
        if fl_feedback:
            fl_skills_and_stars = get_skills_and_stars(fl_link + "/reviews", driver)

        query = ("INSERT INTO quotes_table VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
         %(pid, escape_string(fl_name.text), fl_hired, fl_link, fl_loc_city, fl_loc_country, fl_bud, fl_ratings, fl_date, fl_misc, get_feedback(fl_skills_and_stars["skills"],"Technical"),
                         get_feedback(fl_skills_and_stars["skills"],"Timeliness"), get_feedback(fl_skills_and_stars["skills"],"Creativity"),
                         get_feedback(fl_skills_and_stars["skills"],"Communication"), get_feedback(fl_skills_and_stars["stars"],"5 stars"),
                         get_feedback(fl_skills_and_stars["stars"],"4 stars"), get_feedback(fl_skills_and_stars["stars"],"3 stars"),
                         get_feedback(fl_skills_and_stars["stars"],"2 stars"), datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S')))

        execute_query(db, cursor, query)

    return {"employer" : employee_dets, "project" : project_details}


def get_skills_and_stars(url, driver):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    skill_list = fetch_skill_star_data(soup, "bar1List")
    star_list = fetch_skill_star_data(soup, "bar2List")
    return {"skills" : (skill_list), "stars" : (star_list)}


def fetch_skill_star_data(soup, id):
    skills = soup.find("ul", {"id": id})
    #print skills.find_all("li")
    if not skills:
        return "No Feedback"
    skill_list = dict()
    for skill in skills.find_all("li"):
        skill_name = skill.find("div", {"class": "name"}).text.strip()
        skill_score = skill.find("div", {"class": "score"}).text
        skill_list[skill_name] = skill_score
    return skill_list


def get_ratings_from_img(src):
    return re.findall("x_(\d+)", src)[0]

def post_data():
    url = "http://www.guru.com/jobs/ghostwriter-for-small-book-175-/1289958&ItemNo=1&SearchUrl=search.aspx"
    post_url = "http://www.guru.com/pro/JobDetail.aspx/GetJsonForApplicant_ProposalDetails"

    s = requests.session()
    s.get(url)
    resp = s.post(post_url, params={"projectId" : "1289958"})
    print resp.text.encode("utf-8").json()

def get_api_resp(url):
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    return data["extractorData"]["data"][0]["group"]

def get_project_data(project_urls, driver, driver_wait, cursor, db):
    import traceback

    data = project_urls

    for p_link in data:
        pid = re.findall("^.*?\/(\d+)&[.]*", p_link)[0]
        try:
            job_data = get_and_set_quotes(p_link, pid, driver, driver_wait, cursor, db)
            employer_dets = job_data["employer"]
            project_dets = job_data["project"]

            query = ("INSERT INTO project_dets VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                     %(pid, escape_string(p_link), project_dets["title"], project_dets["skills"], project_dets["submit_date"],
                             project_dets["expiry_date"], project_dets["quotes"], project_dets["job_desc"],
                             project_dets["budget"], project_dets["exposure"], employer_dets["name"], employer_dets["emp_url"],
                             employer_dets["location"], employer_dets["budget_spent"], employer_dets["feedback"],
                             employer_dets["member_since"], employer_dets["jobs_posted"], employer_dets["jobs_paid"], employer_dets["jobs_paid_percent"],
                             employer_dets["invoices_paid"], employer_dets["invoices_paid_percent"], employer_dets["invoices_out"], employer_dets["avg_pag_lag"],
                             project_dets["img"], project_dets["default_img"], datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S')))

            execute_query(db, cursor, query)

        except:

            query = "INSERT INTO error_links VALUES ('%s', '%s')" % (p_link, traceback.print_exc())
            execute_query(db, cursor, query)
            continue


def execute_query(db, cursor, query):
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print query
        time.sleep(10)


def get_all_data(project_urls, driver, driver_wait, cursor, db):
    return get_project_data(project_urls, driver, driver_wait, cursor, db)



#print get_skills_and_stars("http://www.guru.com/freelancers/intelex-informatics/reviews")
import MySQLdb, os
driver = AC.initialize_tor()
driver_wait = WebDriverWait(driver, 5)
db = MySQLdb.connect("localhost", "root", "", "guru_crawler")
cursor = db.cursor()
file_name = '/Users/laveeshrohra/Documents/Workspace/job_RA/new_project_desc.csv'

links = get_project_links.get_all_links(driver, driver_wait, file_name)
AC.login_as_worker(driver, driver_wait)
get_all_data(links, driver, driver_wait, cursor, db)
os.remove(file_name)
driver.close()

#check_json_resp()