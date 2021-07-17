import sys
from PyQt5.QtWidgets import QApplication, QWidget

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        # 창 크기 조절
        self.setFixedSize(1024, 768) #1024 x 768
        # 창 제목 설정
        self.setWindowTitle('GA-lab_Mario')
        # 창 띄우기
        self.show()

    def keyPressEvent(self, event):
        key=event.key()
        print(str(key)+"press")

    def keyReleaseEvent(self, event):
        key=event.key()
        print(str(key)+"relesase")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())