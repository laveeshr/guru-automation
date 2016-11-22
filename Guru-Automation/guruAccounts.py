from selenium.webdriver.support.ui import WebDriverWait
from general_utils_lib import account_creation as AC
from general_utils_lib import  general_utils as GU
from general_utils_lib import read_files
import gmail_read, time, csv, itertools, random, traceback

driver = AC.initialize_tor()#_browser()#AC.initialize_driver()
driver_wait = WebDriverWait(driver, 5)

def fill_elem_list(name, email, password):
    element_ids = list()
    #freelancer_dets = ["freelancer", "btnCreateAccountFreelancer_btnCreateAccountFreelancer_Button"]
    element_ids.append({"name" : "employer", "value" : None, "click" : 1}) #freelancer - for working
    element_ids.append({"name" : "ucRegistration_txtFullName_txtFullName_TextBox", "value" : name, "click" : 0})
    element_ids.append({"name": "ucRegistration_txtEmail_txtEmail_TextBox", "value": email, "click": 0})
    element_ids.append({"name": "ucRegistration_txtPassword_txtPassword_TextBox", "value": password, "click": 0})
    return element_ids


def get_names_from_db(creation_range):
    indian_males = read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/names/indian_male.csv')
    indian_females = read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/names/indian_female.csv')
    asian_males = read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/names/asian_male.csv')
    asian_females = read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/names/asian_female.csv')
    white_males = read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/names/white_male.csv')
    white_females = read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/names/white_female.csv')
    black_males = read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/names/black_male.csv')
    black_females = read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/names/black_female.csv')

    races = [indian_males, indian_females, asian_males, asian_females, black_males, black_females, white_males,
             white_females, 'unknown']

    # names = [["Michael Smith", "Male", "White"], ["Lisa Clart", "Female", "White"], ["Josiah Jones", "Male", "Black"], ["Aliyah Bell", "Female", "Black"], ["Rahul Sharma", "Male", "Indian"],
    #          ["Parul Sharma", "Female", "Indian"], ["xyounis " + GU.randomName(True), None, "Unknown"], ["Kaiwei Lee", "Male", "Asian"], ["Aiko Tan", "Female", "Asian"],
    #          ["Brandon Thomas", "Male", "Black"], ["Alyssa Collins", "Female", "Black"], ["Aman Verma", "Male", "Indian"], ["Priya Patel", "Female", "Indian"],
    #          ["ghpoic " + GU.randomName(True), None, "Unknown"], ["Liyong Tang", "Male", "Asian"], ["Kiyoko Tran", "Female", "Asian"], ["Dave Miller", "Male", "White"], ["Jen Ward", "Female", "Asian"],
    #          ["Siddharta Srinivasan", "Male", "Indian"], ["Soundarya Radhakrishnan", "Female", "Indian"], ["zghraqx " + GU.randomName(True), None, "Unknown"],
    #          ["Jianhua Nguyen", "Male", "Asian"], ["Yangfang Song", "Female", "Asian"], ["Robby Brown", "Male", "White"], ["Melissa Gray", "Female", "White"], ["Jordan Harris", "Make", "Black"], ["Jayla Watson", "Female", "Black"],
    #          ["vepsertq " + GU.randomName(True), None, "Unknown"], ["Zhiqiang Lin", "Male", "Asian"], ["Tingting Lo", "Female", "Asian"], ["Jimmy Williamson", "Male", "White"],
    #          ["Sarah West", "Female", "White"], ["Nathan Walker", "Male", "Black"], ["Kayla Reed", "Female", "Black"], ["Abhishek Gupta", "Male", "Indian"], ["Sanjana Chawla", "Female", "Indian"],
    #          ["Wanglei Lu", "Male", "Asian"], ["Guilan Tam", "Female", "Asian"], ["Mat Moore", "Male", "White"], ["Alexandra Graham", "Female", "White"], ["Joshua Greene", "Male", "Black"],
    #          ["Kiara Fox", "Female", "Black"], ["Saiteja Ramakrishna", "Male", "Indian"], ["Radha Kapoor", "Female", "Indian"], ["cleosrp " + GU.randomName(True), None, "Unknown"]]


    names = list()
      # len(names)
    for perm in itertools.permutations(races):
        for race in perm:
            if race is "unknown":
                name = [GU.randomName(True) + " " + GU.randomName(True), None, "Unknown"]
            else:
                name = random.choice(race)
                if name[0] is '' or name[1] is '':
                    continue
                name = [name[0].upper() + " " + name[1].upper(), name[2], name[3]]

            # writer.writerow(name)
            names.append(name)
        if len(names) == creation_range:
            break

of = open('/Users/laveeshrohra/Documents/Workspace/job_RA/guru_accounts.csv', "wb")	#result file
log = open('/Users/laveeshrohra/Documents/Workspace/job_RA/logs.csv', "w+")
writer = csv.writer(of, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
log_writer = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(["Email Id", "Name", "Password", "Gender", "Race"])

creation_range = 45

names = read_files.read_csv("/Users/laveeshrohra/Documents/Workspace/job_RA/names/latest_names.csv")

# print names

for i in range(0,creation_range):
    try:
        email = ["free_lancer." + GU.randomName(False), "@mail-filter.com"] #guru_acc
        full_name = names[i][0] #GU.randomName(True)+" "+GU.randomName(True)
        password ="guru1234"
        url = "https://www.guru.com/registeraccount.aspx"
        assert_page = {"current_val" : "Join Guru", "next_page" : "changeEmailToggle"}
        element_ids = fill_elem_list(full_name, email[0] + str(i + 1) + email[1], password)
        submit_el_val = "btnCreateAccount_btnCreateAccount_Button"
        AC.fill_form(driver, driver_wait, url, assert_page, element_ids, submit_el_val)
        writer.writerow([email[0] + str(i + 1) + email[1], full_name, password, names[i][1], names[i][2]])
        time.sleep(60)
        # if i>0 and (i % 4) == 0:
        #     driver = AC.wait_ip_change(driver)
    except:
        log_writer.writerow([email[0] + str(i + 1) + email[1], traceback.print_exc()])
        continue


time.sleep(5)
AC.verify_emails(driver, driver_wait, creation_range)


driver.close()
of.close()
log.close()