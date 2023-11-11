import retro
import numpy as np

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()

ram = env.get_ram()

full_screen_tiles = ram[0x0500:0x069F + 1] #1차원 타일 데이터 정보
full_screen_tile_count = full_screen_tiles.shape[0] #타일 전체 길이
print(full_screen_tile_count)


                          #p1                                             13*16
full_screen_page1_tiles = full_screen_tiles[:full_screen_tile_count // 2].reshape((-1, 16)) #스크린에서 보이는 화면
full_screen_page2_tiles = full_screen_tiles[full_screen_tile_count // 2:].reshape((-1, 16)) #스크린에서는 안보이지만
#ppu 스크롤링을 하기 위해 미리 생성하는 화면

# 16px,16px을 덛붙인다.               메모리 상에 있는 정보를 2페이지를 가져온다.           x축 기준으로 붙인다.
full_screen_tiles = np.concatenate((full_screen_page1_tiles, full_screen_page2_tiles), axis=1).astype(np.int)

print(full_screen_tiles)

#앵글을 구하기 위한 재료들 23, 24
current_screen_in_level = ram[0x71A] #나누어져 있는 페이지 번호
screen_x_position_in_level = ram[0x071C] #스크린 페이지 안에 있는 픽셀 단위 좌표값

#offset은 픽셀 단위로 계산 - 2장의 픽셀이 들어 있으니 각 256px, 256px = 512px
screen_x_position_offset = (256 * current_screen_in_level + screen_x_position_in_level) % 512
#256px 마다 페이지 번호 이동

#마리오 위치. what? screen_x_position_in_level//16? -
#표현하는 타일은 16x16px 값으로 이루어져 있다.
#그림에 표현하기 위해서 16px이 움직일때 마다 마리오가 움직여야한다는 것을 보여 줘야 한다.
#따라서 위치에 16을 나누어 주면 몇칸 움직였는지 알 수 있다.
start_x = screen_x_position_offset//16
#print(screen_x_position_in_level, screen_x_position_offset) 같은 0이 나옴

#네모 하나당 16*16 픽셀
#화면이 잘려질 수 있어서 full_screen_tils을 뒤에 덧붙인다.
#오른쪽 위 부터 왼쪽 아래 채우기 - 타일 배치
screen_tilss = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:, start_x:start_x +16]

print(screen_tilss)
print(type(screen_tilss))

