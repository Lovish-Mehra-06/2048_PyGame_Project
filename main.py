# # Interactive and Visually appealing 2048 Game using pygame Module

import pygame
import random

pygame.init()

# Initial set up, Title & Icon
WIDTH, HEIGHT = 400, 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
Icon = pygame.image.load("Icon_2048_Game.png")
pygame.display.set_icon(Icon)

# 2048 Game Color Library
colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
          16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114),
          256: (237, 204, 97), 512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46),
          'light text': (249, 246, 242), 'dark text': (119, 110, 101), 'other': (0, 0, 0), 'bg': (187, 173, 160)}


# ---------------- Game Variables Initializing here :) 
'''This line of code creates a 4x4 grid (2D list) initialized with zeros. Here's how it works:
board_values = [[0 for _ in range(4)] for _ in range(4)]
List Comprehension (Inner Loop):                 [0 for _ in range(4)]
Creates a list of 4 zeros → [0, 0, 0, 0].
_ is a throwaway variable (not used).

Outer Loop:                                      for _ in range(4)
Runs 4 times, creating 4 rows of [0, 0, 0, 0].
ie
[
    [0, 0, 0, 0],  
    [0, 0, 0, 0],  
    [0, 0, 0, 0],  2
    [0, 0, 0, 0]  
]
'''
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over, spawn_new, init_count = False, True, 0
direction = ''
font = pygame.font.Font('freesansbold.ttf', 35)

score = 0
file = open('high_score', 'r')
init_high = int(file.readline()) # Read Data
file.close()
high_score = init_high


# Draw game over and restart text -----
def draw_over():
    font = pygame.font.Font('freesansbold.ttf', 25)

    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# # ---------------- Take Ur turn Based on Direction ----------------
def take_turn(dir, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]

    if dir == 'UP':
        for j in range(4):
            for i in range(1, 4):
                if board[i][j] != 0:
                    shift = i
                    while shift > 0 and board[shift - 1][j] == 0:
                        board[shift - 1][j] = board[shift][j]
                        board[shift][j] = 0
                        shift -= 1
                    if shift > 0 and board[shift - 1][j] == board[shift][j] and not merged[shift - 1][j]:
                        board[shift - 1][j] *= 2
                        score += board[shift - 1][j]
                        board[shift][j] = 0
                        merged[shift - 1][j] = True

    elif dir == 'DOWN':
        for j in range(4):
            for i in range(2, -1, -1):
                if board[i][j] != 0:
                    shift = i
                    while shift < 3 and board[shift + 1][j] == 0:
                        board[shift + 1][j] = board[shift][j]
                        board[shift][j] = 0
                        shift += 1
                    if shift < 3 and board[shift + 1][j] == board[shift][j] and not merged[shift + 1][j]:
                        board[shift + 1][j] *= 2
                        score += board[shift + 1][j]
                        board[shift][j] = 0
                        merged[shift + 1][j] = True

    elif dir == 'LEFT':
        for i in range(4):
            for j in range(1, 4):
                if board[i][j] != 0:
                    shift = j
                    while shift > 0 and board[i][shift - 1] == 0:
                        board[i][shift - 1] = board[i][shift]
                        board[i][shift] = 0
                        shift -= 1
                    if shift > 0 and board[i][shift - 1] == board[i][shift] and not merged[i][shift - 1]:
                        board[i][shift - 1] *= 2
                        score += board[i][shift - 1]
                        board[i][shift] = 0
                        merged[i][shift - 1] = True

    elif dir == 'RIGHT':
        for i in range(4):
            for j in range(2, -1, -1):
                if board[i][j] != 0:
                    shift = j
                    while shift < 3 and board[i][shift + 1] == 0:
                        board[i][shift + 1] = board[i][shift]
                        board[i][shift] = 0
                        shift += 1
                    if shift < 3 and board[i][shift + 1] == board[i][shift] and not merged[i][shift + 1]:
                        board[i][shift + 1] *= 2
                        score += board[i][shift + 1]
                        board[i][shift] = 0
                        merged[i][shift + 1] = True

    return board


# Spawn in the NEW Pieces randomly when turn starts ----------------
def new_pieces(board):
    count = 0
    while any(0 in row for row in board) and count < 1:
        row, col = random.randint(0, 3), random.randint(0, 3)
        if board[row][col] == 0:
            board[row][col] = 4 if random.randint(1, 10) == 10 else 2
            count += 1
    return board, count == 0



# ------------------ Draw Bg for the board ----------------
'''pygame.draw.rect(screen, color, rect, width, border_radius)

--> screen:           The surface where the rectangle is drawn. You need to define screen before calling this function.
--> (200, 200, 200):  The RGB color of the rectangle (light gray).
--> [0, 0, 400, 400]: Defines the rectangle with:
--> 0, 0:             Top-left corner at (0,0).
--> 400, 400:         Width and height of 400x400 pixels.
--> 0:                This means the rectangle is filled. If you give a number (>0), it sets the border thickness instead.
--> 10:               The border radius, making the corners rounded.

It draws a gray 400x400px rectangle with rounded corners on the screen at (0,0).
'''
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)

    score_text = font.render(f'Score: {score}', True, 'Black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))

    pass

# # ---------------- Draw Tiles for the board ----------------
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            color = colors[value] if value <= 2048 else colors['other']
            value_color = colors['light text'] if value > 8 else colors['dark text']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * len(str(value))))
                text = font.render(str(value), True, value_color)
                screen.blit(text, text.get_rect(center=(j * 95 + 57, i * 95 + 57)))
            pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 3, 4)


# ------------------------ Main Game Loop ----------------------
run = True
timer = pygame.time.Clock()
fps = 60
while run:
    timer.tick(fps)
    screen.fill('grey')
    draw_board()
    draw_pieces(board_values)

    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new, init_count = False, init_count + 1

    if direction:
        board_values = take_turn(direction, board_values)
        direction, spawn_new = '', True

    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYUP:
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False
            else:
                direction = {pygame.K_UP: 'UP', pygame.K_DOWN: 'DOWN', pygame.K_LEFT: 'LEFT', pygame.K_RIGHT: 'RIGHT'}.get(event.key, '')


    if score > high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()
