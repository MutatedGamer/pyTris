import pygame
import sys
import random
import time

def random_color():
    colors = [(128, 217, 221),
              (62, 160, 96),
              (252, 180, 35),
              (186, 16, 22),
              (163, 9, 124)
              ]
    return tuple(random.choice(colors))

    rgbl=[255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)

def add_tint(colors):
    new_colors = []
    for color in colors:
        new_colors.append(color + 0.3*(255 - color))
    return tuple(new_colors)

class Block:
    def __init__(self, color, tile_size, board, solid=False, linecolor=(0, 0, 0)):
        self.color = color
        self.tile_size = tile_size
        self.solid = solid
        self.linecolor = linecolor
        self.board = board

    def is_solid(self):
        return self.solid

    def draw(self, x, y):
        draw_x = self.board.x + x*self.tile_size
        draw_y = self.board.y + y*self.tile_size
        if not self.is_solid():
            pygame.draw.rect(self.board.screen, self.color, [draw_x, draw_y, self.tile_size,
                                                      self.tile_size])
            pygame.draw.rect(self.board.screen, self.linecolor, [draw_x, draw_y, self.tile_size,
                                                     self.tile_size], 1)
        else:
            pygame.draw.polygon(self.board.screen, self.color, 
                                [[draw_x + 1, draw_y + 1],
                                 [draw_x + self.tile_size - 1, draw_y + 1],
                                 [draw_x + 1, draw_y + self.tile_size - 1]
                                 ], 0)
            pygame.draw.polygon(self.board.screen, add_tint(self.color), 
                                [[draw_x + self.tile_size - 1, draw_y + 1],
                                 [draw_x+self.tile_size - 1,
                                  draw_y+self.tile_size - 1],
                                 [draw_x + 1, draw_y + self.tile_size - 1]
                                 ], 0)
            pygame.draw.rect(self.board.screen, self.linecolor, [draw_x, draw_y, self.tile_size,
                                                     self.tile_size], 1)
            

class Tetromino:
    def __init__(self, x, y, color, tile_size, board):
        self.x = x
        self.y = y
        self.color = color
        self.tile_size = tile_size
        self.board = board


    def drop(self):
        self.y += 1

    def rotate_cw(self):
        self.pieces = list(zip(*self.pieces[::-1]))

    def rotate_ccw(self):
        self.pieces = list(zip(*self.pieces))[::-1]

    def get_piece_locations(self):
        for y in range(len(self.pieces)):
            for x in range(len(self.pieces)):
                if self.pieces[y][x]:
                    yield (self.y + y, self.x + x)

    def draw(self):
        for y in range(len(self.pieces)):
            for x in range(len(self.pieces)):
                if self.pieces[y][x] and self.y + y >= 0:
                    self.pieces[y][x].draw(self.x + x, self.y + y)


class I_Piece(Tetromino):
    def __init__(self, x, y, color, tile_size, board):
        Tetromino.__init__(self, x, y, color,tile_size, board)
        self.pieces = [[None, None, Block(color, tile_size, board, solid=True), None, None]]*5
class L_Piece(Tetromino):
    def __init__(self, x, y, color, tile_size, board):
        Tetromino.__init__(self, x, y, color,tile_size, board)
        self.pieces = [[None, None, None, None, None],
                       [None, None, Block(color, tile_size, board, solid=True), None, None],
                       [None, None, Block(color, tile_size, board, solid=True), None, None],
                       [None, None, Block(color, tile_size, board, solid=True), Block(color, tile_size, board, solid=True), None],
                       [None, None, None, None, None],
                    ]
class J_Piece(Tetromino):
    def __init__(self, x, y, color, tile_size, board):
        Tetromino.__init__(self, x, y, color,tile_size, board)
        self.pieces = [[None, None, None, None, None],
                       [None, None, Block(color, tile_size, board, solid=True), None, None],
                       [None, None, Block(color, tile_size, board, solid=True), None, None],
                       [None, Block(color, tile_size, board, solid=True), Block(color, tile_size, board, solid=True), None, None],
                       [None, None, None, None, None],
                    ]
class S_Piece(Tetromino):
    def __init__(self, x, y, color, tile_size, board):
        Tetromino.__init__(self, x, y, color,tile_size, board)
        self.pieces = [[None, None, None, None, None],
                       [None, None, None, None, None],
                       [None, None, Block(color, tile_size, board, solid=True), Block(color, tile_size, board, solid=True), None],
                       [None, Block(color, tile_size, board, solid=True), Block(color, tile_size, board, solid=True), None, None],
                       [None, None, None, None, None]
                       ]
class Z_Piece(Tetromino):
    def __init__(self, x, y, color, tile_size, board):
        Tetromino.__init__(self, x, y, color,tile_size, board)
        self.pieces = [[None, None, None, None, None],
                       [None, None, None, None, None],
                       [None, Block(color, tile_size, board, solid=True),Block(color, tile_size, board, solid=True), None, None],
                       [None, None, Block(color, tile_size, board, solid=True), Block(color, tile_size, board, solid=True), None],
                       [None, None, None, None, None]
                       ]
class O_Piece(Tetromino):
    def __init__(self, x, y, color, tile_size, board):
        Tetromino.__init__(self, x, y, color,tile_size, board)
        self.pieces = [[None, None, None, None], [None, Block(color, tile_size, board, solid=True), Block(color, tile_size, board, solid=True), None],
                       [None, Block(color, tile_size, board, solid=True), Block(color, tile_size, board, solid=True), None], [None, None, None, None]]
class T_Piece(Tetromino):
    def __init__(self, x, y, color, tile_size, board):
        Tetromino.__init__(self, x, y, color,tile_size, board)
        self.pieces = [[None, None, None, None, None],
                       [None, None, None, None, None],
                       [None, Block(color, tile_size, board, solid=True),Block(color, tile_size, board, solid=True), Block(color, tile_size, board, solid=True), None],
                       [None, None, Block(color, tile_size, board, solid=True), None, None], 
                       [None, None, None, None, None]]

class Board:
    def __init__(self, x, y, width, height, tile_size, screen, starting_level):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.alive = True

        self.ticks = 0
        self.level = starting_level

        self.tile_size = tile_size

        self.tiles =  [ [Block((109, 110, 112), self.tile_size, self)] * width for _ in range(height)]

        self.screen = screen

        self.get_new_piece()

    def update(self):
        self.ticks += 1

        if self.ticks*10 > 200 - (self.level - 1)*11:
            self.ticks = 0
            if self.would_piece_fit(0, 1):
                self.current_piece.drop()
            else:
                self.lock_piece()
                self.get_new_piece()

    def move_piece_left(self):
        if self.would_piece_fit(-1, 0):
            self.current_piece.x -= 1

    def move_piece_right(self):
        if self.would_piece_fit(1, 0):
            self.current_piece.x += 1

    def move_piece_down(self):
        if self.would_piece_fit(0, 1):
            self.current_piece.y += 1
        else:
            self.lock_piece()
            self.get_new_piece()

    def rotate_cw(self):
        self.current_piece.rotate_cw()
        if not self.would_piece_fit(0,0):
           self.current_piece.rotate_ccw()

    def rotate_ccw(self):
        self.current_piece.rotate_ccw()
        if not self.would_piece_fit(0,0):
            self.current_piece.rotate_cw()


    def hard_drop(self):
        while self.would_piece_fit(0, 1):
            self.current_piece.y += 1
        self.lock_piece()
        self.get_new_piece()

    def lock_piece(self):
        lines_cleared = []
        lines_to_check = set()
        for (y,x) in self.current_piece.get_piece_locations():
            lines_to_check.add(y)
            if y >= 0:
                self.tiles[y][x] = Block(self.current_piece.color, self.tile_size,
                                     self, solid=True)
            else:
                ## gameover
                self.alive = False
        
        # Check if line cleared
        for y in lines_to_check:
            lines_cleared.append(y)
            for x_check in range(self.width):
                if not self.tiles[y][x_check].is_solid():
                    lines_cleared.pop()
                    break

        if len(lines_cleared) > 0:
            self.clear_lines(lines_cleared)

    def clear_lines(self, lines):
        for line in lines:
            self.tiles.pop(line)
            self.tiles = [ [Block((109, 110, 112), self.tile_size, self)] *
                          self.width ] + self.tiles


    def get_new_piece(self):
        possible_pieces = [L_Piece, J_Piece, I_Piece, S_Piece, Z_Piece, T_Piece,
                            O_Piece]
        piece = random.choice(possible_pieces)
        self.current_piece = piece(3, -4, random_color(), self.tile_size,
                                     self)

    def would_piece_fit(self, offset_x, offset_y):
        for (y,x) in self.current_piece.get_piece_locations():
            if y + offset_y < 0:
                continue
            if y + offset_y >= self.height:
                return False
            if x + offset_x >= self.width or x + offset_x < 0:
                return False
            if self.tiles[y + offset_y][x + offset_x].is_solid():
                return False
        return True



    def draw(self):

        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x].draw(x, y)

        self.current_piece.draw()



def main():
    pygame.init()
    pygame.font.init()

    logo = pygame.image.load('logo.png')
    pygame.display.set_icon(logo)
    pygame.display.set_caption("pyTris")

    screen = pygame.display.set_mode((500, 800))

    running = True

    board = Board(10, 10, 10, 24, 30, screen, 10)

    FRAMERATE = 30
    clock = pygame.time.Clock()
    buttons_pressed = dict()

    while board.alive:
        clock.tick(FRAMERATE)

        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for key downs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    board.move_piece_right()
                    buttons_pressed['right'] = 0
                if event.key == pygame.K_LEFT:
                    board.move_piece_left()
                    buttons_pressed['left'] = 0
                if event.key == pygame.K_DOWN:
                    board.move_piece_down()
                    buttons_pressed['down'] = 0
                if event.key == pygame.K_UP:
                    board.hard_drop()
                    buttons_pressed['up'] = 0
                if event.key == pygame.K_q:
                    board.rotate_ccw()
                    buttons_pressed['q'] = 0
                if event.key == pygame.K_r:
                    board.rotate_cw()
                    buttons_pressed['r'] = 0
            # Check for key ups
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    buttons_pressed.pop('right')
                if event.key == pygame.K_LEFT:
                    buttons_pressed.pop('left')
                if event.key == pygame.K_DOWN:
                    buttons_pressed.pop('down')
                if event.key == pygame.K_UP:
                    buttons_pressed.pop('up')
                if event.key == pygame.K_q:
                    buttons_pressed.pop('q')
                if event.key == pygame.K_r:
                    buttons_pressed.pop('r')

        key=pygame.key.get_pressed()
        if buttons_pressed.get('left', 0)  > int(FRAMERATE/3) and key[pygame.K_LEFT]:
            board.move_piece_left()
        if buttons_pressed.get('right', 0)  > int(FRAMERATE/3) and key[pygame.K_RIGHT]:
            board.move_piece_right()
        if buttons_pressed.get('down', 0)  > int(FRAMERATE/3) and key[pygame.K_DOWN]:
            board.move_piece_down()
        if buttons_pressed.get('up', 0)  > int(FRAMERATE/3) and key[pygame.K_UP]:
            #board.hard_drop()
            pass

        # Tick key counters
        for button in buttons_pressed:
            buttons_pressed[button] += 1

        board.update()
        screen.fill((0,0,0))
        board.draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()
