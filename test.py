import pgzrun
import random
import time

WIDTH = 800
HEIGHT = 600

game_over = False
game_started = False
sound_on = True
score = 0  


platforms = []

def generate_platforms():

    platforms.clear()
    step_y = HEIGHT // 12  
    for i in range(12):  
        x = random.randint(0, WIDTH - 100)
        y = HEIGHT - (i * step_y)
        platforms.append(Rect((x, y), (100, 10)))


alien = Actor("alien", midbottom=(WIDTH // 2, HEIGHT - 50)) 


velocity_y = 0
gravity = 1
on_ground = True


birds = []
last_bird_spawn_time = 0


def spawn_bird():
    global last_bird_spawn_time, game_started
    if game_started:
        current_time = time.time()
        if current_time - last_bird_spawn_time > 2:  
            y_position = random.randint(50, HEIGHT - 100)
            bird = Actor("bird")
            bird.pos = 0, y_position
            bird.speed = random.uniform(2, 5)
            birds.append(bird)
            last_bird_spawn_time = current_time


def on_mouse_down(pos):
    global game_started, game_over, sound_on
    if not game_started:  
        if 320 < pos[0] < 480 and 200 < pos[1] < 250:  
            game_started = True
            reset_game(game_started)
        elif 320 < pos[0] < 480 and 270 < pos[1] < 320:  
            sound_on = not sound_on
        elif 320 < pos[0] < 480 and 340 < pos[1] < 390:  
            exit()
    elif game_over:  
        if 320 < pos[0] < 480 and 270 < pos[1] < 320:
            game_started2=True
            reset_game(game_started2)

def reset_game(game_started2):
    global game_over, alien, birds, platforms, velocity_y, on_ground, score
    if game_over:
        score = 0
    game_over = False
    game_started = game_started2

    alien.pos = WIDTH // 2, HEIGHT - 50  
    velocity_y = 0
    on_ground = True

    birds.clear()

    generate_platforms()

    spawn_bird()

def draw():
    screen.clear()
    screen.fill("skyblue") 
    if not game_started:  
        screen.draw.text("Welcome to the Game", center=(WIDTH//2, 150), fontsize=50, color="white")
        screen.draw.filled_rect(Rect((320, 200), (160, 50)), "green")
        screen.draw.text("Start", center=(400, 225), fontsize=30, color="white")
        screen.draw.filled_rect(Rect((320, 270), (160, 50)), "blue")
        screen.draw.text("Sound ON" if sound_on else "Sound OFF", center=(400, 295), fontsize=30, color="white")
        screen.draw.filled_rect(Rect((320, 340), (160, 50)), "red")
        screen.draw.text("Exit", center=(400, 365), fontsize=30, color="white")
        return

    screen.draw.filled_rect(Rect((0, HEIGHT - 50), (WIDTH, 50)), "green")  # Zemin

    alien.draw()
    for platform in platforms:
        screen.draw.filled_rect(platform, "brown")
    
    for bird in birds:
        bird.draw()

    screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=30, color="white")

    if game_over:
        screen.draw.text(
            "GAME OVER", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=50, color="red"
        )
        screen.draw.filled_rect(Rect((320, 270), (160, 50)), "green")
        screen.draw.text(
            "Restart", center=(400, 295), fontsize=30, color="white"
        )

def update():
    global game_over, velocity_y, on_ground, score
    if not game_started or game_over:
        return 

    
    if keyboard.left:
        alien.x -= 5
    if keyboard.right:
        alien.x += 5


    if keyboard.space and on_ground:
        velocity_y = -15
        on_ground = False

    
    alien.y += velocity_y
    velocity_y += gravity

    if alien.y >= HEIGHT - 75: 
        alien.y = HEIGHT - 75
        on_ground = True
        velocity_y = 0

    
    for platform in platforms:
        if alien.colliderect(platform) and velocity_y > 0:
            alien.bottom = platform.top
            on_ground = True
            velocity_y = 0
            break

    
    for bird in birds:
        if alien.colliderect(bird):
            game_over = True
            break

    for bird in birds[:]:
        bird.x += bird.speed  
        if bird.x > WIDTH:  
            birds.remove(bird)

    spawn_bird()

    if alien.bottom <= 0:
        score += 1
        game_started2=True
        reset_game(game_started2)


pgzrun.go()
