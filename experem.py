import json
from bs4 import BeautifulSoup
import requests
import locale
import re
import pandas as pd
import json
import os
from selenium import webdriver


def documents():
    block_info_title = []
    infos = []
    sec_attrib = []
    font= []
    sv = []
    sec_value = []
    col_data = []
    data = {}
    files_links = {}
    main_directory = 'TEST'
    i = 0
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
                      ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
    link = 'https://zakupki.gov.ru/epz/order/notice/ea20/view/documents.html?regNumber=0124200000623001098'
    req = requests.get(url=link, headers=HEADERS)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    col_sm_12 = soup.find_all(class_='col-sm-12 blockInfo')
    for col in col_sm_12:
        titles = col.find(class_='blockInfo__title').get_text().strip()
        block_info_title.append(titles)

        # try:
        section_value = col.find_all(class_='section__value docName')
        for sec in section_value:
            infos.append(sec.get_text().strip())

            #######################LINKS##########################
        link_of_files = col.find_all(class_='blockFilesTabDocs')
        for lux in link_of_files:

            luxit = lux.find_all('a')

            # try:
            for links in luxit:
                if 'download' in links.get('href'):
                    linkl = links.get('href')
                    titk = links.get('title')
                    files_links[titk] = linkl
            if len(files_links) > 0:
                # if not os.path.exists(main_directory):
                path = os.path.join(main_directory, titles)
                os.makedirs(path)
                for title, url in files_links.items():
                    response = requests.get(url, headers=HEADERS)
                    with open(f'{main_directory}/{titles}/{title}', "wb") as f:
                        f.write(response.content)
                files_links = {}
                # except Exception:
            if len(files_links) > 0:
                # if not os.path.exists(main_directory):
                path = os.path.join(main_directory, titles)
                os.makedirs(path)
                for title, url in files_links.items():
                    response = requests.get(url, headers=HEADERS)
                    with open(f'{main_directory}/{titles}/{title}', "wb") as f:
                        f.write(response.content)
                files_links = {}

                #############################################################

        col_sm = col.find_all(class_='col-sm')
        for col_12 in col_sm:
            sec_values = col_12.find_all(class_='section__value')
            for val in sec_values:
                sec_value.append(val.get_text().strip())
            sec_attributs = col_12.find_all(class_='section__attrib')
            for col_12 in sec_attributs:
                try:
                    sec_attrib.append({sec_value[i]:col_12.get_text().strip().replace('\n', '')})
                    i = i + 1
                except Exception:
                    i = 0
                    sec_attrib.append({sec_value[i]:col_12.get_text().strip().replace('\n', '')})
        front = col.find_all('div', attrs={'style': 'font-size: 14px'})
        if len(front) > 0 :
            for f in front:
                font.append(f.get_text().strip())

        if len(col_sm) == 0:
            perm = col.find(class_='section__title').get_text().strip()
            # font = []
            sec_attrib.append(perm)

        infos.append(sec_attrib)
        infos.append(font)
        data[titles] = infos
        infos = []
        font = []
        sec_value = []
        sec_attrib = []

    return data

    # return block_info_title
def Test_Json():
    with open(f"doc.json", "a", encoding="utf-8") as file:
        json.dump(documents(), file, indent=4, ensure_ascii=False)
Test_Json()