from typing import List, Dict, Any

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
def supplier_result():
    block_title = []
    title_data= []
    value_data = []
    list_info= []
    zakazchic_data= []
    table_titles = []
    all_table_info = []
    doc_titles = []
    data = {}
    i = 0
    n = 0
    # row_info = soup.find_all(class_= 'row blockInfo')
    # for info in row_info:
    driver = webdriver.Chrome()
    driver.get(link)
    import time
    time.sleep(0)
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')

    driver.quit()

    col_9 = soup.find_all(class_='row blockInfo')

    for col in col_9:
        title_cap = col.find(class_='blockInfo__title').get_text().strip()


            # td_text = info.find('td',class_='tableBlock__col').get_text().strip()
            #
            # value_text = 'None'
            # title_text = 'None'

        block_section = col.find_all('section', class_="blockInfo__section section")
        for inf in block_section:
            title_text = inf.find(class_='section__title').get_text().strip()
            try:
                title_value = inf.find(class_='section__info').get_text().strip()
                value_data.append({title_text: title_value})
            except  Exception:
                value_data.append({title_text: ''})
        ##Заказчик(и), с которыми планируется заключить контракт
        try:
            th = col.find('th', class_="tableBlock__col tableBlock__col_header").get_text().strip()
            td = col.find('td', class_='tableBlock__col').get_text().strip()
            zakazchic_data.append({th: td})
            zac = zakazchic_data[0]

        except Exception:
            None


    #Таблица если есть
        # elements = soup.find_all('div', class_='blockInfo__table tableBlock')
        # second_element = elements[1]  # выбираем второй элемент (индекс 1)
        try:
            table_sup = col.find_all(class_ = 'blockInfo__table tableBlock')
            if len(table_sup) > 1:
                second_element = table_sup[1]
                table_tr = second_element.find_all(class_= 'tableBlock__col tableBlock__col_header')
                for th in table_tr:
                    table_titles.append(th.get_text().strip())
                table_td = second_element.find_all(class_='tableBlock__body')
                for row in table_td:
                    try:
                        table_td_row = row.find_all(class_='tableBlock__col')
                        for th in table_td_row:
                            try:
                                all_table_info.append({table_titles[n].replace('\n', '').replace(' ', ''):th.get_text().strip().replace('\n', '').replace(' ', '')})
                            except Exception:
                                n = 0
                                all_table_info.append({table_titles[n].replace('\n', '').replace(' ', ''): th.get_text().strip().replace('\n', '').replace(' ', '')})
                            n = n + 1
                    except Exception:
                        None
                value_data.append(all_table_info)
                all_table_info = []

            #Дальнейшие таблицы
            else:
                table_tr = col.find_all(class_='tableBlock__col tableBlock__col_header')
                for th in table_tr:
                    table_titles.append(th.get_text().strip())
                table_td = col.find_all(class_='tableBlock__body')
                for row in table_td:
                    try:
                        table_td_row = row.find_all(class_='tableBlock__col')
                        for th in table_td_row:
                            try:
                                all_table_info.append({table_titles[n].replace('\n', '').replace(' ', ''): th.get_text().strip().replace('\n', '').replace(' ', '')})
                            except Exception:
                                n = 0
                                all_table_info.append({table_titles[n].replace('\n', '').replace(' ', ''): th.get_text().strip().replace('\n', '').replace(' ', '')})
                            n = n + 1
                    except Exception:
                        None
                value_data.append(all_table_info)
                all_table_info = []


        except Exception:
                    None
        value_data.append(zac)
        # value_data.append(all_table_info)
        data[title_cap] = value_data
        value_data = []
        zac = []
        zakazchic_data = []
    return data
#
# print(supplier_result())

def Test_Json():
    with open("for_test.json", "a", encoding="utf-8") as file:
        json.dump(supplier_result(), file, indent=4, ensure_ascii=False)
Test_Json()