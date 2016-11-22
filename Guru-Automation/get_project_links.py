from general_utils_lib import account_creation as AC
from general_utils_lib import read_files

def get_all_links(driver, driver_wait, file_name):
    import csv, traceback

    links = list()

    data_exists = AC.check_file_exists(file_name)
    if data_exists:
        for data in data_exists:
            links.append(data[1])
        return links

    login_dets = read_files.read_csv("/Users/laveeshrohra/Documents/Workspace/job_RA/guru_accounts.csv")

    of = open(file_name, 'w+')
    writer = csv.writer(of, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(["User ID", "Project Link", "Approved"])

    log = open('/Users/laveeshrohra/Documents/Workspace/job_RA/logs.csv', "w+")
    log_writer = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


    for i in range(1, len(login_dets)):
        login = dict()
        login["username"] = login_dets[i][0]#"guru_acc.guruTest33@mail-filter.com"
        login["password"] = login_dets[i][2]#"guru1234"

        try:
            project_dets = get_project_links(login, driver, driver_wait)
            # print project_dets

            for link in project_dets:
                writer.writerow([login["username"], link, project_dets[link]])
                links.append(link)

        except:
            writer.writerow([login["username"], "Unable to connect to account"])
            log_writer.writerow([login["username"]])
            continue

        #break
        #links.extend(get_project_links(login, driver, driver_wait))

    of.close()
    log.close()
    return links

def get_project_links(login_dets, driver, driver_wait):

    import re
    from bs4 import BeautifulSoup

    #driver_wait = AC.initialize_wait(driver)

    # login_dets = dict()
    # login_dets["username"] = "guru_acc.guruTest33@mail-filter.com"
    # login_dets["password"] = "guru1234"

    links = dict()

    AC.login(login_dets, driver, driver_wait)
    AC.check_and_click_el(driver_wait, {"name": "ctl00_ContentPlaceHolder1_ucSq_aSkip", "click": 1},
                          {"name": "e-topnav-dash-in"})

    soup = BeautifulSoup(driver.page_source, "html.parser")

    link_elems = soup.find("ul",{'id', 'hireList'}).find_all("li")

    #print link_elems

    for elem in link_elems:
        #print elem
        link_elem = elem.find("h3").find("a")
        el_id = re.findall("/[0-9]+/", link_elem.get("href"))[0].replace("/", "")
        title = link_elem.text
        approved = elem.find("span", {"class": "pending"})
        approved = "No" if approved else "Yes"

        links['http://www.guru.com/jobs/'+title.replace(' ','-')+"/"+el_id+"&ItemNo=1&SearchUrl=search.aspx"] = approved

    AC.logout(driver_wait)

    return links



# driver = AC.initialize_tor()
# driver_wait = AC.initialize_wait(driver)
# AC.verify_emails(driver, driver_wait, 45)
# print get_all_links(driver, driver_wait)