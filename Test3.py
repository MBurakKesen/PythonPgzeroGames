import pgzrun
import random

# Ekran boyutları
WIDTH = 800
HEIGHT = 600

# Başlangıç ekranı ile ilgili değişkenler
game_started = False

# Alien sınıfı
class Alien:
    def __init__(self, image, start_pos=(0, 0)):
        self.actor = Actor(image)
        self.actor.pos = start_pos
        self.velocity_y = 0
        self.gravity = 1
        self.on_ground = True
    
    def draw(self):
        self.actor.draw()
    
    def move(self, left, right, space):
        if left:
            self.actor.x -= 5
        if right:
            self.actor.x += 5
        if space and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
        self.actor.y += self.velocity_y
        self.velocity_y += self.gravity

        if self.actor.y >= HEIGHT - 75:  # Zemin seviyesine ulaşınca
            self.actor.y = HEIGHT - 75
            self.on_ground = True
            self.velocity_y = 0
    
    def collides_with(self, platform_rect):
        if self.actor.colliderect(platform_rect) and self.velocity_y > 0:
            self.actor.y = platform_rect.top
            self.velocity_y = 0
            self.on_ground = True

# Platform sınıfı
class Platform:
    def __init__(self, x, y):
        self.rect = Rect((x, y), (100, 10))
    
    def draw(self):
        screen.draw.filled_rect(self.rect, "brown")

# Kuş sınıfı
class Bird:
    def __init__(self, image, y_range=(50, HEIGHT - 50)):
        self.actor = Actor(image)
        self.actor.pos = (0, random.randint(*y_range))
    
    def draw(self):
        self.actor.draw()
    
    def move(self):
        self.actor.x += 4
        if self.actor.x > WIDTH:  # Ekranı geçtiğinde tekrar başa al
            self.actor.x = 0
            self.actor.y = random.randint(50, HEIGHT - 50)

# Platformları rastgele oluştur
def generate_platforms(width, height, num_platforms):
    platforms = []
    for _ in range(num_platforms):
        x = random.randint(0, width - 100)
        y = random.randint(50, height - 200)  # Platformları yukarıya yerleştir
        platform = Platform(x, y)
        platforms.append(platform)
    return platforms

# Başlangıçta kuş yaratmaya başla
def spawn_bird():
    if len(birds) < 3:  # Ekranda 3 kuştan fazla olmasın
        bird = Bird("bird", y_range=(50, HEIGHT - 50))  # Kuşu yarat
        birds.append(bird)  # Kuşu listeye ekle

        # Kuşları rastgele zaman aralıklarıyla tekrar oluştur
        clock.schedule(spawn_bird, random.uniform(1, 3))  # Kuşları her 1-3 saniyede bir oluştur

# Başlangıçta kuş yaratmaya başla
birds = []
spawn_bird()

# Platformları oluştur
platforms = generate_platforms(WIDTH, HEIGHT, num_platforms=10)

# Oyun bittiğinde yazıyı gösteren fonksiyon
def game_over(message):
    screen.draw.text(message, center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")
    exit()  # Oyun bitince çıkış yap

def draw():
    screen.clear()

    if not game_started:
        # Başlangıç ekranı
        screen.fill("skyblue")
        screen.draw.text("Welcome to the Game!", center=(WIDTH // 2, HEIGHT // 3), fontsize=50, color="black")
        screen.draw.text("Press 'S' to Start", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="green")
        return

    # Oyun ekranı
    screen.fill("skyblue")
    screen.draw.filled_rect(Rect((0, HEIGHT - 50), (WIDTH, 50)), "green")  # Zemin
    for platform in platforms:
        platform.draw()  # Tüm platformları çiz
    alien.draw()  # Alien çiz
    for bird in birds:
        bird.draw()  # Tüm kuşları çiz

    # Oyun bittiğinde (alien zemin dışında ya da kuşlara çarptığında)
    if alien.actor.y <= 0:  # Alien ekranın en üstüne ulaştığında
        game_over("YOU WIN!")  # Kazanma mesajı
    else:
        for bird in birds:
            if alien.actor.colliderect(bird.actor):  # Kuşa çarptığında
                game_over("GAME OVER!")  # Kaybetme mesajı

def update():
    global game_started
    if not game_started:
        if keyboard.s:  # 'S' tuşuna basıldığında oyun başlasın
            game_started = True
        return

    # `keyboard` kontrolü burada yapılır ve parametre olarak Alien sınıfına iletilir
    left = keyboard.left
    right = keyboard.right
    space = keyboard.space
    alien.move(left, right, space)  # Alien hareketini kontrol et
    for bird in birds:
        bird.move()  # Tüm kuşların hareketini kontrol et
    for platform in platforms:
        alien.collides_with(platform.rect)  # Çarpışma kontrolü için tüm platformları kontrol et

# Platformları sıralarken, alien'ın zıplayarak ekranın en üstüne ulaşabilmesi için yüksekliği rastgele oluşturuyoruz
def generate_platforms(width, height, num_platforms):
    platforms = []
    for _ in range(num_platforms):
        x = random.randint(0, width - 100)
        y = random.randint(50, height - 200)  # Platformları ekranda yukarıya yerleştir
        platform = Platform(x, y)
        platforms.append(platform)
    return platforms

pgzrun.go()
