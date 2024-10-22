import pygame
import numpy as np

pygame.init()

text_colour = (186, 156, 243)
white = (225, 227, 228)
colour = (234, 203, 100)
colour2 = (114, 204, 232)
bg_colour = (42, 47, 56)

font_object = pygame.font.SysFont("Iosevka Nerd Font", 30)
display_text = ["", "Cohen-Sutherland", "Cyrus-Beck", "Liang-Barsky", "Polygon Clipping"]

# square boundary conditions
x_max, x_min = 600, 200
y_max, y_min = 500, 100

# Vertices of polygon boundary
vertices = [[100, 200], [500, 100], [560, 310], [340, 400], [130, 310]]

text = font_object.render(display_text[0], False, text_colour)

screen = pygame.display.set_mode((800, 600))

def reset_screen() :
    screen.fill(bg_colour)

def draw_square_window():
    pygame.draw.line(screen, white, [x_max, y_max], [x_min, y_max])
    pygame.draw.line(screen, white, [x_max, y_min], [x_min, y_min])
    pygame.draw.line(screen, white, [x_max, y_max], [x_max, y_min])
    pygame.draw.line(screen, white, [x_min, y_max], [x_min, y_min])

# assigning bits for Cohen-Sutherland
def calc_position(x, y):
    position = 0

    if x < x_min:
        position |= 1
    elif x > x_max:
        position |= 2
    if y < y_min:
        position |= 4
    elif y > y_max:
        position |= 8

    return position

def intersection(slope, x, y, pos):
    x_out, y_out = 0, 0
    if pos & 8 :
        x_out = x + (y_max - y)/slope
        y_out = y_max
    elif pos & 4 :
        x_out = x + (y_min - y)/slope
        y_out = y_min
    elif pos & 2 :
        y_out = y + slope*(x_max - x)
        x_out = x_max
    elif pos & 1 :
        y_out = y + slope*(x_min - x)
        x_out = x_min

    return round(x_out), round(y_out)

def cohen_sutherland(x1, y1, x2, y2):
    if x1 == -1:
        x1, y1 = 500, 50
        x2, y2 = 130, 400

    pygame.draw.line(screen, colour, [x1, y1], [x2, y2])

    pos1 = calc_position(x1, y1)
    pos2 = calc_position(x2, y2)
    
    
    if (pos1 | pos2) == 0:
        pygame.draw.line(screen, colour2, [x1, y1], [x2, y2])
        return
    elif (pos1 & pos2):
        return
    
    slope = (y2 - y1)/(x2 - x1)


    if pos1 != 0:
        x1, y1 = intersection(slope, x1, y1, pos1)
    if pos2 != 0:
        x2, y2 = intersection(slope, x2, y2, pos2)

    pygame.draw.line(screen, colour2, [x1, y1], [x2, y2])

def dot(p0, p1):
    return p0[0] * p1[0] + p0[1] * p1[1]

def cyrus_beck(x1, y1, x2, y2):
    pygame.draw.polygon(screen, white, vertices, 1)
    if x1 == -1:
        x1, y1 = 150, 400
        x2, y2 = 600, 320
    pygame.draw.line(screen, colour, [x1, y1], [x2, y2])

    n = len(vertices)
    P1_P0 = (x2 - x1, y2 - y1)
    normal = [(vertices[i][1] - vertices[(i + 1) % n][1], vertices[(i + 1) % n][0] - vertices[i][0]) for i in range(n)]
    P0_PEi = [(vertices[i][0] - x1, vertices[i][1] - y1) for i in range(n)]
    numerator = [dot(normal[i], P0_PEi[i]) for i in range(n)]
    denominator = [dot(normal[i], P1_P0) for i in range(n)]
    t = [numerator[i] / denominator[i] if denominator[i] != 0 else 0 for i in range(n)]
    tE = [t[i] for i in range(n) if denominator[i] > 0]
    tL = [t[i] for i in range(n) if denominator[i] < 0]
    tE.append(0)
    tL.append(1)
    temp = [np.max(tE), np.min(tL)]
    if temp[0] > temp[1]:
        return None
    x1_clip = round(x1 + P1_P0[0] * temp[0])
    y1_clip = round(y1 + P1_P0[1] * temp[0])
    x2_clip = round(x1 + P1_P0[0] * temp[1])
    y2_clip = round(y1 + P1_P0[1] * temp[1])
    pygame.draw.line(screen, colour2, [x1_clip, y1_clip], [x2_clip, y2_clip])

def liang_barsky(x1, y1, x2, y2):
    if x1 == -1:
        x1, y1 = 680, 300
        x2, y2 = 180, 260
    pygame.draw.line(screen, colour, [x1, y1], [x2, y2])

    dx = x2 - x1
    dy = y2 - y1

    p = [-dx, dx, -dy, dy]
    q = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]
    t_enter = 0.0
    t_exit = 1.0

    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                if t > t_enter:
                    t_enter = t
            else:
                if t < t_exit:
                    t_exit = t
    
    if t_enter > t_exit :
        return
    
    x1_clip = round(x1 + t_enter * dx)
    y1_clip = round(y1 + t_enter * dy)
    x2_clip = round(x1 + t_exit * dx)
    y2_clip = round(y1 + t_exit * dy)

    pygame.draw.line(screen, colour2, [x1_clip, y1_clip], [x2_clip, y2_clip])

def x_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    num = (x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)
    den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
    return num/den
    
def y_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    num = (x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)
    den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
    return num/den

def polygon_clipping(poly_points, poly_size, x1, y1, x2, y2):
    new_points = np.zeros((10, 2), dtype=int)
    new_poly_size = 0

    for i in range(poly_size):
        k = (i+1) % poly_size
        ix, iy = poly_points[i]
        kx, ky = poly_points[k]

        i_pos = (x2-x1) * (iy-y1) - (y2-y1) * (ix-x1)

        k_pos = (x2-x1) * (ky-y1) - (y2-y1) * (kx-x1)

        if i_pos < 0 and k_pos < 0:
            new_points[new_poly_size] = [kx, ky]
            new_poly_size += 1

        elif i_pos >= 0 and k_pos < 0:
            new_points[new_poly_size] = [x_intersect(x1, y1, x2, y2, ix, iy, kx, ky),
                                         y_intersect(x1, y1, x2, y2, ix, iy, kx, ky)]
            new_poly_size += 1
            new_points[new_poly_size] = [kx, ky]
            new_poly_size += 1

        elif i_pos < 0 and k_pos >= 0:
            new_points[new_poly_size] = [x_intersect(x1, y1, x2, y2, ix, iy, kx, ky),
                                         y_intersect(x1, y1, x2, y2, ix, iy, kx, ky)]
            new_poly_size += 1

    clipped_poly_points = np.zeros((new_poly_size, 2), dtype=int)
    for i in range(new_poly_size):
        clipped_poly_points[i] = new_points[i]

    return clipped_poly_points, new_poly_size

def suth_hodg():
    poly_size = 3
    poly_points = np.array([[100, 250], [650, 460], [400, 80]])
    clipper_size = 4
    clipper_points = np.array([[x_min, y_min], [x_min, y_max], [x_max, y_max], [x_max, y_min]])
    pygame.draw.polygon(screen, colour, poly_points, 1)
    pygame.draw.polygon(screen, white, clipper_points, 1)
    for i in range(clipper_size):
        k = (i+1) % clipper_size

        poly_points, poly_size = polygon_clipping(poly_points, poly_size, clipper_points[i][0],
                                      clipper_points[i][1], clipper_points[k][0],
                                      clipper_points[k][1])
        
    pygame.draw.polygon(screen, colour2, poly_points)


method_type = 0

running = True
x1, y1, x2, y2 = -1, -1, -1, -1
while running:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            if x1 == -1 or x2 != -1:
                x1, y1 = pygame.mouse.get_pos()
                x2, y2 = -1, -1
            else:
                x2, y2 = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                method_type = 1
                reset_screen()
                draw_square_window()
                cohen_sutherland(x1, y1, x2, y2)
            elif event.key == pygame.K_2:
                method_type = 2
                reset_screen()
                cyrus_beck(x1, y1, x2, y2)    
            elif event.key == pygame.K_3:
                method_type = 3
                reset_screen()
                draw_square_window()
                liang_barsky(x1, y1, x2, y2)
            elif event.key == pygame.K_4:
                method_type = 4
                reset_screen()
                suth_hodg()

    text = font_object.render(display_text[method_type], False, text_colour)
    screen.blit(text, (5, 20))
    pygame.display.update()
