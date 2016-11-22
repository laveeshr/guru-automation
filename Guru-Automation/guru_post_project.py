from general_utils_lib import account_creation as AC
from general_utils_lib import read_files
import time

def get_input_data(login, project_desc):
    input_data = dict()
    login_dets = dict()
    login_dets["username"] = login[0]#"guru_acc.esp_id1@mail-filter.com"
    login_dets["password"] = login[2]#"guru1234"
    input_data["login"] = login_dets
    input_data["data"] = project_desc
    return input_data

def element_list(input_data):
    skills = input_data[3].split(",")
    elem_dets = list()
    elem_dets.append({"name": "ctl00_guB_ucPostProject_txtPT_txtPT_TextBox", "value": input_data[0], "click": 0})
    elem_dets.append({"name": "ctl00_guB_ucPostProject_txtPD_txtPD_TextBox", "value": input_data[1], "click": 0})
    elem_dets.append({"name": ".//p[text()='%s']" %(input_data[2]), "type": AC.constants.BY_XPATH, "click": 1})
    elem_dets.append({"name": "token-input-ctl00_guB_ucPostProject_txtSkills_txtSkills_TextBox", "value" : skills, "click": 0})
    elem_dets.append({"name": "ctl00_guB_ucPostProject_rblLocationType_rblLocationType_RadioButton_0", "click": 1})     #update script incase other cases are selected
    elem_dets.append({"name": "ctl00_guB_ucPostProject_rblBudgetType_rblBudgetType_RadioButton_0", "click": 1})
    #elem_dets.append({"name": "ctl00_guB_ucPostProject_ddlBudget_ddlBudget_Select", "click": 1})
    elem_dets.append({"name": ".//option[text()='%s']" % (input_data[6].strip()), "type": AC.constants.BY_XPATH, "click": 1})
    elem_dets.append({"name": ".// label[contains(text(),'%s')]/preceding-sibling::input" %(input_data[7]), "type": AC.constants.BY_XPATH, "click": 1})
    elem_dets.append({"name": "ctl00_guB_btnPostProject_btnPostProject_Button", "click": 1})
    return elem_dets
    #Append script if case for deadline are given


def post_guru_project():
    import menuPagesParse as Menu
    import random, csv, traceback

    driver = AC.initialize_tor()
    driver_wait = AC.initialize_wait(driver)

    project_desc = Menu.get_project_desc('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc.csv')

    project_details = read_files.read_csv("/Users/laveeshrohra/Documents/Workspace/job_RA/sample_project_posts.csv")[2]

    login_dets = read_files.read_csv("/Users/laveeshrohra/Documents/Workspace/job_RA/guru_accounts.csv")

    titles = ["Web Scraping", "Scrape the website", "Data Extractor", "Extract data from website", "Gather data from site",
              "Data Collector", "Collect all data from website", "Website scraper", "Collection of data", "Extraction of Data",
              "Website scraping", "Scrape the website", "Webpage parsing", "Scraping data from website", "Network page scraper",
              "Collect the data from website", "Script for web scraping", "Extraction of data from Web", "Scrape data from web",
              "Collecting info from website", "Webpage Scraping", "Site scraping", "Web scraping",  "Html scraper",
              "Script for web parsing", "Parsing web page", "Webs scraper", "Internet site scraping", "Scrape data from site"]


    of = open('/Users/laveeshrohra/Documents/Workspace/job_RA/project_details.csv', 'a+')
    writer = csv.writer(of, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    log = open('/Users/laveeshrohra/Documents/Workspace/job_RA/logs.csv', "w+")
    log_writer = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    iterations = 1
    prev_iter = 9*(iterations-1)

    for i in range(prev_iter+1, (iterations*9)+1):    #len(login_dets)

        login = login_dets[i % len(login_dets)] if (i % len(login_dets)) > 0 else login_dets[(i % len(login_dets))+1]

        try:
            project_details[0] = random.choice(titles)
            project_details[1] = project_desc[i-1]    #45+ after every rotation
            input_data = get_input_data(login, project_details)

            AC.login(input_data["login"], driver, driver_wait)
            AC.check_and_click_el(driver_wait, {"name": "ctl00_ContentPlaceHolder1_ucSq_aSkip", "click": 1}, {"name" : "e-topnav-dash-in"})

            #print "logged in"

            AC.check_and_click_el(driver_wait, {"name": "e-topnav-postjob-in", "click": 1}, {"name": "ctl00_guB_ucPostProject_txtPT_txtPT_TextBox"})

            # print "clicked post"
            # time.sleep(5)

            els_data = element_list(input_data["data"])
            submit_btn = {"name": ".//button[text()='Continue']", "type": AC.constants.BY_XPATH}
            assert_page = {"next_page": "Post Project Confirmation"}   #"current_val" : "Post",

            AC.fill_form(driver, driver_wait, None, assert_page, els_data, submit_btn, False)
            AC.check_and_click_el(driver_wait, {"name": ".//a[@href='/d/freelancers/']", "type": AC.constants.BY_XPATH, "click": 1}, {"name": "ctl00_guB_txtKeyWord"})
            AC.logout(driver_wait)

            write_data = list()
            write_data.append(input_data["login"]['username'])
            write_data.extend(project_details)
            writer.writerow(write_data)
            time.sleep(210)

        except:
            log_writer.writerow([login[0], traceback.print_exc()])
            continue
        # if (i % 4) == 0:
        #     driver = AC.wait_ip_change(driver)

    of.close()
    driver.close()
    log.close()

post_guru_project()
#print read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc.csv')[1]