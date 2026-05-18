import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# 📱 Mobile Layout Settings (Full Screen Auto-Scaling)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("BLP Cyber Pong")
clock = pygame.time.Clock()

# Dynamic Sizing Proportions
BALL_SIZE = int(HEIGHT * 0.04)
PADDLE_WIDTH = int(WIDTH * 0.025)
PADDLE_HEIGHT = int(HEIGHT * 0.20)
BUTTON_WIDTH, BUTTON_HEIGHT = int(WIDTH * 0.25), int(HEIGHT * 0.11)
FPS = 60

# Palette 
BLACK = (12, 12, 16)
WHITE = (240, 240, 240)
GRAY = (50, 50, 60)
PLAYER_COLOR = (0, 255, 204)  # Electric Mint
AI_COLOR = (255, 51, 102)     # Cyber Pink
SHADOW_COLOR = (40, 20, 40)   # Dark thick shadow background

# Fonts
font_title = pygame.font.Font(None, int(HEIGHT * 0.14))
font_menu = pygame.font.Font(None, int(HEIGHT * 0.07))
font_hud = pygame.font.Font(None, int(HEIGHT * 0.09))
font_countdown = pygame.font.Font(None, int(HEIGHT * 0.25))

# Game States: 'LOADING', 'MENU', 'PLAYING', 'PAUSED'
state = 'LOADING'
loading_progress = 0

# Countdown System Variables
countdown_start_time = 0
countdown_current_value = 0
point_alert_text = ""
point_alert_color = WHITE

# Difficulty Settings
ai_speed = 5
difficulty_selected = 'MEDIUM'

# Core Entities
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
player = pygame.Rect(int(WIDTH * 0.04), HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - int(WIDTH * 0.04) - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Physics Tuning
base_speed_x = int(WIDTH * 0.009)
base_speed_y = int(HEIGHT * 0.012)
ball_speed_x = base_speed_x
ball_speed_y = base_speed_y

player_score = 0
ai_score = 0

# Track mouse movement vectors explicitly
mouse_velocity_x = 0
mouse_velocity_y = 0

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = base_speed_x if ball_speed_x < 0 else -base_speed_x
    ball_speed_y = random.choice([base_speed_y, -base_speed_y])

def start_match_countdown(alert_msg="", alert_color=WHITE):
    global countdown_start_time, countdown_current_value, point_alert_text, point_alert_color
    countdown_start_time = pygame.time.get_ticks()
    countdown_current_value = 3  
    point_alert_text = alert_msg
    point_alert_color = alert_color

def reset_game():
    global player_score, ai_score
    player_score = 0
    ai_score = 0
    reset_ball()
    start_match_countdown("READY...?", WHITE)

def draw_flat_text(text, font, color, y_pos):
    """Renders normal flat text without shadows."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, y_pos))
    screen.blit(surface, rect)

def draw_buggy_text(text, font, color, y_pos):
    """Renders thick layered arcade text mimicking a beach buggy styling engine."""
    shadow_surface = font.render(text, True, SHADOW_COLOR)
    main_surface = font.render(text, True, color)
    
    shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 5, y_pos + 5))
    main_rect = main_surface.get_rect(center=(WIDTH // 2, y_pos))
    
    screen.blit(shadow_surface, shadow_rect)
    screen.blit(main_surface, main_rect)

# Mouse pointer is kept fully visible
pygame.mouse.set_visible(True)

running = True
while running:
    current_ticks = pygame.time.get_ticks()
    
    # Fetch accurate mouse/touch position
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ✅ FIXED: Read individual index values from relative tuple
        if event.type == pygame.MOUSEMOTION:
            mouse_velocity_x = event.rel[0]  # Raw X tracking integer
            mouse_velocity_y = event.rel[1]  # Raw Y tracking integer
            
            # Follow cursor position explicitly
            player.x = mx - PADDLE_WIDTH // 2
            player.y = my - PADDLE_HEIGHT // 2
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 'MENU':
                if pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.24), BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mx, my):
                    difficulty_selected = 'EASY'
                    ai_speed = int(HEIGHT * 0.008)
                elif pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.37), BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mx, my):
                    difficulty_selected = 'MEDIUM'
                    ai_speed = int(HEIGHT * 0.013)
                elif pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.50), BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mx, my):
                    difficulty_selected = 'HARD'
                    ai_speed = int(HEIGHT * 0.020)
                elif pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.65), BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mx, my):
                    state = 'PLAYING'
                    reset_game()
                elif pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.78), BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mx, my):
                    running = False
                    
            elif state == 'PLAYING' and countdown_current_value == 0:
                if pygame.Rect(WIDTH - int(WIDTH*0.14), int(HEIGHT*0.02), int(WIDTH*0.11), int(HEIGHT*0.11)).collidepoint(mx, my):
                    state = 'PAUSED'
                    
            elif state == 'PAUSED':
                if pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.35), BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mx, my):
                    state = 'PLAYING'
                elif pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.49), BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mx, my):
                    state = 'MENU'
                elif pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.63), BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mx, my):
                    running = False

    # Constraints for Left Half Court Boundaries
    if player.left < 0: player.left = 0
    if player.right > WIDTH // 2: player.right = WIDTH // 2
    if player.top < 0: player.top = 0
    if player.bottom > HEIGHT: player.bottom = HEIGHT

    # --- STATE MACHINE PROCESSING ---
    if state == 'LOADING':
        screen.fill(BLACK)
        draw_buggy_text("CYBER PONG", font_title, WHITE, HEIGHT // 3)
        
        loading_progress += 1.5
        bar_width = int(WIDTH * 0.4)
        bar_height = int(HEIGHT * 0.02)
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - bar_width//2, int(HEIGHT*0.55), bar_width, bar_height))
        pygame.draw.rect(screen, PLAYER_COLOR, (WIDTH//2 - bar_width//2, int(HEIGHT*0.55), int(bar_width * (loading_progress/100)), bar_height))
        
        draw_buggy_text("Big lui Productions", font_menu, PLAYER_COLOR, int(HEIGHT * 0.72))
        
        if loading_progress >= 100:
            state = 'MENU'

    elif state == 'MENU':
        screen.fill(BLACK)
        draw_buggy_text("SELECT DIFFICULTY", font_title, WHITE, int(HEIGHT * 0.11))
        
        diff_options = [('EASY', int(HEIGHT*0.24)), ('MEDIUM', int(HEIGHT*0.37)), ('HARD', int(HEIGHT*0.50))]
        for name, y in diff_options:
            bg_color = PLAYER_COLOR if difficulty_selected == name else GRAY
            text_color = BLACK if difficulty_selected == name else WHITE
            pygame.draw.rect(screen, bg_color, (WIDTH//2 - BUTTON_WIDTH//2, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
            draw_flat_text(name, font_menu, text_color, y + BUTTON_HEIGHT//2 - 2)
            
        pygame.draw.rect(screen, AI_COLOR, (WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.65), BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
        draw_buggy_text("START GAME", font_menu, WHITE, int(HEIGHT*0.65) + BUTTON_HEIGHT//2 - 2)

        pygame.draw.rect(screen, GRAY, (WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.78), BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
        draw_buggy_text("QUIT", font_menu, WHITE, int(HEIGHT*0.78) + BUTTON_HEIGHT//2 - 2)

        draw_buggy_text("Big lui Productions", font_menu, (80, 80, 90), int(HEIGHT * 0.93))

    elif state == 'PLAYING':
        screen.fill(BLACK)

        if countdown_current_value != 0:
            elapsed_time = current_ticks - countdown_start_time
            if elapsed_time < 700:
                countdown_current_value = 2  
            elif elapsed_time < 1400:
                countdown_current_value = 1  
            elif elapsed_time < 2000:
                countdown_current_value = -1 
            else:
                countdown_current_value = 0  

        else:
            # AI Engine logic
            if ai_paddle.centery < ball.centery and ai_paddle.bottom < HEIGHT:
                ai_paddle.y += ai_speed
            if ai_paddle.centery > ball.centery and ai_paddle.top > 0:
                ai_paddle.y -= ai_speed

            # Ball Vector calculation
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_speed_y *= -1

            # Hit dynamics
            if ball.colliderect(player):
                ball_speed_x = abs(ball_speed_x)
                if mouse_velocity_x > 4:
                    ball_speed_x += (mouse_velocity_x * 0.35)
                ball_speed_y += (mouse_velocity_y * 0.30)
                ball.left = player.right + 2
                
            elif ball.colliderect(ai_paddle):
                ball_speed_x = -abs(ball_speed_x)
                ball_speed_x *= 1.04

            ball_speed_x = max(-26, min(26, ball_speed_x))
            ball_speed_y = max(-18, min(18, ball_speed_y))

            # Checking point frames
            if ball.left <= 0:
                ai_score += 1
                reset_ball()
                start_match_countdown("AI SCORED!", AI_COLOR)
            if ball.right >= WIDTH:
                player_score += 1
                reset_ball()
                start_match_countdown("POINT FOR YOU!", PLAYER_COLOR)

        # Draw Base Arena Environment
        pygame.draw.line(screen, GRAY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        pygame.draw.rect(screen, PLAYER_COLOR, player, border_radius=4)
        pygame.draw.rect(screen, AI_COLOR, ai_paddle, border_radius=4)
        pygame.draw.ellipse(screen, WHITE, ball)
        
        # UI Pause Button
        pause_btn = pygame.Rect(WIDTH - int(WIDTH*0.14), int(HEIGHT*0.02), int(WIDTH*0.11), int(HEIGHT*0.11))
        pygame.draw.rect(screen, GRAY, pause_btn, border_radius=8)
        p_surf = font_hud.render("||", True, WHITE)
        screen.blit(p_surf, p_surf.get_rect(center=pause_btn.center))

        # HUD Scores
        p_text = font_hud.render(str(player_score), True, PLAYER_COLOR)
        ai_text = font_hud.render(str(ai_score), True, AI_COLOR)
        screen.blit(p_text, (WIDTH // 2 - int(WIDTH*0.08), int(HEIGHT*0.03)))
        screen.blit(ai_text, (WIDTH // 2 + int(WIDTH*0.05), int(HEIGHT*0.03)))

        if countdown_current_value != 0:
            if countdown_current_value != -1 and point_alert_text:
                draw_buggy_text(point_alert_text, font_hud, point_alert_color, HEIGHT // 3)
            
            display_lbl = "GO!" if countdown_current_value == -1 else str(countdown_current_value)
            lbl_color = PLAYER_COLOR if countdown_current_value == -1 else WHITE
            draw_buggy_text(display_lbl, font_countdown, lbl_color, int(HEIGHT * 0.55))

    elif state == 'PAUSED':
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(12)
        screen.blit(overlay, (0, 0))
        
        draw_buggy_text("GAME PAUSED", font_title, WHITE, HEIGHT // 5)
        
        # Overlay Buttons
        pygame.draw.rect(screen, PLAYER_COLOR, (WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.35), BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
        draw_flat_text("RESUME", font_menu, BLACK, int(HEIGHT*0.35) + BUTTON_HEIGHT//2 - 2)

        pygame.draw.rect(screen, GRAY, (WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.49), BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
        draw_buggy_text("MAIN MENU", font_menu, WHITE, int(HEIGHT*0.49) + BUTTON_HEIGHT//2 - 2)

        pygame.draw.rect(screen, AI_COLOR, (WIDTH//2 - BUTTON_WIDTH//2, int(HEIGHT*0.63), BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
        draw_buggy_text("QUIT GAME", font_menu, WHITE, int(HEIGHT*0.63) + BUTTON_HEIGHT//2 - 2)

        draw_buggy_text("Big lui Productions", font_menu, (80, 80, 90), int(HEIGHT * 0.85))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
