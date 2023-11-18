from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QComboBox
import sys
import retro
import numpy as np


class Mario(QWidget):
    def __init__(self, level, speed):
        super().__init__()
        self.setWindowTitle('Mario')

        self.env = retro.make(game='SuperMarioBros-Nes', state=f'Level{level + 1}-1')
        self.screen_image = self.env.reset()
        self.screen_width = self.screen_image.shape[0] * 2
        self.screen_height = self.screen_image.shape[0] * 2

        self.setFixedSize(self.screen_width, self.screen_height)

        self.key_up = False
        self.key_down = False
        self.key_left = False
        self.key_right = False
        self.key_a = False
        self.key_b = False

        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.update_screen()

        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.timer)
        if speed == 0:
            self.qtimer.start(1000 // 30)
        elif speed == 1:
            self.qtimer.start(1000 // 60)
        else:
            self.qtimer.start(1000 // 144)

    def tile_map(self):
        #타일 맵 아직 미완
        ram = self.env.get_ram()

        full_screen_tiles = ram[0x0500:0x069F + 1]  # 1차원 타일 데이터 정보
        full_screen_tile_count = full_screen_tiles.shape[0]  # 타일 전체 길이
        print(full_screen_tile_count)

        # p1                                             13*16
        full_screen_page1_tiles = full_screen_tiles[:full_screen_tile_count // 2].reshape((-1, 16))  # 스크린에서 보이는 화면
        full_screen_page2_tiles = full_screen_tiles[full_screen_tile_count // 2:].reshape((-1, 16))  # 스크린에서는 안보이지만
        # ppu 스크롤링을 하기 위해 미리 생성하는 화면

        # 16px,16px을 덛붙인다.               메모리 상에 있는 정보를 2페이지를 가져온다.           x축 기준으로 붙인다.
        full_screen_tiles = np.concatenate((full_screen_page1_tiles, full_screen_page2_tiles), axis=1).astype(np.int)

        print(full_screen_tiles)

        # 앵글을 구하기 위한 재료들 23, 24
        current_screen_in_level = ram[0x71A]  # 나누어져 있는 페이지 번호
        screen_x_position_in_level = ram[0x071C]  # 스크린 페이지 안에 있는 픽셀 단위 좌표값

        # offset은 픽셀 단위로 계산 - 2장의 픽셀이 들어 있으니 각 256px, 256px = 512px
        screen_x_position_offset = (256 * current_screen_in_level + screen_x_position_in_level) % 512
        # 256px 마다 페이지 번호 이동

        # 마리오 위치. what? screen_x_position_in_level//16? -
        # 표현하는 타일은 16x16px 값으로 이루어져 있다.
        # 그림에 표현하기 위해서 16px이 움직일때 마다 마리오가 움직여야한다는 것을 보여 줘야 한다.
        # 따라서 위치에 16을 나누어 주면 몇칸 움직였는지 알 수 있다.
        start_x = screen_x_position_offset // 16

        # 네모 하나당 16*16 픽셀
        # 화면이 잘려질 수 있어서 full_screen_tils을 뒤에 덧붙인다.
        # 오른쪽 위 부터 왼쪽 아래 채우기 - 타일 배치
        screen_tilss = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:, start_x:start_x + 16]

        return screen_tilss

    def timer(self):
        self.env.step(np.array([self.key_b, 0, 0, 0, self.key_up, self.key_down, self.key_left, self.key_right, self.key_a]))
        self.update_screen()

    def update_screen(self):
        self.screen_image = self.env.get_screen()

        self.screen_qimage = QImage(self.screen_image, self.screen_image.shape[1], self.screen_image.shape[0], QImage.Format.Format_RGB888)
        self.screen_pixmap = QPixmap(self.screen_qimage)
        self.screen_pixmap = self.screen_pixmap.scaled(self.screen_width, self.screen_height, Qt.AspectRatioMode.IgnoreAspectRatio)

        self.screen_label.setPixmap(self.screen_pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up:
            self.key_up = True
        if key == Qt.Key.Key_Down:
            self.key_down = True
        if key == Qt.Key.Key_Left:
            self.key_left = True
        if key == Qt.Key.Key_Right:
            self.key_right = True
        if key == Qt.Key.Key_A:
            self.key_a = True
        if key == Qt.Key.Key_B:
            self.key_b = True

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up:
            self.key_up = False
        if key == Qt.Key.Key_Down:
            self.key_down = False
        if key == Qt.Key.Key_Left:
            self.key_left = False
        if key == Qt.Key.Key_Right:
            self.key_right = False
        if key == Qt.Key.Key_A:
            self.key_a = False
        if key == Qt.Key.Key_B:
            self.key_b = False


class MarioGYM(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mario GYM')
        self.setFixedSize(360, 240)

        self.mario_button = QPushButton(self)
        self.mario_button.setText('Super Mario Bros.')
        self.mario_button.setGeometry(120, 20, 120, 40)
        self.mario_button.clicked.connect(self.run_mario)

        self.mario_ai_button = QPushButton(self)
        self.mario_ai_button.setText('Mario GYM')
        self.mario_ai_button.setGeometry(120, 70, 120, 40)

        self.mario_replay_button = QPushButton(self)
        self.mario_replay_button.setText('Replay')
        self.mario_replay_button.setGeometry(120, 120, 120, 40)

        self.game_level_combo_box = QComboBox(self)
        self.game_level_combo_box.addItem('Level 1')
        self.game_level_combo_box.addItem('Level 2')
        self.game_level_combo_box.addItem('Level 3')
        self.game_level_combo_box.addItem('Level 4')
        self.game_level_combo_box.addItem('Level 5')
        self.game_level_combo_box.addItem('Level 6')
        self.game_level_combo_box.addItem('Level 7')
        self.game_level_combo_box.addItem('Level 8')
        self.game_level_combo_box.setGeometry(120, 170, 120, 20)

        self.game_speed_combo_box = QComboBox(self)
        self.game_speed_combo_box.addItem('보통 속도')
        self.game_speed_combo_box.addItem('빠른 속도')
        self.game_speed_combo_box.addItem('최고 속도')
        self.game_speed_combo_box.setGeometry(120, 200, 120, 20)

    def run_mario(self):
        self.mario = Mario(self.game_level_combo_box.currentIndex(), self.game_speed_combo_box.currentIndex())
        self.mario.show()
        self.hide()


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    mario_gym = MarioGYM()
    mario_gym.show()
    sys.exit(app.exec())