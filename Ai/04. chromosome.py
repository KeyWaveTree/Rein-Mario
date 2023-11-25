import numpy as np

def relu(x): return np.maximum(0, x)
#np.exp() e^x
# 너무 작으면 에러가 나므로 하한을 -700정도
def sigmoid(x): return 1.0/(1.0 + np.exp(-np.exp(-np.maximum(-700, x))))

class Chromosome:
    def __init__(self):
        self.w1 = np.random.uniform(low=-1, high=1, size=(13*16, 11)) #정규 범위를 -1~1로
        self.b1 = np.random.uniform(low=-1, high=1, size=(11,))

        self.w2 = np.random.uniform(low=-1, high=1, size=(11, 6))
        self.b2 = np.random.uniform(low=-1, high =1, size=(6,))

        self.distance = 0
        self.max_distance = 0
        self.frames = 0
        self.stop_frames = 0
        self.win = 0
    def predict(self, data):
        layer1 = relu(np.matmul(data, self.w1)+self.b1)
        output = sigmoid(np.matmul(layer1, self.w2)+self.b2)
        result = (output >0.5).astyep(np.int) #0.5이하이면 false, 초과이면 true가 나오는데 이 행렬을 int로 바꿔라(f:0, t:1)

        return result


    def fitness(self):
        score = self.distance ** 1.8
        score -= self.frames ** 1.5
        if self.distance> 50: score+=2500
        if self.win == 1:  score+=1000000
        if score < 1: score=1
        return score

        # 적합도(점수) 기준
        # 1. 많은 거리를 이동할수록 높은 점수
        # 2. 같은 거리를 더 짧은 시간에 도달할수록 점수
        # 3. 조금이라도 앞으로 이동했다면 기본 점수(2500) 획득
        # 4. 클리어한 경우 매우 높은 점수(1000000) 획득
        # 5. 아무리 낮아도 최저 점수(1) 보장

        #최소 점수 - min(max(self.distance -50, 0), 1) 시작 위치는 50 조금이라도 움직였다면 1을 움직이지 않았다면 0을 준다.
        # 더 먼거리를 갈수록 차이가 커진다. - 지수 함수

        # return int(max(self.distance ** 1.8 -  self.frames ** 1.5
        #                +min(max(self.distance - 50, 0), 1) * 2500
        #                + self.win * 1000000, 1))

