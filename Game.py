import pygame
import random


class Game:
    __O_WIDTH = 10
    __B_WIDTH = 3
    __S_WIDTH = 100 * __O_WIDTH
    __S_HEIGHT = 60 * __O_WIDTH
    __M_HEIGHT = 40

    __U = [0, -__O_WIDTH]
    __D = [0, __O_WIDTH]
    __L = [-__O_WIDTH, 0]
    __R = [__O_WIDTH, 0]

    __FONT = 'David MS'
    __SIZE = 30
    __SCORE = 'Score: '
    __INSTRUCTIONS = '\'p\'-Pause | \'Esc\'-Exit'
    __PAUSE = 'Game paused'
    __CONT = 'Press \'c\' to continue'
    __GAME_OVER_MSG = 'GAME OVER!'
    __NEW_GAME_MSG = 'Press \'n\' to play again'
    __QUIT_GAME_MSG = 'Press \'Esc\' to exit'

    def __init__(self):
        """
        Initializes a game object.
        """
        self.__init_game()
        self.__init_values()
        self.__init_colors()

    def __init_values(self):
        """
        Initializes the values for the game.
        """
        self.__direction = self.__U
        self.__snake = [[self.__S_WIDTH // 2, self.__S_HEIGHT // 2]]
        self.__foods = list()
        self.__counter = 0
        self.__score = 0
        self.__running = True
        self.__start = True
        self.__end_game = False
        self.__pause = False
        self.__refresh_rate = 15
        self.__food_frequency = 29
        self.__max_food = 5

    def __init_game(self):
        """
        Initializes the game window.
        """
        pygame.init()
        pygame.font.init()
        self.__screen = pygame.display.set_mode((self.__S_WIDTH, self.__S_HEIGHT + self.__M_HEIGHT))
        self.__font = pygame.font.SysFont(self.__FONT, self.__SIZE, True)
        self.__clock = pygame.time.Clock()

    def __init_colors(self):
        """
        Initializes the colors used for the game.
        """
        self.__def_color = (255, 255, 255)
        self.__bg_color = (0, 0, 0)
        self.__snake_color = (255, 255, 255)
        self.__food_color = (0, 255, 0)
        self.__text_color = (255, 255, 255)

    def run(self):
        """
        Runs the game.
        """
        while self.__running:
            self.__run_loop()
        self.__quit()

    def __run_loop(self):
        """
        Runs the main loop of the game.
        """
        if self.__start:
            self.__start_screen()
        elif self.__end_game:
            self.__end_loop()
        elif self.__pause:
            self.__pause_loop()
        else:
            self.__game_screen()

    def __pause_loop(self):
        """
        Waits for the player to resume the game or quit.
        """
        while self.__pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__pause = False
                    self.__end_game = True
                elif event.type == pygame.KEYUP and event.key == pygame.K_c:
                    self.__pause = False

    def __start_screen(self):
        """
        Shows the start screen and waits for the player to respond.
        """
        text = self.__font.render('Press \'s\' to start game', False, (255, 255, 255))
        self.__screen.blit(text, (self.__S_WIDTH // 3, self.__S_HEIGHT // 5))
        pygame.display.flip()
        while self.__start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__start = False
                    self.__running = False
                if event.type == pygame.KEYUP and event.key == pygame.K_s:
                    self.__start = False

    def __end_loop(self):
        """
        Waits for the player to either quit or restart the game.
        """
        while self.__end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    self.__end_game = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.__running = False
                    self.__end_game = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_n:
                    self.__end_game = False
                    self.__snake = [[self.__S_WIDTH // 2, self.__S_HEIGHT // 2]]
                    self.__foods = list()
                    self.__score = 0

    def __game_screen(self):
        """
        Runs the main game screen.
        """
        self.__check_quit_event()
        if self.__running:
            self.__game_loop()

    def __game_loop(self):
        """
        Responds to the player and updates the game screen.
        """
        self.__screen.fill(self.__bg_color)
        self.__handle_food()
        self.__handle_keys()
        self.__handle_movement()
        self.__draw()
        self.__update()

    def __check_quit_event(self):
        """
        Checks if the player chose to quit the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

    def __handle_food(self):
        """
        Checks if a food piece should be added to the game.
        """
        if (self.__counter % self.__food_frequency) == 0:
            if len(self.__foods) < self.__max_food:
                self.__make_food()

    def __make_food(self):
        """
        Makes a food piece and adds it to the screen.
        """
        pos = self.__make_food_pos()
        while pos in self.__snake or pos in self.__foods:
            pos = self.__make_food_pos()
        self.__foods.append(pos)

    def __make_food_pos(self):
        """
        Generates a random position for the food piece
        """
        x = random.randint(0, self.__S_WIDTH // self.__O_WIDTH) * self.__O_WIDTH
        y = random.randint(0, self.__S_HEIGHT // self.__O_WIDTH - 1) * self.__O_WIDTH
        return [x, y]

    def __handle_keys(self):
        """
        Handles key presses from the player.
        """
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.__running = False
        elif pressed[pygame.K_p]:
            self.__pause_screen()
        elif pressed[pygame.K_UP]:
            self.__move_up()
        elif pressed[pygame.K_DOWN]:
            self.__move_down()
        elif pressed[pygame.K_LEFT]:
            self.__move_left()
        elif pressed[pygame.K_RIGHT]:
            self.__move_right()

    def __pause_screen(self):
        """
        Shows the 'Pause' screen.
        """
        self.__screen.blit(self.__font.render(self.__PAUSE, False, self.__text_color),
                           (self.__S_WIDTH // 2.5, self.__S_HEIGHT // 5))
        self.__screen.blit(self.__font.render(self.__CONT, False, self.__text_color),
                           (self.__S_WIDTH // 2.75, self.__S_HEIGHT // 4))
        self.__pause = True

    def __move_up(self):
        """
        Handles moving up.
        """
        if self.__direction not in [self.__U, self.__D]:
            self.__direction = self.__U

    def __move_down(self):
        """
        Handles moving down.
        """
        if self.__direction not in [self.__U, self.__D]:
            self.__direction = self.__D

    def __move_left(self):
        """
        Handles moving left.
        """
        if self.__direction not in [self.__R, self.__L]:
            self.__direction = self.__L

    def __move_right(self):
        """
        Handles moving right.
        """
        if self.__direction not in [self.__R, self.__L]:
            self.__direction = self.__R

    def __handle_movement(self):
        """
        Handles results of movement of the player.
        """
        if self.__check_eat():
            self.__eat()
        elif self.__check_collisions():
            self.__game_over_screen()
        else:
            self.__move_snake()

    def __check_eat(self):
        """
        Checks weather the snake reached a piece of food.
        """
        return [self.__snake[0][0] + self.__direction[0], self.__snake[0][1] + self.__direction[1]] in self.__foods

    def __eat(self):
        """
        Feeds the piece of food to the snake.
        """
        self.__snake.insert(0, self.__foods.pop(self.__foods.index([self.__snake[0][0] + self.__direction[0],
                                                                    self.__snake[0][1] + self.__direction[1]])))
        self.__score += 1

    def __check_collisions(self):
        """
        Checks collision between the snake and itself or the edges.
        """
        return self.__snake[0] in self.__snake[1:] or \
            (self.__check_vertical_collision() or self.__check_horizontal_collision())

    def __check_vertical_collision(self):
        """
        Checks collision between the snake and the vertical edges.
        """
        return not (0 <= (self.__snake[0][1] + self.__direction[1]) <= (self.__S_HEIGHT - self.__O_WIDTH))

    def __check_horizontal_collision(self):
        """
        Checks collision between the snake and the horizontal edges.
        """
        return not (0 <= (self.__snake[0][0] + self.__direction[0]) <= (self.__S_WIDTH - self.__O_WIDTH))

    def __game_over_screen(self):
        """
        Shows the 'Game Over' screen.
        """
        self.__screen.blit(self.__font.render(self.__GAME_OVER_MSG, False, self.__text_color),
                           (self.__S_WIDTH // 2.5, self.__S_HEIGHT // 5))
        self.__screen.blit(self.__font.render(self.__NEW_GAME_MSG, False, self.__text_color),
                           (self.__S_WIDTH // 3, self.__S_HEIGHT // 4))
        self.__screen.blit(self.__font.render(self.__QUIT_GAME_MSG, False, self.__text_color),
                           (self.__S_WIDTH // 2.75, self.__S_HEIGHT // 3.5))
        self.__end_game = True

    def __move_snake(self):
        """
        Moves the snake.
        """
        if len(self.__snake) == 1:
            self.__snake[0][0] += self.__direction[0]
            self.__snake[0][1] += self.__direction[1]
        else:
            self.__snake.pop()
            self.__snake.insert(0, [self.__snake[0][0] + self.__direction[0], self.__snake[0][1] + self.__direction[1]])

    def __draw(self):
        """
        Calls drawing methods.
        """
        self.__draw_sub_menu()
        self.__draw_snake()
        self.__draw_food()

    def __draw_sub_menu(self):
        """
        Draws the menu beneath the game.
        """
        pygame.draw.rect(self.__screen, self.__def_color,
                         pygame.Rect(0, self.__S_HEIGHT, self.__S_WIDTH, self.__B_WIDTH))
        self.__screen.blit(self.__font.render(self.__SCORE + str(self.__score), False, self.__text_color),
                           (0, self.__S_HEIGHT + self.__O_WIDTH))
        self.__screen.blit(self.__font.render(self.__INSTRUCTIONS, False, self.__text_color),
                           (self.__S_WIDTH // (3 / 2.25), self.__S_HEIGHT + self.__O_WIDTH))

    def __draw_snake(self):
        """
        Draws the snake.
        """
        for pos in self.__snake:
            pygame.draw.rect(self.__screen, self.__snake_color,
                             pygame.Rect(pos[0], pos[1], self.__O_WIDTH, self.__O_WIDTH))

    def __draw_food(self):
        """
        Draws the pieces of food.
        """
        for food in self.__foods:
            pygame.draw.rect(self.__screen, self.__food_color,
                             pygame.Rect(food[0], food[1], self.__O_WIDTH, self.__O_WIDTH))

    def __update(self):
        """
        Updates the screen
        """
        pygame.display.flip()
        self.__counter += 1
        self.__clock.tick(self.__refresh_rate)

    @staticmethod
    def __quit():
        """
        Quits pygame.
        """
        pygame.font.quit()
        pygame.quit()
