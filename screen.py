def draw_menu(start_button, voice_control, exit_game, screen):
    screen.clear()
    screen.draw.filled_rect(start_button, "blue")
    screen.draw.text("Start", center=(400, 220), fontsize=30, color="white")
    screen.draw.filled_rect(voice_control, "blue")
    screen.draw.text("Voice ON/OFF", center=(400, 320), fontsize=30, color="white")
    screen.draw.filled_rect(exit_game, "blue")
    screen.draw.text("Exit Game", center=(400, 420), fontsize=30, color="white")

def draw_game(alien, platforms, birds, game_over, screen):
    screen.clear()
    screen.fill("skyblue")
    screen.draw.filled_rect(Rect((0, 550), (800, 50)), "green")
    alien.draw()
    for platform in platforms:
        screen.draw.filled_rect(platform, "brown")
    for bird in birds:
        bird.draw()
    if game_over:
        screen.draw.text("GAME OVER", center=(400, 300), fontsize=50, color="red")
