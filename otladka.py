from typing import List, Dict, Any

from bs4 import BeautifulSoup
import requests
import urllib3
import locale
import re
# import pandas as pd
# import json
# import os
# from selenium import webdriver
# link = 'https://zakupki.gov.ru/epz/order/notice/ok20/view/supplier-results.html?regNumber=0172500000423000006'

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC




# driver = webdriver.Chrome()

# # Переходим на страницу
# driver.get("https://example.com")

# # Используем метод find_element_by_class_name для поиска элемента с классом "hidden"
# elem = driver.find_element(By.CLASS_NAME,"tableBlock__col tableBlock__row")

# # Выводим содержимое элемента
# print(elem.text)

# # Закрываем браузер
# driver.quit()

# def supplier_result():
#     block_title = []
#     title_data= []
#     value_data = []
#     list_info= []
#     zakazchic_data= []
#     table_titles = []
#     all_table_info = []
#     doc_titles = []
#     new_dict = {}
#     i = 0
#     n = 0
#     # row_info = soup.find_all(class_= 'row blockInfo')
#     # for info in row_info:
#     driver = webdriver.Firefox()
#     driver.get(link)
#     import time
#     time.sleep(5)
#     html = driver.page_source

#     soup = BeautifulSoup(html, 'lxml')



#     col_9 = soup.find_all(class_='tableBlock__body')
#     print(col_9)


#     driver.quit()

# # supplier_result()

def journal_of_events():

        th_mass = []
        data = []
        fn_date= {}
        i = 0
        test_url3 = f'https://zakupki.gov.ru/epz/order/notice/ok44/view/event-journal.html?regNumber=0373100112518000004'
            
        HEADERS_test = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
                              ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
        params ={

                'regNumber': '0373100112518000004' 
            }
        req = requests.get(test_url3, headers=HEADERS_test, params=None)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        # driver.quit()
        wrapper = soup.find('div', class_='container')
        return soup.get_text()
        #не нашел журнал событий
        try:
            for tbn in wrapper:
                c_th = tbn.find_all('th')
                for th_items in c_th:
                    th_text = th_items.get_text().strip()
                    th_mass.append(th_text)

                c_td = tbn.find_all('td')
                for td_items in c_td:
                    td_text = td_items.get_text().strip()
                    try:
                        data.append({th_mass[i]: td_text})
                    except Exception:
                        i = 0
                        data.append({th_mass[i]: td_text})
                    i += 1
            status = 'Успешный парсинг Журнала'
            return data

        except Exception:
            status = 'Ошибка парснига  Журнала'

# print(journal_of_events())

def agent(numer):
    num = numer
    try:
        search_url = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={numer}&morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1'
        # test_url3 = f'https://zakupki.gov.ru/epz/order/notice/ok20/view/common-info.html?regNumber={numer}'
        HEADERS_test = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
                            ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
        req = requests.get(search_url, headers=HEADERS_test, params=None)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        status = 'Успешное подключение'
        col = soup.find('div', class_ = 'registry-entry__header-mid__number')
        a_tag = col.find('a')
        match = re.search(r'noticeInfoId=(\d+)', a_tag['href'])
        number = match.group(1)
        return  number
    except:
        status = 'Ошибка подключения'
print(agent('31704961137'))