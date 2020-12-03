import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QTableWidgetItem
from addEditCoffeeForm import Ui_Dialog
from main_ui import Ui_MainWindow


class Add(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Add, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Добавить сорт')
        self.pushButton.clicked.connect(self.close)
        self.con = sqlite3.connect('coffee.sqlite')
        self.id = list(self.con.cursor().execute("""SELECT id FROM grades_of_coffee"""))[::-1][0][0] + 1
        roasting = [x[0] for x in list(self.con.cursor().execute("""SELECT title FROM roasting""").fetchall())]
        types = [x[0] for x in list(self.con.cursor().execute("""SELECT title FROM ground_or_in_grains""").fetchall())]
        self.comboBox.addItems(roasting)
        self.comboBox_2.addItems(types)
        self.label_5.hide()

    def close(self):
        cur = self.con.cursor()
        roasting = list(cur.execute("""SELECT id FROM roasting WHERE title=?""",
                                    (f'{self.comboBox.currentText()}',)).fetchall())[0][0]
        type = list(cur.execute("""SELECT id FROM ground_or_in_grains WHERE title=?""",
                                (f'{self.comboBox_2.currentText()}',)).fetchall())[0][0]
        try:
            print(self.id, f'{self.lineEdit.text()}', roasting, type, f'{self.lineEdit_2.text()}',
                  self.lineEdit_3.text(), self.lineEdit_4.text())
            cur.execute("""INSERT INTO grades_of_coffee(id, title, roasting, ground_or_in_grains, taste, price, volume)
                           VALUES(?, ?, ?, ?, ?, ?, ?)""",
                        (self.id, f'{self.lineEdit.text()}', roasting, type, f'{self.lineEdit_2.text()}',
                         self.lineEdit_3.text(), self.lineEdit_4.text()))
            self.con.commit()
            self.close()
        except Exception as e:
            print(e)
            self.label_5.show()


class Update(QDialog, Ui_Dialog):
    def __init__(self, parent=None, coffee=None):
        super(Update, self).__init__(parent)
        self.setupUi(self)
        self.coffee = coffee
        self.setWindowTitle('Редактировать сорт')
        self.pushButton.clicked.connect(self.close)
        self.con = sqlite3.connect('coffee.sqlite')
        self.label_5.hide()
        self.lineEdit.setText(coffee[1])
        self.lineEdit_2.setText(coffee[4])
        self.lineEdit_3.setText(str(coffee[5]))
        self.lineEdit_4.setText(str(coffee[6]))
        roasting = list(self.con.cursor().execute("""SELECT title FROM roasting WHERE id = ?""",
                                                  (coffee[2],)).fetchall())[0][0]
        roastings = [x[0] for x in list(self.con.cursor().execute("""SELECT title FROM roasting""").fetchall())]
        self.comboBox.addItems(roastings)
        self.comboBox.setCurrentText(roasting)
        type = list(self.con.cursor().execute("""SELECT title FROM ground_or_in_grains WHERE id = ?""",
                                              (coffee[3],)).fetchall())[0][0]
        types = [x[0] for x in list(self.con.cursor().execute("""SELECT title FROM ground_or_in_grains""").fetchall())]
        self.comboBox_2.addItems(types)
        self.comboBox.setCurrentText(type)

    def close(self):
        cur = self.con.cursor()
        try:
            roasting = list(self.con.cursor().execute("""SELECT id FROM roasting WHERE title = ?""",
                                                      (f'{self.comboBox.currentText()}',)))[0][0]
            type = list(self.con.cursor().execute("""SELECT id FROM ground_or_in_grains WHERE title = ?""",
                                                  (f'{self.comboBox_2.currentText()}',)))[0][0]
            cur.execute("""UPDATE grades_of_coffee
                           SET title = ?, roasting = ?, ground_or_in_grains = ?, taste = ?, price = ?, volume = ? 
                           WHERE id = ?""",
                        (f'{self.lineEdit.text()}', roasting, type, f'{self.lineEdit_2.text()}', self.lineEdit_3.text(),
                         self.lineEdit_4.text(), self.coffee[0]))
            self.con.commit()
            self.close()
        except Exception as e:
            print(e)
            self.label_5.show()


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Кофе')
        self.con = sqlite3.connect('coffee.sqlite')
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.update)
        self.fill_table()

    def fill_table(self):
        cur = self.con.cursor()
        result = list(cur.execute("""SELECT * FROM grades_of_coffee""").fetchall())
        for i in range(len(result)):
            result[i] = list(result[i])
            result[i][2] = list(cur.execute("""SELECT title FROM roasting
            WHERE id = ?""", (f'{result[i][2]}',)).fetchall())[0][0]
            result[i][3] = list(cur.execute("""SELECT title FROM ground_or_in_grains
            WHERE id = ?""", (f'{result[i][3]}',)).fetchall())[0][0]
        print(result)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                    'описание вкуса', 'цена', 'объем упаковки'])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add(self):
        dialog = Add(self)
        dialog.exec_()
        self.tableWidget.clear()
        self.fill_table()

    def update(self):
        try:
            coffee = list(self.con.cursor().execute("""SELECT * FROM grades_of_coffee WHERE title = ?""",
                                                    (f'{self.tableWidget.currentItem().text()}',)).fetchall())[0]
            dialog = Update(self, coffee)
            dialog.exec_()
            self.tableWidget.clear()
            self.fill_table()
        except Exception as e:
            print(e)
            pass


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec())
