import pygame
import random
import sys
from pygame import mixer

# INITIALIZE PYGAME
pygame.init()
mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Night Market Catch")

clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# FONTS
font_score = pygame.font.SysFont("Arial", 25)
font_title = pygame.font.SysFont("Arial", 55, bold=True)
font_menu = pygame.font.SysFont("Arial", 30, bold=True)
font_gameover = pygame.font.SysFont("Arial", 60, bold=True)
font_pause = pygame.font.SysFont("Arial", 55, bold=True)

# BACKGROUND
background_img = pygame.image.load("background.jpg")
background = pygame.transform.scale(background_img, (800, 600))

# ICON
icon = pygame.image.load("burger.png")
pygame.display.set_icon(icon)

# FOOD ASSETS
burger_img = pygame.image.load("burger.png")
burger = pygame.transform.scale(burger_img, (50, 50))

donut_img = pygame.image.load("donut.png")
donut = pygame.transform.scale(donut_img, (50, 50))

fries_img = pygame.image.load("fries.png")
fries = pygame.transform.scale(fries_img, (50, 50))

trash_img = pygame.image.load("trash.png")
trash = pygame.transform.scale(trash_img, (50, 50))

# BASKET
basket_img = pygame.image.load("basket.png")
basket = pygame.transform.scale(basket_img, (120, 75))

# HEART
heart_img = pygame.image.load("heart.png")
heart = pygame.transform.scale(heart_img, (35, 35))

# SOUNDS
bgmusic = mixer.Sound("bgmusic.mp3")
collect_sound = mixer.Sound("collect.mp3")
gameover_sound = mixer.Sound("gameover.mp3")

# PLAY BACKGROUND MUSIC
bgmusic.play(-1)

# ITEMS
num_of_items = 5
items = []
for i in range(num_of_items):
    item_type = random.choice(
        ["burger", "donut", "fries", "trash"]
    )
    if item_type == "burger":
        image = burger
    elif item_type == "donut":
        image = donut
    elif item_type == "fries":
        image = fries
    else:
        image = trash

    items.append({
        "type": item_type,
        "image": image,
        "x": random.randint(50, 750),
        "y": random.randint(-600, -50),
        "speed": random.uniform(2, 4)
    })

# GAME VARIABLES
score = 0
lives = 3

basket_x = 340
basket_y = 500

game_state = "menu"

# 60 SECOND TIMER
GAME_DURATION = 60000
game_start_time = 0

# Used to keep track of how long the game was paused
pause_start_time = 0

# PAUSE
paused = False

# TRASH HIT EFFECT
stun_duration = 800

stun_start_time = 0

red_effect_duration = 500

red_effect_start_time = 0

# RESET ITEM
def reset_item(item):
    item["x"] = random.randint(50, 750)
    item["y"] = random.randint(-300, -50)
    item["speed"] = random.uniform(2, 4)
    item["type"] = random.choice(
        ["burger", "donut", "fries", "trash"]
    )
    if item["type"] == "burger":
        item["image"] = burger
    elif item["type"] == "donut":
        item["image"] = donut
    elif item["type"] == "fries":
        item["image"] = fries
    else:
        item["image"] = trash

# RESET GAME
def reset_game():
    global score
    global lives
    global basket_x
    global basket_y
    global stun_start_time
    global red_effect_start_time
    global game_start_time
    global pause_start_time
    global paused

    score = 0
    lives = 3

    basket_x = 340
    basket_y = 500

    stun_start_time = 0
    red_effect_start_time = 0

    # Start timer
    game_start_time = pygame.time.get_ticks()

    # Reset pause
    pause_start_time = 0
    paused = False

    # Reset items
    for item in items:
        reset_item(item)

# SHOW SCORE
def show_score():
    score_text = font_score.render(
        "Score: " + str(score),
        True,
        WHITE
    )
    screen.blit(
        score_text,
        (10, 10)
    )

# SHOW LIVES
def show_lives():
    lives_text = font_score.render(
        "Lives:",
        True,
        WHITE
    )
    screen.blit(
        lives_text,
        (650, 10)
    )
    for i in range(lives):
        screen.blit(
            heart,
            (725 + (i * 25), 5)
        )

# SHOW TIMER
def show_timer():
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - game_start_time
    remaining_time = max(
        0,
        (GAME_DURATION - elapsed_time) // 1000
    )
    timer_text = font_score.render(
        "Time: " + str(remaining_time),
        True,
        WHITE
    )
    timer_rect = timer_text.get_rect(
        center=(400, 25)
    )
    screen.blit(
        timer_text,
        timer_rect
    )

# START MENU
def draw_start_menu():
    screen.blit(
        background,
        (0, 0)
    )
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    screen.blit(
        overlay,
        (0, 0)
    )
    # TITLE
    title = font_title.render(
        "NIGHT MARKET CATCH",
        True,
        YELLOW
    )
    title_rect = title.get_rect(
        center=(400, 180)
    )
    screen.blit(
        title,
        title_rect
    )
    # INSTRUCTION 1
    instruction = font_menu.render(
        "Catch the food!",
        True,
        WHITE
    )
    instruction_rect = instruction.get_rect(
        center=(400, 270)
    )
    screen.blit(
        instruction,
        instruction_rect
    )
    # INSTRUCTION 2
    instruction2 = font_menu.render(
        "Avoid the trash!",
        True,
        WHITE
    )
    instruction2_rect = instruction2.get_rect(
        center=(400, 310)
    )
    screen.blit(
        instruction2,
        instruction2_rect
    )
    # START
    start_text = font_menu.render(
        "PRESS ENTER TO START",
        True,
        GREEN
    )
    start_rect = start_text.get_rect(
        center=(400, 400)
    )
    screen.blit(
        start_text,
        start_rect
    )
    # QUIT
    quit_text = font_menu.render(
        "PRESS ESC TO QUIT",
        True,
        WHITE
    )
    quit_rect = quit_text.get_rect(
        center=(400, 450)
    )
    screen.blit(
        quit_text,
        quit_rect
    )

# PAUSE SCREEN
def draw_pause_screen():
    # Dark transparent overlay
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(
        overlay,
        (0, 0)
    )
    # PAUSED
    pause_text = font_pause.render(
        "PAUSED",
        True,
        YELLOW
    )
    pause_rect = pause_text.get_rect(
        center=(400, 220)
    )
    screen.blit(
        pause_text,
        pause_rect
    )
    # Resume
    resume_text = font_menu.render(
        "PRESS P TO RESUME",
        True,
        GREEN
    )
    resume_rect = resume_text.get_rect(
        center=(400, 310)
    )
    screen.blit(
        resume_text,
        resume_rect
    )
    # Restart
    restart_text = font_menu.render(
        "PRESS R TO RESTART",
        True,
        WHITE
    )
    restart_rect = restart_text.get_rect(
        center=(400, 360)
    )
    screen.blit(
        restart_text,
        restart_rect
    )
    # Quit
    quit_text = font_menu.render(
        "PRESS ESC TO QUIT",
        True,
        WHITE
    )
    quit_rect = quit_text.get_rect(
        center=(400, 410)
    )
    screen.blit(
        quit_text,
        quit_rect
    )

# GAME OVER SCREEN
def draw_game_over():
    screen.blit(
        background,
        (0, 0)
    )
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(
        overlay,
        (0, 0)
    )
    # GAME OVER
    gameover_text = font_gameover.render(
        "GAME OVER",
        True,
        RED
    )
    gameover_rect = gameover_text.get_rect(
        center=(400, 200)
    )
    screen.blit(
        gameover_text,
        gameover_rect
    )
    # SCORE
    final_score = font_menu.render(
        "Final Score: " + str(score),
        True,
        WHITE
    )
    final_rect = final_score.get_rect(
        center=(400, 300)
    )
    screen.blit(
        final_score,
        final_rect
    )
    # RESTART
    restart_text = font_menu.render(
        "PRESS R TO RESTART",
        True,
        GREEN
    )
    restart_rect = restart_text.get_rect(
        center=(400, 390)
    )
    screen.blit(
        restart_text,
        restart_rect
    )
    # QUIT
    quit_text = font_menu.render(
        "PRESS ESC TO QUIT",
        True,
        WHITE
    )
    quit_rect = quit_text.get_rect(
        center=(400, 440)
    )
    screen.blit(
        quit_text,
        quit_rect
    )

# WIN SCREEN
def draw_win_screen():
    screen.blit(
        background,
        (0, 0)
    )
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(
        overlay,
        (0, 0)
    )
    # YOU WIN
    win_text = font_gameover.render(
        "YOU WIN!",
        True,
        GREEN
    )
    win_rect = win_text.get_rect(
        center=(400, 180)
    )
    screen.blit(
        win_text,
        win_rect
    )
    # MESSAGE
    survived_text = font_menu.render(
        "You survived 60 seconds!",
        True,
        WHITE
    )
    survived_rect = survived_text.get_rect(
        center=(400, 280)
    )
    screen.blit(
        survived_text,
        survived_rect
    )
    # SCORE
    final_score = font_menu.render(
        "Final Score: " + str(score),
        True,
        YELLOW
    )
    final_rect = final_score.get_rect(
        center=(400, 340)
    )
    screen.blit(
        final_score,
        final_rect
    )
    # RESTART
    restart_text = font_menu.render(
        "PRESS R TO PLAY AGAIN",
        True,
        GREEN
    )
    restart_rect = restart_text.get_rect(
        center=(400, 420)
    )
    screen.blit(
        restart_text,
        restart_rect
    )
    # QUIT
    quit_text = font_menu.render(
        "PRESS ESC TO QUIT",
        True,
        WHITE
    )
    quit_rect = quit_text.get_rect(
        center=(400, 470)
    )
    screen.blit(
        quit_text,
        quit_rect
    )

# RED EFFECT
def draw_red_effect():
    global red_effect_start_time
    current_time = pygame.time.get_ticks()
    if current_time - red_effect_start_time < red_effect_duration:
        elapsed = (
            current_time -
            red_effect_start_time
        )
        alpha = int(
            150 * (
                1 -
                elapsed /
                red_effect_duration
            )
        )
        if alpha < 0:
            alpha = 0
        red_overlay = pygame.Surface(
            (800, 600)
        )
        red_overlay.set_alpha(alpha)
        red_overlay.fill(RED)
        screen.blit(
            red_overlay,
            (0, 0)
        )

# MAIN GAME LOOP
running = True
while running:
    clock.tick(60)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MENU
        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # PLAYING
        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                # PAUSE / RESUME
                if event.key == pygame.K_p:
                    if not paused:
                        # Start pause
                        paused = True
                        pause_start_time = (
                            pygame.time.get_ticks()
                        )

                    else:
                        # Resume
                        paused = False
                        current_time = (
                            pygame.time.get_ticks()
                        )
                        # How long we were paused
                        paused_duration = (
                            current_time -
                            pause_start_time
                        )
                        # Move game start time forward
                        # so the timer does not count pause time
                        game_start_time += (
                            paused_duration
                        )
                        # Also move stun timer forward
                        if stun_start_time > 0:
                            stun_start_time += (
                                paused_duration
                            )
                        # Move red effect timer forward
                        if red_effect_start_time > 0:
                            red_effect_start_time += (
                                paused_duration
                            )

                # RESTART
                elif event.key == pygame.K_r:
                    reset_game()
                    game_state = "playing"

                # QUIT
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # GAME OVER
        elif game_state == "gameover":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # WIN
        elif game_state == "win":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    running = False

    # START MENU
    if game_state == "menu":
        draw_start_menu()

    # PLAYING
    elif game_state == "playing":
        # BACKGROUND
        screen.blit(
            background,
            (0, 0)
        )

        # PAUSED
        if paused:
            # Draw the game exactly as it was
            # before pause
            screen.blit(
                basket,
                (basket_x, basket_y)
            )

            for item in items:
                screen.blit(
                    item["image"],
                    (item["x"], item["y"])
                )
            show_score()
            show_lives()
            show_timer()
            draw_pause_screen()

        # NORMAL PLAYING
        else:
            current_time = pygame.time.get_ticks()
            # CHECK 60 SECOND TIMER
            if (
                current_time -
                game_start_time
                >= GAME_DURATION
            ):
                game_state = "win"

            # CHECK STUN
            is_stunned = (
                current_time -
                stun_start_time
                < stun_duration
            )

            # BASKET MOVEMENT
            if not is_stunned:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    basket_x -= 6
                if keys[pygame.K_RIGHT]:
                    basket_x += 6

            # KEEP BASKET INSIDE SCREEN
            if basket_x < 0:
                basket_x = 0
            if basket_x > 680:
                basket_x = 680

            # DRAW BASKET
            basket_rect = screen.blit(
                basket,
                (basket_x, basket_y)
            )

            # DRAW & MOVE ITEMS
            for item in items:
                item["y"] += item["speed"]
                item_rect = screen.blit(
                    item["image"],
                    (item["x"], item["y"])
                )

                # COLLISION
                if basket_rect.colliderect(
                    item_rect
                ):
                    # TRASH
                    if item["type"] == "trash":
                        lives -= 1
                        stun_start_time = (
                            pygame.time.get_ticks()
                        )
                        red_effect_start_time = (
                            pygame.time.get_ticks()
                        )
                        mixer.Sound.play(
                            collect_sound
                        )
                        reset_item(item)
                        print(
                            "Trash hit! Lives:",
                            lives
                        )

                    # FOOD
                    else:
                        score += 1
                        mixer.Sound.play(
                            collect_sound
                        )
                        reset_item(item)

                # ITEM MISSED
                if item["y"] > 600:
                    reset_item(item)

            # SCORE
            show_score()

            # LIVES
            show_lives()

            # TIMER
            show_timer()

            # STUN EFFECT
            if is_stunned:
                warning_font = pygame.font.SysFont(
                    "Arial",
                    30,
                    bold=True
                )
                warning_text = warning_font.render(
                    "OUCH!",
                    True,
                    RED
                )
                warning_rect = warning_text.get_rect(
                    center=(400, 450)
                )
                screen.blit(
                    warning_text,
                    warning_rect
                )

            # RED EFFECT
            draw_red_effect()

            # GAME OVER
            if lives <= 0:
                mixer.Sound.play(
                    gameover_sound
                )
                game_state = "gameover"

    # GAME OVER SCREEN
    elif game_state == "gameover":
        draw_game_over()

    # WIN SCREEN
    elif game_state == "win":
        draw_win_screen()

    # UPDATE SCREEN
    pygame.display.update()

# QUIT
pygame.quit()
sys.exit()