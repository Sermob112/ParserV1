from bs4 import BeautifulSoup
import requests
import urllib3
import locale
import re
import pandas as pd
import json
import os
from selenium import webdriver

#['Дата и время формирования результатов определения поставщика (подрядчика, исполнителя)', 'Наименование протокола определения поставщика (подрядчика, исполнителя)', 'Заказчик(и), с которыми планируется заключить контракт', 'Основание признания торгов несостоявшимися']
#['Дата и время формирования результатов определения поставщика (подрядчика, исполнителя)', 'Заказчик(и), с которыми планируется заключить контракт', 'Наименование протокола определения поставщика (подрядчика, исполнителя)', 'Участники, с которыми планируется заключить контракт']
files_links = {}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
                  ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
link = 'https://zakupki.gov.ru/epz/order/notice/ok20/view/supplier-results.html?regNumber=0172500000423000006'

req = requests.get(url=link, headers=HEADERS)
src = req.text
soup = BeautifulSoup(src, "lxml")
def main_info_body(soup = soup):
    block_title = []
    title_data= []
    value_data = []
    list_info= []
    all_table_info = []
    data_td = []
    new_dict = {}
    i = 0
    n = 0
    row_info = soup.find_all(class_= 'row blockInfo')
    for info in row_info:
        title_cap = info.find(class_='blockInfo__title').get_text().strip()
        block_title.append(title_cap)
        col_9 = info.find_all(class_='blockInfo__section')
        for col in col_9:
            try:
                td_text = info.find('td',class_='tableBlock__col').get_text().strip()
            except Exception:
                value_text = 'None'
                title_text = 'None'
            block_section = info.find_all('section', class_="blockInfo__section section")
            for inf in block_section:
                try:
                    title_text = inf.find_all(class_='section__title')
                    for tit in title_text:
                        title_data.append(tit.get_text().strip())
                    title_value = inf.find_all(class_='section__info')
                    for val in title_value:
                        value_data.append(val.get_text().strip())
                except Exception:
                    value_text = 'None'
                    title_texts = 'None'
                table = info.find_all(class_='blockInfo__table tableBlock')
                if table != None:
                    for tables in table:
                        # table = info.find(class_='blockInfo__table tableBlock')
                        hiegth_row = tables.find_all('th')
                        table_td = tables.find_all('td')

                        for i in hiegth_row:
                            column_name = i.text.strip()
                            all_table_info.append(column_name)

                        for i in table_td:
                            td = i.get_text().strip()
                            if (td == ''):
                                continue
                            if '\n' in td:
                                td = td.replace('\n', '')  # remove non-breaking spaces
                                td = re.findall('[A-ZА-Я][^A-ZА-Я]*', td)
                            if '\xa0' in td:
                                td = td.replace('\xa0', '').replace(',', '.')  # remove non-breaking spaces

                            data_td.append(td)
                            try:
                                list_info.append({all_table_info[n]: td})
                            except IndexError:
                                # continue

                                list_info.append({all_table_info[n]: td})
                            n = n + 1
                new_dict[title_cap] = list_info
                list_info = []

                    # list_info.append({title_text: values_texts})
        my_set = set(title_data)
        new_list = list(my_set)
        sorted(new_list)
    # my_set = set(titi_text)
    # new_list = list(my_set)
    #
    # for j in new_list:
    #     try:
    #         list_info.append({j: value_text[i]})
    #     except Exception:
    #         list_info.append({j: "None"})
    #     i = + 1

        # list_info.append({title_text: value_text})





    return new_dict



def Test_Json():
    with open("for_test.json", "a", encoding="utf-8") as file:
        json.dump(main_info_body(), file, indent=4, ensure_ascii=False)
Test_Json()