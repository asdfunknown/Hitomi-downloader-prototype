import urllib.request
import lxml.html
import requests
import string
import sys
import os
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QWidget, QMainWindow, QLabel, QToolTip, QMessageBox
from PyQt5.QtGui import QIcon, QFont

#1504291

class downloader(QMainWindow):

    doujinshi = ""
    foldername = ""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont("SansSerif", 9))

        self.statusBar().showMessage("Ready")

        fnamedes = QLabel("Name", self)
        fnamedes.move(25, 50)

        uninumdes = QLabel("Unique\nnumber", self)
        uninumdes.move(25, 100)

        fnameset = QLineEdit(self)
        fnameset.setToolTip("This is where you put folder\'s name")
        fnameset.move(75,50)
        fnameset.textChanged[str].connect(self.onChangedfname)

        uninumset = QLineEdit(self)
        uninumset.setToolTip("This is where you put numbers")
        uninumset.move(75,100)
        uninumset.textChanged[str].connect(self.onChangeduninum)

        initbtn = QPushButton("download", self)
        initbtn.move(200, 110)
        initbtn.resize(initbtn.sizeHint())
        initbtn.released.connect(self.downloading)

        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("Doujinshi downloader")
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def onChangedfname(self, fname):
        print(fname)
        global foldername 
        foldername = fname

    def onChangeduninum(self, uninum):
        global doujinshi 
        doujinshi = uninum

    def downloading(self):
        #Debug
        print("Welcome to the debug world bozisex")
        print("Checking the folder's name and the values : " + foldername + "," + doujinshi)
        #Debug
        if not os.path.exists(foldername):
            os.makedirs(foldername)
            print("Checking if there is already a folder exists with the same name.. no! So we created one")
            print("Let's change the status to downloading")
            self.statusBar().showMessage("Downloading")
        else:
            print("Checking if there is already a folder exists with the same name.. Yes. It will occur an error")
        try:
            page = requests.get("https://sora1.la/r/" + doujinshi + "/1")
            inspect = lxml.html.fromstring(page.text)
            main = inspect.xpath('//*[@id="1"]/img')[0]
            main2 = inspect.xpath('//*[@id="pagination-page-bottom"]/span')[0]
            result = lxml.html.tostring(main)
            result2 = lxml.html.tostring(main2)
            changetostring = result.decode()
            changetostring2 = result2.decode()
            trimlinkstart = result.find(b"data-src=\"https://") + len(b"data-src=\"https://")
            trimlinkend = result.find(b"1.jpg")
            trimpagestart = result2.find(b"1 / ") + len(b"1 / ")
            trimpageend = result2.find(b"</span>")
            link = changetostring[trimlinkstart:trimlinkend]
            page = changetostring2[trimpagestart:trimpageend]
            print(page)
            print(link + "1.jpg")
            intpage = int(page)
            linken = urllib.request.quote(link)
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            for x in range(1, intpage+1):
                urllib.request.urlretrieve(f"https://{linken}{x}.jpg", f"{foldername}/{x}.jpg")

            QMessageBox.about(self, "Completed", "Download Completed")
            self.statusBar().showMessage("Ready")
            return
        except:
            QMessageBox.about(self, "Error", "Error confirmed!\nplease check again whether you put wrong numbers or wrong folder name.\nAlso same folder name can occur an error.")
            self.statusBar().showMessage("Ready")
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = downloader()
    sys.exit(app.exec_())