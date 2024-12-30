from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import QTimer
import sys

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试QTimer")
        self.label = QLabel("测试中...", self)
        self.setCentralWidget(self.label)
        
        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)  # 1秒
        
        self.counter = 0
        
    def update_label(self):
        self.counter += 1
        self.label.setText(f"计数：{self.counter}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec()) 