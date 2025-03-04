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


class AgreementParser:
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
        
        # Находим контейнер с ссылками
        container = soup.find('div', class_='container card-layout')
        if not container:
            return []

        # Находим все ссылки в контейнере
        links = container.find_all('a', class_='tabsNav__item')
        
        # Собираем ссылки и их тексты
        result = []
        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)
            if href:
                full_url = self.base_url + href
                result.append((full_url, text))
        
        return result
    
    def parse_first_level(self,url ):
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # Находим основной контейнер с информацией
        main_container = soup.find('div', class_='cardMainInfo row')
        if not main_container:
            return {}

     
        data = {}
        
        # Парсим левую часть (col-9)
        left_section = main_container.find('div', class_='sectionMainInfo borderRight col-9')
        if left_section:

            status = left_section.find('span', class_='cardMainInfo__state')
            # Заказчик
            contract = left_section.find('a', href=True)
            if contract:
                data['Договор'] = {
                     contract.get_text(strip=True)
                }
                data['Статус'] =  {status.get_text(strip=True)}
                self.contract = contract.get_text(strip=True)
        leff_section_main = main_container.find('div', class_='sectionMainInfo__body')
        left_section_card = leff_section_main.find_all('div', class_='cardMainInfo__section')
        for section in left_section_card:
            title = section.find("span", class_="cardMainInfo__title").text.strip()
            content_tag = section.find("span", class_="cardMainInfo__content")

            if content_tag:
                link_tag = content_tag.find("a")
                if link_tag:
                    content_text = link_tag.text.strip()
                    link = link_tag["href"]
                    data[title] = {content_text , link}
                else:
                    content_text = content_tag.text.strip()
                    data[title] = {content_text}
                    link = None  

    

        # Парсим правую часть (col-3)
        right_section = main_container.find('div', class_='sectionMainInfo borderRight col-3 colSpaceBetween')
        if right_section:
            sections = right_section.find_all(["div"], class_=["price-block", "data-block", "row"])
            for section in sections:
                title_tag = section.find("div", class_="rightBlock__tittle")
                content_tag = section.find("div", class_="rightBlock__text") or section.find("div", class_="rightBlock__price")

                if title_tag and content_tag:
                    title = title_tag.text.strip().replace("\n", " ")
                    content_text = html.unescape(content_tag.text).strip().replace("\xa0", " ")

                    data[title] = content_text

       
        containers = soup.find_all('div', class_='container')
        if len(containers) > 5:  # Нас интересуют контейнеры, начиная с 5-го
            for container in containers[5:]:
                self._parse_general_info(container, data)
        return data

    def parse_second_level(self,  url ):
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        data = {}

        containers = soup.find_all('div', class_='container')
        if len(containers) > 5:  # Нас интересуют контейнеры, начиная с 5-го
            for container in containers[5:]:
                self._parse_general_info(container, data)
        return data
    def parse_third_level(self,  url ):
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        data = {}

        containers = soup.find_all('div', class_='container')
        if len(containers) > 5:  # Нас интересуют контейнеры, начиная с 5-го
            for container in containers[5:]:
                self._parse_general_info(container, data)
        return data
    
    def parse_four_level(self,  url ):
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        data = {}
        container = soup.find('div', id='event-journal-wrapper')
        # containers = soup.find_all('div', class_='container')
        if container:  # Нас интересуют контейнеры, начиная с 5-го
           self._parse_general_info(container, data)
        return data
    
    def close(self):
        self.driver.quit()

    def _parse_general_info(self, container, data):
        # Находим заголовок блока
        block_title = container.find('h2', class_='blockInfo__title')
        if block_title:
            block_title_text = block_title.get_text(strip=True)
            data[block_title_text] = {}
            self.static_block_title_text = block_title_text
        # Находим все секции внутри контейнера
        sections = container.find_all('section', class_='blockInfo__section section')
        for section in sections:
            # Обработка обычных секций
            title = section.find('span', class_='section__title')
            info = section.find('span', class_='section__info')

            if title and info:
                title_text = title.get_text(strip=True)
                info_text = info.get_text(strip=True)
                link = info.find('a')
                if link:
                    info_text = {
                        'Текст': link.get_text(strip=True),
                        'Ссылка': link['href']
                    }
                data[block_title_text][title_text] = info_text
            common_row = container.find_all('div', class_='card-common col-2')
            for row in common_row:
                common_title = row.find('span', class_='common-text__title-inn')
                common_info = row.find('span', class_='common-text__value')
                if common_title and common_info:
                    common_title_text = common_title.get_text(strip=True)
                    common_info_text = common_info.get_text(strip=True)
                    data[block_title_text][common_title_text] = common_info_text
            # Обработка выпадающих элементов с табличной структурой
            table_section = section.find('div', class_='header-grey-light')
            if table_section:
                # Заголовки таблицы
                headers = [header.get_text(strip=True) for header in table_section.find_all('div', class_='col')]
                
                # Данные таблицы
                rows = section.find_all('div', class_='row bt-4 pb-4 pt-4 text-base-mid b-bottom')
                table_data = []
                for row in rows:
                    cells = row.find_all('div', class_='table_info')
                    row_data = {}
                    for i, cell in enumerate(cells):
                        # Проверяем, что индекс i не выходит за пределы списка headers
                        if i < len(headers):
                            row_data[headers[i]] = cell.get_text(strip=True)
                        else:
                            # Если ячеек больше, чем заголовков, добавляем их с ключом "Дополнительно"
                            row_data[f"Строка {i}"] = cell.get_text(strip=True)
                    table_data.append(row_data)
                
                # Сохраняем данные таблицы
                if table_data:
                    data[block_title_text]['Таблица'] = table_data
        inner_html = container.find('div', class_='innerHtml')
        if inner_html:
            tables = inner_html.find_all('table', class_='table')
            for table in tables:
                table_data = self._parse_table(table)
                if table_data:
                    data[self.static_block_title_text]['Таблица'] = table_data

        jornal_versions = container.find('div', class_='blockInfo blockInfo__mb24')
        if jornal_versions:
            tables = jornal_versions.find_all('table', class_='table')
            for table in tables:
                table_data = self._parse_table(table)
                if table_data:
                    data[self.static_block_title_text]['Таблица'] = table_data

        event_table = container.find('table',id="event")
        if event_table:
            event_data = self._parse_event_table(event_table)
            if event_data:
                if 'Журнал событий' not in data:
                    data['Журнал событий'] = {}
                    data['Журнал событий']['События'] = event_data

        total_sum_element = container.find('div', class_='row header-grey-light pt-4 pb-4 b-bottom')
        if total_sum_element:
            total_sum_label = total_sum_element.find('div', class_='col-11 text-right')
            total_sum_value = total_sum_element.find('div', class_='col-1 rightBlock__price text-center noWrap')
            if total_sum_label and total_sum_value:
                label = self._clean_text(total_sum_label.get_text())
                value = self._clean_text(total_sum_value.get_text())
                data[self.static_block_title_text]['Итоговая сумма'] = {label: value}

    def _parse_table(self, table):
        """
        Парсит таблицу и возвращает данные в виде списка словарей.
        
        :param table: Объект BeautifulSoup, представляющий таблицу.
        :return: Список словарей с данными таблицы.
        """
        # Извлекаем заголовки таблицы
        headers = []
        thead = table.find('thead')
        if thead:
            header_rows = thead.find_all('tr')
            for row in header_rows:
                headers.extend([self._clean_text(th.get_text()) for th in row.find_all('th')])

        # Извлекаем данные таблицы
        table_data = []
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = {}
                for i, cell in enumerate(cells):
                    if i < len(headers):
                        row_data[headers[i]] = self._clean_text(cell.get_text())
                    else:
                        row_data[f"Дополнительно {i}"] = self._clean_text(cell.get_text())
                table_data.append(row_data)

        # Извлекаем итоговую строку (если есть)
        tfoot = table.find('tfoot')
        if tfoot:
            footer_rows = tfoot.find_all('tr')
            for row in footer_rows:
                cells = row.find_all(['td', 'th'])
                footer_data = {}
                for i, cell in enumerate(cells):
                    footer_data[f"Итого {i}"] = self._clean_text(cell.get_text())
                table_data.append(footer_data)

        return table_data
    
    def _parse_event_table(self, table):
        """
        Парсит таблицу с событиями и возвращает данные в виде списка словарей.
        
        :param table: Объект BeautifulSoup, представляющий таблицу.
        :return: Список словарей с данными таблицы.
        """
        # Извлекаем заголовки таблицы
        headers = []
        thead = table.find('thead')
        if thead:
            header_rows = thead.find_all('tr')
            for row in header_rows:
                headers.extend([self._clean_text(th.get_text()) for th in row.find_all('th')])

        # Извлекаем данные таблицы
        table_data = []
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = {}
                for i, cell in enumerate(cells):
                    if i < len(headers):
                        row_data[headers[i]] = self._clean_text(cell.get_text())
                    else:
                        row_data[f"Дополнительно {i}"] = self._clean_text(cell.get_text())
                table_data.append(row_data)

        return table_data
    
    def _clean_text(self, text):
        """
        Очищает текст от неразрывных пробелов (\xa0) и переводов строк (\n).
        
        :param text: Исходный текст.
        :return: Очищенный текст.
        """
        if not text:
            return text
        # Удаляем неразрывные пробелы (\xa0) и заменяем их на обычные пробелы
        text = text.replace('\xa0', ' ')
        # Удаляем переводы строк (\n) и лишние пробелы
        text = re.sub(r'\s+', ' ', text).strip()
        return text
 

    def save_to_docx(self, data, filename = "test.docx"):
        """
        Сохраняет данные в формате .docx.

        :param data: Словарь с данными для сохранения.
        :param filename: Имя файла для сохранения.
        """

        doc = Document()
        doc.add_heading('Данные договора', level=1)

        for level_name, level_data in data.items():
      
            doc.add_heading(level_name, level=2)


            for key, value in level_data.items():
                if isinstance(value, dict):
              
                    doc.add_heading(key, level=3)
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, dict):
                           
                            doc.add_heading(sub_key, level=4)
                            self._add_table_to_doc(doc, sub_value)
                        elif isinstance(sub_value, list):
                    
                            doc.add_heading(sub_key, level=4)
                            self._add_table_to_doc(doc, sub_value)
                        else:
                            # Иначе добавляем как текст
                            doc.add_paragraph(f"{sub_key}: {sub_value}")
                elif isinstance(value, list):
                    # Если значение — это список, добавляем его как таблицу
                    doc.add_heading(key, level=3)
                    self._add_table_to_doc(doc, value)
                else:
                    # Иначе добавляем как текст
                    doc.add_paragraph(f"{key}: {value}")

        # Сохраняем документ
        doc.save(filename)

    def _add_table_to_doc(self, doc, data):
        """
        Добавляет таблицу в документ, если данные являются списком словарей.
        Если данные не являются списком словарей, добавляет их как текст.

        :param doc: Объект документа.
        :param data: Данные для таблицы.
        """
        if isinstance(data, list) and all(isinstance(row, dict) for row in data):
            # Если данные — это список словарей, создаем таблицу
            if not data:
                return

            # Создаем таблицу
            table = doc.add_table(rows=1, cols=len(data[0]))
            table.style = 'Table Grid'

            # Добавляем заголовки таблицы
            hdr_cells = table.rows[0].cells
            for i, key in enumerate(data[0].keys()):
                hdr_cells[i].text = key

            # Добавляем строки таблицы
            for row in data:
                row_cells = table.add_row().cells
                for i, value in enumerate(row.values()):
                    row_cells[i].text = str(value)
        else:
            # Если данные не являются списком словарей, добавляем их как текст
            doc.add_paragraph(str(data))

    def start_contract_parser(self, file_path):
        data = {}

        try:
            # Получаем все ссылки
            links = self.parse_links()
            if links:
                # Парсим первую ссылку
                first_link_url, first_link_text = links[0]
                second_link_url, second_link_text = links[1]
                third_link_url, third_link_text = links[2]
                four_link_url, four_link_text = links[3]
                data[first_link_text] = self.parse_first_level(first_link_url)
                data[second_link_text] = self.parse_second_level(second_link_url)
                data[third_link_text] = self.parse_third_level(third_link_url)
                data[four_link_text] = self.parse_four_level(four_link_url)

                # Сохраняем данные в .docx
                self.save_to_docx(data, f"{file_path}/Все данные по договору {self.contract}.docx")
        finally:
            self.close()
# Пример использования
# if __name__ == "__main__":
#     parser = AgreementParser("https://zakupki.gov.ru/epz/contractfz223/card/contract-info.html?id=21555118")
#     parser.start_contract_parser("Test")
    # data = {}
    # try:
    #     # Получаем все ссылки
    #     links = parser.parse_links()
    #     if links:
    #         # Парсим первую ссылку
    #         first_link_url, first_link_text = links[0]
    #         second_link_url, second_link_text = links[1]
    #         third_link_url, third_link_text = links[2]
    #         four_link_url,four_link_text = links[3]
    #         data[first_link_text] = parser.parse_first_level(first_link_url)
    #         data[second_link_text] = parser.parse_second_level(second_link_url)
    #         data[third_link_text] = parser.parse_third_level(third_link_url)
    #         data[four_link_text] = parser.parse_four_level(four_link_url)
    #         parser.save_to_docx(data)
            # print(data)  # Выводим результат
    # finally:
    #     parser.close()