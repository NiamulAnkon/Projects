import pygame
import sys
import time

# --- 1. CONFIGURATION AND INITIALIZATION ---

pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pastel Café Tycoon")

# Load a simple system font (Pygame requirement for text)
try:
    FONT_MD = pygame.font.Font(None, 36)
    FONT_SM = pygame.font.Font(None, 24)
    FONT_LG = pygame.font.Font(None, 48)
except pygame.error:
    print("Warning: Could not load default font. Text might be missing.")
    FONT_MD = pygame.font.SysFont('Arial', 36)
    FONT_SM = pygame.font.SysFont('Arial', 24)
    FONT_LG = pygame.font.SysFont('Arial', 48)

# --- Pastel Café Color Palette ---
COLOR_BEIGE = (245, 245, 220)      # Soft Background
COLOR_BROWN = (160, 100, 70)       # Accent/Text
COLOR_CREAM = (255, 255, 240)      # Button Fill
COLOR_PINK = (255, 210, 225)       # Highlight
COLOR_GREEN = (180, 220, 180)      # Success/Buy
COLOR_RED = (255, 100, 100)        # Error/Broken
COLOR_SHADOW = (200, 200, 180)     # Light Shadow

# Game States
STATE_MAIN = 0
STATE_SHOP = 1
STATE_UPGRADE = 2
STATE_SETTINGS = 3
STATE_BRANCHES = 4
STATE_PAUSE = 5

game_state = STATE_MAIN

# --- 2. GAME DATA ---

# Global data structure for all game variables
game_data = {
    'money': 50.0,
    'level': 1,
    # Core earnings components
    'bean_quality': 1,      # Multiplied by 2
    'machine_tier': 1,      # Multiplied by 5
    'advertising_level': 1, # Multiplied by 3
    # Machine status
    'machine_broken': False,
    'break_chance': 0.05,   # Base 5% chance per break check
    'break_check_interval': 15, # Check every 15 seconds
    'last_break_check': time.time(), # Initialized here
    # Upgrades and Items
    'repair_kit_owned': False, # Auto-repair functionality
    'break_chance_reduction': 0, # Flat reduction in break chance (e.g., 0.02)
    'speed_boost_active': False,
    'speed_boost_end_time': 0,
    # Branches
    'branches': 0,
    'branch_multiplier': 1.0,
    'branch_cost': 5000.0,
    # Audio/Settings (not fully implemented in this silent version, but for UI)
    'music_volume': 0.5,
    'sfx_volume': 0.5,
    'mute_all': False,
}

# --- 3. UTILITY CLASSES ---

class Button:
    """A simple rounded rectangle button."""
    def __init__(self, rect, text, color, text_color=COLOR_BROWN, action=None, disabled_color=COLOR_SHADOW):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.is_hovered = False
        self.disabled_color = disabled_color
        self.is_disabled = False

    def draw(self, surface):
        current_color = self.disabled_color if self.is_disabled else (
            self.color if not self.is_hovered else tuple(min(255, c + 20) for c in self.color)
        )
        # Draw soft shadow (optional offset)
        shadow_rect = self.rect.move(2, 2)
        pygame.draw.rect(surface, COLOR_SHADOW, shadow_rect, border_radius=12)
        
        # Draw the button face
        pygame.draw.rect(surface, current_color, self.rect, border_radius=12)

        # Draw the border (optional)
        pygame.draw.rect(surface, COLOR_BROWN, self.rect, width=2, border_radius=12)

        # Draw text
        text_surface = FONT_MD.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if self.is_disabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False

class Slider:
    """A custom drawn slider for settings."""
    def __init__(self, rect, min_val, max_val, initial_val, callback):
        # rect must be (x, y, w, h)
        self.rect = pygame.Rect(rect)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.callback = callback
        self.is_dragging = False

    def draw(self, surface):
        # Track (Beige)
        # Using self.rect.centery to ensure the track is centered vertically within the bounding box
        track_rect = pygame.Rect(self.rect.left, self.rect.centery - 5, self.rect.width, 10)
        pygame.draw.rect(surface, COLOR_SHADOW, track_rect, border_radius=5)

        # Progress (Pink)
        progress_width = (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        progress_rect = pygame.Rect(self.rect.left, self.rect.centery - 5, progress_width, 10)
        pygame.draw.rect(surface, COLOR_PINK, progress_rect, border_radius=5)

        # Handle (Brown Circle)
        handle_x = int(self.rect.left + progress_width)
        pygame.draw.circle(surface, COLOR_BROWN, (handle_x, self.rect.centery), 10)
        
        # Value Text
        text = FONT_SM.render(f"{int(self.value * 100)}%", True, COLOR_BROWN)
        surface.blit(text, (self.rect.right + 10, self.rect.centery - 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self._update_value(event.pos[0])
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self._update_value(event.pos[0])
            return True
        
        return False

    def _update_value(self, mouse_x):
        relative_x = max(0, min(self.rect.width, mouse_x - self.rect.left))
        normalized_value = relative_x / self.rect.width
        self.value = self.min_val + normalized_value * (self.max_val - self.min_val)
        self.value = round(self.value, 2)
        self.callback(self.value)

class Checkbox:
    """A custom drawn checkbox."""
    def __init__(self, rect, initial_val, callback):
        self.rect = pygame.Rect(rect)
        self.checked = initial_val
        self.callback = callback

    def draw(self, surface):
        # Outer box
        pygame.draw.rect(surface, COLOR_BROWN, self.rect, width=3, border_radius=5)
        
        if self.checked:
            # Inner fill (Pink)
            inner_rect = self.rect.inflate(-6, -6)
            pygame.draw.rect(surface, COLOR_PINK, inner_rect, border_radius=3)
            # Simple checkmark (two lines)
            pygame.draw.line(surface, COLOR_BROWN, inner_rect.topleft, inner_rect.bottomright, 3)
            pygame.draw.line(surface, COLOR_BROWN, inner_rect.topright, inner_rect.bottomleft, 3)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                self.callback(self.checked)
                return True
        return False

class Popup:
    """A modal popup for item info."""
    def __init__(self, title, content, parent_rect):
        self.title = title
        self.content = content
        self.is_open = False
        
        # Center the popup relative to the parent screen
        self.width = 400
        self.height = 200
        self.rect = pygame.Rect(
            parent_rect.centerx - self.width // 2,
            parent_rect.centery - self.height // 2,
            self.width, self.height
        )
        
        # Close button
        self.close_button = Button(
            (self.rect.right - 40, self.rect.top + 10, 30, 30), "X", COLOR_RED, COLOR_CREAM, self.close
        )

    def open(self):
        self.is_open = True
    
    def close(self):
        self.is_open = False

    def draw(self, surface):
        if not self.is_open:
            return

        # Semi-transparent background overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100)) # Dim the background
        surface.blit(overlay, (0, 0))

        # Popup window (Cream/Beige)
        pygame.draw.rect(surface, COLOR_CREAM, self.rect, border_radius=15)
        pygame.draw.rect(surface, COLOR_BROWN, self.rect, width=3, border_radius=15)

        # Title
        title_surf = FONT_MD.render(self.title, True, COLOR_BROWN)
        title_rect = title_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        surface.blit(title_surf, title_rect)

        # Content (Wrapping text is complex in Pygame, so we use a simple label)
        content_surf = FONT_SM.render(self.content, True, COLOR_BROWN)
        content_rect = content_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 70))
        surface.blit(content_surf, content_rect)
        
        # Draw close button
        self.close_button.draw(surface)

    def handle_event(self, event):
        if self.is_open:
            return self.close_button.handle_event(event)
        return False

class ShopItem:
    """Structure for shop items, including buttons and a popup."""
    def __init__(self, name, description, cost_func, buy_action, y_pos, container_rect):
        self.name = name
        self.description = description
        self.cost_func = cost_func
        self.buy_action = buy_action
        
        # UI Rects relative to container
        rect = pygame.Rect(container_rect.left + 20, y_pos, container_rect.width - 40, 60)
        self.rect = rect
        
        # Info button (left)
        info_rect = (rect.left + rect.width - 160, rect.centery - 20, 40, 40)
        self.info_button = Button(info_rect, "i", COLOR_PINK, action=self._open_popup)
        
        # Buy button (right)
        buy_rect = (rect.left + rect.width - 100, rect.centery - 20, 80, 40)
        self.buy_button = Button(buy_rect, "Buy", COLOR_GREEN, action=self._buy_item)
        
        # Popup setup
        self.popup = Popup(name, description, container_rect)

    def _open_popup(self):
        self.popup.open()

    def _buy_item(self):
        cost = self.cost_func(game_data)
        if game_data['money'] >= cost:
            game_data['money'] -= cost
            self.buy_action(game_data)
        else:
            print(f"Not enough money for {self.name}") # In a real app, this would show a small error UI

    def draw(self, surface):
        cost = self.cost_func(game_data)
        
        # Draw item background
        pygame.draw.rect(surface, COLOR_CREAM, self.rect, border_radius=8)
        
        # Draw Name
        name_surf = FONT_MD.render(self.name, True, COLOR_BROWN)
        surface.blit(name_surf, (self.rect.left + 10, self.rect.centery - 15))

        # Draw Cost
        cost_surf = FONT_MD.render(f"${cost:.2f}", True, COLOR_BROWN)
        surface.blit(cost_surf, (self.rect.left + 200, self.rect.centery - 15))

        # Update Buy button state
        self.buy_button.is_disabled = game_data['money'] < cost
        self.buy_button.text = "Buy"

        # Special check for Repair Kit and Speed Boost (only one needed for these)
        if self.name == "Repair Toolkit" and game_data['repair_kit_owned']:
            self.buy_button.is_disabled = True
            self.buy_button.text = "Owned"
        elif self.name == "Advertising Boost" and game_data['speed_boost_active']:
            self.buy_button.is_disabled = True
            self.buy_button.text = "Active"

        # Draw buttons
        self.info_button.draw(surface)
        self.buy_button.draw(surface)
        
        # Draw the popup if open (must be drawn last to be on top)
        self.popup.draw(surface)

    def handle_event(self, event):
        if self.popup.is_open:
            return self.popup.handle_event(event)

        if self.info_button.handle_event(event):
            return True
        if self.buy_button.handle_event(event):
            return True
        return False

class UpgradeItem:
    """Structure for permanent upgrade items."""
    def __init__(self, name, description, cost_func, upgrade_action, y_pos, container_rect):
        self.name = name
        self.description = description
        self.cost_func = cost_func
        self.upgrade_action = upgrade_action
        self.rect = pygame.Rect(container_rect.left + 20, y_pos, container_rect.width - 40, 60)
        
        buy_rect = (self.rect.left + self.rect.width - 100, self.rect.centery - 20, 80, 40)
        self.buy_button = Button(buy_rect, "+", COLOR_GREEN, action=self._upgrade)

    def _upgrade(self):
        cost = self.cost_func(game_data)
        if game_data['money'] >= cost:
            game_data['money'] -= cost
            self.upgrade_action(game_data)
        else:
            print(f"Not enough money for {self.name} upgrade.")
            
    def draw(self, surface):
        cost = self.cost_func(game_data)
        
        pygame.draw.rect(surface, COLOR_CREAM, self.rect, border_radius=8)
        
        name_surf = FONT_MD.render(self.name, True, COLOR_BROWN)
        surface.blit(name_surf, (self.rect.left + 10, self.rect.centery - 15))

        cost_surf = FONT_MD.render(f"${cost:.2f}", True, COLOR_BROWN)
        surface.blit(cost_surf, (self.rect.left + 300, self.rect.centery - 15))

        self.buy_button.is_disabled = game_data['money'] < cost
        self.buy_button.draw(surface)

    def handle_event(self, event):
        return self.buy_button.handle_event(event)

# --- 4. GAME LOGIC FUNCTIONS ---

last_money_update_time = time.time()
last_second_check = time.time()
earnings_per_second = 0.0

def calculate_earnings():
    """Calculates the current earnings per second."""
    global earnings_per_second
    
    # Core Formula
    base_eps = (game_data['bean_quality'] * 2) + \
               (game_data['machine_tier'] * 5) + \
               (game_data['advertising_level'] * 3)

    # Apply branch multiplier
    modified_eps = base_eps * game_data['branch_multiplier']

    # Apply machine broken penalty
    if game_data['machine_broken']:
        modified_eps /= 5.0 # Reduce earnings significantly

    earnings_per_second = modified_eps
    return earnings_per_second

def update_money():
    """Updates money based on elapsed time."""
    global last_money_update_time
    current_time = time.time()
    
    # Only update if the game is not paused
    if game_state != STATE_PAUSE:
        # Calculate time passed since last update
        elapsed = current_time - last_money_update_time
        
        # Add money
        current_eps = calculate_earnings()
        game_data['money'] += current_eps * elapsed

        # Check for machine break periodically
        check_machine_break()

        # Check for speed boost expiration
        check_speed_boost()

    last_money_update_time = current_time

def check_machine_break():
    """Checks if the coffee machine breaks."""
    # last_break_check is now correctly accessed via the game_data dictionary
    
    if game_data['machine_broken']:
        # If machine is broken and repair kit is owned, auto-repair
        if game_data['repair_kit_owned']:
            game_data['machine_broken'] = False
            print("Auto-repaired machine!")
        return # Cannot break if already broken

    current_time = time.time()
    
    # Corrected access to last_break_check
    if current_time - game_data['last_break_check'] >= game_data['break_check_interval']:
        # Check against a random chance
        # Effective break chance = Base - Upgrade Reduction
        effective_break_chance = max(0.01, game_data['break_chance'] - game_data['break_chance_reduction'])
        
        if time.time() % 100 < effective_break_chance * 100: # Simple random check
            game_data['machine_broken'] = True
            print("Machine Broken! Earnings are reduced.")

        # Corrected update of last_break_check
        game_data['last_break_check'] = current_time

def repair_machine():
    """Action for repairing the machine manually."""
    repair_cost = 50.0
    if game_data['machine_broken'] and game_data['money'] >= repair_cost:
        game_data['money'] -= repair_cost
        game_data['machine_broken'] = False
        print("Machine repaired.")

def check_speed_boost():
    """Checks and deactivates advertising speed boost."""
    if game_data['speed_boost_active'] and time.time() > game_data['speed_boost_end_time']:
        game_data['advertising_level'] = max(1, game_data['advertising_level'] // 2) # Halve back
        game_data['speed_boost_active'] = False
        print("Advertising boost expired.")

# --- 5. UI ELEMENTS & SCREEN DRAWING ---

# Global function to change game state 
def set_state(state):
    """Sets the global game_state variable."""
    global game_state
    game_state = state

# Main Menu Buttons (reused in Main Screen)
main_buttons = []

def init_main_buttons():
    """Initializes buttons for the main screen/navigation."""
    global main_buttons
    # Position buttons on the right side of the screen
    button_y = 150
    button_height = 60
    button_width = 150
    button_margin = 20
    
    main_buttons = [
        Button((SCREEN_WIDTH - button_width - button_margin, button_y, button_width, button_height), "Shop", COLOR_PINK, action=lambda: set_state(STATE_SHOP)),
        Button((SCREEN_WIDTH - button_width - button_margin, button_y + 80, button_width, button_height), "Upgrades", COLOR_PINK, action=lambda: set_state(STATE_UPGRADE)),
        Button((SCREEN_WIDTH - button_width - button_margin, button_y + 160, button_width, button_height), "Settings", COLOR_PINK, action=lambda: set_state(STATE_SETTINGS)),
        Button((SCREEN_WIDTH - button_width - button_margin, button_y + 240, button_width, button_height), "Branches", COLOR_PINK, action=lambda: set_state(STATE_BRANCHES)),
    ]

# Shop Screen Setup
shop_container_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, 100, 600, 450)
shop_items = []

def init_shop_items():
    """Defines all shop items and their logic."""
    global shop_items
    
    # 1. Coffee Beans (Tier increases)
    def cost_beans(data):
        return 50.0 * (data['bean_quality'] * 2)
    def buy_beans(data):
        data['bean_quality'] += 1
    
    # 2. Coffee Machines (Tier increases)
    def cost_machine(data):
        return 100.0 * (data['machine_tier'] ** 2)
    def buy_machine(data):
        data['machine_tier'] += 1
    
    # 3. Advertising Boost (Temporary Multiplier)
    def cost_ad_boost(data):
        return 200.0
    def buy_ad_boost(data):
        # Double advertising level for 60 seconds
        data['advertising_level'] *= 2
        data['speed_boost_active'] = True
        data['speed_boost_end_time'] = time.time() + 60
        print("Advertising boost applied for 60 seconds!")
        
    # 4. Repair Toolkit (Auto-Repair)
    def cost_toolkit(data):
        return 500.0
    def buy_toolkit(data):
        if not data['repair_kit_owned']:
            data['repair_kit_owned'] = True
        
    y_start = shop_container_rect.top + 50
    item_height = 80

    shop_items = [
        ShopItem("Coffee Beans", "Increases base earnings by 2 per quality level.", cost_beans, buy_beans, y_start, shop_container_rect),
        ShopItem("Coffee Machine", "Increases base earnings by 5 per tier. Max tier 5.", cost_machine, buy_machine, y_start + item_height, shop_container_rect),
        ShopItem("Advertising Boost", "Doubles current Advertising earnings for 60 seconds.", cost_ad_boost, buy_ad_boost, y_start + item_height * 2, shop_container_rect),
        ShopItem("Repair Toolkit", "Permanently enables auto-repair for broken machines.", cost_toolkit, buy_toolkit, y_start + item_height * 3, shop_container_rect),
    ]

# Upgrade Screen Setup
upgrade_container_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, 100, 600, 450)

upgrade_items = []

def init_upgrade_items():
    global upgrade_items
    
    # 1. Increase Bean Quality (Permanent flat bonus to bean_quality)
    def cost_bean_up(data):
        return 150.0 * data['bean_quality']
    def upgrade_bean(data):
        data['bean_quality'] += 1
    
    # 2. Speed up Machine (Increase earnings per second multiplier)
    def cost_speed_up(data):
        return 200.0 * data['machine_tier']
    def upgrade_speed(data):
        data['machine_tier'] += 1
    
    # 3. Reduce Break Chance (Flat reduction)
    def cost_break_red(data):
        # Max reduction is 0.04 (4%)
        if data['break_chance_reduction'] >= 0.04:
            return 999999.0 # Effectively locked
        return 300.0 * (data['break_chance_reduction'] * 100 + 1)
    def upgrade_break(data):
        if data['break_chance_reduction'] < 0.04:
            data['break_chance_reduction'] += 0.01

    # 4. Improve Advertising Efficiency (Increase advertising_level)
    def cost_ad_eff(data):
        return 100.0 * data['advertising_level']
    def upgrade_ad(data):
        data['advertising_level'] += 1

    y_start = upgrade_container_rect.top + 50
    item_height = 80

    upgrade_items = [
        UpgradeItem("Better Beans", "Increase permanent Bean Quality tier.", cost_bean_up, upgrade_bean, y_start, upgrade_container_rect),
        UpgradeItem("Machine Speed", "Increase permanent Machine Tier level.", cost_speed_up, upgrade_speed, y_start + item_height, upgrade_container_rect),
        UpgradeItem("Maintenance Kit", "Reduces machine break chance by 1%.", cost_break_red, upgrade_break, y_start + item_height * 2, upgrade_container_rect),
        UpgradeItem("Ad Efficiency", "Increase permanent Advertising Level.", cost_ad_eff, upgrade_ad, y_start + item_height * 3, upgrade_container_rect),
    ]

# Settings Screen Setup
settings_container_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, 150, 500, 350)
settings_elements = {}

def set_music_volume(val):
    game_data['music_volume'] = val
def set_sfx_volume(val):
    game_data['sfx_volume'] = val
def set_mute_all(val):
    game_data['mute_all'] = val
    if val:
        game_data['music_volume'] = 0.0
        game_data['sfx_volume'] = 0.0

def init_settings():
    """Initializes settings elements, ensuring all objects have proper dimensions."""
    global settings_elements
    
    y_start = settings_container_rect.top + 50
    slider_height = 20 # Added height parameter
    
    # CORRECTED SLIDER INITIALIZATION (passing 4 values: x, y, width, height)
    music_slider = Slider((settings_container_rect.left + 50, y_start, 300, slider_height), 0, 1, game_data['music_volume'], set_music_volume)
    sfx_slider = Slider((settings_container_rect.left + 50, y_start + 80, 300, slider_height), 0, 1, game_data['sfx_volume'], set_sfx_volume)
    
    mute_checkbox = Checkbox((settings_container_rect.left + 50, y_start + 160, 30, 30), game_data['mute_all'], set_mute_all)
    
    apply_button = Button((settings_container_rect.centerx - 75, y_start + 240, 150, 40), "Apply", COLOR_GREEN, action=lambda: print("Settings applied!"))
    
    settings_elements = {
        'sliders': [music_slider, sfx_slider],
        'checkbox': mute_checkbox,
        'apply': apply_button
    }
    
    # Text labels for settings
    settings_elements['labels'] = [
        (FONT_MD.render("Music Volume:", True, COLOR_BROWN), (settings_container_rect.left - 100, y_start - 10)),
        (FONT_MD.render("SFX Volume:", True, COLOR_BROWN), (settings_container_rect.left - 100, y_start + 70)),
        (FONT_MD.render("Mute All:", True, COLOR_BROWN), (settings_container_rect.left + 100, y_start + 160)),
    ]

# Branches Window Setup
branches_container_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, 100, 600, 450)

def buy_branch():
    """Action to buy a new branch."""
    if game_data['money'] >= game_data['branch_cost']:
        game_data['money'] -= game_data['branch_cost']
        game_data['branches'] += 1
        game_data['branch_multiplier'] += 0.5 # 50% passive multiplier per branch
        game_data['branch_cost'] *= 3 # Cost increases significantly
        print(f"New branch opened! Total branches: {game_data['branches']}")
    else:
        print("Not enough money for a new branch.")

# Branches Button
branch_button_rect = (branches_container_rect.centerx - 100, branches_container_rect.bottom - 100, 200, 50)
branch_buy_button = Button(branch_button_rect, "Open New Branch", COLOR_GREEN, action=buy_branch)

# Repair Button (on main screen)
repair_button = Button(
    (50, 450, 200, 60), 
    "Repair Machine ($50)", 
    COLOR_RED, COLOR_CREAM, 
    action=repair_machine
)

# Navigation and Menu Buttons (Now using the globally defined set_state)
# These must be initialized after set_state is defined.
back_button = Button((20, 20, 100, 40), "Back", COLOR_PINK, action=lambda: set_state(STATE_MAIN))
resume_button = Button((0, 0, 200, 60), "Resume", COLOR_GREEN, action=lambda: set_state(STATE_MAIN))
main_menu_button = Button((0, 0, 200, 60), "Quit Game", COLOR_RED, action=sys.exit) # Simple exit for "Main Menu"


# --- Drawing Functions ---

def draw_main_screen(surface):
    """Draws the main café idle screen."""
    
    # 1. Soft Beige Background
    surface.fill(COLOR_BEIGE)

    # 2. Centered Café Display Area (Soft Cream rectangle)
    cafe_rect = pygame.Rect(50, 100, 400, 300)
    pygame.draw.rect(surface, COLOR_CREAM, cafe_rect, border_radius=20)
    pygame.draw.rect(surface, COLOR_BROWN, cafe_rect, width=3, border_radius=20)

    # 3. Café Icon (Simple shapes - stylized coffee cup)
    cup_rect = pygame.Rect(cafe_rect.centerx - 50, cafe_rect.top + 50, 100, 80)
    pygame.draw.rect(surface, COLOR_BROWN, cup_rect, border_radius=10) # Cup body
    pygame.draw.rect(surface, COLOR_CREAM, cup_rect.inflate(-10, -10), border_radius=5) # Cup interior
    pygame.draw.circle(surface, COLOR_BROWN, (cup_rect.right, cup_rect.centery), 10) # Handle
    pygame.draw.rect(surface, COLOR_SHADOW, pygame.Rect(cafe_rect.centerx - 100, cafe_rect.top + 130, 200, 20), border_radius=5) # Saucer

    # 4. Main Stats (Top Left)
    money_text = FONT_LG.render(f"${game_data['money']:.2f}", True, COLOR_BROWN)
    surface.blit(money_text, (50, 30))

    eps_text = FONT_MD.render(f"EPS: {earnings_per_second:.2f}", True, COLOR_BROWN)
    surface.blit(eps_text, (50, 70))

    # 5. Core Stats in Café Display
    bean_text = FONT_SM.render(f"Bean Quality: T{game_data['bean_quality']}", True, COLOR_BROWN)
    surface.blit(bean_text, (cafe_rect.left + 20, cafe_rect.bottom - 80))

    machine_text = FONT_SM.render(f"Machine Tier: T{game_data['machine_tier']}", True, COLOR_BROWN)
    surface.blit(machine_text, (cafe_rect.left + 20, cafe_rect.bottom - 50))
    
    ad_text = FONT_SM.render(f"Ads Level: {game_data['advertising_level']}", True, COLOR_BROWN)
    surface.blit(ad_text, (cafe_rect.left + 20, cafe_rect.bottom - 20))

    # 6. Machine Status/Repair Button
    if game_data['machine_broken']:
        status_text = FONT_MD.render("BROKEN! (Repair Now)", True, COLOR_RED)
        status_rect = status_text.get_rect(midtop=(cafe_rect.centerx, cafe_rect.top + 180))
        surface.blit(status_text, status_rect)
        
        repair_button.is_disabled = game_data['money'] < 50.0
        repair_button.draw(surface)
    else:
        status_text = FONT_MD.render("OPERATIONAL", True, COLOR_GREEN)
        status_rect = status_text.get_rect(midtop=(cafe_rect.centerx, cafe_rect.top + 180))
        surface.blit(status_text, status_rect)

    # 7. Navigation Buttons (Right Side)
    for button in main_buttons:
        button.draw(surface)

def draw_shop_window(surface):
    """Draws the shop window with buyable items."""
    
    # 1. Background and Title
    surface.fill(COLOR_BEIGE)
    title_text = FONT_LG.render("Coffee Shop - Supply Depot", True, COLOR_BROWN)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))

    # 2. Shop Container
    pygame.draw.rect(surface, COLOR_SHADOW, shop_container_rect, border_radius=15)
    pygame.draw.rect(surface, COLOR_CREAM, shop_container_rect.inflate(-10, -10), border_radius=10)

    # 3. Item List
    for item in shop_items:
        item.draw(surface)
    
    # 4. Back Button
    back_button.draw(surface)
    
    # Draw any open popups last
    for item in shop_items:
        if item.popup.is_open:
            item.popup.draw(surface)
            break

def draw_upgrade_window(surface):
    """Draws the upgrade window."""
    
    # 1. Background and Title
    surface.fill(COLOR_BEIGE)
    title_text = FONT_LG.render("R&D - Permanent Upgrades", True, COLOR_BROWN)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))

    # 2. Upgrade Container
    pygame.draw.rect(surface, COLOR_SHADOW, upgrade_container_rect, border_radius=15)
    pygame.draw.rect(surface, COLOR_CREAM, upgrade_container_rect.inflate(-10, -10), border_radius=10)

    # 3. Item List
    for item in upgrade_items:
        item.draw(surface)

    # 4. Back Button
    back_button.draw(surface)

def draw_settings_window(surface):
    """Draws the settings window with sliders and checkbox."""
    
    # 1. Background and Title
    surface.fill(COLOR_BEIGE)
    title_text = FONT_LG.render("Settings", True, COLOR_BROWN)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))

    # 2. Settings Container
    pygame.draw.rect(surface, COLOR_SHADOW, settings_container_rect, border_radius=15)
    pygame.draw.rect(surface, COLOR_CREAM, settings_container_rect.inflate(-10, -10), border_radius=10)

    # 3. Elements
    if 'sliders' in settings_elements:
        for slider in settings_elements['sliders']:
            slider.draw(surface)
        
        settings_elements['checkbox'].draw(surface)

        # Labels
        for text_surf, pos in settings_elements['labels']:
            surface.blit(text_surf, pos)
        
        # Apply button
        settings_elements['apply'].draw(surface)

    # 4. Back Button
    back_button.draw(surface)

def draw_branches_window(surface):
    """Draws the branches window."""
    
    # 1. Background and Title
    surface.fill(COLOR_BEIGE)
    title_text = FONT_LG.render("Branch Expansion", True, COLOR_BROWN)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))

    # 2. Branches Container
    pygame.draw.rect(surface, COLOR_SHADOW, branches_container_rect, border_radius=15)
    pygame.draw.rect(surface, COLOR_CREAM, branches_container_rect.inflate(-10, -10), border_radius=10)
    
    # 3. Current Status
    branches_count_text = FONT_LG.render(f"Current Branches: {game_data['branches']}", True, COLOR_BROWN)
    count_rect = branches_count_text.get_rect(midtop=(branches_container_rect.centerx, branches_container_rect.top + 50))
    surface.blit(branches_count_text, count_rect)

    mult_text = FONT_MD.render(f"Passive Multiplier: x{game_data['branch_multiplier']:.1f}", True, COLOR_BROWN)
    mult_rect = mult_text.get_rect(midtop=(branches_container_rect.centerx, branches_container_rect.top + 100))
    surface.blit(mult_text, mult_rect)

    # 4. Buy New Branch
    cost = game_data['branch_cost']
    cost_text = FONT_MD.render(f"Next Branch Cost: ${cost:.2f}", True, COLOR_BROWN)
    cost_rect = cost_text.get_rect(midtop=(branches_container_rect.centerx, branches_container_rect.top + 250))
    surface.blit(cost_text, cost_rect)

    branch_buy_button.is_disabled = game_data['money'] < cost
    branch_buy_button.draw(surface)

    # 5. Back Button
    back_button.draw(surface)

def draw_pause_menu(surface):
    """Draws the pause menu overlay."""
    
    # Dim overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    # Pause Box
    pause_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
    pygame.draw.rect(surface, COLOR_CREAM, pause_rect, border_radius=15)
    pygame.draw.rect(surface, COLOR_BROWN, pause_rect, width=3, border_radius=15)

    # Title
    title_text = FONT_LG.render("PAUSED", True, COLOR_BROWN)
    title_rect = title_text.get_rect(midtop=(pause_rect.centerx, pause_rect.top + 30))
    surface.blit(title_text, title_rect)

    # Buttons
    resume_button.rect.center = (pause_rect.centerx, pause_rect.centery - 30)
    main_menu_button.rect.center = (pause_rect.centerx, pause_rect.centery + 60)

    resume_button.draw(surface)
    main_menu_button.draw(surface)


# Initializing UI elements
init_main_buttons()
init_shop_items()
init_upgrade_items()
init_settings() 


# --- 6. MAIN GAME LOOP ---

def handle_events():
    """Handles Pygame events for the current state."""
    global game_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Toggle Pause state with SPACE key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state != STATE_PAUSE:
                set_state(STATE_PAUSE)
            elif game_state == STATE_PAUSE:
                set_state(STATE_MAIN)

        # Handle UI elements based on state
        if game_state == STATE_MAIN:
            for button in main_buttons:
                if button.handle_event(event): return
            if game_data['machine_broken'] and repair_button.handle_event(event): return

        elif game_state == STATE_SHOP:
            if back_button.handle_event(event): return
            for item in shop_items:
                if item.handle_event(event): return

        elif game_state == STATE_UPGRADE:
            if back_button.handle_event(event): return
            for item in upgrade_items:
                if item.handle_event(event): return

        elif game_state == STATE_SETTINGS:
            if back_button.handle_event(event): return
            if settings_elements.get('apply') and settings_elements['apply'].handle_event(event): return
            if settings_elements.get('checkbox') and settings_elements['checkbox'].handle_event(event): return
            if settings_elements.get('sliders'):
                for slider in settings_elements['sliders']:
                    if slider.handle_event(event): return

        elif game_state == STATE_BRANCHES:
            if back_button.handle_event(event): return
            if branch_buy_button.handle_event(event): return

        elif game_state == STATE_PAUSE:
            if resume_button.handle_event(event): return
            if main_menu_button.handle_event(event): return

def update_game():
    """Updates game logic (money, timers, etc.)."""
    if game_state != STATE_PAUSE:
        update_money()
        
# Game loop clock
clock = pygame.time.Clock()

def run_game():
    """The main entry point for the game."""
    while True:
        handle_events()
        update_game()
        
        screen.fill(COLOR_BEIGE) # Ensure the background is cleared

        # Draw current state
        if game_state == STATE_MAIN:
            draw_main_screen(screen)
        elif game_state == STATE_SHOP:
            draw_shop_window(screen)
        elif game_state == STATE_UPGRADE:
            draw_upgrade_window(screen)
        elif game_state == STATE_SETTINGS:
            draw_settings_window(screen)
        elif game_state == STATE_BRANCHES:
            draw_branches_window(screen)
        elif game_state == STATE_PAUSE:
            # Draw Main screen underneath the pause overlay
            draw_main_screen(screen) 
            draw_pause_menu(screen)

        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)

if __name__ == '__main__':
    run_game()