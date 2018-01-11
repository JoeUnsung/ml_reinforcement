#######################################################################################
# Game : 1인 핑퐁 게임 머신 러닝 코드
# Date : 2017.05.12
# Created by MIT university
#######################################################################################


import random

from copy import copy, deepcopy

import csv

EMPTY = 0

PLAYER_X = 1

PLAYER_O = 2

DRAW = 3

BOARD_FORMAT = "------------------------------------\n| {0} | {1} | {2} | {3} |\n|-----------------------------------|\n| {4} | {5} | {6} | {7} |\n|-----------------------------------|\n| {8} | {9} | {10} | {11} |\n|-----------------------------------|\n| {12} | {13} | {14} | {15} |\n------------------------------------"

NAMES = [' ', '○', '●']


def printboard(state):
    cells = []

    for i in range(4):

        for j in range(4):
            cells.append(NAMES[state[i][j]].center(6))

    print(BOARD_FORMAT.format(*cells))


def emptystate():
    return [[EMPTY, EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY, EMPTY]]


def gameover(state):
    for i in range(4):

        if state[i][0] != EMPTY and state[i][0] == state[i][1] and state[i][0] == state[i][2] and state[i][0] == state[i][3] :
            return state[i][0]

        if state[0][i] != EMPTY and state[0][i] == state[1][i] and state[0][i] == state[2][i] and state[0][i] == state[3][i]:
            return state[0][i]

    if state[0][0] != EMPTY and state[0][0] == state[1][1] and state[0][0] == state[2][2] and state[0][0] == state[3][3]:
        return state[0][0]

    if state[0][3] != EMPTY and state[0][3] == state[1][2] and state[0][3] == state[2][1] and state[0][3] == state[3][0]:
        return state[0][3]

    for i in range(4):

        for j in range(4):

            if state[i][j] == EMPTY:
                return EMPTY

    return DRAW

class Agent(object):
    def __init__(self, player, verbose=False, lossval=0, learning=True):

        self.values = {}

        self.player = player

        self.lossval = lossval

        self.learning = learning

        self.epsilon = 0.1

        self.alpha = 0.99

        self.prevstate = None

        self.prevscore = 0




    def episode_over(self, winner):

        self.backup(self.winnerval(winner))

        self.prevstate = None

        self.prevscore = 0

    def action(self, state):

        r = random.random()

        if r < self.epsilon:

            move = self.random(state)

        else:

            move = self.greedy(state)


        state[move[0]][move[1]] = self.player

        self.prevstate = self.statetuple(state)

        self.prevscore = self.lookup(state)

        state[move[0]][move[1]] = EMPTY

        return move

    def random(self, state):

        available = []

        for i in range(4):

            for j in range(4):

                if state[i][j] == EMPTY:
                    available.append((i, j))

        return random.choice(available)

    def greedy(self, state):

        maxval = -50000

        maxmove = None

        for i in range(4):

            for j in range(4): ## 다음 수 중 가장 val이 높은 수를 찾기 그리고 그 수의 위치 반환하기

                if state[i][j] == EMPTY:

                    state[i][j] = self.player

                    val = self.lookup(state)

                    state[i][j] = EMPTY

                    if val > maxval:
                        maxval = val

                        maxmove = (i, j)

        self.backup(maxval)

        return maxmove

    def backup(self, nextval):
        if self.prevstate != None and self.learning:
            prevval = self.values[self.prevstate]
            self.values[self.prevstate] += self.alpha * (nextval - self.prevscore)
            Fn = ("D:\\ttt_4_learning.csv")
            w = csv.writer(open(Fn, 'a', newline=''), delimiter=',')
            w.writerow([self.prevstate[0][0],
                        self.prevstate[0][1],
                        self.prevstate[0][2],
                        self.prevstate[0][3],
                        self.prevstate[1][0],
                        self.prevstate[1][1],
                        self.prevstate[1][2],
                        self.prevstate[1][3],
                        self.prevstate[2][0],
                        self.prevstate[2][1],
                        self.prevstate[2][2],
                        self.prevstate[2][3],
                        self.prevstate[3][0],
                        self.prevstate[3][1],
                        self.prevstate[3][2],
                        self.prevstate[3][3],
                        prevval,
                        self.values[self.prevstate]])

    def lookup(self, state):

        key = self.statetuple(state)

        if not key in self.values:
            self.add(key)

        return self.values[key]

    def add(self, state):

        winner = gameover(state)

        tup = self.statetuple(state)

        self.values[tup] = self.winnerval(winner)

    def winnerval(self, winner):

        if winner == self.player:

            return 1

        elif winner == EMPTY:

            return 0.5

        elif winner == DRAW:

            return 0

        else:

            return self.lossval


    def statetuple(self, state):

        return (tuple(state[0]), tuple(state[1]), tuple(state[2]), tuple(state[3]))
   


class Human(object):
    def __init__(self, player):

        self.player = player

    def action(self, state):

        printboard(state)

        action = None

        while action not in range(1, 17):
            action = int(input('Your move? '))

        switch_map = {

            1: (0, 0),

            2: (0, 1),

            3: (0, 2),

            4: (0, 3),

            5: (1, 0),

            6: (1, 1),

            7: (1, 2),

            8: (1, 3),

            9: (2, 0),
            
            10: (2,1),
            
            11: (2,2),
            
            12: (2,3),
            
            13: (3,0),
            
            14: (3,1),
            
            15: (3,2),
            
            16: (3,3)

        }

        return switch_map[action]

    def episode_over(self, winner):   ## 게임이 누가 이겼는지
                                      ## 출력하는게 아니라 가중치 갱신

        if winner == DRAW:

            print('Game over! It was a draw.')

        else:

            print('Game over! Winner: Player {0}'.format(winner))


def play(agent1, agent2):
    state = emptystate()

    for i in range(16):

        if i % 2 == 0:

            move = agent1.action(state)

        else:

            move = agent2.action(state)

        state[move[0]][move[1]] = (i % 2) + 1

        winner = gameover(state)

        if winner != EMPTY:
            return winner

    return winner


if __name__ == "__main__":

    p1 = Agent(1, lossval=-1)

    p2 = Agent(2, lossval=-1)


    ## 학습
    for i in range(2000000):

        if i % 10000 == 0: ## 10판마다 한번씩 출력되게
            print('Game: {0}'.format(i))

        winner = play(p1, p2)

        p1.episode_over(winner)

        p2.episode_over(winner)

    ## 학습 후 대결
    while True:

        p1 = Human(1)

        winner = play(p1, p2)

        p1.episode_over(winner)

        p2.episode_over(winner)




