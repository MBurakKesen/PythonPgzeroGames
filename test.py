import pgzrun
import random
import time

# Ekran boyutları
WIDTH = 800
HEIGHT = 600

# Oyun durumu
game_over = False
game_started = False
sound_on = True
score = 0  # Skor değişkeni

# Platformlar
platforms = []

def generate_platforms():
    """Platformları ekrandan zeminden tepeye ulaşacak şekilde oluşturur."""
    platforms.clear()
    step_y = HEIGHT // 12  # Platformların aralarındaki yükseklik
    for i in range(12):  # 12 platform oluşturuyoruz
        x = random.randint(0, WIDTH - 100)
        y = HEIGHT - (i * step_y)  # Platformlar yukarı doğru dizilir
        platforms.append(Rect((x, y), (100, 10)))

# Alien karakteri
alien = Actor("alien", midbottom=(WIDTH // 2, HEIGHT - 50))  # Zeminde başlıyor

# Hız ve yer çekimi değişkenleri
velocity_y = 0
gravity = 1
on_ground = True

# Kuş objesi
birds = []
last_bird_spawn_time = 0  # Kuşların en son spawn edildiği zaman

# Kuşların rastgele aralıklarla oluşması
def spawn_bird():
    global last_bird_spawn_time, game_started
    if game_started:
        current_time = time.time()
        if current_time - last_bird_spawn_time > 2:  # 2 saniye arayla kuş oluştur
            y_position = random.randint(50, HEIGHT - 100)
            bird = Actor("bird")
            bird.pos = 0, y_position
            bird.speed = random.uniform(2, 5)
            birds.append(bird)
            last_bird_spawn_time = current_time

# Başla butonuna tıklama kontrolü
def on_mouse_down(pos):
    global game_started, game_over, sound_on
    if not game_started:  # Ana menüdeki butonlar
        if 320 < pos[0] < 480 and 200 < pos[1] < 250:  # Start Butonu
            game_started = True
            reset_game(game_started)
        elif 320 < pos[0] < 480 and 270 < pos[1] < 320:  # Sound ON/OFF Butonu
            sound_on = not sound_on
        elif 320 < pos[0] < 480 and 340 < pos[1] < 390:  # Exit Butonu
            exit()
    elif game_over:  # Oyun sonundaki Restart
        if 320 < pos[0] < 480 and 270 < pos[1] < 320:
            game_started2=True
            reset_game(game_started2)

# Oyun sıfırlama fonksiyonu
def reset_game(game_started2):
    global game_over, alien, birds, platforms, velocity_y, on_ground, score
    if game_over:
        score = 0
    game_over = False
    game_started = game_started2

    # Alien başlangıç pozisyonu
    alien.pos = WIDTH // 2, HEIGHT - 50  # Alien ekranın alt ortasında başlar
    velocity_y = 0
    on_ground = True

    # Kuşları temizle
    birds.clear()

    # Platformları oluştur
    generate_platforms()

    # Yeni kuşları spawn et
    spawn_bird()

# Ekran çizimi
def draw():
    screen.clear()
    screen.fill("skyblue")  # Arka plan rengi

    if not game_started:  # Ana Menü
        screen.draw.text("Welcome to the Game", center=(WIDTH//2, 150), fontsize=50, color="white")
        screen.draw.filled_rect(Rect((320, 200), (160, 50)), "green")
        screen.draw.text("Start", center=(400, 225), fontsize=30, color="white")
        screen.draw.filled_rect(Rect((320, 270), (160, 50)), "blue")
        screen.draw.text("Sound ON" if sound_on else "Sound OFF", center=(400, 295), fontsize=30, color="white")
        screen.draw.filled_rect(Rect((320, 340), (160, 50)), "red")
        screen.draw.text("Exit", center=(400, 365), fontsize=30, color="white")
        return

    # Oyun ekranı
    screen.draw.filled_rect(Rect((0, HEIGHT - 50), (WIDTH, 50)), "green")  # Zemin

    # Alien ve platformları çiz
    alien.draw()
    for platform in platforms:
        screen.draw.filled_rect(platform, "brown")
    
    # Kuşları çiz
    for bird in birds:
        bird.draw()

    # Skoru çiz
    screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=30, color="white")

    # Oyun bitmişse mesaj ve Restart butonu
    if game_over:
        screen.draw.text(
            "GAME OVER", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=50, color="red"
        )
        screen.draw.filled_rect(Rect((320, 270), (160, 50)), "green")
        screen.draw.text(
            "Restart", center=(400, 295), fontsize=30, color="white"
        )

# Oyun güncelleme
def update():
    global game_over, velocity_y, on_ground, score
    if not game_started or game_over:
        return  # Eğer oyun başlamadıysa veya bitmişse hiçbir şey yapma

    # Alien hareketi
    if keyboard.left:
        alien.x -= 5
    if keyboard.right:
        alien.x += 5

    # Zıplama
    if keyboard.space and on_ground:
        velocity_y = -15
        on_ground = False

    # Yer çekimi ve zemin kontrolü
    alien.y += velocity_y
    velocity_y += gravity

    if alien.y >= HEIGHT - 75:  # Zemin seviyesi
        alien.y = HEIGHT - 75
        on_ground = True
        velocity_y = 0

    # Platformlar ile çarpışma
    for platform in platforms:
        if alien.colliderect(platform) and velocity_y > 0:
            alien.bottom = platform.top
            on_ground = True
            velocity_y = 0
            break

    # Kuşlarla çarpışma kontrolü
    for bird in birds:
        if alien.colliderect(bird):
            game_over = True
            break

    # Kuşların hareketi
    for bird in birds[:]:
        bird.x += bird.speed  # Kuşların sağa doğru hareketi
        if bird.x > WIDTH:  # Kuş ekranın dışına çıkarsa
            birds.remove(bird)

    # Rastgele zamanlarla kuş spawn et
    spawn_bird()

    # Alien üst sınıra ulaştıysa oyun yeniden başlat ve skor artır
    if alien.bottom <= 0:
        score += 1
        game_started2=True
        reset_game(game_started2)

# Oyun başlat

# Pygame Zero'yu başlat
pgzrun.go()
