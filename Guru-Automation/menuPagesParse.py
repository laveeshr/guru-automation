from general_utils_lib import account_creation as AC

def get_menupages_data(url):

    import requests, csv, os.path
    from bs4 import BeautifulSoup

    is_file = os.path.isfile('/Users/laveeshrohra/Documents/Workspace/job_RA/menu_pages.csv')

    urls = []
    if is_file:
        with open('/Users/laveeshrohra/Documents/Workspace/job_RA/menu_pages.csv', 'r') as of: # result file
            reader = csv.reader(of, delimiter=",")
            for row in reader:
                urls.append(url + row[0])
    else:
        of = open('/Users/laveeshrohra/Documents/Workspace/job_RA/menu_pages.csv', 'w')  # result file
        writer = csv.writer(of, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        header = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"}
        resp = requests.get(url=url, headers=header)
        soup = BeautifulSoup(resp.content, "html.parser")
        content = soup.find("div", {"id" : "list-by-cuisine"})
        count = 0
        for list in content.find_all("li"):
            link = list.find('a').get("href")
            writer.writerow([link])
            urls.append(requests.compat.urljoin(url, link))
            count += 1
            if count > 22:
                break

    of.close()
    return urls


def get_menupages_url():
    from general_utils_lib import read_files
    return read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_addr.csv')

def get_project_desc(file_name):
    import csv, random
    from general_utils_lib import read_files

    final_desc = list()

    data_exists = AC.check_file_exists(file_name)
    if data_exists:
        for data in data_exists:
            final_desc.append(data[0])
        return final_desc

    of = open(file_name, 'w+')
    writer = csv.writer(of, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    proj_sen_1a = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence1.csv'), "random": True}
    proj_sen_1b = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence1b.csv'), "random": True}
    proj_sen_2 = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence2.csv'), "random": True}
    proj_sen_3 = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence3.csv'), "random": True}
    proj_sen_4a = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence4.csv'), "pick": 1}
    proj_sen_4b = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence4b.csv'), "random": True}
    proj_sen_5a = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence5.csv'), "pick": 1}
    proj_sen_5b = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence5b.csv'), "random": True}
    proj_sen_6a = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence6.csv'), "pick": 1}
    proj_sen_6b = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence6b.csv'), "random": True}
    proj_sen_7a = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence7.csv'), "pick": 1}
    proj_sen_7b = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence7b.csv'), "random": True}
    proj_sen_8a = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence8.csv'), "pick": 1}
    proj_sen_8b = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence8b.csv'), "random": True}
    proj_sen_9a = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence9.csv'), "pick": 1}
    proj_sen_9b = {"data": read_files.read_csv('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc/sentence9b.csv'), "random": True}

    sent = [[proj_sen_1a, proj_sen_1b],
            [proj_sen_2],
            [proj_sen_3],
            [proj_sen_4a, proj_sen_4b],
            [proj_sen_5a, proj_sen_5b],
            [proj_sen_6a, proj_sen_6b],
            [proj_sen_7a, proj_sen_7b],
            [proj_sen_8a, proj_sen_8b],
            [proj_sen_9a, proj_sen_9b]]

    groups = 15

    for i in range(0, groups):
        sent_group = sent#random.sample(sent, len(sent))
        for sentence in sent_group:
            desc = ""
            for part in sentence:
                data = part["data"]
                if 'random' in part and part["random"]:
                    d = random.sample(data, len(data))
                    desc = desc + "\n".join(v[0] if v else '' for v in d) + "\n"
                elif 'pick' in part and part["pick"] > 0:
                    d = random.choice(data)
                    print d
                    desc = desc + d[0] + "\n"
            final_desc.append(desc)
            writer.writerow([desc])
    # proj_sen_1 = [
    #     "Freelancer is required to scrape and collate specified product information from a list of predetermined websites.",
    #     "Freelancer is required to collect specified product data from a list of public websites.",
    #     "The bidder is required to obtain some product data from a set of public websites predetermined by me.",
    #     "The contractor is asked to collect some public data from several websites predetermined by me.",
    #     "I need a freelancer to collate specified product information from some public websites.",
    #     "Need to hire someone to help to scrape specified product information from a couple of predetermined websites.",
    #     "Need to find a freelancer develop script to parse some specified product information from a couple of predetermined websites.",
    #     "Want to find a contractor to develop script to parse some specified product information from a group of websites.",
    #     "Need a freelancer to help to parse a lot of specified product information from several websites predetermined by me.",
    #     "Finding a contractor to generate script to parse some specified product information from a group of websites.",
    #     "Require a freelancer to parse some websites to collect some specified product information."]


    # for i in range(0, 135):
    #
    #
    #     group_sent = sentences[int(i/9)]
    #
    #     #print group_sent[4]
    #
    #     final_sent = random.choice(group_sent[0])[0] + "\n"
    #     final_sent = final_sent + random.choice(group_sent[1])[0] + "\n"
    #     final_sent = final_sent + random.choice(group_sent[2])[0] + "\n"
    #     final_sent = final_sent + random.choice(group_sent[3])[0] + "\n"
    #     final_sent = final_sent + 'Approximate details of the project are : ' + "\n"
    #     final_sent = final_sent + "\n".join(str(v[0]) for v in random.sample(group_sent[4], 4)) + "\n"
    #
    #     writer.writerow([final_sent])
    #     final_desc.append(final_sent)

    # for c_url in urls:
    #     city_url = c_url[0]
    #     city_url = get_menupages_data(city_url)
    #     for url in city_url:
    #         desc[0].append(url) if isinstance(desc[0], list) else desc[1].append(url)
    #         desc_new = [" ".join(desc[0]), desc[1]]
    #         shuffle(desc_new)
    #         shuffle(desc_list)
    #         writer.writerow(["\n".join(desc_new), "\n".join(desc_list)])
    #         final_desc.append("\n".join(desc_new) + "\n" + "\n".join(desc_list))
    #         desc[0].remove(url) if isinstance(desc[0], list) else desc[1].remove(url)

    of.close()
    return final_desc

print (get_project_desc('/Users/laveeshrohra/Documents/Workspace/job_RA/project_desc.csv'))