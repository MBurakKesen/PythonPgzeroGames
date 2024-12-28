from pgzero.actor import Actor

class Alien:
    def __init__(self, image, start_pos, height):
        self.actor = Actor(image)  # Örneğin, "alien.png"
        self.actor.pos = start_pos
        self.velocity_y = 0
        self.gravity = 1
        self.on_ground = True
        self.height = height  # HEIGHT'i parametre olarak alıyoruz

    def move(self, left, right, space):
        # Hareketi dışarıdan gelen parametrelere göre yapıyoruz
        if left:
            self.actor.x -= 5
        if right:
            self.actor.x += 5
        if space and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False

        # Yer çekimi ve zemin kontrolü
        self.actor.y += self.velocity_y
        self.velocity_y += self.gravity
        if self.actor.y >= self.height - 75:  # Zemin seviyesi
            self.actor.y = self.height - 75
            self.on_ground = True
            self.velocity_y = 0

    def draw(self):
        self.actor.draw()

    def collides_with(self, rect):
        if self.actor.colliderect(rect) and self.velocity_y > 0:
            self.actor.y = rect.top
            self.velocity_y = 0
            self.on_ground = True
