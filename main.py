
from PyQt5 import QtWidgets, uic,QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
soup = 0
from Parser import *

mass = ['0373100119621000005', '0373100112518000004', '0373100119621000004']
class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        uic.loadUi('untitled.ui',self)
        self.Parse_but.clicked.connect(self.test)

        # self.new_win_but.clicked.connect(self.new_win)
    def test(self):
        par = Parser()
        for i in mass:
            try:
                par.agent(i)
                par.Make_Json()
                tr = par.status_log()
            except Exception as e:
                self.textBrowser.append(f"Ошибка при обработке элемента {i}: {e}")
            else:
                continue
       


    # def new_win(self):
    #     self.Form = QtWidgets.QWidget()
    #     self.ui.setipUi(self.Form)
    #     self.Form.show()
    #     # uic.loadUi('new_win.ui', self)

def application():
    app = QApplication(sys.argv)
    window = mywindow()

    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    application()



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


