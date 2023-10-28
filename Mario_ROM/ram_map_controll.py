import retro

env = retro.make(game='SuperMarioBros-Nes', state='level1-1')
env.reset() #reset을 안하면 게임 초기 화면으로 - 스테이지에 가는것이 아님

#현제 게임화면에 표시되는 정보를 가져온다.
ram = env.get_ram()
print(ram) #array값
print(type(ram)) #numpy에 ndarray로 표시

#cuurnt tile 정보 -416개 하지만 실제 크기는 288개
#횡 스크롤의 무한 횡 스크롤 방식이다. 