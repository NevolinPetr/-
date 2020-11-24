import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.fill_table()

    def fill_table(self):
        cur = self.con.cursor()
        result = list(cur.execute("""SELECT * FROM coffee""").fetchall())
        for i in range(len(result)):
            result[i] = list(result[i])
            result[i][2] = list(cur.execute("""SELECT title FROM roasting
            WHERE id = ?""", (f'{result[i][2]}',)).fetchall())[0][0]
            result[i][3] = list(cur.execute("""SELECT title FROM type
            WHERE id = ?""", (f'{result[i][3]}',)).fetchall())[0][0]
        print(result)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                    'описание вкуса', 'цена', 'объем упаковки'])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec())
