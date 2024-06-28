import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load sounds
jellyfish_sting_sound = pygame.mixer.Sound("jellyfishsting.mp3")
trash_pickup_sound = pygame.mixer.Sound("trashpickup.mp3")

class TrashCan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("trash_can.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

class Hero(pygame.sprite.Sprite):
    def __init__(self, character):
        super().__init__()
        self.image = pygame.image.load(f"{character}_character.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.trash_picked_up = 0
        self.pickup_radius = 1
        self.level = 1
        self.highest_trash_picked_up = 0
        self.highest_level = 1

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Jellyfish(pygame.sprite.Sprite):
    def __init__(self, hero):
        super().__init__()
        self.image = pygame.image.load("jellyfish.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.hero = hero
        self.speed = random.randint(1, 3)
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def update(self):
        # Calculate vector from jellyfish to hero
        dx = self.hero.rect.centerx - self.rect.centerx
        dy = self.hero.rect.centery - self.rect.centery
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist != 0:
            dx = dx / dist
            dy = dy / dist

        # Update position based on direction and speed
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).contains(self.rect):
            self.direction = (-self.direction[0], -self.direction[1])

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Beach Cleanup Hero")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.state = "START"
        self.character = "woman"
        self.background = pygame.image.load("beach_background.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Load sounds
        self.jellyfish_sting_sound = pygame.mixer.Sound("jellyfishsting.mp3")
        self.trash_pickup_sound = pygame.mixer.Sound("trashpickup.mp3")

        # Initialize hero
        self.hero = Hero(self.character)

    def run(self):
        while True:
            if self.state == "START":
                self.start_menu()
            elif self.state == "INSTRUCTIONS":
                self.show_instructions()
            elif self.state == "GAME":
                self.play_game()

    def start_menu(self):
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        instructions_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
        highest_score_text = f"Highest Score: {self.hero.highest_trash_picked_up} (Level {self.hero.highest_level})"
        highest_score_rendered = self.font.render(highest_score_text, True, BLACK)

        while self.state == "START":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.state = "GAME"
                    elif instructions_button.collidepoint(event.pos):
                        self.state = "INSTRUCTIONS"

            self.screen.blit(self.background, (0, 0))
            pygame.draw.rect(self.screen, (0, 255, 0), start_button)
            pygame.draw.rect(self.screen, (0, 200, 255), instructions_button)

            title = self.font.render("Beach Cleanup Hero", True, BLACK)
            start_text = self.font.render("Start Game", True, BLACK)
            instructions_text = self.font.render("Instructions", True, BLACK)

            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            self.screen.blit(start_text, (start_button.x + 10, start_button.y + 10))
            self.screen.blit(instructions_text, (instructions_button.x + 10, instructions_button.y + 10))
            self.screen.blit(highest_score_rendered, (10, SCREEN_HEIGHT - 50))

            pygame.display.flip()
            self.clock.tick(FPS)

    def show_instructions(self):
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 50)

        while self.state == "INSTRUCTIONS":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        self.state = "START"

            self.screen.blit(self.background, (0, 0))
            pygame.draw.rect(self.screen, (200, 200, 200), back_button)

            instructions = [
                "Use arrow keys to move",
                "Collect trash to increase your score",
                "Avoid jellyfish - they eliminate you",
                "Reach 20 trash to level up",
                "Press 'End Game' to quit"
            ]

            for i, line in enumerate(instructions):
                text = self.font.render(line, True, BLACK)
                self.screen.blit(text, (50, 100 + i * 50))

            back_text = self.font.render("Back", True, BLACK)
            self.screen.blit(back_text, (back_button.x + 10, back_button.y + 10))

            pygame.display.flip()
            self.clock.tick(FPS)

    def play_game(self):
        self.all_sprites = pygame.sprite.Group(self.hero)
        self.trash_cans = pygame.sprite.Group()
        self.jellyfish = pygame.sprite.Group()

        for _ in range(10):
            trash = TrashCan()
            self.all_sprites.add(trash)
            self.trash_cans.add(trash)

        for _ in range(5):
            jelly = Jellyfish(self.hero)  # Pass hero instance to jellyfish
            self.all_sprites.add(jelly)
            self.jellyfish.add(jelly)

        end_button = pygame.Rect(SCREEN_WIDTH - 120, 10, 100, 50)

        while self.state == "GAME":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if end_button.collidepoint(event.pos):
                        self.state = "START"

            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            self.hero.move(dx, dy)

            for jelly in self.jellyfish:
                jelly.update()

            collected_trash = [t for t in self.trash_cans if pygame.sprite.collide_rect(self.hero, t)]
            for trash in collected_trash:
                self.hero.trash_picked_up += 1
                trash.kill()
                new_trash = TrashCan()
                self.all_sprites.add(new_trash)
                self.trash_cans.add(new_trash)
                self.trash_pickup_sound.play()  # Play trash pickup sound

            jellyfish_collisions = pygame.sprite.spritecollide(self.hero, self.jellyfish, False)
            for _ in jellyfish_collisions:
                self.hero.trash_picked_up = max(0, self.hero.trash_picked_up - 5)
                self.jellyfish_sting_sound.play()  # Play jellyfish sting sound
                self.state = "START"  # Game over state

                # Update highest score and level achieved
                if self.hero.trash_picked_up > self.hero.highest_trash_picked_up:
                    self.hero.highest_trash_picked_up = self.hero.trash_picked_up
                    self.hero.highest_level = self.hero.level

            if self.hero.trash_picked_up >= 20 * self.hero.level:
                self.hero.level += 1
                for jelly in self.jellyfish:
                    jelly.speed += 1  # Increase jellyfish speed with each level

            self.screen.blit(self.background, (0, 0))
            self.all_sprites.draw(self.screen)

            pygame.draw.rect(self.screen, (255, 0, 0), end_button)
            end_text = self.font.render("End Game", True, WHITE)
            self.screen.blit(end_text, (end_button.x + 5, end_button.y + 10))

            trash_text = self.font.render(f"Trash Picked Up: {self.hero.trash_picked_up}", True, BLACK)
            level_text = self.font.render(f"Level: {self.hero.level}", True, BLACK)
            self.screen.blit(trash_text, (10, 10))
            self.screen.blit(level_text, (10, 50))

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
