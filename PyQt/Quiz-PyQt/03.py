'''
[도전과제2]
[사각형 가이드]
사각형 크기 (50 x 50)
사각형 색 (파랑, 없음, 없음, 빨강)

[그래프 가이드]
원 반지름 (25)
원 색상 윗층 - (청록, 흰색, 청록) , 아랫층 - (회색)
선 색상 (빨강, 파랑, 빨강)
선을 먼저 그리고, 원 그리기
원 중심 좌표 = 왼쪽 위 좌표 + 반지름
'''

import sys
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt as qt
from PyQt5.QtWidgets import QApplication, QWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 창 크기 조절
        self.setFixedSize(200, 300)  # 1024 x 768
        # 창 제목 설정
        self.setWindowTitle('GA-lab_Mario')
        # 창 띄우기
        self.show()

    # 창이 업데이트 할때 마다 실행되는 함수
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        #1
        painter.drawRect(0, 51, 50, 50)
        painter.setPen(QPen(qt.black, 1.0, qt.SolidLine))
        painter.setBrush(QBrush(QColor.fromRgb(255, 0, 0)))

        #2
        painter.drawRect(0, 0, 50, 50)
        painter.setPen(QPen(qt.black, 1.0, qt.SolidLine))
        painter.setBrush(QBrush(QColor.fromRgb(255, 255, 255)))

        #3
        painter.drawRect(51, 51, 50, 50)
        painter.setPen(QPen(qt.black, 1.0, qt.SolidLine))
        painter.setBrush(QBrush(QColor.fromRgb(255, 255, 255)))

        #4
        painter.drawRect(51, 0, 50, 50)
        painter.setPen(QPen(qt.black, 1.0, qt.SolidLine))
        painter.setBrush(QBrush(QColor.fromRgb(0, 0, 255)))

        # # 팬 설정()테두리
        # painter.setPen(QPen(qt.blue, 2.0, qt.SolidLine))
        # # 선그리기
        # painter.drawLine(0, 10, 200, 100)
        #
        #
        # # RGB 색상으로 펜 설정
        # painter.setPen(QPen(QColor.fromRgb(255, 0, 0), 3.0, qt.solidLine))
        #
        # # 브러쉬 설정()체우기
        # painter.setBrush(QBrush(qt.blue))
        #
        # # 직사각형
        # painter.drawRect(0, 100, 100, 100)
        # painter.setPen(QPen(qt.black, 1.0, qt.SolidLine))
        #
        # # RGB 색상으로 브러쉬 설정
        # painter.setBrush(QBrush(QColor.fromRgb(0, 255, 0)))
        #
        # # 타원 그리기
        # painter.drawEllipse(100, 100, 100, 100)
        #
        # painter.setPen(QPen(qt.cyan, 1.0, qt.SolidLine))
        # painter.setBrush(qt.NoBrush)
        #
        # # 텍스트 그리기
        # painter.drawText(0, 250, 'abcd')

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())