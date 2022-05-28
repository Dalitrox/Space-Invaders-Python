import pygame
import random
import math
from pygame import mixer

# Inicjalizowanie modułu pygame
pygame.init()

# tworzenie okna gry
screen = pygame.display.set_mode((800, 600))

# Zmiana tła gry
background = pygame.image.load('background.png')

# Muzyka w tle
mixer.music.load('Dreamstate Logic - Earthbound.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.3)

# Zmiana tytułu i dodanie ikony
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('launch.png')
pygame.display.set_icon(icon)

# Gracz
playerImg = pygame.image.load('spaceship.png')

# Pozycja startowa gracza
playerX = 370
playerY = 480

# Pozycja X gracza zmieniana podczas gry
playerX_change = 0

# Przeciwnik
enemyImg = []
num_of_enemies = 6

# Pozycja startowa przeciwnika
enemyX = []
enemyY = []

# Pozycja X i Y przeciwnika zmieniana podczas gry
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)

# Pocisk
bulletImg = pygame.image.load('Laser.png')

# Pozycja startowa pocisku
bulletX = 0
bulletY = 480

# Pozycja X i Y pocisku zmieniana podczas gry
bulletX_change = 0
bulletY_change = 5

# Status: ready - pocisku nie da się zobaczyć na ekranie
# Status: fire - pocisk jest w ruchu i widoczny na ekranie
bullet_state = "ready"

# Punkty - wyświetlanie punktów w oknie z grą a nie w konsoli
score_value = 0
font = pygame.font.Font('Chopsic.ttf', 32)

# Położenie napisu z punktami
textX = 10
textY = 10

# tekst Game Over
game_over_font = pygame.font.Font('Chopsic.ttf', 64)

# Wyświetlanie tekstu z punktami
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Funkcja wyświetlająca Game Over
def game_over_text():
    m = 0

    # Jeśli jakikolwiek przeciwnik dojdzie do linii gracza załącza się dźwięk przegranej
    mixer.music.stop()
    lose = mixer.Sound('You Lose.mp3')
    lose.play()
    lose.set_volume(0.3)

    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Wyświetlanie przeciwnika
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 30, y + 10))

# Wyświetlanie gracza
def player(x, y):
    screen.blit(playerImg, (x, y))

# Wyświetlanie przeciwnika
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Funkcja sprawdzająca czy nastąpiła kolizja pocisku z przeciwnikiem
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# pętla gry np. jak naciśnie się X zamknięcia okna to okno powinno się zamknąć
running = True
while running:

    # Ekran gry - RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # Zdjęcie tła
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Jeśi lewy lub prawy klawisz jest wciśnięty to 
        # statek kosmiczny pownien się przesunąć w odpowiednią stronę
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Pobierane są aktualne położenie gracza w pozycji X 
                    # i przypisywane do położenia pocisku X aby pocisk 
                    # nie podążał za graczem po wystrzale
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Zmiana pozycji gracza w trakcie trwania programu
    playerX += playerX_change

    # Powrót gracza na miejsce gry jakby próbował wylecieć poza obszar okna
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Zmiana pozycji przeciwnika w trakcie trwania programu
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        # Powrót przeciwnika na miejsce gry jakby próbował wylecieć poza obszar okna
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        # Kolizja pocisku z przeciwnikiem
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            explosion_sound.set_volume(0.4)
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Ruch pocisku
    if bulletY <= 0: # jeżeli pocisk zostanie wystrzelony i przekroczy okno gry
        bulletY = 480 # to zresetuje pozycję do miejsca pozycji gracza
        bullet_state = "ready" # zmiana statusu pocisku na ready

    # Ruch pocisku po wystrzale ze statku
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Wywołanie funkcji związane z graczem i wyświetlaniem punktów
    player(playerX, playerY)
    show_score(textX, textY)
    # Odświeżanie ekranu do momentu aż nie zostanie wywołany event zamnknięcia gry
    pygame.display.update()