from general_utils_lib import account_creation as AC
from general_utils_lib import read_files

def get_image_url(gender, race, image_urls):
    key = race[0].lower()+gender[0].lower()
    return image_urls[key] if key in image_urls else None

def post_pic_dom(driver, driver_wait, data, image_urls):
    driver.get("http://www.guru.com/emp/modifyaccount.aspx?tab=1")

    AC.check_and_click_el(driver_wait,
                          {"name": ".//a[@id='chooseProfileImage']/following-sibling::a", "type": AC.constants.BY_XPATH,
                           "click": 1}, {
                              "name": "ctl00_guB_ctl00_ucProfilePicture_txtProfileImgAddress_txtProfileImgAddress_TextBox"})
    AC.check_and_click_el(driver_wait, {"name": "btnUseWebUrl", "click": 1}, {
        "name": "ctl00_guB_ctl00_ucProfilePicture_txtProfileImgAddress_txtProfileImgAddress_TextBox"})

    image_url = get_image_url(data[3], data[4], image_urls)
    if image_url:
        driver.find_element(AC.constants.BY_ID,
                            "ctl00_guB_ctl00_ucProfilePicture_txtProfileImgAddress_txtProfileImgAddress_TextBox").send_keys(
            image_url)

    AC.check_and_click_el(driver_wait,
                          {"name": "ctl00_guB_ctl00_ucProfilePicture_btnUpload_btnUpload_Button", "click": 1},
                          {"name": "ctl00_guB_ctl00_btnsubmit_btnsubmit_Button"})
    AC.check_and_click_el(driver_wait, {"name": "ctl00_guB_ctl00_btnsubmit_btnsubmit_Button", "click": 1},
                          {"name": "ctl00_guB_navigation"})
    return


def post_pic(): #driver, driver_wait, login_dets
    from selenium.webdriver.support.ui import WebDriverWait
    from general_utils_lib import read_files
    from selenium.webdriver.support import expected_conditions as EC
    import random, csv, traceback

    driver = AC.initialize_tor()
    driver_wait = WebDriverWait(driver, 20)

    url = "http://www.guru.com/emp/modifyaccount.aspx"

    image_urls = dict()
    image_urls["wf"] = "https://s14.postimg.org/3znnyktrl/image.jpg"
    image_urls["wm"] = "https://s14.postimg.org/5dqvlozap/image.jpg"
    image_urls["bm"] = "https://s22.postimg.org/v4w2nat81/image.jpg"
    image_urls["bf"] = "https://s21.postimg.org/k4gqkxj4n/image.jpg"
    image_urls["im"] = "https://s18.postimg.org/vgy5qdkkp/image.jpg"
    image_urls["if"] = "https://s22.postimg.org/nd4nhy3c1/image.jpg"
    image_urls["am"] = "https://s21.postimg.org/azwep0vdz/image.jpg"
    image_urls["af"] = "https://s21.postimg.org/8ubm72z3r/image.jpg"

    #Login Module
    file_data = read_files.read_csv("/Users/laveeshrohra/Documents/Workspace/job_RA/guru_accounts.csv")
    login_dets = dict()

    zip = ["90003", "90039", "90095", "90013", "90021"]

    log = open('/Users/laveeshrohra/Documents/Workspace/job_RA/logs.csv', "w+")
    writer = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for i in range(1, len(file_data)):


        data = file_data[i]
        try:
            login_dets["username"] = data[0].strip()  #"guru_acc.guruTest33@mail-filter.com"
            login_dets["password"] = data[2].strip()  #"guru1234"
            AC.login(login_dets, driver, driver_wait)
            AC.check_and_click_el(driver_wait, {"name": "ctl00_ContentPlaceHolder1_ucSq_aSkip", "click": 1},
                                  {"name": "e-topnav-dash-in"})

            driver.get(url)

            city = driver.find_element(AC.constants.BY_ID, "ctl00_guB_ctl00_txtCity_txtCity_TextBox")
            city.clear()
            city.send_keys("Los Angeles")
            driver.find_element(AC.constants.BY_XPATH, "//select[@id='ctl00_guB_ctl00_ddlCountry_ddlCountry_Select']/option[@value='1']").click()
            state = driver_wait.until(
                EC.element_to_be_clickable((AC.constants.BY_XPATH, "//select[@id='ctl00_guB_ctl00_ddlState_ddlState_Select']/option[@value='5']"))
            )
            state.click()

            zip_el = driver.find_element(AC.constants.BY_ID, "ctl00_guB_ctl00_txtPostalCode_txtPostalCode_TextBox")
            zip_el.clear()
            zip_el.send_keys(random.choice(zip))

            AC.check_and_click_el(driver_wait, {"name": "ctl00_guB_ctl00_btnSubmit_btnSubmit_Button", "click": 1},
                                  {"name": "ctl00_guB_navigation"})

            if data[4].strip() is "Unknown" or not data[3].strip():
                continue

            # post_pic_dom(driver, driver_wait, data, image_urls)

            AC.logout(driver_wait)
        except:
            writer.writerow([data[0].strip(), traceback.print_exc()])
            continue

    driver.close()
    log.close()

post_pic()
# file_data = read_files.read_csv("/Users/laveeshrohra/Documents/Workspace/job_RA/guru_accounts.csv")
# print  file_data
# driver = AC.initialize_tor()
# driver_wait = AC.initialize_wait(driver)
# AC.verify_emails(driver, driver_wait, 89)


