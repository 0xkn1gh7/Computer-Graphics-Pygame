################################################################
# Computer Graphics Lab 8 - Simulating Phong Shading on a Sphere
# Author - 0xkn1gh7 (Yuval Goyal)
#
#     (()__(()
#      /       \ 
#     ( /    \  \
#      \ o o    /
#      (_()_)__/ \             
#     / _,==.____ \
#    (   |--|      )
#    /\_.|__|'-.__/\_
#   / (        /     \ 
#   \  \      (      /
#    )  '._____)    /    
# (((____.--(((____/
#
# https://0xkn1gh7.github.io/
################################################################

import math
import pygame
import numpy as np

# Creating Window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Phong Shading Model")

# Creating Observer
observer = (400, 300, 1000)

# Creating Sphere
radius = 125
center = (400, 300, 0)
color = (254, 128, 25)
points = []

for x in range(-radius, radius):
    for y in range(-radius, radius):
        if x**2+y**2 <= radius**2:
            z = math.sqrt(radius**2 - x**2 - y**2)
            points.append((center[0]+x, center[1]+y, center[2]+z))

# Creating Light Source
light = (200, 500, 200)

# Simulating Phong
ka, ks, kd = 0.25, 0.5, 0.33 
ia, il = 1, 1
a = 75

def unit_vector(v):
    norm = np.linalg.norm(v)
    return v if norm == 0 else v/norm

def phong_shading(point):
    point = np.array(point)
    N = unit_vector(point - center)
    L = unit_vector(light - point)
    V = unit_vector(observer-point)
    R = 2*np.dot(L, N)*N - L

    N_L = max(np.dot(N, L), 0)
    R_V = max(np.dot(R, V), 0)

    I = ka*ia + il*kd*N_L + il*ks*(R_V**a)
    return np.clip(I, 0, 1)

def render_sphere():
    for point in points:
        I = phong_shading(point)
        sphere_color = np.clip(np.multiply(color, I), 0, 255)
        screen.set_at((point[0], point[1]), sphere_color)

# Eye Candy
def render_properties():
    font_obj = pygame.font.SysFont("Iosevka Nerd Font", 40, bold = True)
    font_obj2 = pygame.font.SysFont("Iosevka Nerd Font", 15)
    color1 = (184, 187, 38)
    color2 = (142, 192, 124)
    color3 = (211, 134, 155)
    heading = font_obj.render("Phong Shading Model", False, color1)
    light_text = font_obj2.render(f"Light Source: {light}", False, color2)
    intensity_text = font_obj2.render(f"I_a: {ia}, I_l: {il}", False, color2)
    observer_text = font_obj2.render(f"Observer: {observer}", False, color2)
    shine_text = font_obj2.render(f"Shine Factor: {a}", False, color2)
    material_text = font_obj2.render(f"K_a: {ka}, K_s: {ks}, K_d: {kd}", False, color2)
    screen.blit(heading, (20, 20))
    screen.blit(light_text, (550, 480))
    screen.blit(intensity_text, (550, 500))
    screen.blit(observer_text, (550, 520))
    screen.blit(shine_text, (550, 540))
    screen.blit(material_text, (550, 560))

    controls = ["Light Source Controls: ", "W: UP", "A: LEFT", "S: DOWN", "D: RIGHT", "LSHIFT: BACKWARD", "LCTRL: FOREWARD", "", "LEFT: Increase Shine", "RIGHT: Decrease Shine"]
    pos = 20
    for i in range(len(controls)): 
        text = font_obj2.render(controls[i], False, color3)
        if i == 0 or i == len(controls)-1 or i == len(controls)-2:
            screen.blit(text, (600, pos))
        else:
            screen.blit(text, (620, pos))
        pos += 20


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                light = (light[0], light[1]-50, light[2])
            if event.key == pygame.K_s:
                light = (light[0], light[1]+50, light[2])
            if event.key == pygame.K_a:
                light = (light[0]-50, light[1], light[2])
            if event.key == pygame.K_d:
                light = (light[0]+50, light[1], light[2])
            if event.key == pygame.K_LSHIFT:
                light = (light[0], light[1], light[2]-50)
            if event.key == pygame.K_LCTRL:
                light = (light[0], light[1], light[2]+50)
            if event.key == pygame.K_LEFT:
                a = a-5
            if event.key == pygame.K_RIGHT:
                a = a+5
    screen.fill((40, 40, 40))
    render_sphere()
    pygame.draw.circle(screen, (235, 219, 178), (light[0], light[1]), 5)
    render_properties()
    pygame.display.flip()

pygame.quit()

