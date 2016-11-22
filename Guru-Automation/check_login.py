def check_login():
    from general_utils_lib import read_files, account_creation as AC

    login_dets = read_files.read_csv("/Users/laveeshrohra/Documents/Workspace/job_RA/guru_accounts.csv")

    driver = AC.initialize_tor()
    driver_wait = AC.initialize_wait(driver)

    for i in range(1, len(login_dets)):
        login = {"username": login_dets[i][0], "password" : login_dets[i][2]}
        AC.login(login, driver, driver_wait)
        AC.check_and_click_el(driver_wait, {"name": "ctl00_ContentPlaceHolder1_ucSq_aSkip", "click": 1},
                              {"name": "e-topnav-dash-in"}, login)
        AC.logout(driver_wait)

        if (i % 4) == 0:
            driver = AC.wait_ip_change(driver)


check_login()
