from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, traceback

class constants :
    BY_ID = By.ID
    BY_XPATH = By.XPATH

def exception_print(elem_dets = None):
    print traceback.print_exc()
    if elem_dets:
        print elem_dets

def get_assert_type(type = constants.BY_ID):
    if type == constants.BY_XPATH:
        return constants.BY_XPATH
    else:
        return constants.BY_ID

def check_and_click_el(driver_wait, elem_dets, assert_page, print_excep=False) :
    try:
        search_type = elem_dets["type"] if "type" in elem_dets else constants.BY_ID
        elem = driver_wait.until(
            EC.element_to_be_clickable((search_type, elem_dets["name"]))
        )
        if "click" in elem_dets and elem_dets["click"] == 1:
            elem.click()
            assert_type = get_assert_type(assert_page["type"] if ("type" in assert_page) else constants.BY_ID)
            #print assert_type
            driver_wait.until(
                EC.presence_of_element_located((assert_type, assert_page["name"]))
            )

    except:
        exception_print(elem_dets if not print_excep else print_excep)
        return

def login(login_data, driver, driver_wait):
    log_in = "ctl00_ContentPlaceHolder1_btnLoginAccount_btnLoginAccount_Button"
    login_url = "https://www.guru.com/login.aspx"

    elem_dets = list()
    elem_dets.append({"name" : "ctl00_ContentPlaceHolder1_ucLogin_txtUserName_txtUserName_TextBox", "value" : login_data["username"], "click" : 0})
    elem_dets.append({"name": "ctl00_ContentPlaceHolder1_ucLogin_txtPassword_txtPassword_TextBox", "value": login_data["password"], "click": 0})

    assert_page = {"current_val" : ".//div[@class='headerLogo']", "next_page" : ".//div[@class='headerLogo']", "search_type" : "xpath"}   #
    fill_form(driver, driver_wait, login_url, assert_page, elem_dets, log_in, False)

def logout(driver_wait):
    check_and_click_el(driver_wait, {"name": "e-topnav-signout-in", "click": 1},
                       {"name" : "ctl00_ContentPlaceHolder1_ucLogin_txtUserName_txtUserName_TextBox"})

def initialize_driver():
    return webdriver.Firefox()#Chrome("/Users/laveeshrohra/Downloads/chromedriver")

def initialize_wait(driver):
    return WebDriverWait(driver, 5)

def initialize_tor():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9050)
    return webdriver.Firefox(profile)

def initialize_tor_browser():
    import os
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

    binary = '/Applications/TorBrowser.app/Contents/MacOS/firefox'
    profile = FirefoxProfile("/Users/laveeshrohra/Library/Application Support/TorBrowser-Data/Browser/kv9dcr1l.default")
    if os.path.exists(binary) is False:
        raise ValueError("The binary path to Tor firefox does not exist.")
    firefox_binary = FirefoxBinary(binary)
    return webdriver.Firefox(firefox_binary=firefox_binary, firefox_profile=profile)

def fill_form(driver, driver_wait, url, assert_page, element_ids, submit_el_val, clear_cookies = True):
    if clear_cookies:
        driver.delete_all_cookies()

    if url:
        driver.get(url)

    assert_search_by = get_assert_type()

    if assert_page is not None and "current_val" in assert_page:
        if "search_type" in assert_page and assert_page["search_type"] == "xpath":
            assert_search_by = get_assert_type(constants.BY_XPATH)
            driver_wait.until(
                EC.presence_of_element_located((assert_search_by, assert_page["current_val"]))
            )
        else:
            assert assert_page["current_val"] in driver.title

    if element_ids is None:
        return
    for id in element_ids:

        search_type = get_assert_type(id["type"] if "type" in id else constants.BY_ID)
        element = driver.find_element(search_type, id["name"])

        if id['click'] == 1:
            element.click()
        elif "set_attr" in id and id["set_attr"] is not None :
            element.set_attribute(id["set_attr"][0], id["set_attr"][1])
        elif isinstance(id["value"], list):
            for value in id["value"]:
                value.strip()
                element.clear()
                element.send_keys(value)
                element.send_keys(Keys.TAB)
        else:
            element.clear()
            element.send_keys(id['value'])

    if submit_el_val:
        try:
            submit_el_type = None
            submit_value = submit_el_val
            if isinstance(submit_el_val, dict) :
                submit_el_type = submit_el_val["type"]
                submit_value = submit_el_val["name"]

            submit_type = get_assert_type(submit_el_type if submit_el_type else constants.BY_ID)
            submit_el = driver_wait.until(
                EC.element_to_be_clickable((submit_type, submit_value))
            )
            submit_el.click()
            driver_wait.until(
                EC.presence_of_element_located((assert_search_by, assert_page["next_page"]))
            )
        except:
            exception_print()
            return driver
    return driver


def wait_ip_change(driver):
    from bs4 import BeautifulSoup

    driver.get(url="http://icanhazip.com")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ip = soup.get_text().strip()
    print ip
    while True:
        driver.get(url="http://icanhazip.com")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        if ip != soup.get_text().strip():
            print soup.get_text().strip()
            # diff = datetime.now() - start_time
            # print divmod(diff.days * 86400 + diff.seconds, 60)
            break
    return driver

def verify_emails(driver, driver_wait, creation_range):
    import gmail_read


    activations_links = list()
    activations_links = gmail_read.read_gmail('jdd1234ewwe@gmail.com', 'Guru@1234', creation_range)
    print activations_links

    for i in range(0, len(activations_links)):
        # assert_page = {"current_val": "verified"}
        fill_form(driver, driver_wait, activations_links[i], None, None, None)

def login_as_worker(driver, driver_wait, login_dets={'username':'guru_acc.guruWorker2@mail-filter.com', 'password':'guru1234'}):
    # login_dets["username"] = "guru_acc.guruWorker1@mail-filter.com"
    # login_dets["password"] = "guru1234"
    login(login_dets, driver, driver_wait)
    check_and_click_el(driver_wait, {"name": "ctl00_ContentPlaceHolder1_ucSq_aSkip", "click": 1},
                          {"name": "e-topnav-dash-in"})

def check_file_exists(file_name):
    import os
    from general_utils_lib import read_files

    is_file = os.path.isfile(file_name)
    if is_file:
        data = read_files.read_csv(file_name)
        # with open(file_name, 'r') as of: # result file
        #     reader = csv.reader(of, delimiter=",")
        #     data = list()
        #     for row in reader:
        #         data.append(row)
        return data
    else:
        return None

# wait_ip_change(driver)