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


class State():
    def __init__(self):
        self.container = [[Cell(x,y) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        self.snake = [Snake(0, [5,5]), Snake(1, [4,5]), Snake(2, [3,5])]


    def __iter__(self):
        iter_container = []
        for row in self.container:
            for cell in row:
                iter_container.append(cell)
        return iter(iter_container)

    def clear(self):
        for cell in self:
            cell.snake = None

    def move(self, position):

        self.clear()
        
        for piece in reversed(self.snake):
            x = piece.position[0]
            y = piece.position[1]
            if piece.number == 0:
                piece.position = [x+1, y]
            else:
                beginer_piece = self.snake[piece.number - 1]
                piece.position = beginer_piece.position


        for piece in self.snake:
            x = piece.position[0]
            y = piece.position[1]
            self.container[y][x].snake = piece

    def draw(self, surface):
        for cell in self:
            cell.draw(surface)
            
        

running = True
c = State()
while running:
    CLOCK.tick(1)
    c.draw(screen)
    pprint(c.snake)
    c.move(1)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False