import csv
import html
from bs4 import BeautifulSoup
import requests
import locale
import re
from typing import Dict, List, Optional
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from docx import Document



class ContractParser:
    def __init__(self, link):
        self.link = link
        self.base_url = "https://zakupki.gov.ru"
        self.driver = self._init_driver()
    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Включаем headless-режим
        chrome_options.add_argument("--disable-gpu")  # Отключаем GPU, чтобы избежать предупреждений
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    def parse_links(self):
        self.driver.get(self.link)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # Находим div с классом "tabsNav d-flex align-items-end"
        tabs_nav_div = soup.find('div', class_='tabsNav d-flex align-items-end')
        
        # Инициализируем пустой словарь для хранения ссылок и их текстов
        links_dict = {}
        
        # Если div найден, ищем все элементы <a> внутри него
        if tabs_nav_div:
            for a_tag in tabs_nav_div.find_all('a', class_='tabsNav__item'):
                # Извлекаем текст и ссылку
                text = a_tag.get_text(strip=True)
                href = a_tag['href']
                if href:
                    full_url = self.base_url + href
                # Добавляем в словарь
                links_dict[text] = full_url
        
        return links_dict
    def base_information(self, link):
        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # Находим основной блок с информацией
        card_main_info = soup.find('div', class_='cardMainInfo row')
        
        # Инициализируем словарь для хранения данных
        data = {}
        
        if card_main_info:
            contract = card_main_info.find('span', class_="cardMainInfo__purchaseLink distancedText")
            self.contract_num = contract.find('a', href=True).get_text(strip=True)
            status = card_main_info.find('span', class_='cardMainInfo__state distancedText')
            data['Номер договора'] = self.contract_num
            data['Статус'] = status.get_text(strip=True)
            # Извлекаем данные из левой части (col-6)
            left_section = card_main_info.find('div', class_='sectionMainInfo borderRight col-6')
            if left_section:
                for section in left_section.find_all('div', class_='cardMainInfo__section'):
                    try:
                        title = section.find('span', class_='cardMainInfo__title').get_text(strip=True)
                        content = section.find('span', class_='cardMainInfo__content').get_text(strip=True)
                        # Очищаем текст от спецсимволов
                        content = self._clean_text(content)
                        data[title] = content
                    except:
                        title = section.find('div', class_='cardMainInfo__title').get_text(strip=True)
                        content = section.find('span', class_='text-break d-block').get_text(strip=True)
                        content = self._clean_text(content)
                        data[title] = content
            
            # Извлекаем данные из правой части (col-3)
            right_section = card_main_info.find('div', class_='sectionMainInfo borderRight col-3 colSpaceBetween')
            if right_section:
                # Обрабатываем цену контракта
                price_section = right_section.find('div', class_='price')
                if price_section:
                    price_title = price_section.find('span', class_='cardMainInfo__title').get_text(strip=True)
                    price_content = price_section.find('span', class_='cardMainInfo__content cost').get_text(strip=True)
                    price_content = self._clean_text(price_content)
                    data[price_title] = price_content
                
                # Обрабатываем даты
                date_section = right_section.find('div', class_='date')
                if date_section:
                    for section in date_section.find_all('div', class_='cardMainInfo__section'):
                        title = section.find('span', class_='cardMainInfo__title').get_text(strip=True)
                        content = section.find('span', class_='cardMainInfo__content').get_text(strip=True)
                        content = self._clean_text(content)
                        data[title] = content
        

        containers = soup.find_all('div', class_='container')
        if len(containers) > 2:  # Нас интересуют контейнеры, начиная с 5-го
            for container in containers[2:]:
                self._parse_general_info(container, data)

        return data
    def payment_information(self, link):
        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        data = {}
        containers = soup.find_all('div', class_='container')
        if len(containers) > 3:  # Нас интересуют контейнеры, начиная с 5-го
            for container in containers[3:]:
                self._parse_general_info(container, data)
                

        return data
    def executor_information(self,link):
        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        data = {}
        containers = soup.find_all('div', class_='container')
        if len(containers) > 5:  # Нас интересуют контейнеры, начиная с 5-го
            for container in containers[5:]:
                self._parse_general_info(container, data)
        return data
    
    def inserte_information(self,link):
        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        data = {}
        containers = soup.find_all('div', class_='container')
        if len(containers) > 5:  # Нас интересуют контейнеры, начиная с 5-го
            for container in containers[5:]:
                self._parse_general_info(container, data)
        return data
    def _parse_general_info(self, container, data):
        # Извлекаем заголовок блока (например, "Общая информация")      
        block_title = container.find('h2', class_='blockInfo__title')
        if block_title:
            block_title = block_title.get_text(strip=True)
        else:
            block_title = "Без названия"  # Если заголовок отсутствует
        
        # Инициализируем словарь для текущего блока
        block_data = {}
        block_data_none = {}
        i= 0
         # Обрабатываем таблицы
        text_blocks = container.find_all('span', class_=['cost', 'section__title'])
        if text_blocks:
            text_data = {}
            for block in text_blocks:
                # Извлекаем текст и очищаем его
                text = self._clean_text(block.get_text(strip=True))
                # Определяем тип блока (например, "Этап" или "Детализация")
                if "cost" in block.get('class', []):
                    text_data["Этап"] = text
                elif "section__title" in block.get('class', []):
                    text_data["Заголовок"] = text
                i = i + 1
                if i == 2:
                    block_data["Текстовые блоки"] = text_data
                    break 
       
        tables = container.find_all('table', class_='blockInfo__table')
        if tables:
            table_list = []
            for table in tables:
                table_data = self._parse_table(table )
                table_list.append(table_data)
            block_data["Таблицы"] = table_list

        # Находим все секции внутри контейнера
        sections = container.find_all(['section', 'div'], class_=['blockInfo__section section','row blockInfo'])
        if sections:
            for section in sections:
                try:
                    # Извлекаем заголовок и значение
                    title = section.find('span', class_='section__title').get_text(strip=True)
                    info = section.find('span', class_='section__info').get_text(strip=True)
                    
                    # Очищаем текст от спецсимволов
                    info = self._clean_text(info)
                    
                    # Сохраняем данные в словарь текущего блока
                    
                    data[title] = info
                except:
                    continue


        payment_details = self._parse_payment_details(container)
        if payment_details:
                data[block_title] = payment_details
        
        data[block_title] = block_data
     
    def _clean_text(self, text):
        # Удаляем лишние пробелы, символы новой строки и &nbsp;
        text = re.sub(r'\s+', ' ', text)  # Заменяем множественные пробелы на один
        text = re.sub(r'&nbsp;', ' ', text)  # Заменяем &nbsp; на пробел
        text = text.strip()  # Убираем пробелы в начале и конце
        return text

    def _parse_table(self, table):
        # Инициализируем список для хранения данных таблицы
        table_data = []
        
        # Извлекаем заголовки столбцов
        headers = []
        thead = table.find('thead')
        if thead:
            header_row = thead.find('tr')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]

        tbody = table.find('tbody')
        if tbody:
            for row in tbody.find_all('tr'):
                row_data = {}
                cells = row.find_all('td')
                for i, cell in enumerate(cells):
                    # Очищаем текст от спецсимволов
                    cell_text = self._clean_text(cell.get_text(strip=True))
                    
                    # Если заголовков больше, чем ячеек, используем индекс
                    header = headers[i] if i < len(headers) else f"Column_{i}"
                    row_data[header] = cell_text
                
                # Добавляем строку в данные таблицы
                table_data.append(row_data)
        
        return table_data
    
    def _parse_payment_details(self, container):
        """
        Универсальный метод для парсинга платежных реквизитов.
        Возвращает список словарей, где каждый словарь представляет блок с реквизитами.
        """
        payment_details = []
        
        # Ищем все блоки с реквизитами
        payment_blocks = container.find_all('div', class_=['padTop20', 'padBottom20', 'font-weight-bold', 'border-top'])
        
        for block in payment_blocks:
            block_data = {}
            
            # Извлекаем заголовок блока (например, "Реквизиты счёта заказчика")
            title = block.find('span', class_='cost')
            if title:
                block_data["Заголовок"] = self._clean_text(title.get_text(strip=True))
            
            # Ищем таблицу, связанную с этим блоком
            table = block.find_next('table', class_='tableBlock')
            if table:
                table_data = self._parse_table(table)
                block_data["Таблица"] = table_data
            
            # Добавляем данные блока в список
            payment_details.append(block_data)
        
        return payment_details

if __name__ == "__main__":
    parser = ContractParser("https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber=2645211102824000046&contractInfoId=97549520")
    global_data = {}
    links = parser.parse_links()
    base_url = list(links.values())[0]  
    base_title = list(links.keys())[0]
    payment_url =  list(links.values())[1]  
    payment_title =  list(links.keys())[1] 
    executor_url =  list(links.values())[2]  
    executor_title =  list(links.keys())[2] 
    inserts_url =  list(links.values())[3]  
    inserts_title =  list(links.keys())[3]   
    # global_data[base_title] = parser.base_information(base_url)
    # global_data[payment_title] = parser.payment_information(payment_url)
    # global_data[executor_title] = parser.executor_information(executor_url)
    global_data[inserts_title] = parser.inserte_information(inserts_url)
    print(global_data)
    # data = {}