from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс"""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод отрисовки для объектов"""
        pass


class Apple(GameObject):
    """Дочерний класс (яблоко)"""

    def __init__(self):
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Меняет положение яблока на случайное"""
        apple_weight = randint(0, 31) * GRID_SIZE
        apple_height = randint(0, 23) * GRID_SIZE
        self.position = (apple_weight, apple_height)

    def draw(self):
        """Отрисовывает яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс (змея)"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Меняет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод работает с координатами змейки"""
        self.update_direction()
        head_position = self.get_head_position()
        # Следующая позиция головы змейки
        next_head_position = (head_position[0] + self.direction[0] * GRID_SIZE,
                              head_position[1] + self.direction[1] * GRID_SIZE)
        # Следующая позиция головы змейки учитывая границы
        next_head_position_bor = (next_head_position[0] % SCREEN_WIDTH,
                                  next_head_position[1] % SCREEN_HEIGHT)

        if next_head_position_bor in self.positions:
            self.reset()
        else:
            self.positions.insert(0, next_head_position_bor)
            self.last = self.positions[-1]
        if (self.last is not None) and (len(self.positions) > self.length + 1):
            self.positions.pop(-1)

    def get_head_position(self):
        """Возвращает координаты головы змейки"""
        return self.positions[0]

    def draw(self):
        """Отрисовывает змею"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def reset(self):
        """Обновляет змейку в начальное состояние"""
        self.__init__()
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """Выход из игры и смена направлений с помощью клавиш клавиатуры"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main"""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            while True:
                apple.randomize_position()
                if apple.position in snake.positions:
                    apple.randomize_position()
                else:
                    break
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
