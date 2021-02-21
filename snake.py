import pygame
import time
import random
import sys

### init

black = (0, 0, 0)
red = (252, 0, 0)
blue = (0, 0, 252)
white = (255, 255, 255)
yellow = (241, 255, 30)

pygame.init()
screen = pygame.display.set_mode((840, 690))
pygame.display.set_caption("snake")
screen.fill(black)

# class Food
class Food:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.x = x
        self.y = y
        
        self.color = white

    def display(self, rect):
        pygame.draw.rect(rect, self.color, self.rect)
        pygame.display.flip()
        
snake_height = 30
snake_width = 30
launched = True
snake = [(130, 220, snake_height, snake_width)]
direction = "right"
has_food = False

### utils

# when game over, we write game over on the screen
def game_over(score, launched):
    pygame.display.set_mode((840, 690))
    arial_font = pygame.font.SysFont("arial", 50) #font and size
    game_over_text = arial_font.render("Game Over... Your score : {}!".format(score), True, blue) #text with font and color
    text_rect = game_over_text.get_rect(center=(int(screen.get_rect().width/2), int(screen.get_rect().height/2))) #we want to center the text
    screen.blit(game_over_text, text_rect) #display the text
    pygame.display.flip()

    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:              
                game(True, [(130, 220, snake_height, snake_width)], "right", False)
                return launched

# to draw the score
def draw_score(score):
    arial_font = pygame.font.SysFont("arial", 30) #font and size
    score_text = arial_font.render("Score : {}".format(len(snake)-1), True, yellow)
    text_rect = score_text.get_rect(center=(55, 20)) 
    return score_text, text_rect

# we draw the snake in the screen
def draw_snake(snake):
    screen = pygame.display.set_mode((840, 690))
    for block in snake:
        rect = pygame.Rect(block[0], block[1], block[2], block[3])
        pygame.draw.rect(screen, red, rect)
    pygame.display.update()

# we watch if the snake touched a food block or not
def touch_food(snake, food):
    if snake[len(snake)-1][0] <= food.x + 30 and snake[len(snake)-1][0] >= food.x - 30 and snake[len(snake)-1][1] <= food.y + 30 and snake[len(snake)-1][1] >= food.y - 30:
        return True
    else:
        return False

# the snake must moving forward, we need to move him
def snake_move(snake, direction, old_direction, food, has_food):
    if len(snake) == 1:
        pass
    else:
        if direction == "up" and old_direction == "down":
            direction = "down"
        if direction == "down" and old_direction == "up":
            direction = "up"
        if direction == "right" and old_direction == "left":
            direction = "left"
        if direction == "left" and old_direction == "right":
            direction = "right"
    
    if food == True:
        if direction == "up":
            snake.append((snake[len(snake)-1][0], snake[len(snake)-1][1]-20, snake_height, snake_width))
            has_food = False
        if direction == "down":
            snake.append((snake[len(snake)-1][0], snake[len(snake)-1][1]+20, snake_height, snake_width))
            has_food = False
        if direction == "left":
            snake.append((snake[len(snake)-1][0]-20, snake[len(snake)-1][1], snake_height, snake_width))
            has_food = False
        if direction == "right":
            snake.append((snake[len(snake)-1][0]+20, snake[len(snake)-1][1], snake_height, snake_width))
            has_food = False

    if food == False:
        if direction == "up":
            snake.append((snake[len(snake)-1][0], snake[len(snake)-1][1]-20, snake_height, snake_width))
            snake.pop(0)
        if direction == "down":
            snake.append((snake[len(snake)-1][0], snake[len(snake)-1][1]+20, snake_height, snake_width))
            snake.pop(0)
        if direction == "left":
            snake.append((snake[len(snake)-1][0]-20, snake[len(snake)-1][1], snake_height, snake_width))
            snake.pop(0)
        if direction == "right":
            snake.append((snake[len(snake)-1][0]+20, snake[len(snake)-1][1], snake_height, snake_width))
            snake.pop(0)

    return snake, has_food, direction # we return the new snake and if he ate food we increase his length

# game over if the snake touches himself
def self_touch(snake, head, direction):
    snake_temp = list(snake) # we work with a copy
    launched = True
    if len(snake) == 1:
        return snake, launched
    snake_temp.pop(len(snake_temp)-1)
    for block in snake_temp:
        if head[1] == block[1] and head[0] == block[0]:
            launched = game_over(len(snake_temp)-1, True)
    return snake, launched

# launch the game
def game(launched, snake, direction, has_food):
    # main boucle
    while launched:
        if snake[len(snake)-1][0] > 810 or snake[len(snake)-1][0] < 0 or snake[len(snake)-1][1] > 660 or snake[len(snake)-1][1] < 0:
            launched = game_over(len(snake)-1, launched)

        old_direction = direction

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = "up"
                if event.key == pygame.K_DOWN:
                    direction = "down"
                if event.key == pygame.K_RIGHT:
                    direction = "right"
                if event.key == pygame.K_LEFT:
                    direction = "left"
                if event.key == pygame.K_SPACE: # the user can pause the game
                    paused = True
                    while paused:
                        for paused_event in pygame.event.get():
                            if paused_event.type == pygame.QUIT:
                                sys.exit()
                            if paused_event.type == pygame.KEYDOWN and paused_event.key == pygame.K_SPACE:
                                paused = False

        draw_snake(snake)
        score_text, text_rect = draw_score(len(snake)-1)
        screen.blit(score_text, text_rect)

        if has_food == False:
            food = Food(random.randint(0, 810), random.randint(0, 660))
            food.display(screen)
            has_food = True

        if has_food == True:
            food.display(screen)

        snake, has_food, direction = snake_move(snake, direction, old_direction, touch_food(snake, food), has_food)

        snake, launched = self_touch(snake, (snake[len(snake)-1][0], snake[len(snake)-1][1]), direction)

        time.sleep(0.1)

game(launched, snake, direction, has_food)