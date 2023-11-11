import sys
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle('MyApp')

    #추가 그리기 - event 함수를 사용
    def paintEvent(self, event) -> None:

        #turtle 처럼 Painter를 가져온다.
        painter = QPainter()
        painter.begin(self) #그리기 시작

        #그리기 실행 구간

        #Qpan(컬러, 두깨, 선종류)
        painter.setPen(QPen(Qt.GlobalColor.blue, 2.0, Qt.PenStyle.SolidLine)) #팬 세팅
        painter.drawLine(0, 10, 200, 100) #세팅한 팬으로 좌표를 따라 그려라 (x1,y1,x2,y2)

        #세세한 색상 - QColor.fromRgb(r, g, b)
        painter.setPen(QPen(QColor.fromRgb(255, 0, 0), 3.0, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.blue)) #안에 있는 색상을 채워라
        painter.drawRect(0, 100, 100, 100) #박스 위치와 크기 지정(x1, y1, x2, y2)

        painter.setPen(QPen(Qt.GlobalColor.black, 1.0, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.green))
        painter.drawEllipse(100, 100, 100, 100) #타원 그리기 (x1, y1, x2, y2)

        #text
        painter.setPen(QPen(Qt.GlobalColor.cyan, 1.0, Qt.PenStyle.SolidLine))
        painter.setBrush(Qt.BrushStyle.NoBrush) #색상 컬러 채워지지 않음 - 음? 원래 지정안하면 채워지지 않는거아닌가? -아님
        #no brush를 사용하지 않는다면 기존에 있던 Brush컬러가 그래도 사용되게 된다.
        painter.drawText(0, 250, 'abcd') #(x,y)좌표, text

        painter.end() #그리기 끝

def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
