from selenium.webdriver.support.ui import WebDriverWait
from general_utils_lib import account_creation as AC

driver = AC.initialize_driver() #webdriver.Chrome("/Users/laveeshrohra/Downloads/chromedriver")
driver_wait = WebDriverWait(driver, 5)

def fill_elem_list(name, uname, email, bday):
    element_ids = list()
    element_ids.append({"name" : "FirstName", "value" : name[0], "click" : 0})
    element_ids.append({"name": "LastName", "value": name[1], "click": 0})
    element_ids.append({"name": "GmailAddress", "value": uname, "click": 0})
    element_ids.append({"name": "Passwd", "value": "guru1234", "click": 0})
    element_ids.append({"name": "PasswdAgain", "value": "guru1234", "click": 0})
    element_ids.append({"name": ":0", "value": "6", "click": 0, "set_attr" : ["aria-posinset", 6]})
    element_ids.append({"name": "BirthDay", "value": bday[0], "click": 0})
    element_ids.append({"name": "BirthYear", "value": bday[1], "click": 0})
    element_ids.append({"name": ":d", "value": "2", "click": 0, "set_attr": ["aria-posinset", 2]})
    element_ids.append({"name": "RecoveryPhoneNumber", "value": "4804104100", "click": 0})
    element_ids.append({"name": "RecoveryEmailAddress", "value": email, "click": 0})
    return element_ids


url = "https://www.google.com/accounts/CreateAccount"
assert_page = {"current_val" : "Google Account", "next_page" : "changeEmailToggle"}
element_ids = fill_elem_list(['Guru', "test"], "guruacc01", "laveeshr@yahoo.in", [30, 1993])
submit_el_val = "submitbutton"
AC.fill_form(driver, driver_wait, url, assert_page, element_ids, submit_el_val)
