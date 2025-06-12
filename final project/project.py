from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QApplication, QCalendarWidget, QSizePolicy
)
from PyQt5.QtCore import (QTimer, Qt, QDate)
from PyQt5 import QtWidgets, QtGui
import queue
import sys

class Project(QWidget):
    next_exam_time = queue.Queue()
    def __init__(self):
        # 下次考試時間 queue，裡面放的是距今天要考的天數（或直接放 QDate 也可以）
        super().__init__()
        self.UI()

    def UI(self):
        h_layout = QtWidgets.QHBoxLayout()

        # 左側按鈕區
        left_widget = QWidget()
        v_item = QVBoxLayout(left_widget)
        self.label1 = QLabel('1')
        self.btn2 = QPushButton('2')
        self.btn3 = QPushButton('番茄鐘')
        
        v_item.addWidget(self.label1, 1)
        v_item.addWidget(self.btn2,   1)
        v_item.addWidget(self.btn3,   1)
        for w in (self.label1, self.btn2, self.btn3):
            w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.label1_text()
        #self.btn3.clicked.connect(self.label1_text)

        # 右側日曆區
        right_widget = QWidget()
        v_calendar = QVBoxLayout(right_widget)
        self.cal = QCalendarWidget()
        self.cal.setGridVisible(True)
        self.cal.clicked[QDate].connect(self.showDate)
        self.cal.clicked[QDate].connect(self.showdatedetail)
        v_calendar.addWidget(self.cal)

        self.lbl = QLabel()
        today = self.cal.selectedDate()
        self.lbl.setText(today.toString())
        v_calendar.addWidget(self.lbl)

        h_layout.addWidget(left_widget)
        h_layout.addWidget(right_widget)
        self.setLayout(h_layout)

        self.setWindowTitle('final project www')
        self.resize(600, 400)
        self.show()

        # **在這裡呼叫一次，先把 queue 裡的日期標紅**
        self.highlight_exam_dates()

    def showDate(self, date):
        self.lbl.setText(date.toString())

    def label1_text(self):
        if self.next_exam_time.empty():
            self.label1.setText('no next exam')
        else:
            # 只顯示 queue 最前面那個天數
            self.label1.setText(str(self.next_exam_time.queue[0][1].toString()))

    def highlight_exam_dates(self):
        """把 queue 裡的每個天數（以今天為基準）在 calendar 上標紅底"""
        # 建立紅色底的格式
        fmt = QtGui.QTextCharFormat()
        fmt.setBackground(QtGui.QBrush(Qt.red))

        for exam_date in list(self.next_exam_time.queue):
            self.cal.setDateTextFormat(exam_date[1], fmt)
    
    def showdatedetail(self, date):
        self.nw = Date_detail(date)
        ex.nw.show_detail()
        self.nw.show()


class Date_detail(QWidget):
    date = QDate()
    def __init__(self, date):
        super().__init__()
        self.setWindowTitle(date.toString())
        self.date = date
        self.resize(300, 200) 
        self.UI()
        
    def UI(self):
        #垂直容器
        v_layout =  QVBoxLayout()
        label_addnew = QWidget()
        to_do = QWidget()
        label_addnew_item = QtWidgets.QHBoxLayout(label_addnew)
        to_do_item = QtWidgets.QVBoxLayout(to_do)

        self.label1 = QLabel('今日待辦:')
        self.btn2 = QPushButton('加入新計畫/行程')
        self.label4 = QLabel()

        label_addnew_item.addWidget(self.label1)
        label_addnew_item.addWidget(self.btn2)
        to_do_item.addWidget(self.label4)

        v_layout.addWidget(label_addnew, 1)
        v_layout.addWidget(to_do, 3)
        self.setLayout(v_layout)
        self.show()
        self.btn2.clicked.connect(self.select_mode)

    def select_mode(self):
        self.nw = Select_mode(self.date)
        self.nw.show()

    def get_date(self):
        return self.date
    
    def show_detail(self):
        t = []
        for i, d, ed, p, c, m in Project.next_exam_time.queue:
            if self.date == d:
                t.append(i)
                t.append('\n')
        if not t:
            self.label4.setText("無")
        else:
            self.label4.setText("".join(str(x) for x in t))

            
        

class Select_mode(QWidget):
    date = QDate()
    def __init__(self, date):
        super().__init__()
        self.setWindowTitle('select mode')
        self.setFixedSize(250, 150)
        self.date = date
        self.UI()
    def UI(self):
        layout = QVBoxLayout(self)

        self.label1 = QLabel('新增', self)
        self.btn2 = QPushButton('讀書計劃', self)
        self.btn3 = QPushButton('行程', self)

        layout.addWidget(self.label1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)

        self.setLayout(layout)

        self.btn2.clicked.connect(self.study_plan)

    def study_plan(self):
        self.nw = Study_plan(self.date)
        self.nw.show()        
        self.close()

class Study_plan(QWidget):
    date = QDate()
    def __init__(self, date):
        super().__init__()
        self.setWindowTitle('讀書計畫')
        self.resize(300, 200)
        self.date = date
        self.UI()

    def UI(self):
        self.content = QtWidgets.QGridLayout()
        self.plan_name_label = QLabel('項目名稱')
        self.plan_name_input = QtWidgets.QLineEdit(self)
        self.add = QPushButton('加入', self)
        self.deadline_label = QLabel('結束日')
        self.deadline_y = QtWidgets.QComboBox(self)
        self.deadline_y.addItems([str(i) for i in range(2025, 2036)])
        self.deadline_m = QtWidgets.QComboBox(self)  
        self.deadline_m.addItems([str(i) for i in range(1, 13)])
        self.deadline_d = QtWidgets.QComboBox(self)  
        self.deadline_d.addItems([str(i) for i in range(1, 32)])
        self.preread_label = QLabel('預讀頁數')
        self.preread_input = QtWidgets.QComboBox(self)  
        self.preread_input.addItems([str(i) for i in range(1, 1001)])
        self.cycle_label = QLabel('每隔幾天複習')
        self.cycle_input = QtWidgets.QComboBox(self)  
        self.cycle_input.addItems([str(i) for i in range(1, 1001)])
        self.memory = QtWidgets.QCheckBox('記憶曲線', self)
        self.memory.toggled.connect(lambda checked: self.cycle_input.setDisabled(checked))

        self.content.addWidget(self.plan_name_label, 0, 0)
        self.content.addWidget(self.plan_name_input, 0, 1)
        self.content.addWidget(self.add, 0, 2)

        self.content.addWidget(self.deadline_label, 1, 0)
        self.content.addWidget(self.deadline_y, 1, 1)
        self.content.addWidget(self.deadline_m, 1, 2)
        self.content.addWidget(self.deadline_d, 1, 3)
        self.content.addWidget(self.preread_label, 2, 0)
        self.content.addWidget(self.preread_input, 2, 1)
        self.content.addWidget(self.cycle_label, 3, 0)
        self.content.addWidget(self.cycle_input, 3, 1)
        self.content.addWidget(self.memory, 4, 0)

        self.setLayout(self.content)

        self.add.clicked.connect(self.add_plan)

    def add_plan(self):
        li = list()
        li.append(self.plan_name_input.text())
        li.append(self.date)
        li.append(QDate(int(self.deadline_y.currentText()),int(self.deadline_m.currentText()),int(self.deadline_d.currentText())))
        li.append(self.preread_input.currentText())
        li.append(self.cycle_input.currentText())
        li.append(self.memory.isChecked())        
        Project.next_exam_time.put(li)        
        self.close()
        ex.highlight_exam_dates()
        ex.nw.show_detail()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Project()
    #ex.show()
    sys.exit(app.exec_())
