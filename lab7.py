import pygame
import numpy as np

pygame.init()

text_color = (184, 187, 38)
fg_color = (235, 219, 178)
bg_color = (40, 40, 40)

font_obj = pygame.font.SysFont("Iosevka Nerd Font", 40, bold = True)
font_obj2 = pygame.font.SysFont("Iosevka Nerd Font", 20)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

methods = ["Bezier Curve", "Hermite Curve"]
method_number = 0

def clear_screen():
    screen.fill(bg_color)
    text = font_obj.render(methods[method_number], False, text_color)
    screen.blit(text, (20, 20))

points = []

def bezier():
    if len(points) < 4:
        return
    basis = np.array([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 3, 0, 0],
        [1, 0, 0, 0],
    ])
    pygame.draw.line(screen, (131 ,165, 152), points[0], points[1], 1)
    pygame.draw.line(screen, (131 ,165, 152), points[1], points[2], 1)
    pygame.draw.line(screen, (131 ,165, 152), points[2], points[3], 1)
    draw_spline(basis)

def hermite():
    if len(points) < 4:
        return
    basis = np.array([
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
    ])
    pygame.draw.line(screen, (131 ,165, 152), (0, 0), points[2], 1)
    pygame.draw.line(screen, (211 ,134, 155), (0, 0), points[3], 1)
    pygame.draw.line(screen, (131 ,165, 152), points[0], (points[0][0]+points[2][0], points[0][1]+points[2][1]), 1)
    pygame.draw.line(screen, (211 ,134, 155), points[1], (points[1][0]+points[3][0], points[1][1]+points[3][1]), 1)
    draw_spline(basis)

def draw_spline(basis):
    weights = basis@points
    for u in np.linspace(0, 1, 1000):
        screen.set_at([*map(round, ([u**3, u**2, u, 1]@weights))], text_color)

clear_screen()

running = True
while running:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if len(points) == 4:
                points = []
                clear_screen()
            points.append((x,y))
            if len(points) == 4:
                if method_number == 0:
                    bezier()
                else:
                    hermite()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                clear_screen()
            if event.key == pygame.K_1:
                method_number = 0
                clear_screen()
                bezier()
            if event.key == pygame.K_2:
                method_number = 1
                clear_screen()
                hermite()
    
    for i in range(0, len(points)):
        text = font_obj2.render(f"P{i}", False, fg_color)
        screen.blit(text, (points[i][0], points[i][1]+10))
        pygame.draw.circle(screen, fg_color, points[i], 3)
    pygame.display.update()
