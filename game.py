import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # For sound effects

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I'm Going Mental!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (70, 140, 200)
SKIN = (240, 200, 160)

# Load sound effects (replace with your own files)
try:
    mission_complete_sound = pygame.mixer.Sound("mission_complete.wav")
    level_change_sound = pygame.mixer.Sound("level_change.wav")
except:
    # Create dummy sounds if files not found
    silent_sound = bytearray([80, 75, 3, 4])  # Minimal sound data
    mission_complete_sound = pygame.mixer.Sound(buffer=silent_sound)
    level_change_sound = pygame.mixer.Sound(buffer=silent_sound)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        self.animation_frames = 4
        
        # Create animation frames
        for i in range(self.animation_frames):
            surf = pygame.Surface((40, 70), pygame.SRCALPHA)
            
            # Draw body parts
            pygame.draw.circle(surf, SKIN, (20, 15), 10)  # Head
            pygame.draw.rect(surf, BLUE, (15, 25, 10, 25))  # Body
            
            # Animated legs
            leg_offset = i * 2
            pygame.draw.line(surf, BLACK, (17, 50), (10 + leg_offset, 65), 3)
            pygame.draw.line(surf, BLACK, (23, 50), (30 - leg_offset, 65), 3)
            
            # Arms
            arm_angle = i * 15
            arm1_x = 20 + 15 * pygame.math.Vector2(1, 0).rotate(arm_angle).x
            arm1_y = 30 + 15 * pygame.math.Vector2(1, 0).rotate(arm_angle).y
            arm2_x = 20 + 15 * pygame.math.Vector2(1, 0).rotate(-arm_angle).x
            arm2_y = 30 + 15 * pygame.math.Vector2(1, 0).rotate(-arm_angle).y
            
            pygame.draw.line(surf, BLACK, (20, 30), (arm1_x, arm1_y), 3)
            pygame.draw.line(surf, BLACK, (20, 30), (arm2_x, arm2_y), 3)
            
            self.sprites.append(surf)
        
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.animation_speed = 0.2
        self.facing_right = True

    def update(self, keys):
        # Movement
        moving = False
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            moving = True
            self.facing_right = False
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            moving = True
            self.facing_right = True
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            moving = True
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            moving = True

        # Animation
        if moving:
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
            
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.sprites[0]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

        # Screen boundaries
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

class Level:
    def __init__(self, name, mission, bg_color):
        self.name = name
        self.mission = mission
        self.bg_color = bg_color
        self.completed = False
        self.obstacles = pygame.sprite.Group()
        self.setup_obstacles()
        
    def setup_obstacles(self):
        for _ in range(random.randint(3, 7)):
            obstacle = pygame.sprite.Sprite()
            w, h = random.randint(30, 80), random.randint(30, 80)
            obstacle.image = pygame.Surface((w, h))
            obstacle.image.fill((random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)))
            obstacle.rect = obstacle.image.get_rect()
            obstacle.rect.x = random.randint(0, WIDTH - 100)
            obstacle.rect.y = random.randint(0, HEIGHT - 100)
            self.obstacles.add(obstacle)
    
    def draw(self, screen):
        screen.fill(self.bg_color)
        self.obstacles.draw(screen)
        
        font = pygame.font.SysFont('Arial', 36)
        screen.blit(font.render(f"Level: {self.name}", True, BLACK), (20, 20))
        screen.blit(font.render(f"Mission: {self.mission}", True, BLACK), (20, 60))

def create_levels():
    return [
        Level("Theater", "Run around the stage doing crazy poses!", (200, 200, 255)),
        Level("Museum", "Steal a dinosaur bone!", (255, 200, 200)),
        Level("Political Event", "Give the politician a wedgie!", (200, 255, 200)),
        Level("Dance Hall", "Breakdance on the chandelier!", (255, 255, 100)),
        Level("Library", "Build a book fort!", (200, 150, 100)),
        Level("Japanese Tea Garden", "Flip all the tea cups!", (100, 200, 150)),
        Level("College Campus", "Set off the fire alarm in class!", (150, 100, 200)),
        Level("Airport", "Steal a plane and do wheelies!", (100, 100, 255))
    ]

def show_game_over_screen():
    screen.fill((0, 0, 0))
    font_large = pygame.font.SysFont('Arial', 72)
    font_small = pygame.font.SysFont('Arial', 36)
    
    texts = [
        ("GAME COMPLETED!", (255, 255, 0), HEIGHT//3),
        ("You've gone completely mental!", WHITE, HEIGHT//2),
        ("Press any key to quit", WHITE, HEIGHT*2//3)
    ]
    
    for text, color, y in texts:
        rendered = font_large.render(text, True, color) if text == texts[0][0] else font_small.render(text, True, color)
        screen.blit(rendered, (WIDTH//2 - rendered.get_width()//2, y))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYUP:
                waiting = False
    return True

def main():
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    levels = create_levels()
    current_level = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not levels[current_level].completed:
                levels[current_level].completed = True
                mission_complete_sound.play()
                if current_level < len(levels) - 1:
                    current_level += 1
                    level_change_sound.play()
                    player.rect.center = (WIDTH // 2, HEIGHT // 2)
                else:
                    if not show_game_over_screen():
                        running = False
                    else:
                        running = False

        player.update(pygame.key.get_pressed())
        
        if pygame.sprite.spritecollide(player, levels[current_level].obstacles, False):
            if pygame.key.get_pressed()[pygame.K_a]: player.rect.x += player.speed
            if pygame.key.get_pressed()[pygame.K_d]: player.rect.x -= player.speed
            if pygame.key.get_pressed()[pygame.K_w]: player.rect.y += player.speed
            if pygame.key.get_pressed()[pygame.K_s]: player.rect.y -= player.speed
        
        levels[current_level].draw(screen)
        all_sprites.draw(screen)

        if levels[current_level].completed and current_level < len(levels) - 1:
            font = pygame.font.SysFont('Arial', 36)
            screen.blit(font.render("MISSION COMPLETE! Press SPACE for next level.", True, RED), 
                       (WIDTH // 4, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()