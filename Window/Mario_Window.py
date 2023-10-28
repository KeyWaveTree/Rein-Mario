import sys
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

import retro #RAM 정보 불러오기

class Mario_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('')

        #환경 - openAi에서 제공하는 retro - 게임을 RAM 정보를 가져와 셋팅한다. state는 1-1
        self.env = retro.make(game='SuperMarioBros-Nes', state='level1-1')
        self.env.reset() #환경을 초기화 해준다.

        self.screen_image = self.env.get_screen() #환경 스크린 정보를 가지고 온다.
        self.screen_width =self.screen_image.shape[0] #스크린 정보에서 너비의 길이를
        self.screen_height =self.screen_image.shape[1]# 스크린 정보에서 높이의 길이를

        self.setFixedSize(self.screen_width, self.screen_height) #윈도우 창 공간을 고정시켜 준다.


        #동영상을 처리하는 과정과 똑같음
        self.screen_label = QLabel(self)

        self.screen_qimage = QImage(
            self.screen_image, #게임 이미지 bytes 정보
            self.screen_image.shape[1], #높이정보를 너비정보로
            self.screen_image.shape[0], #너비정보를 높이정보로
            QImage.Format.Format_RGB888 #포멧 - 픽셀 값이 0~255
        )
        #확대 크기
        self.screen_pixmap = QPixmap(self.screen_qimage) #img 자료구조
        self.screen_pixmap = self.screen_pixmap.scaled(
            self.screen_width,
            self.screen_height,
            Qt.AspectRatioMode.IgnoreAspectRatio #이미지 원본 비율 무시
        )

        self.screen_label.setPixmap(self.screen_pixmap)
        self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)

def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)

if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    mario_gym = Mario_Window()
    mario_gym.show()
    sys.exit(app.exec())
