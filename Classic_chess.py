import pygame
from Pieces_classes import *

pygame.init()
pawn_moved_two_squares = False
last_moved_piece = ''
height, quantity = 760, 8
width = height
screen = pygame.display.set_mode((width, height))
all_sprites = pygame.sprite.Group()
board = {}
for x in range(1, 9):
    for y in range(1, 9):
        if 2 < y < 7:
            board[(x, y)] = False
        elif y in (1, 2):
            board[(x, y)] = 'b'
        else:
            board[(x, y)] = 'w'
for colour in ('w', 'b'):
    for piece in ('B', 'K', 'R', 'Q', 'N', 'P'):
        if piece == 'B' and colour == 'w':
            Bishop((3, 8), colour, all_sprites)
            Bishop((6, 8), colour, all_sprites)
        if piece == 'B' and colour == 'b':
            Bishop((3, 1), colour, all_sprites)
            Bishop((6, 1), colour, all_sprites)
        if piece == 'N' and colour == 'w':
            Knight((2, 8), colour, all_sprites)
            Knight((7, 8), colour, all_sprites)
        if piece == 'N' and colour == 'b':
            Knight((2, 1), colour, all_sprites)
            Knight((7, 1), colour, all_sprites)
        if piece == 'R' and colour == 'w':
            Rook((1, 8), colour, all_sprites)
            Rook((8, 8), colour, all_sprites)
        if piece == 'R' and colour == 'b':
            Rook((1, 1), colour, all_sprites)
            Rook((8, 1), colour, all_sprites)
        if piece == 'K' and colour == 'w':
            King((5, 8), colour, all_sprites)
        if piece == 'K' and colour == 'b':
            King((5, 1), colour, all_sprites)
        if piece == 'Q' and colour == 'w':
            Queen((4, 8), colour, all_sprites)
        if piece == 'Q' and colour == 'b':
            Queen((4, 1), colour, all_sprites)
        if piece == 'P' and colour == 'w':
            for x_coord in range(1, 9):
                Pawn((x_coord, 7), colour, all_sprites)
        if piece == 'P' and colour == 'b':
            for x_coord in range(1, 9):
                Pawn((x_coord, 2), colour, all_sprites)
running = True
left_mouse_clicked = False
wanna_move = []
wanna_move_dublicate = []
last_piece = ''
moving_colour = 'w'
while running:
    screen.fill(pygame.Color('#B58863'))
    for i in range(0, quantity):
        n = i % 2
        for j in range(n, quantity, 2):
            pygame.draw.rect(screen, pygame.Color('#F0D9B5'),
                             ((i * height) // quantity, (j * height) // quantity, height // quantity,
                              height // quantity))
    if left_mouse_clicked:
        if board[(x, y)] == moving_colour:
            surf = pygame.Surface((95, 95))
            surf.fill(pygame.Color('#073826'))
            surf.set_alpha(180)
            screen.blit(surf, (coords_to_pixels((x, y))))
            for piece in all_sprites:
                can_move = piece.can_move(board, all_sprites)
                if piece.coords == (x, y):
                    last_piece = piece
                    if type(piece) is Pawn and type(last_moved_piece) is Pawn and pawn_moved_two_squares:
                        if moving_colour == 'w':
                            if abs(piece.coords[0] - last_moved_piece.coords[0]) == 1 and piece.coords[1] == \
                                    last_moved_piece.coords[1]:
                                can_move[last_moved_piece.coords[0], last_moved_piece.coords[1] - 1] = True
                        else:
                            if abs(piece.coords[0] - last_moved_piece.coords[0]) == 1 and piece.coords[1] == \
                                    last_moved_piece.coords[1]:
                                can_move[last_moved_piece.coords[0], last_moved_piece.coords[1] + 1] = True
                    for cell in can_move.keys():
                        if can_move[cell] and not board[cell]:
                            wanna_move.append(cell)
                            pygame.draw.ellipse(screen, pygame.Color('#073826'), (
                                coords_to_pixels(cell)[0] + 30, coords_to_pixels(cell)[1] + 30, 35, 35))
                        elif can_move[cell] and piece.colour != board[cell]:
                            wanna_move.append(cell)
                            pygame.draw.rect(screen, pygame.Color('#073826'), (coords_to_pixels(cell), (95, 95)), 5)
        if (x, y) in wanna_move_dublicate:
            if board[(x, y)]:
                for piece in all_sprites:
                    if piece.coords == (x, y):
                        all_sprites.remove(piece)
            if type(last_piece) is Pawn and abs(x - last_piece.coords[0]) == 1 and not board[(x, y)]:
                all_sprites.remove(last_moved_piece)
            if type(last_piece) is Pawn and abs(last_piece.coords[1] - y) == 2:
                pawn_moved_two_squares = True
            else:
                pawn_moved_two_squares = False
            last_piece.coords = (x, y)
            last_moved_piece = last_piece
            try:
                last_piece.first_move = False
            except AttributeError:
                pass
            try:
                for piece in all_sprites:
                    try:
                        if piece.coords == last_piece.castling_rook[(x, y)][0]:
                            piece.coords = last_piece.castling_rook[(x, y)][1]
                            last_piece.castling_rook.clear()
                            piece.first_move = False
                    except KeyError:
                        pass
            except AttributeError:
                pass
            if moving_colour == 'w':
                moving_colour = 'b'
            else:
                moving_colour = 'w'
            wanna_move_dublicate.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                left_mouse_clicked = True
                x, y = cell_coords(pygame.mouse.get_pos())
                wanna_move_dublicate = wanna_move.copy()
                wanna_move.clear()
    for key in board.keys():
        board[key] = False
    for piece in all_sprites:
        board[piece.coords] = piece.colour
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    pass
pygame.quit()
