from pgzero.rect import Rect
import random

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = Rect((x, y), (width, height))

    def draw(self, screen):  # screen parametresi alacak şekilde değiştirdik
        screen.draw.filled_rect(self.rect, "brown")

# Platformları oluşturacak fonksiyon
def generate_platforms(width, height, num_platforms=5):
    platforms = []
    platform_height = 10
    for _ in range(num_platforms):
        x = random.randint(0, width - 100)  # platform genişliğine göre x
        y = random.randint(100, height - platform_height)  # y için alt ve üst sınır
        platforms.append(Platform(x, y, 100, platform_height))

    # Platformları y eksenine göre sıralama (en alttan en üste)
    platforms.sort(key=lambda p: p.rect.y)
    return platforms
