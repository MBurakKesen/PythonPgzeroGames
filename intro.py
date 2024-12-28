print("ctrl+c to end games")
# import time 


def draw():
     screen.fill((0.,0,0)) #ekranı belirlenmiş renk ile doldurur
     screen.clear()
     alien.draw()

alien=Actor("alien")
alien.pos=100,56

WIDTH=500
HEIGHT=alien.height+20

alien.topright=0,10

def update():# her frame de bu kod çalışıcak
    alien.left+=2
    if alien.left>WIDTH:
        alien.right=0

# def on_mouse_down(pos):
#     if alien.collidepoint(pos):
#         print("eek!")
#     else:
#         print("you missed me!")    

# def on_mouse_down(pos):
#     if alien.collidepoint(pos):
#         sounds.eep.play()
#         alien.image="alien_hurt"

#         time.sleep(1)
#         alien.image = 'alien'

#     else:
#         alien.image="alien"    

def on_mouse_down(pos):
    if alien.collidepoint(pos):
        set_alien_hurt()


def set_alien_hurt():
    alien.image="alien_hurt"
    sounds.eep.play()
    clock.schedule_unique(set_alien_normal, 1.0)

def set_alien_normal():
    alien.image="alien"