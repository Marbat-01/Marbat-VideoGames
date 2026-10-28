#Proyecto hecho por Marito Roberto / "Marbat" Guiado de "Coding With Russ" - Youtube
#https://www.youtube.com/watch?v=s5bd9KMSSW4
print("Hehco por: Marito Roberto ('Marbat') Con Python en: Visual Studio 2022.")
print("Iniciado el 26 de Febrero del 2026.")
print("Guiado con: https://www.youtube.com/watch?v=s5bd9KMSSW4")
print("- - - - - - - - - - - - - - - - - - - - -")
print("-Controles del jugador 1:")
print("'W' = Salto")
print("'A' = Izquierda")
print("'D' = Derecha")
print("'H' = Ataque A")
print("'J' = Ataque B")
print("- - - - - - - - - - - - - - - - - - - - -")
print("-Controles del jugador 2:")
print("'Flecha arriba' = Salto")
print("'Flecha izquierda' = Izquierda")
print("'Flecha derecha' = Derecha")
print("'Tecla 1' = Ataque A")
print("'Tecla 2' = Ataque B")

import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#crear ventana del juego.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("M.B Fighters (Prototype)")

#hacer el Frame Rate
clock = pygame.time.Clock()
FPS = 60

#Definir colores
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#Definir variables del juego:
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#Puntuacion del jugador. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#Definir las variables de los luchadores
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#Cargar musica y sonidos
pygame.mixer.music.load("principal/assets/audio/kirby-robobot.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("principal/assets/audio/hit.mp3")
sword_fx.set_volume(1000)
magic_fx = pygame.mixer.Sound("principal/assets/audio/hit.mp3")
magic_fx.set_volume(1000)

#Cargar imagen de background
bg_image = pygame.image.load("principal/assets/images/background/steampunk.jpg").convert_alpha()

#Cargar Spritesheets
warrior_sheet = pygame.image.load("principal/assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("principal/assets/images/wizard/Sprites/wizard.png").convert_alpha()

#Cargar imagen de victoria
victory_img = pygame.image.load("principal/assets/images/icons/victorygra.png").convert_alpha()

#definir la cantidad de pasos en cada animacion
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#Defnir fuente
count_font = pygame.font.Font("principal/assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("principal/assets/fonts/turok.ttf", 30)

#Funcion para dibujar texto.
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Cargar sprites
testa = pygame.image.load("principal/assets/images/warrior/sprites/warrior.png").convert_alpha()
testb = pygame.image.load("principal/assets/images/wizard/sprites/wizard.png").convert_alpha()

#funcion para dibujar background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#Funcion para dibujar las barras de vida.
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 4, y - 4, 406, 38))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#create 2 instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#loop del juego
run = True
while run:

    clock.tick(FPS)

    #dibujar background
    draw_bg()

    #Mostrar el estado del jugador:
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("Victorias J1: " + str(score[0]), score_font, WHITE, 20, 60)
    draw_text("Victorias J2: " + str(score[1]), score_font, WHITE, 580, 60)

    #Actualizar cuenta atras.
    if intro_count <= 0:
        #Mover fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        #Display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #Actualizar cuenta
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks() 

    #Actualizar peleadores
    fighter_1.update()
    fighter_2.update()

    #dibujar fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #Chequear si el jugador es derrotado
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            screen.blit(victory_img, (720, 300))
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            screen.blit(victory_img, (1, 300))
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
         #Mostrar la imagen de victoria.
         if fighter_1.alive == False:
             screen.blit(victory_img, (720, 300))
         elif fighter_2.alive == False:
             screen.blit(victory_img, (1, 300))
         #screen.blit(victory_img, (360, 150))
         if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
             round_over = False
             intro_count = 3
             fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
             fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #update display
    pygame.display.update()

#Salir de Pygame
pygame.quit()