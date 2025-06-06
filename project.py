from PyQt5 import QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle('oxxo.studio')      # 設定標題
Form.resize(320, 240)                   # 設定長寬尺寸
Form.setStyleSheet('background:#fcc;')  # 使用網頁 CSS 樣式設定背景

print(Form.width())                     # 印出寬度
print(Form.height())                    # 印出高度

Form.show()
sys.exit(app.exec_())