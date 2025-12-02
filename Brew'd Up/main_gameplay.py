#=====================#
# Brew'd Up - Main Gameplay Module
#=====================#
import pygame
import math
import json
import os

#=====================#
# Initialize Pygame #
#=====================#
pygame.init()

# ======================#
# Setup Display #
# ======================#
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brew'd Up")
icon  = pygame.image.load('Graphics/logo.png')
pygame.display.set_icon(icon)

# Fallback if image is missing, create a simple background
try:
    background = pygame.image.load('Graphics/main background.png').convert()
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((255, 231, 184)) # Beige background

# ======================#
# Notification System  #
# ======================#
class NotificationSystem:
    def __init__(self):
        self.messages = []
        self.font = pygame.font.SysFont('comicsans', 24)
        
    def add(self, text, color=(0, 0, 0)):
        # Add message with a timer (120 frames = ~2 seconds)
        self.messages.append({
            'text': text,
            'color': color,
            'timer': 120 
        })
        # Keep only last 5 messages to prevent clutter
        if len(self.messages) > 5:
            self.messages.pop(0)
            
    def update(self):
        # Decrease timer
        for msg in self.messages:
            msg['timer'] -= 1
        # Remove expired messages
        self.messages = [m for m in self.messages if m['timer'] > 0]
        
    def draw(self, surface):
        # Start drawing from bottom center
        start_y = HEIGHT - 80
        
        # Iterate backwards so newest is at the bottom
        for i, msg in enumerate(reversed(self.messages)):
            # Render Text
            text_surf = self.font.render(msg['text'], True, msg['color'])
            
            # Create a box behind the text
            bg_rect = text_surf.get_rect(center=(WIDTH // 2, start_y - (i * 45)))
            bg_rect.inflate_ip(30, 14) # Make box slightly larger than text
            
            # Draw Box (White with Black Border)
            pygame.draw.rect(surface, (250, 250, 250), bg_rect, border_radius=10)
            pygame.draw.rect(surface, (61, 40, 30), bg_rect, 2, border_radius=10)
            
            # Draw Text
            text_rect = text_surf.get_rect(center=bg_rect.center)
            surface.blit(text_surf, text_rect)

# Initialize Notifications
notifications = NotificationSystem()

# ======================#
# Save/Load System #
# ======================#
SAVE_FILE = "game_save.json"

def save_game(game_state_obj):
    """Save game progress to JSON file."""
    save_data = {
        "money": game_state_obj.money,
        "owned_shop_items": game_state_obj.owned_shop_items,
        "current_machine_tier": game_state_obj.current_machine_tier,
        "upgrade_levels": game_state_obj.upgrade_levels
    }
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(save_data, f, indent=4)
        print(f"Game saved to {SAVE_FILE}")
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def load_game():
    """Load game progress from JSON file. Returns data dict or None if no save exists."""
    if not os.path.exists(SAVE_FILE):
        print(f"No save file found at {SAVE_FILE}. Starting new game.")
        return None
    try:
        with open(SAVE_FILE, 'r') as f:
            save_data = json.load(f)
        print(f"Game loaded from {SAVE_FILE}")
        return save_data
    except Exception as e:
        print(f"Error loading game: {e}")
        return None

# ======================#
# Game State Class #
# ======================#
class GameState:
    def __init__(self, load_save=True):
        # Try to load saved game if requested
        save_data = load_game() if load_save else None
        
        if save_data:
            # Load from save file
            self.money = save_data.get("money", 305.00)
            self.owned_shop_items = save_data.get("owned_shop_items", {
                "coffee_beans": False,
                "advertise": False,
                "repair_kit": False
            })
            self.current_machine_tier = save_data.get("current_machine_tier", None)
            self.upgrade_levels = save_data.get("upgrade_levels", {
                "beans": 0,
                "advertising": 0,
                "decoration": 0,
                "shop": 0,
                "branches": 0
            })
        else:
            # New game defaults
            self.money = 305.00
            self.owned_shop_items = {
                "coffee_beans": False,
                "advertise": False,
                "repair_kit": False
            }
            self.current_machine_tier = None
            self.upgrade_levels = {
                "beans": 0,
                "advertising": 0,
                "decoration": 0,
                "shop": 0,
                "branches": 0
            }
        
        # --- CONFIGURATION: VALUES ---
        self.BASE_TAP_VALUE = 0.10
        
        self.SHOP_BONUSES = {
            "coffee_beans": 0.10,
            "advertise": 0.05,
            "repair_kit": 0.00 
        }
        
        self.MACHINE_VALUES = {
            None: 0.00,
            "basic": 0.05,
            "advanced": 0.15,
            "pro": 0.30,
            "master": 0.50
        }
        
        self.UPGRADE_BONUSES = {
            "beans": 0.10,
            "advertising": 0.05,
            "decoration": 0.02,
            "shop": 0.20,
            "branches": 1.00
        }

    def calculate_income_per_tap(self):
        total = self.BASE_TAP_VALUE
        for item, is_owned in self.owned_shop_items.items():
            if is_owned:
                total += self.SHOP_BONUSES.get(item, 0.0)

        if self.current_machine_tier:
            total += self.MACHINE_VALUES.get(self.current_machine_tier, 0.0)

        for upgrade_name, level in self.upgrade_levels.items():
            bonus_per_level = self.UPGRADE_BONUSES.get(upgrade_name, 0.0)
            total += (level * bonus_per_level)

        return round(total, 2)

    # --- ACTION METHODS ---
    def tap(self):
        income = self.calculate_income_per_tap()
        self.money += income
        self.money = round(self.money, 2)
        return income

    def buy_shop_item(self, item_key, cost):
        # Check if already owned (except actions like advertise if you want them repeatable, 
        # but your code treats advertise as one-time here based on logic)
        if self.owned_shop_items.get(item_key):
             return "owned"
             
        if self.money >= cost:
            self.money -= cost
            self.owned_shop_items[item_key] = True
            return "success"
        return "poor"

    def buy_upgrade(self, upgrade_key, cost):
        if self.money >= cost:
            self.money -= cost
            self.upgrade_levels[upgrade_key] += 1
            return "success"
        return "poor"
        
    def buy_machine(self, tier_key, cost):
        # Prevent buying the same active machine repeatedly
        if self.current_machine_tier == tier_key:
            return "owned"
        if self.money >= cost:
            self.money -= cost
            self.current_machine_tier = tier_key
            return "success"
        return "poor"
    
    def save(self):
        """Save current game state to file."""
        return save_game(self)

# Initialize Game State (will load from save if exists)
game_state_obj = GameState(load_save=True)
if game_state_obj.money > 305.00 or any(game_state_obj.owned_shop_items.values()) or game_state_obj.current_machine_tier or any(game_state_obj.upgrade_levels.values()):
    notifications.add("Progress loaded!", (0, 100, 0))

# ======================#
# Assets & UI Setup #
# ======================#
money = game_state_obj.money
font_text = pygame.font.SysFont('comicsans', 30)

level = 1
font_level = pygame.font.SysFont('comicsans', 30)
level_text = font_level.render(f'Level: {level}', True, (0, 0, 0))
level_rect = level_text.get_rect(topright=(WIDTH - 20, 20))

# Helper to load images safely
def load_icon(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except:
        s = pygame.Surface((50, 50))
        s.fill((100, 100, 100))
        return s

shop_button_img = load_icon('Graphics/Shop button.png')
settings_button_img = load_icon('Graphics/Settings button.png')
upgrade_button_img = load_icon('Graphics/Upgrade button.png')
branches_button_img = load_icon('Graphics/Branches button.png')

class ButtonIcon:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topright=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

shop_button = ButtonIcon(WIDTH - 20, 70, shop_button_img)
settings_button = ButtonIcon(WIDTH - 20, 140, settings_button_img)
upgrade_button = ButtonIcon(WIDTH - 20, 210, upgrade_button_img)
branches_button = ButtonIcon(WIDTH - 20, 280, branches_button_img)

# ... [Slider, Checkbox, Button Classes omitted for brevity, they are unchanged] ...
# Re-including them for a complete file run:
class Slider:
    def __init__(self, x, y, width, label, initial=0.5):
        self.x, self.y, self.width = x, y, width
        self.height, self.radius = 6, 10
        self.value, self.dragging = initial, False
        self.label = label
        self.font = pygame.font.SysFont('comicsans', 28)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.handle_x) < 15 and abs(event.pos[1] - self.y) < 15:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.value = max(0, min(1, (event.pos[0] - self.x) / self.width))
    @property
    def handle_x(self): return int(self.x + self.value * self.width)
    def draw(self, surface):
        pygame.draw.rect(surface, (176, 138, 99), (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, (107, 78, 55), (self.handle_x, self.y + self.height // 2), self.radius)
        txt = self.font.render(f"{self.label}: {int(self.value * 100)}%", True, (61, 40, 30))
        surface.blit(txt, (self.x, self.y - 30))

class Checkbox:
    def __init__(self, x, y, label, checked=False):
        self.x, self.y, self.size = x, y, 28
        self.checked, self.label = checked, label
        self.font = pygame.font.SysFont('comicsans', 28)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.x, self.y, self.size, self.size).collidepoint(event.pos):
                self.checked = not self.checked
    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surface, (61, 40, 30), rect, 3)
        if self.checked: pygame.draw.rect(surface, (107, 78, 55), rect.inflate(-6, -6))
        surface.blit(self.font.render(self.label, True, (61, 40, 30)), (self.x + self.size + 12, self.y - 2))

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('comicsans', 32)
    def draw(self, surface, mouse_pos):
        color = (176, 138, 99) if self.rect.collidepoint(mouse_pos) else (192, 160, 121)
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        label = self.font.render(self.text, True, (61, 40, 30))
        surface.blit(label, (self.rect.centerx - label.get_width()//2, self.rect.centery - label.get_height()//2))
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

class ShopButton:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = pygame.font.SysFont("comicsans", 28)
    def draw(self, surface, mouse_pos):
        color = (176, 138, 99) if self.rect.collidepoint(mouse_pos) else (192, 160, 121)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        label = self.font.render(self.text, True, (61, 40, 30))
        surface.blit(label, (self.rect.centerx - label.get_width()//2, self.rect.centery - label.get_height()//2))
    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

# ======================#
# Settings Elements #
# ======================#
settings_title_font = pygame.font.SysFont('comicsans', 90)
footer_font = pygame.font.SysFont('comicsans', 24)
music_slider = Slider(450, 250, 400, "Music Volume", 0.5)
sfx_slider = Slider(450, 350, 400, "SFX Volume", 0.5)
mute_checkbox = Checkbox(450, 450, "Mute All Sound", False)
apply_button = Button(WIDTH // 2 - 80, 550, 160, 50, "Apply")

# ======================#
# Data #
# ======================#
shop_items = [
    {"name": "Coffee Beans", "price": 430, "info": "Better beans allow you to earn more money.", "type": "buy", "key": "coffee_beans"},
    {"name": "Advertise", "price": 90, "info": "Spend money to boost income permanently.", "type": "action", "key": "advertise"},
    {"name": "Machines", "price": None, "info": "Open machine tiers to buy machines of different quality.", "type": "machine"},
    {"name": "Repair Toolkit", "price": 100, "info": "Automatically repairs a broken machine when it breaks.", "type": "buy", "key": "repair_kit"},
]
upgrade_items = [
    {"name": "Beans", "info": "+0.10 per tap per bean upgrade", "cost": 200, "key": "beans"},
    {"name": "Advertising", "info": "+0.05 per tap per advertising upgrade", "cost": 150, "key": "advertising"},
    {"name": "Decoration", "info": "+0.02 per tap per decoration upgrade", "cost": 100, "key": "decoration"},
    {"name": "Shop", "info": "+0.20 per tap per shop upgrade", "cost": 300, "key": "shop"},
    {"name": "Branches", "info": "+1 tap per branch upgrade", "cost": 700, "key": "branches"},
]
machine_tiers = [
    {"tier": "Basic Machine", "price": 100, "info": "Standard machine. Decent speed. Higher break chance.", "key": "basic"},
    {"tier": "Advanced Machine", "price": 300, "info": "Better performance and lower break chance.", "key": "advanced"},
    {"tier": "Pro Machine", "price": 700, "info": "Very fast and rarely breaks.", "key": "pro"},
    {"tier": "Master Machine", "price": 1200, "info": "Top-tier performance with almost no downtime.", "key": "master"},
]
branches_tiers = [
    {"tier": "Local Branch", "price": 500, "info": "A small local branch to increase your reach."},
    {"tier": "City Branch", "price": 1500, "info": "A bustling city branch to maximize exposure."},
    {"tier": "National Branch", "price": 3000, "info": "A nationwide branch to dominate the market."},
]

shop_buttons, upgrade_buttons, tier_buttons, branches_tier_buttons = [], [], [], []

def create_branches_tier_buttons():
    global branches_tier_buttons
    branches_tier_buttons = []
    start_x, start_y = 160, 200
    for i, tier in enumerate(branches_tiers):
        y = start_y + i * 90
        branches_tier_buttons.append({
            "info": ShopButton((start_x + 400, y, 120, 60), "INFO"),
            "buy": ShopButton((start_x + 550, y, 120, 60), "BUY")
        })

def create_shop_buttons():
    global shop_buttons
    shop_buttons = []
    start_x, start_y = 200, 180
    col_width = 300
    for i, item in enumerate(shop_items):
        y = start_y + i * 90
        action_text = "BUY" if item["type"] in ["buy", "machine"] else "DO"
        shop_buttons.append({
            "info": ShopButton((start_x + col_width, y, 120, 60), "INFO"),
            "action": ShopButton((start_x + col_width * 2, y, 120, 60), action_text)
        })

def create_upgrade_buttons():
    global upgrade_buttons
    upgrade_buttons = []
    start_x, start_y = 200, 180
    col_width = 300
    for i, item in enumerate(upgrade_items):
        y = start_y + i * 90
        upgrade_buttons.append({
            "info": ShopButton((start_x + col_width, y, 120, 60), "INFO"),
            "buy": ShopButton((start_x + col_width * 2, y, 120, 60), "BUY")
        })

def create_machine_tier_buttons():
    global tier_buttons
    tier_buttons = []
    start_x, start_y = 160, 200
    for i, tier in enumerate(machine_tiers):
        y = start_y + i * 90
        tier_buttons.append({
            "info": ShopButton((start_x + 400, y, 120, 60), "INFO"),
            "buy": ShopButton((start_x + 550, y, 120, 60), "BUY")
        })

create_shop_buttons()
create_upgrade_buttons()
create_branches_tier_buttons()
create_machine_tier_buttons()  

# ======================#
# Draw Functions #
# ======================#
def draw_info_screen(surface, title_txt, info_txt):
    surface.fill((255, 231, 184))
    title = settings_title_font.render(title_txt, True, (61, 40, 30))
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    for i, line in enumerate(info_txt.split("\n")):
        line_text = footer_font.render(line, True, (61, 40, 30))
        surface.blit(line_text, (WIDTH//2 - line_text.get_width()//2, 220 + i*30))
    back = footer_font.render("Press SPACE to return", True, (61, 40, 30))
    surface.blit(back, (WIDTH//2 - back.get_width()//2, HEIGHT - 60))

def draw_shop_window(surface, mouse_pos):
    surface.fill((255, 231, 184))
    title = settings_title_font.render("Shop", True, (61, 40, 30))
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    for i, item in enumerate(shop_items):
        y = 180 + i * 90
        price_text = f"${item['price']}" if item.get("price") else ""
        surface.blit(font_text.render(f"{item['name']} {price_text}", True, (61, 40, 30)), (200, y + 15))
        shop_buttons[i]["info"].draw(surface, mouse_pos)
        shop_buttons[i]["action"].draw(surface, mouse_pos)
    surface.blit(footer_font.render("Press SPACE to return", True, (61, 40, 30)), (WIDTH//2 - 100, HEIGHT - 60))

def draw_upgrade_window(surface, mouse_pos):
    surface.fill((255, 231, 184))
    title = settings_title_font.render("Upgrade Shop", True, (61, 40, 30))
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    for i, item in enumerate(upgrade_items):
        y = 180 + i * 90
        level = game_state_obj.upgrade_levels.get(item['key'], 0)
        surface.blit(font_text.render(f"{item['name']} - ${item['cost']}   |   Level {level}", True, (61, 40, 30)), (200, y + 15))
        upgrade_buttons[i]["info"].draw(surface, mouse_pos)
        upgrade_buttons[i]["buy"].draw(surface, mouse_pos)
    surface.blit(footer_font.render("Press SPACE to return", True, (61, 40, 30)), (WIDTH//2 - 100, HEIGHT - 60))

def draw_machine_tiers(surface, mouse_pos):
    surface.fill((255, 231, 184))
    title = settings_title_font.render("Select Machine Tier", True, (61, 40, 30))
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    for i, t in enumerate(machine_tiers):
        y = 200 + i * 90
        surface.blit(font_text.render(f"{t['tier']}   |   ${t['price']}", True, (61, 40, 30)), (160, y + 15))
        if i < len(tier_buttons):
            tier_buttons[i]["info"].draw(surface, mouse_pos)
            tier_buttons[i]["buy"].draw(surface, mouse_pos)
    surface.blit(footer_font.render("Press SPACE to return", True, (61, 40, 30)), (WIDTH//2 - 100, HEIGHT - 60))

def draw_branches_window(surface, mouse_pos):
    surface.fill((255, 231, 184))
    title = settings_title_font.render("Branches", True, (61, 40, 30))
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    for i, b in enumerate(branches_tiers):
        y = 180 + i * 90
        surface.blit(font_text.render(f"{b['tier']} - ${b['price']}", True, (61, 40, 30)), (200, y + 15))
        if i < len(branches_tier_buttons):
            branches_tier_buttons[i]["info"].draw(surface, mouse_pos)
            branches_tier_buttons[i]["buy"].draw(surface, mouse_pos)
    surface.blit(footer_font.render("Press SPACE to return", True, (61, 40, 30)), (WIDTH//2 - 100, HEIGHT - 60))

# ======================#
# Game Loop #
# ======================#
tap_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 200)
tap_button_color = (210, 180, 140)
tap_button_hover = (200, 170, 130)

game_state = 'main_gameplay'
selected_shop_info = None
selected_upgrade_info = None
selected_machine_tier = None
selected_branch_tier = None
shop_level, shop_upgrade_count, shop_upgrades_needed = 1, 0, 3

try:
    pygame.mixer.music.load('Musics/Main_Gameplay_Music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
except:
    pass

def run_game():
    """Main gameplay runner. Call this to start the gameplay loop."""
    # Declare module-level state variables that we update in this function
    global game_state, selected_shop_info, selected_upgrade_info, selected_machine_tier, selected_branch_tier
    global shop_level, shop_upgrade_count, shop_upgrades_needed, level

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        notifications.update() # Update notifications timer
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw Background
        if game_state == "main_gameplay":
            WIN.blit(background, (0, 0))
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "main_gameplay":
                    # Handle Menu Buttons
                    if shop_button.rect.collidepoint(event.pos): game_state = 'shop'
                    elif settings_button.rect.collidepoint(event.pos): game_state = 'settings'
                    elif upgrade_button.rect.collidepoint(event.pos): game_state = 'upgrade'
                    elif branches_button.rect.collidepoint(event.pos):
                        game_state = 'branches'
                        create_branches_tier_buttons()
                    # Handle Tap
                    elif tap_button_rect.collidepoint(event.pos):
                        earned = game_state_obj.tap()

            # SHOP Logic
            if game_state == "shop":
                for i, item in enumerate(shop_items):
                    if shop_buttons[i]["info"].clicked(event):
                        selected_shop_info = item
                        game_state = "shop_info"
                    if shop_buttons[i]["action"].clicked(event):
                        if item.get("type") == "machine":
                            create_machine_tier_buttons()
                            game_state = "machine_tiers"
                        else:
                            price = item.get("price", 0) or 0
                            result = game_state_obj.buy_shop_item(item.get("key"), price)
                            if result == "success":
                                notifications.add(f"Purchased: {item['name']}!", (0, 100, 0))
                            elif result == "owned":
                                notifications.add(f"You already own {item['name']}!", (200, 100, 0))
                            else:
                                notifications.add("Not enough money!", (200, 0, 0))

            # UPGRADE Logic
            if game_state == "upgrade":
                for i, item in enumerate(upgrade_items):
                    if upgrade_buttons[i]["info"].clicked(event):
                        selected_upgrade_info = item
                        game_state = "upgrade_info"
                    if upgrade_buttons[i]["buy"].clicked(event):
                        price = item.get("cost", 0) or 0
                        if game_state_obj.buy_upgrade(item.get("key"), price) == "success":
                            notifications.add(f"Upgraded {item['name']}!", (0, 100, 0))
                            if item.get("name") == "Shop":
                                shop_upgrade_count += 1
                                if shop_upgrade_count >= shop_upgrades_needed:
                                    shop_level += 1
                                    shop_upgrade_count = 0
                                    shop_upgrades_needed *= 2
                                    level += 1
                                    notifications.add(f"Shop Leveled Up to {shop_level}!", (0, 0, 255))
                        else:
                            notifications.add("Not enough money!", (200, 0, 0))

            # MACHINE TIER Logic
            if game_state == "machine_tiers":
                for i, t in enumerate(machine_tiers):
                    if i < len(tier_buttons):
                        if tier_buttons[i]["info"].clicked(event):
                            selected_machine_tier = t
                            game_state = "machine_tier_info"
                        if tier_buttons[i]["buy"].clicked(event):
                            price = t.get("price", 0) or 0
                            if game_state_obj.buy_machine(t.get("key"), price) == "success":
                                notifications.add(f"Equipped: {t['tier']}", (0, 100, 0))
                            else:
                                notifications.add("Not enough money!", (200, 0, 0))
            
            # BRANCHES Logic
            if game_state == "branches":
                for i, t in enumerate(branches_tiers):
                    if i < len(branches_tier_buttons):
                        if branches_tier_buttons[i]["info"].clicked(event):
                            selected_branch_tier = t
                            game_state = "branches_tier_info"
                        if branches_tier_buttons[i]["buy"].clicked(event):
                            price = t.get("price", 0) or 0
                            # Logic for buying branches (assuming same money pool for now)
                            if game_state_obj.money >= price:
                                game_state_obj.money -= price
                                notifications.add(f"Opened: {t['tier']}", (0, 100, 0))
                            else:
                                notifications.add("Not enough money!", (200, 0, 0))

            # SETTINGS Logic
            if game_state == 'settings':
                music_slider.handle_event(event)
                sfx_slider.handle_event(event)
                mute_checkbox.handle_event(event)
                if apply_button.is_clicked(event):
                    notifications.add("Settings Saved", (0, 100, 0))
                    try:
                        if mute_checkbox.checked: pygame.mixer.music.set_volume(0)
                        else: pygame.mixer.music.set_volume(music_slider.value)
                    except: pass

        # --- DRAWING ---
        if game_state == "shop": draw_shop_window(WIN, mouse_pos)
        elif game_state == "shop_info": draw_info_screen(WIN, selected_shop_info["name"], selected_shop_info["info"])
        elif game_state == "machine_tiers": draw_machine_tiers(WIN, mouse_pos)
        elif game_state == "machine_tier_info": draw_info_screen(WIN, selected_machine_tier["tier"], selected_machine_tier["info"])
        elif game_state == "upgrade": draw_upgrade_window(WIN, mouse_pos)
        elif game_state == "upgrade_info": draw_info_screen(WIN, selected_upgrade_info["name"], selected_upgrade_info["info"])
        elif game_state == "branches": draw_branches_window(WIN, mouse_pos)
        elif game_state == "branches_tier_info": draw_info_screen(WIN, selected_branch_tier["tier"], selected_branch_tier["info"])
        elif game_state == "settings":
            WIN.fill((255, 231, 184))
            title = settings_title_font.render("Settings", True, (61, 40, 30))
            WIN.blit(title, (WIDTH//2 - title.get_width()//2, 60))
            music_slider.draw(WIN)
            sfx_slider.draw(WIN)
            mute_checkbox.draw(WIN)
            apply_button.draw(WIN, mouse_pos)
            back = footer_font.render("Press SPACE to return", True, (61, 40, 30))
            WIN.blit(back, (WIDTH//2 - back.get_width()//2, HEIGHT - 60))
        elif game_state == "main_gameplay":
            # Draw UI
            money_text = font_text.render(f'Money: ${game_state_obj.money:.2f}', True, (0, 0, 0))
            WIN.blit(money_text, (20, 20))
            WIN.blit(level_text, level_rect)
            
            shop_button.draw(WIN)
            settings_button.draw(WIN)
            upgrade_button.draw(WIN)
            branches_button.draw(WIN)
            
            button_color = tap_button_hover if tap_button_rect.collidepoint(mouse_pos) else tap_button_color
            pygame.draw.rect(WIN, button_color, tap_button_rect, border_radius=20)
            tap_text = settings_title_font.render("TAP", True, (61, 40, 30))
            WIN.blit(tap_text, (tap_button_rect.centerx - tap_text.get_width()//2, tap_button_rect.centery - tap_text.get_height()//2))

        # Draw Notifications Last (On Top)
        notifications.draw(WIN)

        # Return key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game_state != "main_gameplay":
            game_state = 'main_gameplay'
            selected_shop_info = None

        pygame.display.update()

    # Save before exit
    game_state_obj.save()
    pygame.quit()


if __name__ == '__main__':
    run_game()