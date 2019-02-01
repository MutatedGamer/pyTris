import pygame
import sys
import random
import time
import os
import copy

def AAfilledRoundedRect(surface,rect,color,radius=0.05):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = pygame.Rect(rect)
    color        = pygame.Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

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

    def draw(self, x, y, tile_size = None, opacity=255):
        if not tile_size:
            tile_size = self.tile_size
        draw_x = self.board.x + x*tile_size
        draw_y = self.board.y + y*tile_size
        if not self.is_solid():
            pygame.draw.rect(self.board.screen, self.color, [draw_x, draw_y, tile_size,
                                                      tile_size])
            pygame.draw.rect(self.board.screen, self.linecolor, [draw_x, draw_y, tile_size,
                                                     tile_size], 1)
        else:
            surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            pygame.draw.polygon(surf, self.color + (opacity,), 
                                [[1, 1],
                                 [tile_size-1, 1],
                                 [1, tile_size-1]
                                 ], 0)
            pygame.draw.polygon(surf, add_tint(self.color) + (opacity,), 
                                [[tile_size-1, 1],
                                 [tile_size-1, tile_size-1],
                                 [1, tile_size-1]
                                 ], 0)
            self.board.screen.blit(surf, [draw_x,draw_y])
            pygame.draw.rect(self.board.screen, self.linecolor, [draw_x, draw_y, tile_size,
                                                     tile_size], 1)
            

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

    def draw(self, opacity=255):
        for y in range(len(self.pieces)):
            for x in range(len(self.pieces)):
                if self.pieces[y][x] and self.y + y >= 0:
                    self.pieces[y][x].draw(self.x + x, self.y + y,
                                           opacity=opacity)


class I_Piece(Tetromino):
    def __init__(self, x, y, color, tile_size, board):
        Tetromino.__init__(self, x, y, color,tile_size, board)
        self.pieces = [ [None, None, None, None],
                        [None, None, None, None],
                        [Block(color, tile_size, board, solid=True)]*4,
                        [None, None, None, None]
                      ]
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
    def __init__(self, x, y, width, height, tile_size, screen, starting_level,
                 queue_length = 4, ghost=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.alive = True

        self.ticks = 0
        self.level = starting_level
        self.lines = 0
        self.score = 0


        self.ghost = ghost


        self.held = False
        self.held_piece = None


        self.lines_until_level_up = 10

        self.tile_size = tile_size

        self.tiles =  [ [Block((109, 110, 112), self.tile_size, self)] * width for _ in range(height)]

        self.screen = screen


        self.piece_queue = []
        while len(self.piece_queue) != queue_length:
            self.queue_new_piece()

        self.get_new_piece()

    def hold(self):
        if not self.held:
            if self.held_piece:
                self.held_piece, self.current_piece = self.current_piece, self.held_piece
                self.reset_piece_position()
            else:
                self.held_piece = self.current_piece
                self.get_new_piece()
            self.held = True

    def update(self):
        self.ticks += 1

        if self.ticks*10 > 200 - (self.level - 1)*13:
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
            if isinstance(self.current_piece, I_Piece):
                shift = 2
            else:
                shift = 1
            ## Check if would fit by moving it to left
            if self.would_piece_fit(-1*shift, 0):
                self.current_piece.x -= shift
                return
            ## Check if would fit by moving it to right
            if self.would_piece_fit(shift, 0):
                self.current_piece.x += shift
                return
            self.current_piece.rotate_ccw()

    def rotate_ccw(self):
        self.current_piece.rotate_ccw()
        if not self.would_piece_fit(0,0):
            if isinstance(self.current_piece, I_Piece):
                shift = 2
            else:
                shift = 1
            ## Check if would fit by moving it to left
            if self.would_piece_fit(-1*shift, 0):
                self.current_piece.x -= shift
                return
            ## Check if would fit by moving it to right
            if self.would_piece_fit(shift, 0):
                self.current_piece.x += shift
                return
            self.current_piece.rotate_cw()


    def hard_drop(self):
        while self.would_piece_fit(0, 1):
            self.current_piece.y += 1
        self.lock_piece()
        self.get_new_piece()

    def lock_piece(self):
        self.score += 10
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
        self.score += self.level*(len(lines))*10
        self.lines += len(lines)
        self.lines_until_level_up -= len(lines)
        if self.lines_until_level_up <= 0:
            self.lines_until_level_up = 10
            self.level += 1
        for line in lines:
            self.tiles.pop(line)
            self.tiles = [ [Block((109, 110, 112), self.tile_size, self)] *
                          self.width ] + self.tiles


    def queue_new_piece(self):
        possible_pieces = [L_Piece, J_Piece, I_Piece, S_Piece, Z_Piece, T_Piece,
                            O_Piece]
        piece = random.choice(possible_pieces)
        self.piece_queue.append(piece(self.width, None, random_color(),
                                      self.tile_size,
                                     self))

    def get_new_piece(self):
        if self.held:
            self.held = False
        self.current_piece = self.piece_queue.pop(0)
        self.reset_piece_position()
        self.current_piece.tile_size = self.tile_size
        self.queue_new_piece()

    def reset_piece_position(self):
        self.current_piece.x = 3
        if len(self.current_piece.pieces) == 4:
            self.current_piece.y = -3
        else:
            self.current_piece.y = -4
        

    def would_piece_fit(self, offset_x, offset_y, piece=None):
        if not piece:
            piece=self.current_piece
        for (y,x) in piece.get_piece_locations():
            if x + offset_x >= self.width or x + offset_x < 0:
                return False
            if y + offset_y < 0:
                continue
            if y + offset_y >= self.height:
                return False
            if self.tiles[y + offset_y][x + offset_x].is_solid():
                return False
        return True



    def draw(self):
        
        def render_piece_queue(pieces, starting_col):
            current_y = starting_col
            for i, piece in enumerate(pieces):
                piece.y = current_y
                top = min([el[0] for el in piece.get_piece_locations()]) - current_y
                piece.y -= top
                piece.y += 1
                if len(piece.pieces) == 4:
                    piece.x = self.width + 0.5 
                else:
                    piece.x = self.width
                piece.draw()
                current_y = max([el[0] for el in piece.get_piece_locations()]) + 1




        # Draw Border
        AAfilledRoundedRect(self.screen, (self.x-6,
                                          self.y-6,
                                          (self.width+5)*self.tile_size + 6,
                                          self.height*self.tile_size + 12
                                         ),
                            (191, 205, 224)
                           )

        # Font settings
        info_y = self.y + self.tile_size*(self.height) + 20
        font_size = 20
        myfont = pygame.font.Font(os.path.join('NotoSans-Regular.ttf'),
                                  font_size)

        # Draw next piece box
        text = myfont.render('Next Piece', True, (0,0,0))
        self.screen.blit(text, (self.x + self.tile_size*(self.width) + 30,
                           self.y + 5)
                    )
        render_piece_queue(self.piece_queue, 1)
        

        # Draw hold box
        text = myfont.render('Hold', True, (0,0,0))
        self.screen.blit(text, (self.x + self.tile_size*(self.width) + 55,
                           self.y + self.tile_size*(self.height - 6) + 5)
                    )
        # Divider line
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x + self.tile_size*(self.width),
                                       self.y + self.tile_size*(self.height -
                                                                6) - 10,
                                       self.tile_size*5,
                                       2
                                      )
                        )
        if self.held_piece:
            render_piece_queue([self.held_piece], self.height-5)
            

        # Draw info box
        AAfilledRoundedRect(self.screen,
                            (self.x - 6,
                             self.y + self.tile_size*(self.height) + 12,
                             self.screen.get_width() - self.x,
                             50),
                            (191, 205, 224)
                            )
        text = myfont.render('Level: ' + str(self.level), True, (0,0,0))
        self.screen.blit(text, (self.x + 5,
                                info_y)
                         )
        text = myfont.render('Lines: ' + str(self.lines), True, (0,0,0))
        self.screen.blit(text, (self.x + 110,
                                info_y)
                         )
        text = myfont.render('Score: ' + str(self.score), True, (0,0,0))
        self.screen.blit(text, (self.x + 220,
                                info_y)
                         )



        # Draw all tiles
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x].draw(x, y)

        self.current_piece.draw()

        if self.ghost:
            ghost_piece = copy.copy(self.current_piece)
            offset_y = 0
            while self.would_piece_fit(0, offset_y+1, ghost_piece):
                offset_y += 1
            ghost_piece.y += offset_y
            ghost_piece.draw(opacity=80)




def main():
    pygame.init()
    pygame.font.init()

    logo = pygame.image.load('logo.png')
    pygame.display.set_icon(logo)
    pygame.display.set_caption("pyTris")

    screen = pygame.display.set_mode((465, 800))

    running = True

    board = Board(10, 10, 10, 24, 30, screen, 1)

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
                if event.key == pygame.K_SPACE:
                    board.hold()
                    buttons_pressed['space'] = 0
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
                if event.key == pygame.K_SPACE:
                    buttons_pressed.pop('space')

        key=pygame.key.get_pressed()
        if buttons_pressed.get('left', 0)  > int(FRAMERATE/5) and key[pygame.K_LEFT]:
            board.move_piece_left()
        if buttons_pressed.get('right', 0)  > int(FRAMERATE/5) and key[pygame.K_RIGHT]:
            board.move_piece_right()
        if buttons_pressed.get('down', 0)  > int(FRAMERATE/6) and key[pygame.K_DOWN]:
            board.move_piece_down()

        # Tick key counters
        for button in buttons_pressed:
            buttons_pressed[button] += 1

        board.update()
        screen.fill((0,0,0))
        board.draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()
