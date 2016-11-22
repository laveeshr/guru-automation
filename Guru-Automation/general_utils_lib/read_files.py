import csv, traceback, re, general_utils as GU
import codecs

def read_csv(file_name):
    try:
        file_data = list()
        fi = (codecs.open(file_name, "rb+", errors='ignore'))
        reader = csv.reader(fi)
        for row in reader:
            # row = list(row)
            empty_line = 0
            for i in range(0, len(row)):
                if row[i].isspace():
                    empty_line = empty_line + 1
                    continue
                row[i] = re.sub('(' + '|'.join(GU.bad_chars.keys()) + ')', GU.replace_bad_chars, row[i])

            if empty_line == len(row):
                continue

            file_data.append(row)
    except:
        print traceback.print_exc()
        return

    return file_data

def get_numbers(str):
    str = str.replace(",", "")
    return re.findall(r'\d+', str)

def get_names(driver, driver_wait, url, name_el, file_name):
    from bs4 import BeautifulSoup
    import requests

    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"}
    resp = requests.get(url=url, headers=header)
    soup = BeautifulSoup(resp.content, "html.parser")

    soup.find("")
