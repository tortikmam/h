import os
import random
import sys
import pygame
import requests


def createMap(x, y, z, l):
    slide = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&z={z}&l={l}"
    response = requests.get(slide)
    if not response:
        print("Ошибка выполнения запроса:")
        print(slide)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = 'Data/maps/map.png'
    with open(map_file, "wb") as file:
        file.write(response.content)
    return pygame.image.load('Data/maps/map.png')


# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
size = 10
x, y = 60.2, 60
delta = 0.821
l = 'map'
mapImage = createMap(x, y, size, l)
pygame.display.flip()
run = True
while run:
    screen.fill(pygame.Color('black'))
    screen.blit(mapImage, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                size += 1
                size %= 18
                delta /= 2
                mapImage = createMap(x, y, size, l)
            if event.key == pygame.K_PAGEDOWN:
                size -= 1
                size %= 18
                delta *= 2
                mapImage = createMap(x, y, size, l)
            if event.key == pygame.K_UP:
                if -90 < y + delta < 90:
                    y += delta
                mapImage = createMap(x, y, size, l)
            if event.key == pygame.K_DOWN:
                if -90 < y - delta < 90:
                    y -= delta
                mapImage = createMap(x, y, size, l)
            if event.key == pygame.K_RIGHT:
                if -180 < x + delta < 180:
                    x += delta
                mapImage = createMap(x, y, size, l)
            if event.key == pygame.K_LEFT:
                if -180 < x - delta < 180:
                    x -= delta
                mapImage = createMap(x, y, size, l)
    pygame.display.flip()
pygame.quit()
os.remove('Data/maps/map.png')