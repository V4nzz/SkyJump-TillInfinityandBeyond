from PIL import Image
import pygame
import random
import sys
import time
import pygame.image


# Initialize pygame
pygame.init()
pygame.mixer.init()

# Ukuran layar game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Membuat jendela game dengan ukuran yang sudah ditentukan
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Froggie Jump")

# Warna yang digunakan dalam RGB
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

# Status game yang memungkinkan pengaturan kondisi game saat ini
STATE_MENU = 0              # Tampilan menu utama
STATE_GAME = 1              # Game sedang berlangsung
STATE_LEVEL_SELECT = 2      # Menu Pemilihan level
STATE_GAME_OVER = 3         # Kondisi game over
STATE_LEVEL_COMPLETE = 4    # Kondisi saat level selesai
STATE_COUNTDOWN = 5         # Countdown sebelum memulai level

# Pengaturan font dengan berbagai ukuran
font_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Clock untuk mengatur frame per second (FPS)
clock = pygame.time.Clock()
FPS = 60

# Pengaturan player
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
JUMP_SPEED = -15    # Kecepatan lompatan (negatif karena koordinat y ke bawah)
MOVE_SPEED = 5      # Kecepatan gerak horizontal player
GRAVITY = 0.3       # Percepatan jatuh ke bawah

# Pengaturan platform
PLATFORM_WIDTH = 50
PLATFORM_HEIGHT = 50
PLATFORM_SPEED = 2      # Kecepatan platform bergerak (untuk platform moving)
TRAMPOLINE_BOOST = -20  # Kecepatan lompatan dari trampoline (lebih kuat)
MAX_PLATFORM_GAP = 80  # Jarak vertikal maksimum antar platform agar terjangkau

# Variabel untuk tracking progres game
max_level_unlocked = 4      # Level tertinggi yang sudah terbuka
current_level = 1           # Level saat ini yang dimainkan
score = 0                   # Skor pemain saat ini
high_scores = [0, 0, 0, 0]  # High score untuk tiap level

# Skor yang dibutuhkan untuk menyelesaikan level
SCORE_TO_COMPLETE = 1000
SCORE_PER_PLATFORM = 100

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

# Load asset gambar dan sprite sheet dari folder
sprite_sheet1 = pygame.image.load("E:/vscode/TUBES PBO GACOR/tiles_page1.png").convert_alpha()
sprite_sheet2 = pygame.image.load("E:/vscode/TUBES PBO GACOR/tiles_page3.png").convert_alpha()
sprite_sheet3 = pygame.image.load("E:/vscode/TUBES PBO GACOR/tiles_page7.png").convert_alpha()
sprite_sheet4 = pygame.image.load("E:/vscode/TUBES PBO GACOR/tiles_page13.png").convert_alpha()
sprite_sheet5 = pygame.image.load("E:/vscode/TUBES PBO GACOR/tiles_page6.png").convert_alpha()
play_button_img = pygame.image.load("E:/vscode/TUBES PBO GACOR/play button2.png").convert_alpha()
level_select_button_img = pygame.image.load("E:/vscode/TUBES PBO GACOR/select lvl button4.png").convert_alpha()
quit_button_img = pygame.image.load("E:/vscode/TUBES PBO GACOR/quit button2.png").convert_alpha()
level_select_bg = pygame.image.load("E:/vscode/TUBES PBO GACOR/select lvl menu.png").convert_alpha()
level_button_imgs = [
    pygame.image.load("E:/vscode/TUBES PBO GACOR/lvl 1 button2.png").convert_alpha(),
    pygame.image.load("E:/vscode/TUBES PBO GACOR/lvl 2 button2.png").convert_alpha(),
    pygame.image.load("E:/vscode/TUBES PBO GACOR/lvl 3 button2.png").convert_alpha(),
    pygame.image.load("E:/vscode/TUBES PBO GACOR/lvl 4 button2.png").convert_alpha()
]
back_button_img = pygame.image.load("E:/vscode/TUBES PBO GACOR/back button2.png").convert_alpha()

#Ukuran Tile
TILE_WIDTH = 32
TILE_HEIGHT = 32

sprite_sheet6 = pygame.image.load("E:/vscode/TUBES PBO GACOR/green_frog_spritesheet_.png").convert_alpha()
frame_width = 60
frame_height = 64
rect = pygame.Rect(0, 0, frame_width, frame_height)
player_image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
player_image.blit(sprite_sheet6, (0, 0), rect)

scale_factor = 1.5
new_size = (int(frame_width * scale_factor), int(frame_height * scale_factor))
player_image = pygame.transform.scale(player_image, new_size)

def load_gif(filename):
    gif = Image.open(filename)
    frames = []

    while True:
        frame = gif.convert("RGBA")
        size = frame.size
        data = frame.tobytes()
        frame = pygame.image.fromstring(data, size, "RGBA").convert_alpha()
        frames.append(frame)
        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break
    return frames

menu_gif_frames = load_gif("E:/vscode/TUBES PBO GACOR/main menu.gif")
menu_current_frame = 0
gif_frames = load_gif("E:/vscode/TUBES PBO GACOR/bumi yg cerah.gif")
current_frame = 0
bg_level2 = pygame.image.load("E:/vscode/TUBES PBO GACOR/bg salju1.png").convert_alpha()
bg_level3 = pygame.image.load("E:/vscode/TUBES PBO GACOR/bg angkasa1.png").convert_alpha()
bg_level4 = pygame.image.load("E:/vscode/TUBES PBO GACOR/bg hutan1.png").convert_alpha()
bg_complete = load_gif("E:/vscode/TUBES PBO GACOR/complete2.gif")
complete_current_frame = 0
bg_gameover = load_gif("E:/vscode/TUBES PBO GACOR/game over.gif")
gameover_current_frame = 0

# Fungsi untuk mengambil gambar tile dari sprite sheet berdasarkan koordinat grid
def get_tile(x, y, sheet=1):
    if sheet == 1:
        sheet_img = sprite_sheet1
    elif sheet == 2:
        sheet_img = sprite_sheet2
    elif sheet == 3:
        sheet_img = sprite_sheet3
    elif sheet == 4:
        sheet_img = sprite_sheet4
    elif sheet == 5:
        sheet_img = sprite_sheet5

    rect = pygame.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
    tile = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
    tile.blit(sheet_img, (0, 0), rect)
    return tile

# Player class
class Player(pygame.sprite.Sprite):
    """
    Kelas yang merepresentasikan karakter pemain.
    Bertugas meng-handle pergerakan, gravitasi, lompatan, dan interaksi dengan platform.
    """
    def __init__(self):
        super().__init__()
        self.current_frame = 0
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

        self.velocity_y = 0
        self.is_jumping = False
        self.stuck_timer = 0
        self.platforms_touched = set()
        self.on_platform = False

    def update(self, platforms):
        """
        Update posisi pemain setiap frame:
        - Cek input keyboard (kiri, kanan)
        - Terapkan gravitasi
        - Deteksi tabrakan dengan platform
        - Tangani lompatan dan platform khusus (trampoline, fragile)
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += MOVE_SPEED
        
        # Batas gerak horizontal agar tidak keluar layar
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Terapkan gravitasi ke kecepatan vertikal dan update posisi y
        self.velocity_y += GRAVITY
        previous_bottom = self.rect.bottom
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

        # Deteksi tabrakan dengan platform saat jatuh
        for platform in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0 and previous_bottom <= platform.rect.top and self.rect.bottom >= platform.rect.top:
                self.rect.bottom = platform.rect.top
                # Lompatan trampoline lebih tinggi
                if platform.platform_type == "trampoline":
                    self.velocity_y = TRAMPOLINE_BOOST
                else:
                    self.velocity_y = JUMP_SPEED

                # Jika platform rapuh, trigger break
                if platform.platform_type == "fragile":
                    platform.break_platform()
                
                # Tambah skor jika platform baru disentuh
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
        """
        Cari platform terdekat yang berada di atas pemain.
        Digunakan untuk reset posisi jika pemain stuck.
        """
        closest_platform = None
        closest_distance = float('inf')
        for platform in platforms:
            # Hanya pertimbangkan platform yang ada di atas pemain
            if platform.rect.bottom < self.rect.top:
                distance = self.rect.top - platform.rect.bottom
                if distance < closest_distance:
                    closest_distance = distance
                    closest_platform = platform
        return 
    
def load_sprite_sheet(filename, frame_width, frame_height):
    sprite_sheet = pygame.image.load(filename).convert_alpha()
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()

    for y in range (0, sheet_height, frame_height):
        for x in range (0, sheet_width, frame_width):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), (x, y, frame_width, frame_height))
            frames.append(frame)

    return frames

# Platform class
class Platform(pygame.sprite.Sprite):
    """
    Kelas platform yang bisa berjenis normal, trampoline, fragile, moving.
    Masing-masing platform memiliki perilaku dan gambar tersendiri.
    """
    next_id = 0 # ID unik untuk setiap platform
    def __init__(self, x, y, platform_type="normal", direction=1, level=1):
        super().__init__()
        self.platform_type = platform_type
        self.level = level
        self.id = Platform.next_id
        Platform.next_id += 1

        # Load gambar tile berdasarkan tipe platform dan level
        # Contoh: platform normal level 1 mengambil tile dari sprite_sheet1 koordinat (28, 15)
        # dst ...
        if platform_type == "normal":
            if self.level == 1:
                self.image = get_tile(28, 15, sheet=1)
                self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
                self.rect = self.image.get_rect(topleft=(x, y))
            elif self.level == 2:
                self.image = get_tile(31, 0, sheet=4)
                self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
                self.rect = self.image.get_rect(topleft=(x, y))
            elif self.level == 3:
                self.image = get_tile(2, 12, sheet=3)
                self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
                self.rect = self.image.get_rect(topleft=(x, y))
            elif self.level == 4:
                self.image = get_tile(9, 4, sheet=5)
                self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
                self.rect = self.image.get_rect(topleft=(x, y))
        elif platform_type == "trampoline":
            self.image = get_tile(29, 7, sheet=1)
            self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.rect = self.image.get_rect(topleft=(x, y))
        elif platform_type == "fragile":
            if self.level == 2:
                self.image = get_tile(11, 8, sheet=2)
                self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
                self.rect = self.image.get_rect(topleft=(x, y))
            elif self.level == 4:
                self.image = get_tile(5, 4, sheet=5)
                self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
                self.rect = self.image.get_rect(topleft=(x, y))
        elif platform_type == "moving":
            if self.level == 3:
                self.image = get_tile(2, 12, sheet=3)
                self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
                self.rect = self.image.get_rect(topleft=(x, y))
            elif self.level == 4:
                self.image = get_tile(9, 4, sheet=5)
                self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
                self.rect = self.image.get_rect(topleft=(x, y))

        self.move_direction = direction     # Arah gerak platform moving
        self.move_counter = 0               # Counter untuk pergerakan platform
        self.move_limit = 100               # Batas pergerakan sebelum balik arah
        self.to_remove = False              # Flag untuk menghapus platform (rapuh yang pecah)
        self.break_timer = 0                # Timer pecah platform rapuh

    def update(self):
        """
        Update posisi platform moving dan handle timer pecah platform fragile.
        """
        if self.platform_type == "moving":
            self.move_counter += 1
            self.rect.x += self.move_direction * PLATFORM_SPEED
            
            # Balik arah jika sudah mencapai batas gerak
            if self.move_counter >= self.move_limit:
                self.move_direction *= -1
                self.move_counter = 0
            
            # Batas gerak agar platform tidak keluar layar
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                self.move_direction *= -1
            if self.rect.left < 0:
                self.rect.left = 0
                self.move_direction *= -1

        # Jika platform rapuh sedang pecah, hitung timer
        if self.break_timer > 0:
            self.break_timer -= 1
            if self.break_timer <= 0:
                self.to_remove = True

    def break_platform(self):
        """
        Mulai proses pecah platform rapuh.
        """
        if self.platform_type == "fragile":
            self.break_timer = 1 

# Raindrop class for forest level
class Raindrop(pygame.sprite.Sprite):
    """
    Efek hujan berupa tetesan air yang jatuh secara acak.
    """
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
    """
    Kelas utama pengatur game, termasuk state management, update, dan render.
    """
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
        self.back_button_img = back_button_img
        self.menu_music_file = "E:/vscode/TUBES PBO GACOR/sound menu.mp3"
        self.level_music_files = [
            "E:/vscode/TUBES PBO GACOR/level1_music.mp3",
            "E:/vscode/TUBES PBO GACOR/level2_music.mp3",
            "E:/vscode/TUBES PBO GACOR/level3_music.mp3",
            "E:/vscode/TUBES PBO GACOR/level4_music.mp3"
        ]
        self.current_music = None

    def play_music_for_state(self):
        if self.state == STATE_MENU or self.state == STATE_LEVEL_SELECT:
            music_file = self.menu_music_file
        elif self.state == STATE_GAME or STATE_COUNTDOWN:
            music_file = self.level_music_files[self.level - 1]
        else:
            music_file = None
            

        if music_file and music_file != self.current_music:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.current_music = music_file
        elif music_file is None:
            pygame.mixer.music.stop()
            self.current_music = None

    def reset_game(self):
        """
        Reset data game saat memulai level baru.
        """
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

        # Untuk level hutan (4), buat efek hujan
        if self.level == 4:
            for _ in range(50):
                self.raindrops.add(Raindrop())

    def start_level(self, level):
        """
        Mulai level baru dengan reset game dan set state countdown.
        """
        global current_level
        current_level = level
        self.level = level
        self.state = STATE_COUNTDOWN
        self.countdown_timer = 3
        self.last_countdown_time = time.time()
        self.reset_game()

    def generate_platforms(self):
        """
        Buat platform-platform awal dengan jarak yang sesuai agar bisa dilompati.
        """
        self.platforms.empty()
        # Platform awal
        self.platforms.add(Platform(SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, SCREEN_HEIGHT - 50, "normal", level=self.level))
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
            
            # Posisi x dengan distribusi merata horizontal
            section_width = SCREEN_WIDTH // 3
            section = i % 3  # 0, 1, atau 2 untuk distribusi platform yang lebih merata
            x = random.randint(section * section_width, (section + 1) * section_width - PLATFORM_WIDTH)
            
            # Koreksi posisi agar tidak terlalu ke pinggir
            if x < 50:
                x = 50
            elif x > SCREEN_WIDTH - PLATFORM_WIDTH - 50:
                x = SCREEN_WIDTH - PLATFORM_WIDTH - 50
            
            # Pilih tipe platform berdasarkan level
            if self.level == 1:
                platform_type = "trampoline" if random.random() < 0.2 else "normal"
                self.platforms.add(Platform(x, y, platform_type))
            elif self.level == 2:
                platform_type = "fragile" if self.level == 2 and random.random() < 0.4 else "normal"
                self.platforms.add(Platform(x, y, platform_type, level=self.level))
            elif self.level == 3:
                platform_type = "moving"
                direction = 1 if random.random() < 0.5 else -1
                self.platforms.add(Platform(x, y, platform_type, direction, level=self.level))
            elif self.level == 4:
                r = random.random()
                if r < 0.3:
                    platform_type = "fragile"
                elif r < 0.7:
                    platform_type = "moving"
                    direction = 1 if random.random() < 0.5 else -1
                    self.platforms.add(Platform(x, y, platform_type, direction, level=self.level))
                    continue
                else:
                    platform_type = "normal"
                self.platforms.add(Platform(x, y, platform_type, level=self.level))
            self.highest_point = y

    def add_platforms(self):
        """
        Tambah platform secara dinamis jika pemain naik terus (scrolling).
        """
        # Logika mirip dengan generate_platforms, namun jumlah lebih sedikit (10)
        # dan dipicu ketika kamera sudah mencapai batas platform yang ada
        # dst ...
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
                    self.platforms.add(Platform(x, y, platform_type, level = self.level))
                elif self.level == 3:
                    platform_type = "moving"
                    direction = 1 if random.random() < 0.5 else -1
                    self.platforms.add(Platform(x, y, platform_type, direction, self.level))
                elif self.level == 4:
                    r = random.random()
                    if r < 0.3:
                        platform_type = "fragile"
                    elif r < 0.7:
                        platform_type = "moving"
                        direction = 1 if random.random() < 0.5 else -1
                        self.platforms.add(Platform(x, y, platform_type, direction, level = self.level))
                        continue
                    else:
                        platform_type = "normal"
                    self.platforms.add(Platform(x, y, platform_type, level=self.level))
                self.highest_point = y

    def update(self):
        """
        Update game setiap frame berdasarkan state saat ini.
        """
        self.play_music_for_state()
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

            # Hapus platform yang sudah pecah
            for platform in list(self.platforms):
                if platform.to_remove:
                    self.platforms.remove(platform)
                    if platform in self.emergency_platforms:
                        self.emergency_platforms.remove(platform)

            # Scroll layar jika pemain naik melewati threshold            
            if self.player.rect.top < self.scroll_threshold and self.player.velocity_y < 0:
                self.camera_offset += abs(self.player.velocity_y)
                self.player.rect.y += abs(self.player.velocity_y)
                for platform in self.platforms:
                    platform.rect.y += abs(self.player.velocity_y)
                for raindrop in self.raindrops:
                    raindrop.rect.y += abs(self.player.velocity_y)
                    
            self.player.update(self.platforms)

             # Jika pemain jatuh melewati bawah layar, game over
            if self.player.rect.top > SCREEN_HEIGHT:
                self.state = STATE_GAME_OVER
            self.add_platforms()
            
            # Logika hujan dan petir untuk level 4
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
                        self.lightning_flash_timer = FPS * 2
                        self.lightning_warning = False
                        self.lightning_cycle_timer = 0
                if self.lightning_flash:
                    self.lightning_flash_timer -= 1
                    if self.lightning_flash_timer <= 0:
                        self.lightning_flash = False
                        
            # Buffer game over sedikit lebih longgar
            if self.player.rect.top > SCREEN_HEIGHT + 150:
                self.state = STATE_GAME_OVER

    # Fungsi-fungsi draw untuk menggambar ke layar sesuai state game
    def draw_menu(self):
        screen.blit(menu_gif_frames[menu_current_frame], (0, 0))
        play_pos = (300, 310)
        level_select_pos = (300, 200)
        quit_pos = (300, 390)
        screen.blit(play_button_img, play_pos)
        screen.blit(level_select_button_img, level_select_pos)
        screen.blit(quit_button_img, quit_pos)
        self.buttons = [
            {"rect": pygame.Rect(play_pos, play_button_img.get_size()), "action": "play"},
            {"rect": pygame.Rect(level_select_pos, level_select_button_img.get_size()), "action": "level_select"},
            {"rect": pygame.Rect(quit_pos, quit_button_img.get_size()), "action": "quit"}
        ]

    def draw_level_select(self):
        screen.blit(level_select_bg, (0, 0))
        self.level_buttons = []
        button_width, button_height = level_button_imgs[0].get_size()
        margin = 20
        start_x = (SCREEN_WIDTH - (4*(button_width + margin))) // 2
        y = 150
        for i in range(4):
            x = start_x + i*(button_width + margin)
            rect = pygame.Rect(x, y, button_width, button_height)
            unlocked = (i + 1) <= max_level_unlocked
        #    color_filter = (255, 255, 255) if unlocked else (100, 100, 100)
            btn_img = level_button_imgs[i].copy()
            if not unlocked:
                dark_surface = pygame.Surface(btn_img.get_size()).convert_alpha()
                dark_surface.fill ((0, 0, 0, 150))
                btn_img.blit(dark_surface, (0, 0))

            screen.blit(btn_img, (x, y))

            self.level_buttons.append({
                "rect": rect,
                "level": i + 1,
                "unlocked": unlocked
            })

        # Gambar tombol back dengan gambar baru
        self.back_rect = pygame.Rect(20, 500, back_button_img.get_width(), back_button_img.get_height())
        screen.blit(self.back_button_img, (self.back_rect.x, self.back_rect.y))

    def draw_game(self):
        if self.level == 1:
            screen.fill((0, 0, 0))
            screen.blit(gif_frames[current_frame], (0, 0))
        elif self.level == 2:
            screen.fill((0, 0, 0))
            screen.blit(bg_level2, (0, 0))
        elif self.level == 3:
            screen.fill((0, 0, 0))
            screen.blit(bg_level3, (0, 0))
        elif self.level == 4:
            screen.fill((0, 0, 0))
            screen.blit(bg_level4, (0, 0))
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
        if self.level == 1:
            screen.blit(gif_frames[current_frame], (0, 0))
        elif self.level == 2:
            screen.fill((0, 0, 0))
            screen.blit(bg_level2, (0, 0))
        elif self.level == 3:
            screen.fill((0, 0, 0))
            screen.blit(bg_level3, (0, 0))
        elif self.level == 4:
            screen.fill((0, 0, 0))
            screen.blit(bg_level4, (0, 0))
        countdown_text = font_large.render(str(self.countdown_timer) if self.countdown_timer > 0 else "GO!", True, WHITE)
        screen.blit(countdown_text, (SCREEN_WIDTH//2 - countdown_text.get_width()//2, SCREEN_HEIGHT//2 - countdown_text.get_height()//2))

    def draw_game_over(self):
        screen.fill((0, 0, 0))
        screen.blit(bg_gameover[gameover_current_frame], (0, 0))
        score_text = font_medium.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 275))

    def draw_level_complete(self):
        screen.fill((0, 0, 0))
        screen.blit(bg_complete[complete_current_frame], (0, 0))
        score_text = font_medium.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 300))

    def handle_input(self, event):
        """
        Menangani input keyboard dan mouse sesuai state game saat ini.
        """
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
                if self.back_rect.collidepoint(pos):
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
animation_speed = 5
frame_counter = 0
menu_frame_delay = 5
menu_frame_counter = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_input(event)
    game.update()
    if game.level == 1:
        frame_counter += 1
        if frame_counter >= animation_speed:
            current_frame = (current_frame + 1) % len(gif_frames)
            frame_counter = 0
    if game.state == STATE_MENU:
        menu_frame_counter += 1
        if menu_frame_counter >= menu_frame_delay:
            menu_current_frame = (menu_current_frame + 1) % len(menu_gif_frames)
            menu_frame_counter = 0
        game.draw_menu()
    elif game.state == STATE_LEVEL_SELECT:
        game.draw_level_select()
    elif game.state == STATE_COUNTDOWN:
        game.draw_countdown()
    elif game.state == STATE_GAME:
        game.draw_game()
        # Tambah petunjuk restart
        restart_text = font_small.render("Press R to restart level", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30))
    elif game.state == STATE_GAME_OVER:
        frame_counter += 1
        if frame_counter >= animation_speed:
            gameover_current_frame = (gameover_current_frame + 1) % len(gif_frames)
            frame_counter = 0
        game.draw_game_over()
    elif game.state == STATE_LEVEL_COMPLETE:
        frame_counter += 1
        if frame_counter >= animation_speed:
            complete_current_frame = (complete_current_frame + 1) % len(gif_frames)
            frame_counter = 0
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