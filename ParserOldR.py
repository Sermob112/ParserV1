import csv
import os
import re
import json
import logging
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from docx import Document
from ParserAgreement import AgreementParser

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ParserOldR:
    def __init__(self):
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36',
            'accept': '*/*'
        }
        self.status = None
        self.filePath = None
        self.main_directory = None
        self.ObjectName = None
        self.num = None
        self.soup = None

    def make_link_num(self, numer, filePath):
        self.filePath = filePath
        search_url = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={numer}&morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1'
        
        try:
            req = requests.get(search_url, headers=self.HEADERS)
            req.raise_for_status()
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            col = soup.find('div', class_='registry-entry__header-mid__number')
            a_tag = col.find('a')
            match = re.search(r'noticeInfoId=(\d+)', a_tag['href'])
            link_text = 'https://zakupki.gov.ru/' + a_tag.get('href')
            number = match.group(1)
            self.main_directory = f'Закупка № {numer} '
            self.num = numer
            self.agent(number, link_text)
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            self.status = 'Ошибка подключения'

    def agent(self, numer, link_text):
        try:
            req = requests.get(link_text, headers=self.HEADERS)
            req.raise_for_status()
            src = req.text
            self.soup = BeautifulSoup(src, 'lxml')
            self.status = 'Успешное подключение'
            return self.soup
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            self.status = 'Ошибка подключения'

    def parse_head(self):
        source = self.soup.find(class_="col-6 pr-0 mr-21px")
        self.ObjectName = source.find(class_='registry-entry__body-value').get_text().strip().replace('"', '').replace('\r', '')[:48].replace(' ', '_').replace('\n', '')
        return self.ObjectName

    def get_links(self):
        tabs_of_links = {}
        link_razdels = self.soup.find(class_='container card-layout')
        if link_razdels:
            try:
                link_razdels = self.soup.find(class_='tabsNav d-flex').find_all('a')
            except:
                link_razdels = self.soup.find(class_='tabsNav d-flex align-items-end').find_all('a')
            for links in link_razdels:
                linkl = 'https://zakupki.gov.ru/' + links.get('href')
                title_razde = links.text.strip()
                tabs_of_links[title_razde] = linkl
        return tabs_of_links

    def main_info(self):
        mainMass = []
        newmainMass = []
        JornalMass = []
        DockMass = []
        AgreMass = []
        tabs_of_links = self.get_links()
        for title, link in tabs_of_links.items():
            req = requests.get(url=link, headers=self.HEADERS)
            src = req.text
            soup = BeautifulSoup(src, "lxml")
            if title == 'Журнал событий':
                JornalMass = self.get_jornals(link)
            if title == 'Сведения о договорах':
                AgreMass = self.get_agreements(link)
            if title == 'Документы':
                DockMass = self.get_documents(link)
            try:
                containerMain = soup.find_all(class_='card-common-content')
                containerMain2 = soup.find_all(class_='card-attachments')
                if containerMain:
                    for i in containerMain:
                        lines = i.get_text().strip().splitlines()
                        Mass = [line.strip() for line in lines if line.strip()]
                        cleaned_Mass = [item.replace('\xa0', ' ') for item in Mass]
                        mainMass += cleaned_Mass
                if containerMain2:
                    for i in containerMain2:
                        lines = i.get_text().strip().splitlines()
                        Mass = [line.strip() for line in lines if line.strip()]
                        cleaned_Mass = [item.replace('\xa0', ' ') for item in Mass]
                        mainMass += cleaned_Mass
                        newmainMass += cleaned_Mass
            except Exception as e:
                logger.error(f"Ошибка при обработке контейнера: {e}")
        mainMass.append(newmainMass)
        mainMass.append(JornalMass)
        mainMass.append(DockMass)
        mainMass.append(AgreMass)
        return mainMass

    def get_agreements(self, link):
        req = requests.get(link, headers=self.HEADERS, params=None)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        no_data_message = soup.find('div', class_='section__title', text='Сведения отсутствуют')
        if no_data_message:
            return ["Сведения отсутствуют"]
        table = soup.find('table', class_='table')
        if table:
            rows = table.find_all('tr')
            agreements = []
            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    links = cols[0].find_all('a', href=True)
                    self.contract_info_link = None
                    for link in links:
                        if 'contract-info' in link['href']:
                            self.contract_info_link = link['href']
                    agreement_text = cols[0].get_text(strip=True)
                    agreement_revision = cols[1].get_text(strip=True)
                    agreement_status = cols[2].get_text(strip=True)
                    agreement_date = cols[3].get_text(strip=True)
                    agreements.append(f"Текст: {agreement_text}")
                    agreements.append(f"Редакция: {agreement_revision}")
                    agreements.append(f"Статус: {agreement_status}")
                    agreements.append(f"Дата: {agreement_date}")
                    agreements.append("\n")
            try:
                link = "https://zakupki.gov.ru" + self.contract_info_link
                par_agreement = AgreementParser(link)
                par_agreement.start_contract_parser(file_path=f"{self.filePath}/{self.main_directory + self.ObjectName}")
            except Exception as e:
                logger.error(f"Ошибка при парсинге договора: {e}")
            return agreements
        else:
            return ["Таблица с договорами не найдена"]

    def get_jornals(self, link):
        JornalMass = []
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        driver.quit()
        containerMain3 = soup.find_all(class_='tabBoxWrapper tabBoxWrapper__mb24')
        if containerMain3:
            for i in containerMain3:
                lines = i.get_text().strip().splitlines()
                Mass = [line.strip() for line in lines if line.strip()]
                JornalMass += Mass
        print(JornalMass)
        return JornalMass

    def get_documents(self, link):
        titlesMass = []
        linkMass = []
        req = requests.get(link, headers=self.HEADERS, params=None)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        findTitle = soup.find_all(class_='container card-attachments-container')
        for titles in findTitle:
            title = titles.find(class_='title')
            if title:
                title_text = title.get_text().strip()
                values = titles.find_all(class_='col-6 b-left')
                for laxir in values:
                    luxit = laxir.find_all('a')
                    try:
                        for links in luxit:
                            href = links.get('href')
                            if href and 'download/download.html?id' in href:
                                linkl = href
                                tooltip_value = links.get('data-tooltip')
                                tooltip_soup = BeautifulSoup(tooltip_value, 'html.parser')
                                span_element = tooltip_soup.find('span')
                                if span_element:
                                    text = span_element.get_text(strip=True).replace('"', '')
                                    response = requests.get(f'https://zakupki.gov.ru{linkl}', headers=self.HEADERS)
                                    if response.status_code == 200:
                                        os.makedirs(f'{self.filePath}/{self.main_directory + self.ObjectName}/{title_text}', exist_ok=True)
                                        with open(f'{self.filePath}/{self.main_directory + self.ObjectName}/{title_text}/{text}', "wb") as f:
                                            f.write(response.content)
                                    else:
                                        logger.error(f"Не удалось скачать файл: {linkl}")
                    except Exception as e:
                        logger.error(f"Произошла ошибка: {e}")
    
    def make_doc(self):
        mainMass = self.main_info()
        # print(mainMass)
        try:
            doc = Document()
            doc.add_heading('Данные о закупке', level=1)
            for item in mainMass:
                doc.add_paragraph(item)
            doc.save(f"{self.filePath}/{self.main_directory + self.ObjectName}/Все данные о закупке №{self.num}.docx")
        except Exception as e:
            logger.error(f"Ошибка записи файлов: {e}")
            self.status = 'Ошибка записи файлов'

# if __name__ == "__main__":
#         parR= ParserOldR()
#         parR.parse_head()
#         parR.documents(i)
#         parR.get_supplier_links(i)
#         parR.get_result_contracts(i)
#         parR.Make_Dock(i)
