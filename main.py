import pygame
import random
import math
from pygame import mixer


# Inicializar Pygame
pygame.init()
count = 0
source = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# Añadir musica
mixer.music.load("archivos/MusicaFondo.mp3")
bullet_sound = mixer.Sound("archivos/disparo.mp3")
collision_sound = mixer.Sound("archivos/Golpe.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Texto final del juego
final_source = pygame.font.Font("freesansbold.ttf", 40)


def endgame():
    endgame_text = final_source.render("GAME OVER", True, (255,0,0))
    screen.blit(endgame_text, (300, 200))


# Mostrar puntaje
def show_count(x, y):
    text = source.render(f"Score: {count}", True, (255,255,255))
    screen.blit(text, (x,y))
    '''max = 0
    for e in enemy_speed:
        if e > max:
            max = e

    screen.blit(max, (x, y - 50))'''


# Crear fondo
fondo = pygame.image.load("archivos/Fondo.jpg")

# Creacion de la pantalla
screen = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("archivos/ovni.png")
pygame.display.set_icon(icon)

# Creacion del jugador
img_player = pygame.image.load("archivos/cohete.png")
player_x = 368
player_y = 500
player_x_change = 0

# Creacion de enemigos
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change =  []
enemy_speed = []
enemy_quantity = 10
for e in range(enemy_quantity):
    img_enemy.append(pygame.image.load("archivos/enemigo.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(1)
    enemy_y_change.append(50)
    enemy_speed.append(0.2)

# Creacion de bala
img_bullet = pygame.image.load("archivos/bala.png")
bullet_x = 0
bullet_y = 500
bullet_y_change = 1
bullet_visible = False

def player(x, y):
    screen.blit(img_player, (x, y))


def enemy(x, y, ene):
    screen.blit(img_enemy[ene], (x, y))


def bullet(x, y):
    global bullet_visible
    bullet_visible = True
    screen.blit(img_bullet, (x + 16, y + 10))


def collisions(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
    if distance < 27:
        return True
    else:
        return False


# Loop del juego
executing = True
while executing:
    screen.blit(fondo, (0,0))
    for event in pygame.event.get():
        # Evento de cierre del programa
        if event.type == pygame.QUIT:
            executing = False

        # Eventos de control de posicion del jugador y disparo de bala
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                player_x_change= 0.5
            if event.key == pygame.K_SPACE:
                if not bullet_visible:
                    bullet_sound.play()
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    # Mantener al jugador en pantalla
    if player_x <= 0:
        player_x = 0
    if player_x >= 750:
        player_x = 750

    for e in range(enemy_quantity):
        # END GAME
        if enemy_y[e] > 350:
            for k in range(enemy_quantity):
                enemy_y[k] = 1000
            endgame()
            break

        enemy_x[e] += enemy_x_change[e]
        # Mantener al enemigo en pantalla
        if enemy_x[e] <= 0:
            enemy_x_change[e] = enemy_speed[e]
            enemy_y[e] += enemy_y_change[e]
        elif enemy_x[e] >= 750:
            enemy_x_change[e] = -enemy_speed[e]
            enemy_y[e] += enemy_y_change[e]

        collision = collisions(enemy_x[e], enemy_y[e], bullet_x, bullet_y)
        if collision:
            collision_sound.play()
            bullet_y = 500
            bullet_visible = False
            count += 1
            enemy_x[e] = random.randint(0, 736)
            enemy_y[e] = random.randint(50,200)
            enemy_speed[e] = enemy_speed[e] + 0.01

        enemy(enemy_x[e], enemy_y[e], e)


    # Movimiento de la bala
    if bullet_y <= 0:
        bullet_y = player_y
        bullet_visible = False

    if bullet_visible:
        bullet_y -= bullet_y_change
        bullet(bullet_x, bullet_y)

    player(player_x, player_y)
    show_count(text_x, text_y)
    pygame.display.update()
