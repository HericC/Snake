import pygame
from pygame.locals import *
import random


class Snake:
    def __init__(self, default=False):
        self.__status = False

        if not default:
            self.__minVelocity = 10
            self.__maxVelocity = 40
            self.__increaseVelocity = 0.5
            self.__increaseTail = 2
            self.__grid = 10
            self.__size = 600

            self.__snakeRGB = (155, 155, 155)
            self.__headSnakeSkinRGB = (255, 255, 255)
            self.__appleRGB = (255, 0, 0)
            self.__mapRGB = (55, 55, 55)
            self.__borderMapRGB = (0, 0, 0)

        elif default:
            self.__sizeMap = (self.__size // self.__grid * self.__grid) + self.__grid
            self.__points = 0
            self.__velocity = self.__minVelocity

            self.__up = 0
            self.__down = 1
            self.__left = 2
            self.__right = 3

            self.__myDirection = self.__right
            self.__lastDirection = self.__myDirection
            self.__lastSnake = -self.__grid, -self.__grid

            self.__snake = [self.__onGrid(100, 200),
                            self.__onGrid(100, 200),
                            self.__onGrid(100, 200),
                            self.__onGrid(100, 200)]

            self.__snakeSkin = pygame.Surface((self.__grid, self.__grid))
            self.__snakeSkin.fill(self.__snakeRGB)
            self.__headSnakeSkin = pygame.Surface((self.__grid, self.__grid))
            self.__headSnakeSkin.fill(self.__headSnakeSkinRGB)

            self.__applePos = self.__onGridRandom()
            self.__apple = pygame.Surface((self.__grid, self.__grid))
            self.__apple.fill(self.__appleRGB)

            self.__borderMapSkin = pygame.Surface((self.__grid, self.__grid))
            self.__borderMapSkin.fill(self.__borderMapRGB)

    @staticmethod
    def __getStatusMSG():
        print('\033[1;31mGame já iniciado, não é possivel alterar seus atributos!\n'
              'Para alterar seus atributos, encerre o jogo!\033[0;0m')

    def start(self):
        self.__init__(True)
        self.__status = True

        pygame.init()
        screen = pygame.display.set_mode((self.__sizeMap, self.__sizeMap))
        pygame.display.set_caption('Snake')

        clock = pygame.time.Clock()

        while True:
            clock.tick(self.__velocity)

            self.__collisionApple()
            nextPos = self.__snakeMove()

            if self.__collisionMap(nextPos):
                break

            if self.__collisionTail():
                break

            self.__getKEY()

            screen.fill(self.__mapRGB)
            for m in range(self.__sizeMap):
                screen.blit(self.__borderMapSkin, (m, 0))
                screen.blit(self.__borderMapSkin, (m, self.__sizeMap-self.__grid))
                screen.blit(self.__borderMapSkin, (0, m))
                screen.blit(self.__borderMapSkin, (self.__sizeMap - self.__grid, m))

            screen.blit(self.__apple, self.__applePos)
            for pos in range(len(self.__snake)):
                if pos == 0:
                    screen.blit(self.__headSnakeSkin, self.__snake[pos])
                else:
                    screen.blit(self.__snakeSkin, self.__snake[pos])
            pygame.display.update()
        print('==========')
        print('\033[1;31mGame Over\033[0;0m')
        print(f'Pontuação: \033[1;32m{self.__points}\033[0;0m')

    def __getKEY(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if not self.__lastDirection == self.__down:
                        if not self.__collision(self.__snake[0], self.__lastSnake):
                            self.__myDirection = self.__up
                            self.__lastSnake = self.__snake[0]
                            self.__lastDirection = self.__myDirection
                elif event.key == K_DOWN:
                    if not self.__lastDirection == self.__up:
                        if not self.__collision(self.__snake[0], self.__lastSnake):
                            self.__myDirection = self.__down
                            self.__lastSnake = self.__snake[0]
                            self.__lastDirection = self.__myDirection
                elif event.key == K_LEFT:
                    if not self.__lastDirection == self.__right:
                        if not self.__collision(self.__snake[0], self.__lastSnake):
                            self.__myDirection = self.__left
                            self.__lastSnake = self.__snake[0]
                            self.__lastDirection = self.__myDirection
                elif event.key == K_RIGHT:
                    if not self.__lastDirection == self.__left:
                        if not self.__collision(self.__snake[0], self.__lastSnake):
                            self.__myDirection = self.__right
                            self.__lastSnake = self.__snake[0]
                            self.__lastDirection = self.__myDirection
                elif event.key == K_ESCAPE:
                    pygame.quit()

    def __snakeMove(self):
        for i in range(len(self.__snake) - 1, 0, -1):
            self.__snake[i] = (self.__snake[i - 1][0], self.__snake[i - 1][1])

        if self.__myDirection == self.__up:
            self.__snake[0] = self.__snake[0][0], self.__snake[0][1] - self.__grid
            return self.__snake[0][0], self.__snake[0][1] - self.__grid

        elif self.__myDirection == self.__down:
            self.__snake[0] = self.__snake[0][0], self.__snake[0][1] + self.__grid
            return self.__snake[0][0], self.__snake[0][1] + self.__grid

        elif self.__myDirection == self.__left:
            self.__snake[0] = self.__snake[0][0] - self.__grid, self.__snake[0][1]
            return self.__snake[0][0] - self.__grid, self.__snake[0][1]

        elif self.__myDirection == self.__right:
            self.__snake[0] = self.__snake[0][0] + self.__grid, self.__snake[0][1]
            return self.__snake[0][0] + self.__grid, self.__snake[0][1]

    def __onGridRandom(self):
        x = random.randint(self.__grid, self.__sizeMap - self.__grid*2)
        y = random.randint(self.__grid, self.__sizeMap - self.__grid*2)
        return x // self.__grid * self.__grid, y // self.__grid * self.__grid

    def __onGrid(self, x, y):
        return x // self.__grid * self.__grid, y // self.__grid * self.__grid

    @staticmethod
    def __collision(c1, c2):
        return c1[0] == c2[0] and c1[1] == c2[1]

    def __collisionMap(self, nextPos):
        for j in range(-self.__grid, self.__sizeMap + self.__grid, self.__grid):
            if self.__collision(nextPos, (j, -self.__grid)):
                return True
            elif self.__collision(nextPos, (j, self.__sizeMap)):
                return True
            elif self.__collision(nextPos, (-self.__grid, j)):
                return True
            elif self.__collision(nextPos, (self.__sizeMap, j)):
                return True
        return False

    def __collisionTail(self):
        for i in range(len(self.__snake) - 1):
            if self.__collision(self.__snake[0], self.__snake[i + 1]):
                return True
        return False

    def __newApple(self):
        for a in range(len(self.__snake)):
            if self.__collision(self.__snake[a], self.__applePos):
                return False
        return True

    def __collisionApple(self):
        if self.__collision(self.__snake[0], self.__applePos):
            while True:
                self.__applePos = self.__onGridRandom()
                if self.__newApple():
                    for p in range(self.__increaseTail):
                        self.__snake.append((-self.__grid, -self.__grid))
                    self.__points += 1
                    if self.__velocity < self.__maxVelocity:
                        self.__velocity += self.__increaseVelocity
                    break

    def getAll(self):
        return {
            'minVelocity': self.__minVelocity,
            'maxVelocity': self.__maxVelocity,
            'increaseVelocity': self.__increaseVelocity,
            'increaseTail': self.__increaseTail,
            'grid': self.__grid,
            'size': self.__size,
            'snakeRGB': self.__snakeRGB,
            'headSnakeSkinRGB': self.__headSnakeSkinRGB,
            'appleRGB': self.__appleRGB,
            'mapRGB': self.__mapRGB,
            'borderMapRGB': self.__borderMapRGB
        }

    def setMinVelocity(self, num):
        if not self.__status:
            self.__minVelocity = num
        else:
            self.__getStatusMSG()

    def setMaxVelocity(self, num):
        if not self.__status:
            self.__maxVelocity = num
        else:
            self.__getStatusMSG()

    def setIncreaseVelocity(self, num):
        if not self.__status:
            self.__increaseVelocity = num
        else:
            self.__getStatusMSG()

    def setIncreaseTail(self, num):
        if not self.__status:
            self.__increaseTail = num
        else:
            self.__getStatusMSG()

    def setgrid(self, num):
        if not self.__status:
            self.__grid = num
        else:
            self.__getStatusMSG()

    def setSize(self, num):
        if not self.__status:
            self.__size = num
        else:
            self.__getStatusMSG()

    def setSnakeRGB(self, num):
        if not self.__status:
            self.__snakeRGB = num
        else:
            self.__getStatusMSG()

    def setHeadSnakeSkinRGB(self, num):
        if not self.__status:
            self.__headSnakeSkinRGB = num
        else:
            self.__getStatusMSG()

    def setAppleRGB(self, num):
        if not self.__status:
            self.__appleRGB = num
        else:
            self.__getStatusMSG()

    def setMapRGB(self, num):
        if not self.__status:
            self.__mapRGB = num
        else:
            self.__getStatusMSG()

    def setBorderMapRGB(self, num):
        if not self.__status:
            self.__borderMapRGB = num
        else:
            self.__getStatusMSG()
