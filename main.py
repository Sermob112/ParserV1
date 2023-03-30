
from bs4 import BeautifulSoup
import requests




# URL = {'fz223': 'https://zakupki.gov.ru/223/purchase/public/purchase/info/documents.html',
#        'fz44': 'https://zakupki.gov.ru/epz/order/notice/view/documents.html',} # шаблон адреса страницы с документами по закупке
# CONTRACT_URL = {'fz44': 'https://zakupki.gov.ru/epz/contract/search/results.html'}# шаблон адреса страницы с контрактами
# CONTRACT_DOCS_URL = {'fz44': 'https://zakupki.gov.ru/epz/contract/contractCard/document-info.html'}# шаблон адреса страницы с документами по контракту
#
# HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                          '(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
#            'accept': '*/*'}
#
#
# test_url = 'https://zakupki.gov.ru/epz/order/notice/notice223/common-info.html?noticeInfoId=15097592'
# HEADERS_test = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
#                          ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36',
#            'accept': '*/*'}
# req = requests.get(test_url, headers= HEADERS_test)
# src = req.text
# print(src)
#
# with open("index.html", 'w', encoding="utf-8") as file:
#     file.write(src)
with open ('index.html','r', encoding="utf-8") as file:
    source = file.read()
soup = BeautifulSoup(source, 'lxml')
##############################################################################################################
#основная информация
serial_number = soup.find(class_="registry-entry__header-mid__number").find('a').text.strip()
# print(serial_number)
# zakupchik  = soup.find(class_ = 'registry-entry__body').text.strip()# Нашли всех закупщиков
zakupchik = soup.find(class_ = 'registry-entry__body').find_all(class_ = 'registry-entry__body-block')
for i in zakupchik:
    object_zak = i.find(class_ = 'registry-entry__body-title').text.strip()
    zakazchic = i.find(class_ = 'registry-entry__body-value').text.strip()
    a_tag = i.find('a')
    if a_tag == None:
        continue
    else:
        link = 'https://zakupki.gov.ru' + a_tag["href"]
    # link = a_tag["href"]
    # print(object_zak)
    # print(zakazchic)
    # print(link)
    # print(linker)
# print(zakupchik)
###########################################################################################################
####Начальная цена
price = soup.find(class_ = 'price-block').find_all('div')
for i in price:
    title = i.text
    # print(title)
# print(price)
###########################################################################################################
#Парсинг всех ссылок на информацию
tabs_of_links = []
link_razdels = soup.find(class_ = 'tabsNav d-flex').find_all('a')
for links in link_razdels:
    linkl = 'https://zakupki.gov.ru/' + links.get('href')
    title_razde = links.text.strip()
    tabs_of_links.append({title_razde:linkl})
# print(tabs_of_links)
##################################################################################
#Парсинг сведений о закупке

main_infp = soup.find_all(class_ ='common-text b-bottom pb-3')
# title_cap = soup.find(class_= 'common-text__caption').text.strip()
# print(title_cap)
list_info = []
for info in main_infp:
    #весь текст
    # zagolovok = info.text.strip()
    col_9 = info.find_all(class_='col-9 mr-auto')
    title_cap = info.find(class_='common-text__caption').text.strip()
    list_info.append({title_cap})
    for values in col_9:
        # title_cap = info.find(class_='common-text__caption')

        title_text = values.find(class_= 'common-text__title')
        value_text = values.find(class_= 'common-text__value')
        if (title_text == None  or value_text == None):
            continue
        else:
            title_text = values.find(class_='common-text__title').text.strip()
            value_text = values.find(class_='common-text__value').text.strip()
        list_info.append({title_text:value_text})
print(list_info)



# col_9 = soup.find_all(class_='col-9 mr-auto')
# for values in col_9:
#     title_text = values.find(class_= 'common-text__title')
#     value_text = values.find(class_= 'common-text__value')
