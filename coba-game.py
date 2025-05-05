import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sky Jump - Ultimate Journey")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 180, 255)
LIGHT_BLUE = (200, 230, 255)
GREEN = (50, 150, 50)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
YELLOW = (255, 255, 0)
RED = (255, 50, 50)
PURPLE = (150, 50, 200)
SPACE_BLUE = (15, 15, 50)
FOREST_GREEN = (20, 80, 20)
ICE_BLUE = (200, 240, 255)

# Game states
STATE_MENU = 0
STATE_GAME = 1
STATE_LEVEL_SELECT = 2
STATE_GAME_OVER = 3
STATE_LEVEL_COMPLETE = 4
STATE_COUNTDOWN = 5

# Fonts
font_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Clock for controlling game speed
clock = pygame.time.Clock()
FPS = 60

# Player settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
JUMP_SPEED = -15  # Meningkatkan kecepatan lompatan dasar
MOVE_SPEED = 5
GRAVITY = 0.3

# Platform settings
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 2
TRAMPOLINE_BOOST = -20
# Mengurangi jarak maksimum antar platform
MAX_PLATFORM_GAP = 100  # Diturunkan dari 120 agar lebih terjangkau

# Game progress tracking
max_level_unlocked = 1
current_level = 1
score = 0
high_scores = [0, 0, 0, 0]

# Level settings
SCORE_TO_COMPLETE = 5000
SCORE_PER_PLATFORM = 100

# Level backgrounds and features
level_backgrounds = [
    BLUE,          # Level 1 - Earth
    ICE_BLUE,      # Level 2 - Antarctica
    SPACE_BLUE,    # Level 3 - Space
    FOREST_GREEN   # Level 4 - Forest
]

level_names = [
    "Earth",
    "Antarctica",
    "Space",
    "Forest"
]

level_difficulty = [
    "Easy",
    "Medium",
    "Hard",
    "Extreme"
]

#Asset
sprite_sheet = pygame.image.load("E:/vscode/TUBES PBO GACOR/tiles_page1.png").convert_alpha()

#Ukuran Tile
TILE_WIDTH = 32
TILE_HEIGHT = 32

#Fungsi ambil tile berdasarkan koordinat grid
def get_tile(x, y):
    rect = pygame.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
    tile = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SCRALPHA)
    tile.blit(sprite_sheet, (0, 0), rect)
    return tile

# Load images (placeholder rectangles)
def load_image(name, size=None):
    surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)) if name == "player" else pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
    if name == "player":
        surf.fill(YELLOW)
        pygame.draw.rect(surf, RED, (10, 10, 20, 20))
    elif name == "platform":
        surf.fill(GREEN)
    elif name == "trampoline":
        surf.fill(PURPLE)
    elif name == "fragile":
        surf.fill(ICE_BLUE)
        pygame.draw.line(surf, WHITE, (0, 0), (PLATFORM_WIDTH, PLATFORM_HEIGHT), 2)
        pygame.draw.line(surf, WHITE, (PLATFORM_WIDTH, 0), (0, PLATFORM_HEIGHT), 2)
    elif name == "moving":
        surf.fill(GRAY)
    else:
        surf.fill(RED)
    if size:
        surf = pygame.transform.scale(surf, size)
    return surf

player_img = load_image("player")
platform_img = load_image("platform")
trampoline_img = load_image("trampoline")
fragile_img = load_image("fragile")
moving_img = load_image("moving")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.platforms_touched = set()
        # Tambah variabel untuk melacak waktu sejak lompatan terakhir
        self.last_jump_time = 0
        self.stuck_timer = 0

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += MOVE_SPEED
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Deteksi jika pemain tidak bergerak ke atas dalam waktu lama
        current_time = pygame.time.get_ticks()
        if self.velocity_y >= 0:
            self.stuck_timer += 1
        else:
            self.stuck_timer = 0
            self.last_jump_time = current_time

        # Jika pemain terdeteksi stuck (tidak bisa naik setelah waktu tertentu)
        if self.stuck_timer > FPS * 5:  # Terjebak selama 5 detik
            # Reset posisi ke platform terdekat di atas
            closest_platform = self.find_closest_platform_above(platforms)
            if closest_platform:
                self.rect.bottom = closest_platform.rect.top
                self.velocity_y = JUMP_SPEED
                self.stuck_timer = 0
                return True

        for platform in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0 and self.rect.bottom > platform.rect.top and self.rect.bottom < platform.rect.top + 30:
                self.rect.bottom = platform.rect.top
                if platform.platform_type == "trampoline":
                    self.velocity_y = TRAMPOLINE_BOOST
                else:
                    self.velocity_y = JUMP_SPEED
                if platform.platform_type == "fragile":
                    platform.break_platform()
                global score
                if platform.id not in self.platforms_touched:
                    score += SCORE_PER_PLATFORM
                    self.platforms_touched.add(platform.id)
                # Reset stuck timer setiap kali berhasil mendarat
                self.stuck_timer = 0
                self.last_jump_time = current_time
                return True
        return False

    def find_closest_platform_above(self, platforms):
        closest_platform = None
        closest_distance = float('inf')
        for platform in platforms:
            # Hanya pertimbangkan platform yang ada di atas pemain
            if platform.rect.bottom < self.rect.top:
                distance = self.rect.top - platform.rect.bottom
                if distance < closest_distance:
                    closest_distance = distance
                    closest_platform = platform
        return closest_platform

# Platform class
class Platform(pygame.sprite.Sprite):
    next_id = 0
    def __init__(self, x, y, platform_type="normal", direction=1):
        super().__init__()
        self.platform_type = platform_type
        self.id = Platform.next_id
        Platform.next_id += 1
        if platform_type == "normal":
            self.image = get_tile(0, 8)
            self.rect = self.image.get_rect(topleft=(x, y))
        elif platform_type == "trampoline":
            self.image = trampoline_img
        elif platform_type == "fragile":
            self.image = fragile_img
        elif platform_type == "moving":
            self.image = moving_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = direction
        self.move_counter = 0
        self.move_limit = 100
        self.to_remove = False
        self.break_timer = 0

    def update(self):
        if self.platform_type == "moving":
            self.move_counter += 1
            self.rect.x += self.move_direction * PLATFORM_SPEED
            if self.move_counter >= self.move_limit:
                self.move_direction *= -1
                self.move_counter = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                self.move_direction *= -1
            if self.rect.left < 0:
                self.rect.left = 0
                self.move_direction *= -1
        if self.break_timer > 0:
            self.break_timer -= 1
            if self.break_timer <= 0:
                self.to_remove = True

    def break_platform(self):
        if self.platform_type == "fragile":
            self.break_timer = 30

# Raindrop class for forest level
class Raindrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 10))
        self.image.fill(LIGHT_BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(-100, 0)
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.rect.y = random.randint(-100, -10)

# Game class
class Game:
    def __init__(self):
        self.state = STATE_MENU
        self.level = 1
        self.buttons = []
        self.platforms = pygame.sprite.Group()
        self.player = Player()
        self.countdown_timer = 3
        self.last_countdown_time = 0
        self.raindrops = pygame.sprite.Group()
        self.lightning_warning = False
        self.lightning_flash = False
        self.lightning_timer = 0
        self.lightning_cycle_timer = 0
        self.camera_offset = 0
        self.highest_point = SCREEN_HEIGHT
        self.scroll_threshold = SCREEN_HEIGHT // 3
        self.level_buttons = []
        # Tambahan untuk safety net
        self.last_platform_y = 0
        self.emergency_platforms = []

    def reset_game(self):
        global score
        score = 0
        self.player = Player()
        self.platforms = pygame.sprite.Group()
        self.camera_offset = 0
        self.highest_point = SCREEN_HEIGHT
        Platform.next_id = 0
        self.generate_platforms()
        self.raindrops.empty()
        self.lightning_warning = False
        self.lightning_flash = False
        self.lightning_timer = 0
        self.lightning_cycle_timer = 0
        if self.level == 4:
            for _ in range(50):
                self.raindrops.add(Raindrop())

    def start_level(self, level):
        global current_level
        current_level = level
        self.level = level
        self.state = STATE_COUNTDOWN
        self.countdown_timer = 3
        self.last_countdown_time = time.time()
        self.reset_game()

    def generate_platforms(self):
        self.platforms.empty()
        # Platform awal
        self.platforms.add(Platform(SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, SCREEN_HEIGHT - 50))
        last_y = SCREEN_HEIGHT - 50
        self.last_platform_y = last_y
        
        for i in range(20):
            # Buat platform dengan jarak yang terjangkau
            platform_vertical_gap = random.randint(40, MAX_PLATFORM_GAP)
            
            # Sesuaikan tinggi lompatan maksimal pemain
            max_jump_height = abs(JUMP_SPEED) * 2 + abs(TRAMPOLINE_BOOST) * 0.5
            
            # Pastikan platform tidak terlalu jauh vertikal
            if platform_vertical_gap > max_jump_height:
                platform_vertical_gap = max_jump_height
                
            y = last_y - platform_vertical_gap
            last_y = y
            self.last_platform_y = y
            
            # Posisi horizontal yang lebih terdistribusi
            section_width = SCREEN_WIDTH // 3
            section = i % 3  # 0, 1, atau 2 untuk distribusi platform yang lebih merata
            x = random.randint(section * section_width, (section + 1) * section_width - PLATFORM_WIDTH)
            
            # Koreksi jika terlalu di tepi
            if x < 50:
                x = 50
            elif x > SCREEN_WIDTH - PLATFORM_WIDTH - 50:
                x = SCREEN_WIDTH - PLATFORM_WIDTH - 50
            
            if self.level == 1:
                platform_type = "trampoline" if random.random() < 0.2 else "normal"
                self.platforms.add(Platform(x, y, platform_type))
            elif self.level == 2:
                platform_type = "fragile" if random.random() < 0.4 else "normal"
                self.platforms.add(Platform(x, y, platform_type))
            elif self.level == 3:
                platform_type = "moving"
                direction = 1 if random.random() < 0.5 else -1
                self.platforms.add(Platform(x, y, platform_type, direction))
            elif self.level == 4:
                r = random.random()
                if r < 0.3:
                    platform_type = "fragile"
                elif r < 0.5:
                    platform_type = "trampoline"
                elif r < 0.7:
                    platform_type = "moving"
                    direction = 1 if random.random() < 0.5 else -1
                    self.platforms.add(Platform(x, y, platform_type, direction))
                    continue
                else:
                    platform_type = "normal"
                self.platforms.add(Platform(x, y, platform_type))
            self.highest_point = y

    def add_platforms(self):
        if self.camera_offset > len(self.platforms) * 30 - SCREEN_HEIGHT:
            last_y = self.highest_point
            
            for i in range(10):
                # Buat platform dengan jarak yang terjangkau
                platform_vertical_gap = random.randint(40, MAX_PLATFORM_GAP)
                
                # Sesuaikan tinggi lompatan maksimal pemain
                max_jump_height = abs(JUMP_SPEED) * 2
                if platform_vertical_gap > max_jump_height:
                    platform_vertical_gap = max_jump_height
                    
                y = last_y - platform_vertical_gap
                last_y = y
                self.last_platform_y = y
                
                # Posisi horizontal yang lebih terdistribusi
                section_width = SCREEN_WIDTH // 3
                section = i % 3  # Memastikan distribusi yang lebih merata
                x = random.randint(section * section_width, (section + 1) * section_width - PLATFORM_WIDTH)
                
                # Koreksi jika terlalu di tepi
                if x < 50:
                    x = 50
                elif x > SCREEN_WIDTH - PLATFORM_WIDTH - 50:
                    x = SCREEN_WIDTH - PLATFORM_WIDTH - 50
                
                if self.level == 1:
                    platform_type = "trampoline" if random.random() < 0.2 else "normal"
                    self.platforms.add(Platform(x, y, platform_type))
                elif self.level == 2:
                    platform_type = "fragile" if random.random() < 0.4 else "normal"
                    self.platforms.add(Platform(x, y, platform_type))
                elif self.level == 3:
                    platform_type = "moving"
                    direction = 1 if random.random() < 0.5 else -1
                    self.platforms.add(Platform(x, y, platform_type, direction))
                elif self.level == 4:
                    r = random.random()
                    if r < 0.3:
                        platform_type = "fragile"
                    elif r < 0.5:
                        platform_type = "trampoline"
                    elif r < 0.7:
                        platform_type = "moving"
                        direction = 1 if random.random() < 0.5 else -1
                        self.platforms.add(Platform(x, y, platform_type, direction))
                        continue
                    else:
                        platform_type = "normal"
                    self.platforms.add(Platform(x, y, platform_type))
                self.highest_point = y

    def check_and_add_safety_platforms(self):
        # Tambahkan platform "keselamatan" jika pemain terdeteksi jatuh terlalu jauh
        if self.player.velocity_y > 10 and len(self.emergency_platforms) == 0:
            # Tambahkan platform darurat di bawah pemain
            safety_x = self.player.rect.x - PLATFORM_WIDTH//2 + self.player.rect.width//2
            if safety_x < 0:
                safety_x = 0
            if safety_x > SCREEN_WIDTH - PLATFORM_WIDTH:
                safety_x = SCREEN_WIDTH - PLATFORM_WIDTH
                
            safety_y = self.player.rect.y + 200
            emergency_platform = Platform(safety_x, safety_y, "normal")
            self.platforms.add(emergency_platform)
            self.emergency_platforms.append(emergency_platform)
            
        # Hapus platform darurat setelah beberapa saat
        if len(self.emergency_platforms) > 0:
            for platform in list(self.emergency_platforms):
                if self.player.rect.y < platform.rect.y - 200:
                    self.platforms.remove(platform)
                    self.emergency_platforms.remove(platform)

    def update(self):
        if self.state == STATE_COUNTDOWN:
            current_time = time.time()
            if current_time - self.last_countdown_time >= 1:
                self.countdown_timer -= 1
                self.last_countdown_time = current_time
                if self.countdown_timer < 0:
                    self.state = STATE_GAME
        elif self.state == STATE_GAME:
            global score, high_scores, max_level_unlocked, current_level
            if score >= SCORE_TO_COMPLETE:
                if current_level == max_level_unlocked and max_level_unlocked < 4:
                    max_level_unlocked += 1
                if score > high_scores[current_level-1]:
                    high_scores[current_level-1] = score
                self.state = STATE_LEVEL_COMPLETE
                return
                
            self.platforms.update()
            for platform in list(self.platforms):
                if platform.to_remove:
                    self.platforms.remove(platform)
                    if platform in self.emergency_platforms:
                        self.emergency_platforms.remove(platform)
                        
            if self.player.rect.top < self.scroll_threshold and self.player.velocity_y < 0:
                self.camera_offset += abs(self.player.velocity_y)
                self.player.rect.y += abs(self.player.velocity_y)
                for platform in self.platforms:
                    platform.rect.y += abs(self.player.velocity_y)
                for raindrop in self.raindrops:
                    raindrop.rect.y += abs(self.player.velocity_y)
                    
            self.player.update(self.platforms)
            self.add_platforms()
            
            # Check for stuck situations and add safety platforms if needed
            self.check_and_add_safety_platforms()
            
            # Level 4: Rain and Lightning
            if self.level == 4:
                self.raindrops.update()
                self.lightning_cycle_timer += 1
                if not self.lightning_warning and self.lightning_cycle_timer > FPS * 5:
                    self.lightning_warning = True
                    self.lightning_warning_timer = FPS * 2
                if self.lightning_warning:
                    self.lightning_warning_timer -= 1
                    if self.lightning_warning_timer <= 0:
                        self.lightning_flash = True
                        self.lightning_flash_timer = FPS // 2
                        self.lightning_warning = False
                        self.lightning_cycle_timer = 0
                if self.lightning_flash:
                    self.lightning_flash_timer -= 1
                    if self.lightning_flash_timer <= 0:
                        self.lightning_flash = False
                        
            # Game over buffer (sedikit lebih longgar)
            if self.player.rect.top > SCREEN_HEIGHT + 150:
                self.state = STATE_GAME_OVER

    def draw_menu(self):
        screen.fill(BLUE)
        title_text = font_large.render("SKY JUMP", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        self.buttons = [
            {"rect": pygame.Rect(300, 250, 200, 50), "text": "Play Level 1", "action": "play"},
            {"rect": pygame.Rect(300, 320, 200, 50), "text": "Level Select", "action": "level_select"},
            {"rect": pygame.Rect(300, 390, 200, 50), "text": "Quit", "action": "quit"}
        ]
        for btn in self.buttons:
            pygame.draw.rect(screen, DARK_GRAY, btn["rect"])
            text = font_medium.render(btn["text"], True, WHITE)
            screen.blit(text, (btn["rect"].x + 20, btn["rect"].y + 10))

    def draw_level_select(self):
        screen.fill(SPACE_BLUE)
        title_text = font_large.render("SELECT LEVEL", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        self.level_buttons = []
        button_width = 150
        button_height = 100
        margin = 20
        start_x = (SCREEN_WIDTH - (4*(button_width + margin))) // 2
        for i in range(4):
            x = start_x + i*(button_width + margin)
            y = 150
            rect = pygame.Rect(x, y, button_width, button_height)
            unlocked = (i+1) <= max_level_unlocked
            color = GREEN if unlocked else DARK_GRAY
            text_color = WHITE if unlocked else GRAY
            self.level_buttons.append({
                "rect": rect,
                "level": i+1,
                "unlocked": unlocked
            })
            pygame.draw.rect(screen, color, rect)
            level_text = font_medium.render(f"Level {i+1}", True, text_color)
            screen.blit(level_text, (x + 20, y + 10))
            if not unlocked:
                lock_text = font_small.render("LOCKED", True, RED)
                screen.blit(lock_text, (x + 20, y + 50))
            else:
                diff_text = font_small.render(level_difficulty[i], True, WHITE)
                screen.blit(diff_text, (x + 20, y + 50))
                score_text = font_small.render(f"Best: {high_scores[i]}", True, YELLOW)
                screen.blit(score_text, (x + 20, y + 70))

    def draw_game(self):
        screen.fill(level_backgrounds[self.level-1])
        self.platforms.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        if self.level == 4:
            self.raindrops.draw(screen)
            if self.lightning_warning:
                warning_text = font_medium.render("Lightning incoming!", True, YELLOW)
                screen.blit(warning_text, (SCREEN_WIDTH//2 - warning_text.get_width()//2, 50))
            if self.lightning_flash:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill(WHITE)
                screen.blit(overlay, (0,0))
        score_text = font_medium.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        level_text = font_small.render(f"Level: {level_names[self.level-1]}", True, BLACK)
        screen.blit(level_text, (10, 40))
        # Tampilkan target skor
        target_text = font_small.render(f"Target: {SCORE_TO_COMPLETE}", True, BLACK)
        screen.blit(target_text, (10, 70))

    def draw_countdown(self):
        screen.fill(level_backgrounds[self.level-1])
        countdown_text = font_large.render(str(self.countdown_timer) if self.countdown_timer > 0 else "GO!", True, WHITE)
        screen.blit(countdown_text, (SCREEN_WIDTH//2 - countdown_text.get_width()//2, SCREEN_HEIGHT//2 - countdown_text.get_height()//2))

    def draw_game_over(self):
        screen.fill(BLACK)
        over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 200))
        score_text = font_medium.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 300))
        retry_text = font_small.render("Press ENTER to retry or ESC to return to menu", True, WHITE)
        screen.blit(retry_text, (SCREEN_WIDTH//2 - retry_text.get_width()//2, 400))

    def draw_level_complete(self):
        screen.fill(GREEN)
        complete_text = font_large.render("LEVEL COMPLETE!", True, YELLOW)
        screen.blit(complete_text, (SCREEN_WIDTH//2 - complete_text.get_width()//2, 200))
        score_text = font_medium.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 300))
        next_text = font_small.render("Press ENTER for next level or ESC to return to menu", True, BLACK)
        screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 400))

    def handle_input(self, event):
        if self.state == STATE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in self.buttons:
                    if btn["rect"].collidepoint(pos):
                        if btn["action"] == "play":
                            self.start_level(1)
                        elif btn["action"] == "level_select":
                            self.state = STATE_LEVEL_SELECT
                        elif btn["action"] == "quit":
                            pygame.quit()
                            sys.exit()
        elif self.state == STATE_LEVEL_SELECT:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in self.level_buttons:
                    if btn["rect"].collidepoint(pos) and btn["unlocked"]:
                        self.start_level(btn["level"])
                # Tambahan tombol kembali ke menu
                if pygame.Rect(20, 500, 100, 40).collidepoint(pos):
                    self.state = STATE_MENU
            # Tambahan untuk tombol escape ke menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = STATE_MENU
        elif self.state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_level(self.level)
                elif event.key == pygame.K_ESCAPE:
                    self.state = STATE_MENU
        elif self.state == STATE_LEVEL_COMPLETE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.level < 4:
                        self.start_level(self.level+1)
                    else:
                        self.state = STATE_MENU
                elif event.key == pygame.K_ESCAPE:
                    self.state = STATE_MENU
        # Tambahan hotkey untuk memulai ulang level saat sedang bermain
        elif self.state == STATE_GAME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.start_level(self.level)

# Main game loop
game = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_input(event)
    game.update()
    if game.state == STATE_MENU:
        game.draw_menu()
    elif game.state == STATE_LEVEL_SELECT:
        game.draw_level_select()
        # Tombol kembali ke menu
        back_btn = pygame.Rect(20, 500, 100, 40)
        pygame.draw.rect(screen, DARK_GRAY, back_btn)
        back_text = font_small.render("Back", True, WHITE)
        screen.blit(back_text, (back_btn.x + 30, back_btn.y + 10))
    elif game.state == STATE_COUNTDOWN:
        game.draw_countdown()
    elif game.state == STATE_GAME:
        game.draw_game()
        # Tambah petunjuk restart
        restart_text = font_small.render("Press R to restart level", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30))
    elif game.state == STATE_GAME_OVER:
        game.draw_game_over()
    elif game.state == STATE_LEVEL_COMPLETE:
        game.draw_level_complete()
# Tambah petunjuk restart
        restart_text = font_small.render("Press R to restart level", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH - restart_text.get_width() - 10, 10))
    elif game.state == STATE_GAME_OVER:
        game.draw_game_over()
    elif game.state == STATE_LEVEL_COMPLETE:
        game.draw_level_complete()
    pygame.display.update()
    clock.tick(FPS)
