import pygame
from rgb_colors_lib import *


class Button(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, rect: pygame.Rect):
        super().__init__(self)
        self.image = image
        self.rect = rect
    
    def click(self) -> None:
        self.rect.fill



# Инициализация pygame
pygame.init()

# Установка размеров окна
screen = pygame.display.set_mode((1920, 1080))

# Установка FPS в переменную
FPS = 30

# Установка заголовка окна
pygame.display.set_caption("My Game")

# Получение Часов
clock = pygame.time.Clock()

# Цикл игры
game_loop = True
while game_loop:
    # Контроль FPS
    clock.tick(FPS)
    # Рендеринг
    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()

    # События
    for event in pygame.event.get():
        # Проврить закрытие окна
        if event.type == pygame.QUIT:
            game_loop = False
        

# Деинициализация Pygame
pygame.quit()