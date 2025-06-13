import pygame
import pymunk
import pymunk.pygame_util

from config import *
from sprites import Block, Bomb
from levels import level_1, level_2

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Physics Demolition Puzzler")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "main_menu"

        # Pymunk space
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)
        self.space.sleep_time_threshold = 0.5
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()

        # Game state
        self.bombs_available = 0
        self.placing_bombs = True
        self.level_complete = False
        self.score = 0
        self.game_over = False

        # Level Manager
        self.levels = [level_1, level_2]
        self.current_level_index = 0
        
        # Main menu buttons
        self.start_button_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 50, 200, 50)
        self.quit_button_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 20, 200, 50)
        self.menu_button_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 90, 200, 50)

        # Detonate button
        self.detonate_button_rect = pygame.Rect(WIDTH - 150, 50, 120, 50)

        # Collapse line
        self.collapse_line_y = 0

    def load_level(self, level_data):
        # Reset state
        self.all_sprites.empty()
        self.bombs.empty()
        for shape in list(self.space.shapes):
            self.space.remove(shape)
        for body in list(self.space.bodies):
            self.space.remove(body)
        
        self.bombs_available = level_data['bombs_available']
        self.collapse_line_y = level_data['collapse_line_y']
        self.placing_bombs = True
        self.level_complete = False
        self.score = 0
        self.game_over = False

        for block_data in level_data['blocks']:
            block = Block(
                pos=block_data['pos'],
                size=block_data['size'],
                space=self.space,
                material=block_data['material']
            )
            self.all_sprites.add(block)

        # Create static ground
        ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        ground_shape = pymunk.Segment(ground_body, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 5)
        ground_shape.friction = 1.0
        self.space.add(ground_body, ground_shape)

        # Let the world settle
        for _ in range(10):
            self.space.step(1 / FPS)

    def run(self):
        while self.running:
            if self.game_state == "main_menu":
                self.main_menu_events()
                self.main_menu_draw()
            elif self.game_state == "playing":
                self.events()
                self.update()
                self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def main_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    self.game_state = "playing"
                    self.load_level(self.levels[self.current_level_index])
                if self.quit_button_rect.collidepoint(event.pos):
                    self.running = False

    def main_menu_draw(self):
        self.screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        title_text = font.render("Demolition Puzzler", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        self.screen.blit(title_text, title_rect)

        # Start button
        pygame.draw.rect(self.screen, GREEN, self.start_button_rect)
        font = pygame.font.Font(None, 36)
        start_text = font.render("Start", True, WHITE)
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, start_text_rect)

        # Quit button
        pygame.draw.rect(self.screen, RED, self.quit_button_rect)
        quit_text = font.render("Quit", True, WHITE)
        quit_text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
        self.screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_button_rect.collidepoint(event.pos):
                        self.game_state = "main_menu"
                        self.game_over = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN and self.placing_bombs:
                if self.bombs_available > 0:
                    pos = pygame.mouse.get_pos()
                    bomb = Bomb(pos, (20, 20))
                    self.all_sprites.add(bomb)
                    self.bombs.add(bomb)
                    self.bombs_available -= 1
                if self.detonate_button_rect.collidepoint(event.pos):
                    self.detonate()

    def detonate(self):
        self.placing_bombs = False
        self.score -= len(self.bombs) * 50 # Penalty for each bomb used
        for bomb in self.bombs:
            for block_sprite in self.all_sprites:
                if isinstance(block_sprite, Block):
                    dist_vec = block_sprite.body.position - bomb.pos
                    distance = dist_vec.length
                    if distance < 250: # Explosion radius
                        impulse_strength = 500000 / (distance + 10)
                        block_sprite.body.apply_impulse_at_local_point(
                            impulse_strength * dist_vec.normalized(), (0, 0)
                        )
            bomb.kill()

    def update(self):
        self.space.step(1 / FPS)
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        # self.space.debug_draw(self.draw_options) # Optional: for debugging physics

        # Draw collapse line
        pygame.draw.line(self.screen, BLUE, (0, self.collapse_line_y), (WIDTH, self.collapse_line_y), 2)

        # Draw detonate button
        pygame.draw.rect(self.screen, RED, self.detonate_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Detonate", True, WHITE)
        text_rect = text.get_rect(center=self.detonate_button_rect.center)
        self.screen.blit(text, text_rect)

        # Draw bomb count
        bomb_text = font.render(f"Bombs: {self.bombs_available}", True, BLACK)
        self.screen.blit(bomb_text, (20, 20))

        # Draw score
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 50))

        # Check win/loss condition
        if not self.placing_bombs and not self.level_complete and not self.game_over:
            self.check_win_condition()
        
        if self.game_over:
            font = pygame.font.Font(None, 100)
            loss_text = font.render("YOU LOSE!", True, RED)
            loss_rect = loss_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            self.screen.blit(loss_text, loss_rect)

            # Menu button
            pygame.draw.rect(self.screen, BLUE, self.menu_button_rect)
            font = pygame.font.Font(None, 36)
            menu_text = font.render("Menu", True, WHITE)
            menu_text_rect = menu_text.get_rect(center=self.menu_button_rect.center)
            self.screen.blit(menu_text, menu_text_rect)

        pygame.display.flip()

    def check_win_condition(self):
        all_blocks_below_line = True
        for sprite in self.all_sprites:
            if isinstance(sprite, Block):
                if sprite.rect.bottom < self.collapse_line_y:
                    all_blocks_below_line = False
                    break
        
        if all_blocks_below_line:
            self.level_complete = True
            # Calculate score
            for sprite in self.all_sprites:
                if isinstance(sprite, Block):
                    self.score += 100
            font = pygame.font.Font(None, 100)
            win_text = font.render("YOU WIN!", True, GREEN)
            win_rect = win_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            self.screen.blit(win_text, win_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            self.next_level()
        elif self.bombs_available == 0 and not self.bombs and not self.level_complete:
            self.game_over = True
            pygame.time.wait(2000)
            self.load_level(self.levels[self.current_level_index])

    def next_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            self.load_level(self.levels[self.current_level_index])
        else:
            # Handle game completion
            self.running = False

if __name__ == "__main__":
    game = Game()
    game.run()
