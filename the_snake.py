from random import choice, randrange, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
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

# Золотое яблоко
GOLD_APPLE_COLOR = (255, 255, 0)

# Цвет какахи
SHIT_COLOR = (150, 75, 0)

# Цвет камня
STONE_COLOR = (144, 144, 144)

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
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс (яблоко)"""

    def __init__(self):
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_type(self):
        """Тип яблока"""
        chance_gold_apple = randint(1, 15)
        if chance_gold_apple == 1:
            self.body_color = GOLD_APPLE_COLOR
        else:
            self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Меняет положение яблока на случайное"""
        self.randomize_type()
        # randint -> randrange
        apple_weight = randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
        # randint -> randrange
        apple_height = randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
        self.position = (apple_weight, apple_height)


class Shit(GameObject):
    """Дочерний класс (какаха)"""

    def __init__(self):
        self.position = None
        self.body_color = SHIT_COLOR

    def randomize_spawn(self):
        """Шанс какахи"""
        return randint(1, 2)

    def randomize_position(self):
        """Меняет положение какахи на случайное"""
        if self.randomize_spawn() == 1:
            shit_weight = randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
            shit_height = randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
            self.position = (shit_weight, shit_height)
        elif self.position:
            self.position = None


class Stone(GameObject):
    """Дочерний класс (камень)"""

    def __init__(self):
        self.position = None
        self.body_color = STONE_COLOR

    def randomize_spawn(self):
        """Шанс камня"""
        return randint(1, 5)

    def randomize_position(self):
        """Меняет положение камня на случайное"""
        if self.randomize_spawn() == 1:
            stone_weight = randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
            stone_height = randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
            self.position = (stone_weight, stone_height)
        elif self.position:
            self.position = None


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
        a, b = self.get_head_position()
        # Следующая позиция головы змейки
        next_head_position = (a + self.direction[0] * GRID_SIZE,
                              b + self.direction[1] * GRID_SIZE)
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

    def reset(self):
        """Обновляет змейку в начальное состояние"""
        self.__init__()
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """Выход из игры и смена направлений с помощью клавиш клавиатуры"""
    directions = {
        (pygame.K_LEFT, UP): LEFT, (pygame.K_LEFT, DOWN): LEFT,
        (pygame.K_RIGHT, UP): RIGHT, (pygame.K_RIGHT, DOWN): RIGHT,
        (pygame.K_UP, LEFT): UP, (pygame.K_UP, RIGHT): UP,
        (pygame.K_DOWN, LEFT): DOWN, (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_a, UP): LEFT, (pygame.K_a, DOWN): LEFT,
        (pygame.K_d, UP): RIGHT, (pygame.K_d, DOWN): RIGHT,
        (pygame.K_w, LEFT): UP, (pygame.K_w, RIGHT): UP,
        (pygame.K_s, LEFT): DOWN, (pygame.K_s, RIGHT): DOWN
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            game_object.next_direction = directions.get(
                (event.key, game_object.direction)
            )


def main():
    """Main"""
    pygame.init()
    apple = Apple()
    snake = Snake()
    shit = Shit()
    stone = Stone()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            if apple.body_color == APPLE_COLOR:
                snake.length += 1
            else:
                snake.length += 5
            while apple.position in snake.positions:
                apple.randomize_position()
            if snake.length > 5:
                shit.randomize_position()
                stone.randomize_position()
        if snake.get_head_position() == shit.position:
            snake.length -= 5
            del snake.positions[-5:]
            shit.position = None
        if snake.get_head_position() == stone.position:
            snake.reset()
            apple.randomize_position()
            shit.randomize_position()
            stone.randomize_position()
        shit.draw() if shit.position else None
        stone.draw() if stone.position else None
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

# Спасибо за помощь с ошибками! Буду рад и дальше с вами учиться:)
# Ненмного не понял с методом draw(), но вроде исправил(меньше строк стало)
