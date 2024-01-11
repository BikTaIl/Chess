import pygame
import os
import sys

pygame.init()



def coords_to_pixels(coords):
    if 0 <= coords[0] <= 8 and 0 <= coords[1] <= 8:
        x = (coords[0] - 1) * 95
        y = (coords[1] - 1) * 95
        return x, y
    return None


def load_image(name):
    fullname = os.path.join('Sprites', f'{name}.svg')
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (85, 85))
    return image


def cell_coords(pos):
    if 0 <= pos[0] // 95 <= 7 and 0 <= pos[1] // 95 <= 7:
        return pos[0] // 95 + 1, pos[1] // 95 + 1


class Piece(pygame.sprite.Sprite):
    def __init__(self, coords, colour, *group):
        super(Piece, self).__init__(*group)
        self.coords = coords
        self.colour = colour
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords_to_pixels(self.coords)[0] + 5, coords_to_pixels(self.coords)[1] + 5

    def update(self):
        self.rect.x, self.rect.y = coords_to_pixels(self.coords)[0] + 5, coords_to_pixels(self.coords)[1] + 5


class Pawn(Piece):
    def __init__(self, coords, colour, *group):
        self.image = load_image(f'{colour}P')
        super(Pawn, self).__init__(coords, colour, *group)
        self.first_move = True

    def can_move(self, board):
        good_cells = {}
        for x in range(1, 9):
            for y in range(1, 9):
                good_cells[(x, y)] = False
        if self.colour == 'w':
            if not board[(self.coords[0], self.coords[1] - 1)]:
                good_cells[(self.coords[0], self.coords[1] - 1)] = True
            try:
                if board[(self.coords[0] + 1, self.coords[1] - 1)] == 'b':
                    good_cells[(self.coords[0] + 1, self.coords[1] - 1)] = True
            except KeyError:
                pass
            try:
                if board[(self.coords[0] - 1, self.coords[1] - 1)] == 'b':
                    good_cells[(self.coords[0] - 1, self.coords[1] - 1)] = True
            except KeyError:
                pass
            if self.first_move:
                try:
                    if not board[(self.coords[0]), self.coords[1] - 2]:
                        good_cells[(self.coords[0]), self.coords[1] - 2] = True
                except KeyError:
                    pass
        else:
            if not board[(self.coords[0], self.coords[1] + 1)]:
                good_cells[(self.coords[0], self.coords[1] + 1)] = True
            try:
                if board[(self.coords[0] + 1, self.coords[1] + 1)] == 'w':
                    good_cells[(self.coords[0] + 1, self.coords[1] + 1)] = True
            except KeyError:
                pass
            try:
                if board[(self.coords[0] - 1, self.coords[1] + 1)] == 'w':
                    good_cells[(self.coords[0] - 1, self.coords[1] + 1)] = True
            except KeyError:
                pass
            if self.first_move:
                try:
                    if not board[(self.coords[0]), self.coords[1] + 2]:
                        good_cells[(self.coords[0]), self.coords[1] + 2] = True
                except KeyError:
                    pass
        return good_cells


class Bishop(Piece):
    def __init__(self, coords, colour, *group):
        self.image = load_image(f'{colour}B')
        super(Bishop, self).__init__(coords, colour, *group)

    def can_move(self, board):
        good_cells = {}
        for x in range(1, 9):
            for y in range(1, 9):
                if abs(x - self.coords[0]) != abs(y - self.coords[1]):
                    good_cells[(x, y)] = False
                else:
                    distance = x - self.coords[0]
                    if y - self.coords[1] < 0:
                        for x_distance in range(distance // abs(distance), distance, distance // abs(distance)):
                            try:
                                if board[self.coords[0] + x_distance, self.coords[1] - abs(x_distance)]:
                                    good_cells[(x, y)] = False
                                    break
                            except KeyError:
                                pass
                        else:
                            good_cells[(x, y)] = True
                    elif y - self.coords[1] > 0:
                        for x_distance in range(distance // abs(distance), distance, distance // abs(distance)):
                            try:
                                if board[self.coords[0] + x_distance, self.coords[1] + abs(x_distance)]:
                                    good_cells[(x, y)] = False
                                    break
                            except KeyError:
                                pass
                        else:
                            good_cells[(x, y)] = True
                    else:
                        good_cells[(x, y)] = False
        return good_cells


class Knight(Piece):
    def __init__(self, coords, colour, *group):
        self.image = load_image(f'{colour}N')
        super(Knight, self).__init__(coords, colour, *group)

    def can_move(self, board):
        good_cells = {}
        for x in range(1, 9):
            for y in range(1, 9):
                if (abs(x - self.coords[0]) == 1 and (abs(y - self.coords[1])) == 2) or (
                        abs(x - self.coords[0]) == 2 and (
                        abs(y - self.coords[1])) == 1):
                    good_cells[(x, y)] = True
                else:
                    good_cells[(x, y)] = False
        return good_cells


class Rook(Piece):
    def __init__(self, coords, colour, *group):
        self.image = load_image(f'{colour}R')
        super(Rook, self).__init__(coords, colour, *group)

    def can_move(self, board):
        good_cells = {}
        for x in range(1, 9):
            for y in range(1, 9):
                if x != self.coords[0] and y != self.coords[1] or (x == self.coords[0] and y == self.coords[1]):
                    good_cells[(x, y)] = False
                else:
                    distance = max(x - self.coords[0], y - self.coords[1], key=lambda i: abs(i))
                    if x == self.coords[0]:
                        for current_distance in range(distance // abs(distance), distance, distance // abs(distance)):
                            try:
                                if board[(self.coords[0], self.coords[1] + current_distance)]:
                                    good_cells[(x, y)] = False
                                    break
                            except KeyError:
                                pass
                        else:
                            good_cells[(x, y)] = True
                    else:
                        for current_distance in range(distance // abs(distance), distance, distance // abs(distance)):
                            try:
                                if board[(self.coords[0] + current_distance, self.coords[1])]:
                                    good_cells[(x, y)] = False
                                    break
                            except KeyError:
                                pass
                        else:
                            good_cells[(x, y)] = True
        return good_cells


class Queen(Piece):
    def __init__(self, coords, colour, *group):
        self.image = load_image(f'{colour}Q')
        super(Queen, self).__init__(coords, colour, *group)

    def can_move(self, board):
        good_cells = {}
        rook_good_cells = {}
        bishop_good_cells = {}
        for x in range(1, 9):
            for y in range(1, 9):
                if x != self.coords[0] and y != self.coords[1] or (x == self.coords[0] and y == self.coords[1]):
                    good_cells[(x, y)] = False
                else:
                    distance = max(x - self.coords[0], y - self.coords[1], key=lambda i: abs(i))
                    if x == self.coords[0]:
                        for current_distance in range(distance // abs(distance), distance, distance // abs(distance)):
                            try:
                                if board[(self.coords[0], self.coords[1] + current_distance)]:
                                    good_cells[(x, y)] = False
                                    break
                            except KeyError:
                                pass
                        else:
                            good_cells[(x, y)] = True
                    else:
                        for current_distance in range(distance // abs(distance), distance, distance // abs(distance)):
                            try:
                                if board[(self.coords[0] + current_distance, self.coords[1])]:
                                    good_cells[(x, y)] = False
                                    break
                            except KeyError:
                                pass
                        else:
                            good_cells[(x, y)] = True
        rook_good_cells = good_cells.copy()
        good_cells.clear()
        for x in range(1, 9):
            for y in range(1, 9):
                if abs(x - self.coords[0]) != abs(y - self.coords[1]):
                    good_cells[(x, y)] = False
                else:
                    distance = x - self.coords[0]
                    if y - self.coords[1] < 0:
                        for x_distance in range(distance // abs(distance), distance, distance // abs(distance)):
                            try:
                                if board[self.coords[0] + x_distance, self.coords[1] - abs(x_distance)]:
                                    good_cells[(x, y)] = False
                                    break
                            except KeyError:
                                pass
                        else:
                            good_cells[(x, y)] = True
                    elif y - self.coords[1] > 0:
                        for x_distance in range(distance // abs(distance), distance, distance // abs(distance)):
                            try:
                                if board[self.coords[0] + x_distance, self.coords[1] + abs(x_distance)]:
                                    good_cells[(x, y)] = False
                                    break
                            except KeyError:
                                pass
                        else:
                            good_cells[(x, y)] = True
                    else:
                        good_cells[(x, y)] = False
        bishop_good_cells = good_cells.copy()
        good_cells.clear()
        for x in range(1, 9):
            for y in range(1, 9):
                good_cells[(x, y)] = rook_good_cells[(x, y)] + bishop_good_cells[(x, y)]
        return good_cells


class King(Piece):
    def __init__(self, coords, colour, *group):
        self.image = load_image(f'{colour}K')
        super(King, self).__init__(coords, colour, *group)

    def can_move(self, board):
        good_cells = {}
        for x in range(1, 9):
            for y in range(1, 9):
                try:
                    if abs(x - self.coords[0]) <= 1 and abs(y - self.coords[1]) <= 1 and (x, y) != self.coords:
                        good_cells[(x, y)] = True
                    else:
                        good_cells[(x, y)] = False
                except KeyError:
                    pass
        return good_cells