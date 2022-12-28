import pygame
from random import randrange, choice
import numpy
import time
from pygame import mixer

pygame.init()

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
    
def play():
    class Square:
        height = 100
        width = 100
        
        def __init__(self, row, column, value):
            self.row = row
            self.column = column
            self.value = value

    def create_square(intensity):
        if intensity >= len(numbers):
            square = Square(0, randrange(5), choice(list(numbers.keys())[:]))
        else:
            square = Square(0, randrange(5), choice(list(numbers.keys())[:5 + intensity]))
        screen.fill((255,255,255), pygame.Rect(top_left_x, top_left_y-100,top_left_x+610,top_left_y))
        screen.fill(numbers[square.value], pygame.Rect(top_left_x + 100*square.column, top_left_y-100,100,100))
        screen.blit(square.value, (top_left_x + 11 +square.column * 100, top_left_y + 7 - 100))
        pygame.display.flip()
        return square

    def update_state(board, taken_squares = {}):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if (j,i) in taken_squares:
                    board[i][j] = taken_squares[(j,i)]
                    
    def check_and_merge(board, square):
        if board[square.row][square.column] != 0:
            count = 0
            again = False
            fall = False
            nonlocal score
            nonlocal score_change
            nonlocal fall_time

            sqaure_merge = mixer.Sound("square_merge.wav")
            draw_scoreBoard(score)
            print('before', [[scores[num] for num in row] for row in board])
            if square.column != 0 and board[square.row][square.column - 1] == square.value:
                count += 1
                board[square.row][square.column - 1] = 0
                #sqaure_merge.play()
                again = True
                
            if square.column != 4 and board[square.row][square.column + 1] == square.value:
                count += 1
                board[square.row][square.column + 1] = 0
                #sqaure_merge.play()
                again = True

            if square.row != 5 and board[square.row + 1][square.column] == square.value:
                count += 1
                board[square.row + 1][square.column] = 0
                #sqaure_merge.play()
                fall = True
                
            if square.row != 0 and board[square.row - 1][square.column] == square.value:
                count += 1
                board[square.row - 1][square.column] = 0
                #sqaure_merge.play()
            print(count, [[scores[num] for num in row] for row in board])
            board[square.row][square.column] = list(numbers.keys())[list(numbers.keys()).index(square.value) + count]
            square.value = list(numbers.keys())[list(numbers.keys()).index(square.value) + count]
            score += 2 * scores[square.value] * count
            score_change += 2 * scores[square.value] * count
            if count != 0:
                sqaure_merge.play()
                draw_board(board)
                draw_scoreBoard(score)
                time.sleep(0.44)
                fall_time -= 0.44
            
            flattened_board = list(numpy.concatenate(board).flat)
            for i in range(len(board)-1):
                for j in range(len(board[i])):
                    if board[i][j] != 0 and board[i+1][j] == 0:
                        board[i+1][j] = board[i][j]
                        board[i][j] = 0
                        #check_and_merge(board, Square(i+1, j, board[i+1][j]))
            updated_flattened_board = list(numpy.concatenate(board).flat)
            if flattened_board != updated_flattened_board:
                draw_board(board)
                time.sleep(0.44)
                fall_time -= 0.44
            if fall:
                check_and_merge(board, Square(square.row+1, square.column, square.value))
            elif again:
                check_and_merge(board, square)
            
            if flattened_board != updated_flattened_board:
                for i in range(len(board)):
                    for j in range(len(board[i])):
                        check_and_merge(board, Square(i,j,board[i][j]))
            
            draw_scoreBoard(score)
            #check_and_merge(board, updated_square)
                    
    def is_valid(board, square, move):
        if move == "down":
            if (square.row + 1) > 5:
                return 'invalid'
            elif board[square.row + 1][square.column] != 0:
                return 'taken'
        elif move == "left":
            if (square.column - 1) < 0:
                return 'invalid'
            elif board[square.row][square.column - 1] != 0:
                return 'invalid'
        elif move == "right":
            if (square.column + 1) > 4:
                return 'invalid'
            elif board[square.row][square.column + 1] != 0:
                return 'invalid'
        return 'valid'
    
    def collapse(board, square, column, drop_sound):

        for i in range(len(board)-1):
            res = i
            if board[i+1][column] != 0 or i==len(board):
                board[i][column] = square.value
                initiate_fall(Square(i, column, square.value))
                draw_board(board)
                time.sleep(0.44)
                return Square(i, column, square.value)
        board[len(board)-1][column] = square.value
        initiate_fall(Square(len(board)-1, column, square.value))
        draw_board(board)
        drop_sound.play()
        time.sleep(0.44)
        return Square(len(board)-1, column, square.value)
    
    def initiate_fall(square):
        y = top_left_y + 51
        square_fall_time = 0
        square_fall_speed = 0.05
        clock = pygame.time.Clock()
        step = 50
        while y != top_left_y+1+square.row*100:
            square_fall_time += clock.get_rawtime()
            clock.tick()
            if square_fall_time/1000 >= square_fall_speed:
                square_fall_time = 0
                screen.fill((255,255,255), pygame.Rect(top_left_x + 1 + 100*square.column, y - step,98,98))
                screen.fill(numbers[square.value], pygame.Rect(top_left_x + 1 + 100*square.column, y,98,98))
                screen.blit(square.value, (top_left_x + 11 + square.column*100, y + 7))
                pygame.display.update(pygame.Rect(top_left_x + 1 + 100*square.column, top_left_y+1,98,720))
                y += step
                    
    def draw_board(board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    #pygame.draw.rect(screen, (10,10,10), (top_left_x + j*100, top_left_y+i*100,100,100),1)
                    screen.fill((255,255,255), pygame.Rect(top_left_x + j*100, top_left_y+i*100,100,100))
                else:
                    #pygame.draw.rect(screen, (10,10,10), (top_left_x + j*100, top_left_y+i*100,100,100),1)
                    screen.fill(numbers[board[i][j]], pygame.Rect(top_left_x + j*100, top_left_y+i*100,100,100))
                    screen.blit(board[i][j], (top_left_x + 11 + j*100, top_left_y + 7 + i*100))
                    
        for i in range(6):
            pygame.draw.line(screen, (0,0,0), (top_left_x + i*100, top_left_y), (top_left_x + i*100, top_left_y + 600))
        pygame.draw.line(screen, (0,0,0), (top_left_x, top_left_y + 0*100), (top_left_x + 500, top_left_y + 0*100))
        pygame.draw.line(screen, (0,0,0), (top_left_x, top_left_y + 6*100), (top_left_x + 500, top_left_y + 6*100))
        #pygame.draw.rect(screen, (10,10,10), (top_left_x + j*100, top_left_y+i*100,100,100),1)
        #screen.blit(square.value, (top_left_x + 11 + square.x*100, top_left_y + 7 + square.y*100))
        pygame.display.update()
        
    def is_over(board, column = None):
        if column != None:
            if board[0][column] == 0:
                return False
            return True
        else:
            for i in range(len(board[0])):
                if board[0][i] == 0:
                    return False
            return True
            
        
    def draw_square(square):
        screen.fill((255,255,255), pygame.Rect(top_left_x, top_left_y-100,top_left_x+610,top_left_y))
        screen.fill(numbers[square.value], pygame.Rect(top_left_x + 100*square.column, top_left_y-100,100,100))
        screen.blit(square.value, (top_left_x + 11 +square.column * 100, top_left_y + 7 - 100))
                
    def draw_scoreBoard(score):
        #screen.fill((255,255,255))
        total_score = get_font(50).render(str(score), 1, (0,0,0))
        image = pygame.image.load("play.png")
        screen.blit(image, (15, 0))
        scoreBoard = total_score.get_rect(center=(200, 50))
        screen.blit(total_score, scoreBoard)


                    
    s_width = 1280
    s_height = 720
    play_width = 710
    play_height = 570
    block_size = 100

    screen = pygame.display.set_mode([s_width, s_height])
    top_left_x = s_width - play_width - 150
    top_left_y = s_height - play_height - 50
    running = True
    screen.fill((255,255,255))
    font = get_font(25)

    two = font.render('2', 1, (255,255,255))
    four = font.render('4', 1, (255,255,255))
    eight = font.render('8', 1, (255,255,255))
    sixteen = font.render('16', 1, (255,255,255))
    thirty2 = font.render('32', 1, (255,255,255))
    sixty4 = font.render('64', 1, (255,255,255))
    hundred28 = font.render('128', 1, (255,255,255))
    two_hundred56 = font.render('256', 1, (255,255,255))
    five_hundred12 = font.render('512', 1, (255,255,255))
    thousand024 = font.render('1024', 1, (255,255,255))
    two_thousand048 = font.render('2048', 1, (255,255,255))

    numbers = {two: (0,128,0), four: (205,85,85), eight: (255,246,143), sixteen: (178,223,238), thirty2: (255,174,185), sixty4: (255,165,0), hundred28: (84,139,84), two_hundred56: (139,95,101), five_hundred12: (139,37,0), thousand024: (106,90,205), two_thousand048: (69, 69, 69)}
    scores = {two: 2, four: 4, eight: 8, sixteen: 16, thirty2: 32, sixty4: 64, hundred28: 128, two_hundred56: 256, five_hundred12: 512, thousand024: 1024, two_thousand048: 2048, 0: 0}
    score = 0
    score_change = 0
    board = [[0 for i in range(5)] for j in range(6)]
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.44
    intensity = 0

    current_square = create_square(intensity)
    draw_scoreBoard(0)
    while running:
        drop_sound = mixer.Sound("drop.wav")

        if score_change >= 5000:
            intensity += 1
            score_change = 0
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if is_over(board, 0) == False:
                        if board[1][0] != 0:
                            next_square = create_square(intensity)
                            board[0][0] = current_square.value
                            screen.fill(numbers[current_square.value], pygame.Rect(top_left_x + 0*100, top_left_y+0*100,100,100))
                            screen.blit(current_square.value, (top_left_x + 11 + 0*100, top_left_y + 7 + 0*100))
                            drop_sound.play()
                            draw_board(board)
                            check_and_merge(board, Square(0,0,current_square.value))
                            current_square = next_square
                            
                        else:
                            next_square = create_square(intensity)
                            current_square = collapse(board, current_square, 0, drop_sound)
                            check_and_merge(board, current_square)
                            current_square = next_square
                            
                elif event.key == pygame.K_2:
                    if not is_over(board, 1):
                        if board[1][1] != 0:
                            next_square = create_square(intensity)
                            board[0][1] = current_square.value
                            screen.fill(numbers[current_square.value], pygame.Rect(top_left_x + 1*100, top_left_y+0*100,100,100))
                            screen.blit(current_square.value, (top_left_x + 11 + 1*100, top_left_y + 7 + 0*100))
                            drop_sound.play()
                            draw_board(board)
                            check_and_merge(board, Square(0,1,current_square.value))
                            current_square = next_square
                           
                            
                        else:
                            next_square = create_square(intensity)
                            current_square = collapse(board, current_square, 1, drop_sound)
                            check_and_merge(board, current_square)
                            current_square = next_square
                            
                elif event.key == pygame.K_3:
                    if not is_over(board, 2):
                        if board[1][2] != 0:
                            next_square = create_square(intensity)
                            board[0][2] = current_square.value
                            screen.fill(numbers[current_square.value], pygame.Rect(top_left_x + 2*100, top_left_y+0*100,100,100))
                            screen.blit(current_square.value, (top_left_x + 11 + 2*100, top_left_y + 7 + 0*100))
                            drop_sound.play()
                            draw_board(board)
                            check_and_merge(board, Square(0,2,current_square.value))
                            current_square = next_square
                            
                        else:
                            next_square = create_square(intensity)
                            current_square = collapse(board, current_square, 2, drop_sound)
                            check_and_merge(board, current_square)
                            current_square = next_square
                        
                elif event.key == pygame.K_4:
                    if not is_over(board, 3):
                        if board[1][3] != 0:
                            next_square = create_square(intensity)
                            board[0][3] = current_square.value
                            screen.fill(numbers[current_square.value], pygame.Rect(top_left_x + 3*100, top_left_y+0*100,100,100))
                            screen.blit(current_square.value, (top_left_x + 11 + 3*100, top_left_y + 7 + 0*100))
                            drop_sound.play()
                            draw_board(board)
                            
                            check_and_merge(board, Square(0,3,current_square.value))
                            current_square = next_square
                            
            
                        else:
                            next_square = create_square(intensity)
                            current_square = collapse(board, current_square, 3, drop_sound)
                            
                            check_and_merge(board, current_square)
                            current_square = next_square
                            
                elif event.key == pygame.K_5:
                    if not is_over(board, 4):
                        if board[1][4] != 0:
                            next_square = create_square(intensity)
                            board[0][4] = current_square.value
                            screen.fill(numbers[current_square.value], pygame.Rect(top_left_x + 4*100, top_left_y+0*100,100,100))
                            screen.blit(current_square.value, (top_left_x + 11 + 4*100, top_left_y + 7 + 0*100))
                            drop_sound.play()
                            draw_board(board)
                            check_and_merge(board, Square(0,4,current_square.value))
                            current_square = next_square
                            
                        else:
                            next_square = create_square(intensity)
                            current_square = collapse(board, current_square, 4, drop_sound)
                            check_and_merge(board, current_square)
                            current_square = next_square
                            
                            
        if is_over(board):
            endscreen(score)
        
        #pygame.display.flip()
        draw_board(board)
        #pygame.display.flip()

SCREEN = pygame.display.set_mode((1280,720))
BG = pygame.image.load("rickroll_4k.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        click_sound = mixer.Sound("click.wav")
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("play.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("quit.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    pygame.quit()

        pygame.display.flip()

def endscreen(score):
    while True:
        ES_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        click_sound = mixer.Sound("click.wav")

        ES_TEXT = get_font(45).render("Game Over", True, "Black")
        ES_RECT = ES_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(ES_TEXT, ES_RECT)

        Score_TEXT = get_font(30).render("Score {}".format(score), True, "Black")
        Score_RECT = ES_TEXT.get_rect(center=(700, 300))
        SCREEN.blit(Score_TEXT, Score_RECT)

        ES_Restart = Button(image=None, pos=(640, 460), 
                            text_input="RESTART", font=get_font(75), base_color="Black", hovering_color="Green")

        ES_BACK = Button(image=None, pos=(640, 550), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        ES_Restart.changeColor(ES_MOUSE_POS)
        ES_Restart.update(SCREEN)

        ES_BACK.changeColor(ES_MOUSE_POS)
        ES_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                click_sound.play()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ES_BACK.checkForInput(ES_MOUSE_POS):
                    click_sound.play()
                    main_menu()
                if ES_Restart.checkForInput(ES_MOUSE_POS):
                    click_sound.play()
                    play()

        pygame.display.update()

mixer.music.load("background.wav")
mixer.music.play(-1)
main_menu()