from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHeaderView
)
from datetime import datetime, timedelta
import sys


# 定義記憶項目類別
class MemoryItem:
    def __init__(self, subject, content):
        self.subject = subject        # 科目
        self.content = content        # 學習內容
        self.learned_at = datetime.now()  # 最後複習時間
        self.repetition = 0           # 複習次數
        self.next_review = self.calculate_next_review()  # 下一次複習時間

    # 根據複習次數計算下一次複習時間（記憶曲線）
    def calculate_next_review(self):
        intervals = [1, 2, 4, 7, 15, 30]
        if self.repetition < len(intervals):
            days = intervals[self.repetition]
        else:
            days = intervals[-1] * 2 ** (self.repetition - len(intervals) + 1)
        return self.learned_at + timedelta(days=days)

    # 執行複習，更新複習次數與下次時間
    def review(self):
        self.repetition += 1
        self.learned_at = datetime.now()
        self.next_review = self.calculate_next_review()

    # 判斷是否需要今天複習
    def is_due_today(self):
        return self.next_review.date() <= datetime.now().date()


# PyQt 主介面
class ReviewApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("記憶曲線複習表")
        self.setGeometry(300, 300, 600, 400)
        self.items = self.load_items()  # 載入複習項目
        self.initUI()

    # 預設複習資料（可替換為檔案載入）
    def load_items(self):
        return [
            MemoryItem("英文", "abandon"),
            MemoryItem("數學", "微積分定義"),
            MemoryItem("物理", "牛頓第二運動定律")
        ]

    # 建立介面
    def initUI(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["科目", "內容", "下一次複習", "已複習次數"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        self.review_btn = QPushButton("✅ 已完成今天複習")
        self.review_btn.clicked.connect(self.mark_reviewed)
        layout.addWidget(self.review_btn)

        self.setLayout(layout)
        self.load_due_items()

    # 載入今天要複習的項目
    def load_due_items(self):
        self.due_items = [item for item in self.items if item.is_due_today()]
        self.table.setRowCount(len(self.due_items))

        for row, item in enumerate(self.due_items):
            self.table.setItem(row, 0, QTableWidgetItem(item.subject))
            self.table.setItem(row, 1, QTableWidgetItem(item.content))
            self.table.setItem(row, 2, QTableWidgetItem(item.next_review.strftime("%Y-%m-%d")))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.repetition)))

    # 標記為已複習，更新內容
    def mark_reviewed(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.information(self, "提示", "請先選擇一項目")
            return

        item = self.due_items[selected]
        item.review()
        QMessageBox.information(self, "完成", f"已更新「{item.subject}」複習進度")
        self.load_due_items()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReviewApp()
    window.show()
    sys.exit(app.exec_())

