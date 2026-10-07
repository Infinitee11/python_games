import pygame as pg
from dataclasses import dataclass
from pprint import pprint

pg.init()
screen = pg.display.set_mode((800, 800))  

HEAD = (255, 0, 0)
BODY = (0, 0, 255)
BOARD = (255, 255, 255)

CELL_SIZE = 50
BOARD_SIZE = 10

CLOCK = pg.Clock()

@dataclass
class Cell():
    x :int
    y :int
    snake:'Snake' = None

    def draw(self,surface):
        if self.snake is not None:
            if self.snake.is_head:
                color = HEAD
            elif not self.snake.is_head:
                color = BODY
        else:
            color = BOARD

        rect = pg.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        rect.inflate_ip(-10, -10)    
        pg.draw.rect(surface, (color), rect)
        pg.display.flip()

@dataclass
class Snake():
    number :int
    position: list


    @property
    def is_head(self):
        if self.number == 0:
            return True
        else:
            return False

    def set_position(self, position):
        x, y = position

        if x < 0:
            x = BOARD_SIZE - 1
        if x >= BOARD_SIZE:
            x = 0 
        if y < 0:
            y = BOARD_SIZE - 1
        if y >= BOARD_SIZE:
            y = 0

        self.position = [x, y]


class State():
    def __init__(self):
        self.container = [[Cell(x,y) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        self.snake = [Snake(0, [5,5]), Snake(1, [4,5]), Snake(2, [3,5])]
        self.direction = "right"


    def __iter__(self):
        iter_container = []
        for row in self.container:
            for cell in row:
                iter_container.append(cell)
        return iter(iter_container)

    def clear(self):
        for cell in self:
            cell.snake = None

    def move(self):

        self.clear()
        
        for piece in reversed(self.snake):
            x = piece.position[0]
            y = piece.position[1]
            x_change = 0
            y_change = 0

            if self.direction == 'up':
                y_change = -1
            elif self.direction == 'down':
                y_change = 1
            elif self.direction == 'right':
                x_change = 1
            elif self.direction == 'left':
                x_change = -1

            if piece.number != 0:
                beginer_piece = self.snake[piece.number - 1]
                piece.set_position(beginer_piece.position)

            elif piece.number == 0:
                piece.set_position([x+x_change, y+y_change])


        for piece in self.snake:
            x = piece.position[0] if piece.position[0] < BOARD_SIZE else 0
            y = piece.position[1] if piece.position[1] < BOARD_SIZE else 0
            self.container[y][x].snake = piece

    def draw(self, surface):
        for cell in self:
            cell.draw(surface)
            
        
class Board():
    
    def __init__(self):
        self.state = State()

    def move(self):
        move = self.state.direction
        for ev in pg.event.get():
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_RIGHT:
                    move = 'right'
                elif ev.key == pg.K_LEFT:
                    move = 'left'
                elif ev.key == pg.K_UP:
                    move = 'up'
                elif ev.key == pg.K_DOWN:
                    move = 'down'

            elif ev.type == pg.QUIT:
                pg.quit()

        self.state.direction = move
        self.state.move()




running = True
b = Board()
while running:
    CLOCK.tick(3)
    b.state.draw(screen)
    print(b.state.snake)
    b.move()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False