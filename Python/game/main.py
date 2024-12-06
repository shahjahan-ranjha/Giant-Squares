import pygame
import random
from settings import WIDTH, HEIGHT, WHITE, BLACK, GREEN, ORANGE, RED, FPS
from player import Player
from enemy import Enemy
from item import Item
from utils import check_collision

# Initialize pygame
pygame.init()

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Game")

# Clock for frame rate
clock = pygame.time.Clock()

# Create game objects
player = Player(100, 500)

# Generate more enemies with random positions
enemies = [Enemy(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(10)]

# Place items near the enemies
items = []
for enemy in enemies:
    offset_x = random.choice([-30, 30])
    offset_y = random.choice([-30, 30])
    items.append(Item(enemy.rect.x + offset_x, enemy.rect.y + offset_y))

inventory = []


# Load sounds
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except FileNotFoundError:
        print(f"Warning: Sound file not found: {path}")
        return None


collect_sound = load_sound("assets/sounds/collect.wav")
hit_sound = load_sound("assets/sounds/hit.wav")

# Load background music
try:
    pygame.mixer.music.load("assets/sounds/bg_music.wav")
    pygame.mixer.music.play(-1)  # Loop indefinitely
except FileNotFoundError:
    print("Warning: Background music not found.")

# Font for text
font = pygame.font.Font(None, 36)


def draw_health_bar():
    """Draw health bar with color changing based on health."""
    if player.health > 60:
        health_color = GREEN
    elif player.health > 30:
        health_color = ORANGE
    else:
        health_color = RED

    pygame.draw.rect(screen, RED, (10, 10, 200, 20))  # Max health
    pygame.draw.rect(screen, health_color, (10, 10, player.health * 2, 20))  # Current health


def draw():
    """Draw all game elements."""
    screen.fill(WHITE)

    # Draw game objects
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for item in items:
        item.draw(screen)

    # Draw health bar
    draw_health_bar()

    # Display health, energy, and strength
    health_text = font.render(f"Health: {player.health}", True, BLACK)
    energy_text = font.render(f"Energy: {int(player.energy)}", True, BLACK)
    strength_text = font.render(f"Strength: {player.strength}", True, BLACK)
    screen.blit(health_text, (10, 40))
    screen.blit(energy_text, (10, 70))
    screen.blit(strength_text, (10, 100))

    # Display inventory
    inventory_text = font.render(f"Inventory: {len(inventory)} items", True, BLACK)
    screen.blit(inventory_text, (10, 130))

    pygame.display.flip()


def use_item():
    """Use an item from the inventory."""
    if inventory:
        item = inventory.pop(0)  # Remove the first item in the inventory
        if item == "health":
            player.health = min(player.health + 20, 100)  # Increase health
            print("Used health item. Health increased!")
        elif item == "strength":
            player.strength += 5  # Increase strength
            print("Used strength item. Strength increased!")
    else:
        print("No items in inventory!")


def show_victory_screen():
    """Display the Victory screen."""
    screen.fill(WHITE)
    victory_font = pygame.font.Font(None, 72)
    victory_text = victory_font.render("You Win!", True, GREEN)
    instruction_text = font.render("Press R to Restart or Q to Quit", True, BLACK)

    # Center the victory message
    victory_rect = victory_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(victory_text, victory_rect)
    screen.blit(instruction_text, instruction_rect)
    pygame.display.flip()

    # Wait for player input to restart or quit
    wait_for_restart_or_quit()


def show_game_over_screen():
    """Display the Game Over screen."""
    screen.fill(WHITE)
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over", True, RED)
    instruction_text = font.render("Press R to Restart or Q to Quit", True, BLACK)

    # Center the game over message
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(instruction_text, instruction_rect)
    pygame.display.flip()

    # Wait for player input to restart or quit
    wait_for_restart_or_quit()


def wait_for_restart_or_quit():
    """Wait for the player to restart or quit the game."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    restart_game()  # Restart the main game loop
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    exit()


def restart_game():
    """Reset all game objects and restart the game."""
    global player, enemies, items, inventory
    player = Player(100, 500)
    enemies = [Enemy(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(10)]
    items = []
    for enemy in enemies:
        offset_x = random.choice([-30, 30])
        offset_y = random.choice([-30, 30])
        items.append(Item(enemy.rect.x + offset_x, enemy.rect.y + offset_y))
    inventory = []
    main()  # Restart the game loop


def main():
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Use an item when the player presses the 'U' key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    use_item()

        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Enemy interactions
        for enemy in enemies:
            enemy.move()
            if check_collision(player.rect, enemy.rect):
                player.health -= 1
                if player.health <= 0:
                    show_game_over_screen()  # Show Game Over screen
                    return  # Exit the main loop
                if hit_sound:
                    hit_sound.play()

        # Item collection and effects
        for item in items[:]:
            if check_collision(player.rect, item.rect):
                # Add collected item to inventory with a random type
                inventory.append(random.choice(["health", "strength"]))
                items.remove(item)
                if collect_sound:
                    collect_sound.play()

        # Check win condition
        if not items:
            show_victory_screen()  # Show Victory screen
            return  # Exit the main loop

        draw()

    pygame.quit()


if __name__ == "__main__":
    main()
