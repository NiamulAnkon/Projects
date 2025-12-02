import pygame
from main_gameplay import money, level

pygame.init()

# ======================#
# Setup Display #
# ======================#
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brew’d Up")
icon  = pygame.image.load('Graphics/logo.png')
pygame.display.set_icon(icon)

# ======================#
# Background Music #
# ======================#
background = pygame.image.load('Graphics/Menu_Background.png')

# ======================#
# Menu State #
# ======================#
menu_state = 'main_menu'

# ======================#
# Title & Footer #
# ======================#
font = pygame.font.SysFont('comicsans', 130)
title_text = font.render("Brew’d Up", True, (61, 40, 30))
title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))

footer_font = pygame.font.SysFont('comicsans', 24)
footer_text = footer_font.render(
    'Created by MD NIAMUL ISLAM ANKON aka ATHECAL', True, (61, 40, 30)
)
footer_rect = footer_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))

# ======================#
# Button Setup #
# ======================#
BUTTON_WIDTH = int(min(500, WIDTH * 0.5))
BUTTON_HEIGHT = 80
SPACING = 24

button_images = [
    pygame.image.load('Graphics/start_btn.png'),
    pygame.image.load('Graphics/setting_btn.png'),
    pygame.image.load('Graphics/info_btn.png'),
    pygame.image.load('Graphics/progression_btn.png'),
]

top_margin = title_rect.bottom + 20
bottom_margin = HEIGHT - 20
available_space = bottom_margin - top_margin

n = len(button_images)
total_height = n * BUTTON_HEIGHT + (n - 1) * SPACING

if total_height > available_space:
    scale = available_space / total_height
    BUTTON_HEIGHT = max(40, int(BUTTON_HEIGHT * scale))
    SPACING = max(8, int(SPACING * scale))
    total_height = n * BUTTON_HEIGHT + (n - 1) * SPACING

start_y = top_margin + (available_space - total_height) // 2
center_x = WIDTH // 2

button_rects = []
for i, img in enumerate(button_images):
    scaled = pygame.transform.smoothscale(img, (int(BUTTON_WIDTH), BUTTON_HEIGHT))
    button_images[i] = scaled
    y = start_y + i * (BUTTON_HEIGHT + SPACING) + BUTTON_HEIGHT // 2
    button_rects.append(scaled.get_rect(center=(center_x, y)))


def draw_buttons(mouse_pos):
    for img, rect in zip(button_images, button_rects):
        if rect.collidepoint(mouse_pos):
            hover_img = pygame.transform.scale(
                img, (int(BUTTON_WIDTH * 1.02), int(BUTTON_HEIGHT * 1.05))
            )
            hover_rect = hover_img.get_rect(center=rect.center)
            WIN.blit(hover_img, hover_rect)
        else:
            WIN.blit(img, rect)


def handle_button_click(mouse_pos):
    global menu_state
    for i, rect in enumerate(button_rects):
        if rect.collidepoint(mouse_pos):
            if i == 0:
                # signal to caller that Start was clicked
                return 'start'
            elif i == 1:
                menu_state = 'settings'
                return None
            elif i == 2:
                menu_state = 'info'
                return None
            elif i == 3:
                menu_state = 'progression'
                return None
    return None


# ======================#
# Slider & Checkbox #
# ======================#
class Slider:
    def __init__(self, x, y, width, label, initial=0.5):
        self.x = x
        self.y = y
        self.width = width
        self.height = 6
        self.radius = 10
        self.value = initial
        self.dragging = False
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
    def handle_x(self):
        return int(self.x + self.value * self.width)

    def draw(self, surface):
        pygame.draw.rect(surface, (176, 138, 99), (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, (107, 78, 55), (self.handle_x, self.y + self.height // 2), self.radius)
        label_text = self.font.render(f"{self.label}: {int(self.value * 100)}%", True, (61, 40, 30))
        surface.blit(label_text, (self.x, self.y - 30))


class Checkbox:
    def __init__(self, x, y, label, checked=False):
        self.x = x
        self.y = y
        self.size = 28
        self.checked = checked
        self.label = label
        self.font = pygame.font.SysFont('comicsans', 28)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect = pygame.Rect(self.x, self.y, self.size, self.size)
            if rect.collidepoint(event.pos):
                self.checked = not self.checked

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surface, (61, 40, 30), rect, 3)
        if self.checked:
            pygame.draw.rect(surface, (107, 78, 55), rect.inflate(-6, -6))
        label_text = self.font.render(self.label, True, (61, 40, 30))
        surface.blit(label_text, (self.x + self.size + 12, self.y - 2))


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('comicsans', 32)

    def draw(self, surface, mouse_pos):
        color = (176, 138, 99) if self.rect.collidepoint(mouse_pos) else (192, 160, 121)
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        label = self.font.render(self.text, True, (61, 40, 30))
        surface.blit(label, (self.rect.centerx - label.get_width() // 2,
                             self.rect.centery - label.get_height() // 2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


# ======================#
# Settings Elements #
# ======================#
music_slider = Slider(450, 250, 400, "Music Volume", 0.5)
sfx_slider = Slider(450, 350, 400, "SFX Volume", 0.5)
mute_checkbox = Checkbox(450, 450, "Mute All Sound", False)
apply_button = Button(WIDTH // 2 - 80, 550, 160, 50, "Apply")

# ======================#
# Menu runner - callable from main entry
# ======================#
def run_menu():
    """Run the menu loop. Returns True if Start Game clicked, False if user closed window."""
    global menu_state
    running = True
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load('Musics/Main_Menu_Music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    except:
        pass

    while running:
        clock.tick(60)
        WIN.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Single Event Loop
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False

            if menu_state == 'main_menu':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    action = handle_button_click(mouse_pos)
                    if action == 'start':
                        return True

            elif menu_state == 'settings':
                music_slider.handle_event(event)
                sfx_slider.handle_event(event)
                mute_checkbox.handle_event(event)
                if apply_button.is_clicked(event):
                    if mute_checkbox.checked:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(music_slider.value)

        # Draw states
        if menu_state == 'main_menu':
            WIN.blit(title_text, title_rect)
            WIN.blit(footer_text, footer_rect)
            draw_buttons(mouse_pos)

        elif menu_state == 'settings':
            WIN.fill((255, 231, 184))
            title = font.render("Settings", True, (61, 40, 30))
            WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

            music_slider.draw(WIN)
            sfx_slider.draw(WIN)
            mute_checkbox.draw(WIN)
            apply_button.draw(WIN, mouse_pos)

            back_text = footer_font.render("Press SPACE to return", True, (61, 40, 30))
            WIN.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 60))

        elif menu_state == 'info':
            WIN.fill((255, 231, 184))
            lines = [
                "The Game Is Created By an Individual Named MD Niamul Islam Ankon",
                "Also known as ATHECAL. When I thought of creating this game, I was literally chilling",
                "at my computer and suddenly this idea snapped in my head. Although I’m a software",
                "developer, creating games is like a side hobby I do once a year—it’s really fun.",
                "I hope you enjoy this game as much as I enjoyed creating it. Happy Gaming!",
                "Press Space to return"
            ]
            for i, line in enumerate(lines):
                text = footer_font.render(line, True, (61, 40, 30))
                WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 28))

        elif menu_state == 'progression':
            WIN.fill((255, 231, 184))
            title = font.render("Progression", True, (61, 40, 30))
            WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))
            money_text = footer_font.render(f"Money: ${money}", True, (61, 40, 30))
            WIN.blit(money_text, (WIDTH // 2 - money_text.get_width() // 2, HEIGHT // 2 - 20))
            level_text = footer_font.render(f"Level: {level}", True, (61, 40, 30))
            WIN.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 + 20))
            info_text = footer_font.render("press space to go back", True, (61, 40, 30))
            WIN.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT - 60))

        # Space to go back
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            menu_state = 'main_menu'

        pygame.display.update()

    return False


if __name__ == '__main__':
    # Standalone run
    result = run_menu()
    if not result:
        pygame.quit()
