import pgzrun
import random
import time

class AlienGame:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600

        self.game_over = False
        self.game_started = False
        self.sound_on = True
        self.score = 0

        self.platforms = []

        self.alien = Actor("alien", midbottom=(self.WIDTH // 2, self.HEIGHT - 50))

        self.velocity_y = 0
        self.gravity = 1
        self.on_ground = True

        self.birds = []
        self.last_bird_spawn_time = 0

    def generate_platforms(self):
       
        self.platforms.clear()
        step_y = self.HEIGHT // 12 
        for i in range(12):  
            x = random.randint(0, self.WIDTH - 100)
            y = self.HEIGHT - (i * step_y)  
            self.platforms.append(Rect((x, y), (100, 10)))

    def spawn_bird(self):
        
        if self.game_started:
            current_time = time.time()
            if current_time - self.last_bird_spawn_time > 2: 
                y_position = random.randint(50, self.HEIGHT - 100)
                bird = Actor("bird")
                bird.pos = 0, y_position
                bird.speed = random.uniform(2, 5)
                self.birds.append(bird)
                self.last_bird_spawn_time = current_time

    def reset_game(self,score):
        
        self.score = score
        self.game_over = False
        self.alien.pos = self.WIDTH // 2, self.HEIGHT - 50
        self.velocity_y = 0
        self.on_ground = True
        self.birds.clear()
        self.generate_platforms()

    def on_mouse_down(self, pos):
        
        if not self.game_started: 
            if 320 < pos[0] < 480 and 200 < pos[1] < 250:  
                self.reset_game(score=0)
            elif 320 < pos[0] < 480 and 270 < pos[1] < 320:  
                self.sound_on = not self.sound_on
            elif 320 < pos[0] < 480 and 340 < pos[1] < 390: 
                exit()
        elif self.game_over:  
            if 320 < pos[0] < 480 and 270 < pos[1] < 320:
                self.reset_game(score=0)

    def draw(self):
       
        screen.clear()
        screen.fill("skyblue")

        if not self.game_started:  
            screen.draw.text("Welcome to the Game", center=(self.WIDTH // 2, 150), fontsize=50, color="white")
            screen.draw.filled_rect(Rect((320, 200), (160, 50)), "green")
            screen.draw.text("Start", center=(400, 225), fontsize=30, color="white")
            screen.draw.filled_rect(Rect((320, 270), (160, 50)), "blue")
            screen.draw.text("Sound ON" if self.sound_on else "Sound OFF", center=(400, 295), fontsize=30, color="white")
            screen.draw.filled_rect(Rect((320, 340), (160, 50)), "red")
            screen.draw.text("Exit", center=(400, 365), fontsize=30, color="white")
            return

       
        screen.draw.filled_rect(Rect((0, self.HEIGHT - 50), (self.WIDTH, 50)), "green") 
        self.alien.draw()

        for platform in self.platforms:
            screen.draw.filled_rect(platform, "brown")

        for bird in self.birds:
            bird.draw()

        screen.draw.text(f"Score: {self.score}", topleft=(10, 10), fontsize=30, color="white")

        if self.game_over:
            screen.draw.text("GAME OVER", center=(self.WIDTH // 2, self.HEIGHT // 2 - 50), fontsize=50, color="red")
            screen.draw.filled_rect(Rect((320, 270), (160, 50)), "green")
            screen.draw.text("Restart", center=(400, 295), fontsize=30, color="white")

    def update(self):
        """Oyun güncelleme."""
        if not self.game_started or self.game_over:
            return

       
        if keyboard.left:
            self.alien.x -= 5
        if keyboard.right:
            self.alien.x += 5

    
        if keyboard.space and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False

        
        self.alien.y += self.velocity_y
        self.velocity_y += self.gravity

        if self.alien.y >= self.HEIGHT - 75:  
            self.alien.y = self.HEIGHT - 75
            self.on_ground = True
            self.velocity_y = 0

      
        for platform in self.platforms:
            if self.alien.colliderect(platform) and self.velocity_y > 0:
                self.alien.bottom = platform.top
                self.on_ground = True
                self.velocity_y = 0
                break

        
        for bird in self.birds:
            if self.alien.colliderect(bird):
                self.game_over = True
                break

       
        for bird in self.birds[:]:
            bird.x += bird.speed
            if bird.x > self.WIDTH:
                self.birds.remove(bird)

       
        self.spawn_bird()

        
        if self.alien.bottom <= 0:
            
            self.reset_game(self.score+1)


alien_game = AlienGame()

def draw():
    alien_game.draw()

def update():
    alien_game.update()

def on_mouse_down(pos):
    alien_game.on_mouse_down(pos)

