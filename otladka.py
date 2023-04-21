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
link = 'https://zakupki.gov.ru/epz/order/notice/ok20/view/supplier-results.html?regNumber=0172500000423000006'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




driver = webdriver.Chrome()

# Переходим на страницу
driver.get("https://example.com")

# Используем метод find_element_by_class_name для поиска элемента с классом "hidden"
elem = driver.find_element(By.CLASS_NAME,"tableBlock__col tableBlock__row")

# Выводим содержимое элемента
print(elem.text)

# Закрываем браузер
driver.quit()

def supplier_result():
    block_title = []
    title_data= []
    value_data = []
    list_info= []
    zakazchic_data= []
    table_titles = []
    all_table_info = []
    doc_titles = []
    new_dict = {}
    i = 0
    n = 0
    # row_info = soup.find_all(class_= 'row blockInfo')
    # for info in row_info:
    driver = webdriver.Firefox()
    driver.get(link)
    import time
    time.sleep(5)
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')



    col_9 = soup.find_all(class_='tableBlock__body')
    print(col_9)


    driver.quit()

# supplier_result()
