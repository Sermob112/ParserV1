from bs4 import BeautifulSoup
import requests
import urllib3
import locale
import re
import pandas as pd
import json
import os
files_links = {}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0'
                  ' YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
link = 'https://zakupki.gov.ru/epz/order/notice/ea20/view/documents.html?regNumber=0124200000623001832'
req = requests.get(url=link, headers=HEADERS)
src = req.text
soup = BeautifulSoup(src, "lxml")


# file_url = 'https://zakupki.gov.ru/44fz/filestore/public/1.0/download/priz/file.html?uid=F5FD422496BAC03FE05334548D0AB464'
# file_content = requests.get(file_url, headers=HEADERS)
# with open("docx_file.docx", "wb") as f:
#     f.write(file_content.content)


link_razdels = soup.find_all(class_='blockFilesTabDocs')
print(link_razdels)
for kol in link_razdels:
    test = kol.find_all('a')
    for links in test:
        if 'download' in links.get('href'):
            linkl =links.get('href')
            title = links.get('title')
            files_links[title] = linkl
        else:
            pass
i = 0
print(files_links)
print(len(files_links))

# for url in files_links:
#     response = requests.get(url, headers=HEADERS)
#     filename = os.path.basename(url)
#     with open(f'{i}.docx', "wb") as f:
#         f.write(response.content)
#     i = i + 1


   # #######################LINKS##########################
   #              link_of_files = col.find(class_='blockFilesTabDocs').find_all('a')
   #              for links in link_of_files:
   #                  if 'download' in links.get('href'):
   #                      linkl = links.get('href')
   #                      titk = links.get('title')
   #                      files_links[titk] = linkl
   #              if len(files_links) > 0:
   #                  os.makedirs(titles)
   #                  for title, url  in files_links.items():
   #                      response = requests.get(url, headers=HEADERS)
   #                      with open(f'{titles}/{title}', "wb") as f:
   #                          f.write(response.content)
   #              files_links = {}
   #
   #              #############################################################