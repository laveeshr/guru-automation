import imaplib, email, re, datetime

# def get_activation_link(message):
#     activation_key = re.findall('ActivationCode=[^\"]*', email_message.get_payload())[0]  # ActivationCode=.+?(?=\r)
#     activation_key = re.sub("[(=\r\n)]", '', activation_key)
#     return ("http://www.guru.com/ValidateAccount.aspx?" + activation_key.replace("3D", "=", 1))

def read_gmail(uname, pwd, no_of_links):
    activation_links = list()
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail_uids = list()
    try:
        mail.login(uname, pwd)
        mail.list()
        mail.select("inbox") # connect to inbox.
        # print status
        # if status != "OK":
        #     return
        t_end = datetime.datetime.now() + datetime.timedelta(seconds=10)
        while datetime.datetime.now() < t_end:
            result, search_data = mail.uid("search", None, "(UNSEEN HEADER Subject 'Verify')") # search and return uids instead
            mail_uids = search_data[0].split()
            #print uids
            if len(mail_uids) < no_of_links :
                mail.uid('STORE', ','.join(mail_uids), '-FLAGS', '(\Seen)')
                continue
            for latest_email_uid in mail_uids:
                result, data = mail.uid("fetch", latest_email_uid, '(RFC822)')
                raw_email = data[0][1]
                email_message = email.message_from_string(raw_email)

                if email_message.is_multipart():

                    for payload in email_message.get_payload():
                        print payload.get_payload()
                else:
                    activation_key = re.findall('ActivationCode=[^\"]*', email_message.get_payload())[0]   #ActivationCode=.+?(?=\r)
                    activation_key = re.sub("[(=\r\n)]", '', activation_key)
                    activation_links.append("http://www.guru.com/ValidateAccount.aspx?"+activation_key.replace("3D", "=", 1))

            if len(mail_uids) >= no_of_links : break

    except:
        if(mail_uids):
            mail.uid('STORE', ','.join(mail_uids), '-FLAGS', '(\Seen)')

    return activation_links

# activations_links = read_gmail('jdd1234ewwe@gmail.com', 'Guru@1234', 2)
# print len(activations_links)
# print activations_links