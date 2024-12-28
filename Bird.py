from pgzero.actor import Actor
import random

class Bird:
    def __init__(self, image, y_range, width):
        self.actor = Actor(image)  # Örneğin, "bird.png"
        self.actor.pos = (0, random.randint(*y_range))  # Rastgele bir y pozisyonu
        self.speed = 4  # Kuşun hızı
        self.width = width  # WIDTH'i parametre olarak alıyoruz

    def move(self):
        self.actor.x += self.speed
        if self.actor.x > self.width:  # Ekranı geçtiğinde tekrar başa al
            self.actor.x = 0
            self.actor.y = random.randint(50, self.width - 50)

    def draw(self):
        self.actor.draw()
