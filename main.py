import csv

from bs4 import BeautifulSoup
import requests
import locale
import re
import pandas as pd
import json
import os


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
# test_url2 = 'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0124200000623001098'
# test_url3 = 'https://zakupki.gov.ru/epz/order/notice/ok20/view/common-info.html?regNumber=0172500000423000006'
# HEADERS_test = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
#                          ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36','accept': '*/*'}
# req = requests.get(test_url, headers= HEADERS_test)
# src = req.text
# req = requests.get(test_url2, headers= HEADERS_test, params= None)
# src = req.text
# print(src)
# req = requests.get(test_url3, headers= HEADERS_test, params= None)
# src = req.text
# with open("index3.html", 'w', encoding="utf-8") as file:
#     file.write(src)
# with open ('index2.html','r', encoding="utf-8") as file:
#     source = file.read()

def agent():
    test_url3 = 'https://zakupki.gov.ru/epz/order/notice/ok20/view/common-info.html?regNumber=0172500000423000006'
    HEADERS_test = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
                      ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36', 'accept': '*/*'}

    req = requests.get(test_url3, headers=HEADERS_test, params=None)
    src = req.text
    with open("index3.html", 'w', encoding="utf-8") as file:
        file.write(src)
    with open ('index3.html','r', encoding="utf-8") as file:
        source = file.read()
    soup = BeautifulSoup(source, 'lxml')
    return  soup

##############################################################################################################
#основная информация
######################################################
#Серийный номер
soup = agent()
def parse_head():
    mass = []
    serial_date = {}
    serial_number = soup.find(class_="registry-entry__header-mid__number")
    if serial_number != None:
        serial_number = soup.find(class_="registry-entry__header-mid__number").find('a').text.strip()
    else:
        serial_number = soup.find('a', {'class': 'distancedText'})
        regNumber = serial_number['href'].split('=')[1]
        status_text = soup.find(class_= 'cardMainInfo__state distancedText').get_text().strip()
        mass.append({regNumber:status_text})

#####Сведенья о закупке###########################
    svedenia_o_zakupke = []
    zakupchik = soup.find(class_ = 'registry-entry__body')
    if zakupchik != None:
        zakupchik = soup.find(class_ = 'registry-entry__body').find_all(class_ = 'registry-entry__body-block')
        for i in zakupchik:
            object_zak = i.find(class_ = 'registry-entry__body-title').text.strip()
            zakazchic = i.find(class_ = 'registry-entry__body-value').text.strip()
            svedenia_o_zakupke.append({object_zak: zakazchic})
            a_tag = i.find('a')
            if a_tag == None:
                continue
            else:
                link = 'https://zakupki.gov.ru' + a_tag["href"]
            svedenia_o_zakupke.append({object_zak: zakazchic, 'ссылка на огранизацию': link})
    else:
        zakupchik = soup.find(class_='sectionMainInfo__body').find_all(class_='cardMainInfo__section')
        for i in zakupchik:
            object_zak = i.find(class_='cardMainInfo__title').text.strip()
            zakazchic = i.find(class_='cardMainInfo__content').text.strip()
            svedenia_o_zakupke.append({object_zak: zakazchic})
            a_tag = i.find('a')
            if a_tag == None:
                continue
            else:
                link = 'https://zakupki.gov.ru' + a_tag["href"]
            mass.append({object_zak:zakazchic, 'ссылка на огранизацию':link})
        mass.append(svedenia_o_zakupke)

    # link = a_tag["href"]


#######################################
#Сведенья о закупе (начальная цена и пр)
# ####Начальная цена
    priece_info = []
    price = soup.find(class_ = 'price-block')
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
    if price != None:
        price = soup.find(class_ = 'price-block').find_all('div')
        for i in price:
            title = i.text
    else:
        price = soup.find(class_='sectionMainInfo borderRight col-3 colSpaceBetween').find_all('span')
        for i in price:
            title = i.text.strip()
            if '\xa0' in title:
                title = title.replace('\xa0', '')  # remove non-breaking spaces
                title = title.replace(',', '.')  # replace comma with dot
            priece_info.append(title)
    result = []
    for i in range(0, len(priece_info), 2):
        key = priece_info[i]
        value = priece_info[i+1] if i+1 < len(priece_info) else ''
        # result.append({key: value})
        mass.append({key: value})
        serial_date['Номер заказа'] = mass
    return serial_date



# ###########################################################################################################
# #Парсинг всех ссылок на информацию
def all_link():
    tabs_of_links = {}
    link_razdels = soup.find(class_ = 'tabsNav d-flex')
    try:
        link_razdels = soup.find(class_ = 'tabsNav d-flex').find_all('a')
        for links in link_razdels:
            linkl = 'https://zakupki.gov.ru/' + links.get('href')
            title_razde = links.text.strip()
            tabs_of_links.append({title_razde:linkl})
    except Exception:
        link_razdels = soup.find(class_='tabsNav d-flex align-items-end').find_all('a')
        for links in link_razdels:
            linkl = 'https://zakupki.gov.ru/' + links.get('href')
            title_razde = links.text.strip()
            tabs_of_links[title_razde] = linkl
    return tabs_of_links
# print(all_link())
# ##################################################################################
#Парсинг сведений о закупке
def main_info_body(soup):
    main_infp = soup.find_all(class_ ='common-text b-bottom pb-3')
    list_info = []
    all_table_info = []
    data_td = []
    block_title = []
    new_dict = {}
    table_info = []
    if len(main_infp) != 0:
    # title_cap = soup.find(class_= 'common-text__caption').text.strip()
    # print(title_cap)
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


    else:
        b = 0
        n = 0
        main_infp = soup.find_all(class_='row blockInfo')
        for info in main_infp:
            # col_9 = info.find_all(class_='blockInfo__section section')
            col_9 = info.find_all(class_='blockInfo__section')
            title_cap = info.find(class_='blockInfo__title').get_text().strip()
            block_title.append(title_cap)
            for values in col_9:
                title_text = values.find(class_='section__title')
                value_text = values.find(class_='section__info')
                if (title_text == None  or value_text == None):
                    continue
                else:
                    title_text = values.find(class_='section__title').get_text().strip()
                    value_text = values.find(class_='section__info').get_text().strip()
                    if '\n' in title_text or '\n' in value_text:
                        title_text = title_text.replace('\n', '')  # remove non-breaking spaces
                        value_text = value_text.replace('\n', '')
                    if ' ' in value_text:
                        value_text = value_text.replace(' ', '')  # remove non-breaking spaces
                    list_info.append({title_text:value_text})
            # new_dict[title_cap] = list_info
            # list_info = []
            # b = b + 1
            table = info.find_all(class_ ='blockInfo__table tableBlock')
            if table != None:
                for tables in table:
                    # table = info.find(class_='blockInfo__table tableBlock')
                    hiegth_row = tables.find_all('th')
                    table_td = tables.find_all('td')

                    for i in hiegth_row:
                        column_name = i.text.strip()
                        all_table_info.append(column_name)
                        # print(column_name)
                    for i in table_td:
                        td = i.get_text().strip()
                        if(td == ''):
                            continue
                        if '\n' in td:
                            td = td.replace('\n', '') # remove non-breaking spaces
                            td = re.findall('[A-ZА-Я][^A-ZА-Я]*', td)
                        if '\xa0' in td:
                            td = td.replace('\xa0', '').replace(',', '.')   # remove non-breaking spaces

                        data_td.append(td)
                        try:
                            list_info.append({all_table_info[n]:td})
                        except IndexError:
                            # continue
                            list_info.append({'': td})
                        n = n + 1
            new_dict[title_cap] = list_info
            list_info = []
            b = b + 1
        # return data_td
        return new_dict

# print(main_info_body())
#############################################################################################
#Выподающая страница
##############################################################################################
def collapse_element(soup):
    i = 0
    j = 0
    collaps_titles  = []
    collaps_main_title_mass = []
    cont_main_title_mass = []
    th_mass = []
    titls_table_main = []
    collaps_main = []
    collaps_data = {}
    conteiner_text = []
    table_data = {}
    conteiner_titls_data = {}
    fgh = 0
    collaps_content = soup.find_all( 'div', class_ = 'blockInfo__collapse collapseInfo')
    if collaps_content != None:
        for infos in collaps_content:
            collaps_title = infos.find( class_ = 'collapse__title_text').get_text()
            collaps_title = collaps_title.replace('\n', '').replace('\xa0', ' ')
            collaps_titles.append(collaps_title)
            content_block_info  = infos.find_all('div', class_="content__block blockInfo")
            collaps_data[0] = collaps_title
            for item in content_block_info:

                block_info_title = item.find( class_ = 'blockInfo__title').get_text()
                collaps_titles.append(block_info_title)
                block_sec_title = item.find_all(class_='section__title')
                for its in block_sec_title:
                    collaps_main_title_mass.append(its.get_text().replace('\n', ''))
                block_sec_info = item.find_all(class_='section__info')
                for it in block_sec_info:
                    # block_sec_info_mass.append(it.get_text().replace('\n', '').replace('\xa0', ' '))
                    try:
                        collaps_main.append(
                            {collaps_main_title_mass[fgh]: it.get_text().replace('\n', '').replace('\xa0', ' ')})
                    except IndexError:
                        collaps_main.append({'': it.get_text().replace('\n', '').replace('\xa0', ' ')})
                    fgh = fgh +1
            #     if(block_sec_title != None):
            #         block_sec_title = item.find(class_='section__title').get_text()
            #         block_sec_info= item.find(class_='section__info').get_text()
            #         collaps_main.append({block_sec_title:block_sec_info})
                collaps_data[block_info_title] = collaps_main
                collaps_main = []
            #####парсинг таблицы
            conteiner_table= infos.find_all('div', class_="container")
            if conteiner_table != None:
                conteiner_table = infos.find_all('div', class_="container")

                ###################################################
                #Парсинг значений таблицы
                for tb in conteiner_table:
                    # может быть несколько тайтлов\ пока только один
                    row_block_info = tb.find_all(class_ = 'row blockInfo')
                    for rower in row_block_info:
                        tit = rower.find(class_ = 'blockInfo__title').get_text().strip()

                    block_info = tb.find_all(class_='blockInfo__section')
                    for bs in block_info:
                        cont_sec_title = bs.find_all(class_='section__title')
                        for its in cont_sec_title:
                            cont_main_title_mass.append(its.get_text().strip().replace('\n', ''))
                        cont_sec_info = bs.find_all(class_='section__info')
                        for its in cont_sec_info:
                            try:
                                titls_table_main.append(
                                    {cont_main_title_mass[j]: its.get_text().replace('\n', '').replace('\xa0',
                                                                                                       ' ').strip()})
                            except IndexError:
                                titls_table_main.append(
                                    {'': its.get_text().replace('\n', '').replace('\xa0', ' ').strip()})

                            j = j + 1
                        conteiner_titls_data[tit] = titls_table_main
                    t = j
                    #Поиск всех элементов таблицы
                    tablos = tb.find_all('table')
                    for tbn in tablos:
                        c_th = tbn.find_all('th')
                        for th_items in c_th:
                            th_text = th_items.get_text().strip()
                            th_mass.append(th_text)

                        c_td = tbn.find_all('td')
                        for td_items in c_td:
                            td_text = td_items.get_text().strip()
                            try:
                                conteiner_text.append({th_mass[i]: td_text})
                            except Exception:
                                conteiner_text.append({'': td_text})
                            i += 1

                        table_data[cont_main_title_mass[t]] = conteiner_text
                        t = t + 1
                        conteiner_text = []
        collaps_data.update(conteiner_titls_data)
        collaps_data.update(table_data)
        return collaps_data


def other_info():
    i = 0
    HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
                          ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
    for title, link in all_link().items():
        req = requests.get(url=link, headers=HEADERS)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        test = main_info_body(soup)
        i += 1
        if i == 3:
            break
    return test
#
# print(other_info())

def documents():
    block_info_title = []
    infos = []
    sec_attrib = []
    sec_value = []
    col_data = []
    data= {}
    files_links = {}
    i = 0
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
                      ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
    link = 'https://zakupki.gov.ru/epz/order/notice/ea20/view/documents.html?regNumber=0124200000623001098'
    req = requests.get(url=link, headers=HEADERS)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    try:
        col_sm_12 = soup.find_all(class_ ='col-sm-12 blockInfo')
        for col in col_sm_12:
            titles = col.find(class_='blockInfo__title').get_text().strip()
            block_info_title.append(titles)

            try:
                section_value = col.find_all(class_='section__value docName')
                for sec in section_value:
                    infos.append(sec.get_text().strip())
                # sec_atrribs = col.find_all(class_ = 'section__attrib')
                # for atr in sec_atrribs:
                #     sec_attrib.append(atr.get_text().strip())
                #######################LINKS##########################
                link_of_files = col.find_all(class_='blockFilesTabDocs')
                for lux in link_of_files:
                    luxit = lux.find_all('a')
                    for links in luxit:
                        if 'download' in links.get('href'):
                            linkl = links.get('href')
                            titk = links.get('title')
                            files_links[titk] = linkl
                    if len(files_links) > 0:
                        os.makedirs(titles)
                        for title, url in files_links.items():
                            response = requests.get(url, headers=HEADERS)
                            with open(f'{titles}/{title}', "wb") as f:
                                f.write(response.content)
                        files_links = {}

                #############################################################
                sec_values = col.find_all(class_= 'section__value')
                for val in sec_values:
                    sec_value.append(val.get_text().strip())
                #     i= i + 1
                col_sm = col.find_all(class_ = 'col-sm')
                for col_12 in col_sm:
                    col_data.append(col_12.get_text().strip().replace('\n',''))
                infos.append(sec_value)
                infos.append(col_data)
                data[titles] = infos
                infos = []
                sec_value = []
                col_data = []

            except Exception:
                sec_titl = col.find_all(class_ = 'section__title')
                for ttl in sec_titl:
                    col_data.append(ttl.get_text().strip())
                data[titles] = col_data
                infos = []
                sec_value = []
                col_data = []



            #Дописать эту функциюю


    except Exception:
        pass
    # return block_info_title
    return data


def Test_Json():
    with open("docs.json", "a", encoding="utf-8") as file:
        json.dump(documents(), file, indent=4, ensure_ascii=False)
Test_Json()
#######################################################################

#############################################
#!!!!!!!!!!!!!!!!!!!!!!!Добавить conteiner Этого класса!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




#########################################################################
#JSON#####
def Make_Json():
    global_dict = {}
    global_dict.update(parse_head())
    global_dict.update(main_info_body())
    global_dict.update(collapse_element())
    with open("all_info_test.json", "a", encoding="utf-8") as file:
        json.dump(global_dict, file, indent=4, ensure_ascii=False)
#######################################################################
# Make_Json()

# print(parse_head())
# print(main_info_body())
# print(collapse_element())
# for element in data_td:
#     element = element.split(' ')
# stringus = 'СварочныйаппаратНеобходимоенапряжениесети380ВСварочныйток'
# new_set = re.findall('[A-ZА-Я][^A-ZА-Я]*', stringus)
# print(new_set)



# data.append({all_table_info:data_td})

# for row in table_tr:
#     table_td = table.find_all('td')
#     row_data = [cell.get_text(strip=True) for cell in table_td]
#     data.append(row_data)
#
# with open('output.csv', 'w',  encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(list_info)
#
# df = pd.DataFrame(new_dict)
# df.to_excel(f'TEST.xlsx', index=False)

# test = table.find(class_ ='truInfo_126739907')
# print(test)

# col_9 = soup.find_all(class_='col-9 mr-auto')
# for values in col_9:
#     title_text = values.find(class_= 'common-text__title')
#     value_text = values.find(class_= 'common-text__value')
