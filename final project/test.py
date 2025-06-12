from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QFrame, QSplitter,
    QApplication
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        hbox = QHBoxLayout(self)

        # 左上區塊
        left_top = QFrame(self)
        left_top.setFrameShape(QFrame.StyledPanel)
        left_top.setStyleSheet("QWidget { background-color: %s }" 
            % QColor(50, 50, 50).name())

        # 左下區塊
        left_bottom = QFrame(self)
        left_bottom.setFrameShape(QFrame.StyledPanel)
        left_bottom.setStyleSheet("QWidget { background-color: %s }" 
            % QColor(80, 80, 80).name())

        # 右邊區塊
        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)
        right.setStyleSheet("QWidget { background-color: %s }" 
            % QColor(0, 0, 0).name())

        # 左側垂直分割（左上、左下）
        splitterLeft = QSplitter(Qt.Vertical)
        splitterLeft.addWidget(left_top)
        splitterLeft.addWidget(left_bottom)

        # 主分割器（左側與右側）
        splitterMain = QSplitter(Qt.Horizontal)
        splitterMain.addWidget(splitterLeft)
        splitterMain.addWidget(right)

        hbox.addWidget(splitterMain)
        self.setLayout(hbox)
        self.resize(1500, 900) 
        self.setWindowTitle('QSplitter')
        self.show()

        splitterMain.setSizes([10, 20])  # 👉 設定左:右 2:5 比例

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())