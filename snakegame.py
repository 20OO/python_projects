import random
import sys
import pygame

# Khởi tạo Pygame
pygame.init()

# Cấu hình màn hình và ô lưới
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Màu sắc (RGB)
COLOR_BG = (15, 23, 42)  # Xanh đen đậm
COLOR_GRID = (30, 41, 59)  # Đường lưới mờ
COLOR_SNAKE_HEAD = (34, 197, 94)  # Đầu rắn (Xanh lá sáng)
COLOR_SNAKE_BODY = (74, 222, 128)  # Thân rắn
COLOR_FOOD = (239, 68, 68)  # Thức ăn (Đỏ)
COLOR_TEXT = (241, 245, 249)  # Trắng xám

# Hướng di chuyển
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame:

  def __init__(self):
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game - Python Pro")
    self.clock = pygame.time.Clock()
    self.font_score = pygame.font.SysFont("Arial", 24, bold=True)
    self.font_over = pygame.font.SysFont("Arial", 40, bold=True)
    self.reset_game()

  def reset_game(self):
    self.snake = [
        (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
    ]
    self.direction = RIGHT
    self.next_direction = RIGHT
    self.score = 0
    self.game_over = False
    self.spawn_food()

  def spawn_food(self):
    while True:
      self.food = (
          random.randint(0, GRID_WIDTH - 1),
          random.randint(0, GRID_HEIGHT - 1),
      )
      if self.food not in self.snake:
        break

  def handle_input(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if self.game_over:
          if event.key == pygame.K_SPACE:
            self.reset_game()
        else:
          if (
              event.key in (pygame.K_UP, pygame.K_w)
              and self.direction != DOWN
          ):
            self.next_direction = UP
          elif (
              event.key in (pygame.K_DOWN, pygame.K_s)
              and self.direction != UP
          ):
            self.next_direction = DOWN
          elif (
              event.key in (pygame.K_LEFT, pygame.K_a)
              and self.direction != RIGHT
          ):
            self.next_direction = LEFT
          elif (
              event.key in (pygame.K_RIGHT, pygame.K_d)
              and self.direction != LEFT
          ):
            self.next_direction = RIGHT

  def update(self):
    if self.game_over:
      return

    self.direction = self.next_direction
    head_x, head_y = self.snake[0]
    dir_x, dir_y = self.direction
    new_head = (head_x + dir_x, head_y + dir_y)

    # Kiểm tra va chạm với tường
    if not (
        0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT
    ):
      self.game_over = True
      return

    # Kiểm tra va chạm với chính mình
    if new_head in self.snake:
      self.game_over = True
      return

    # Di chuyển rắn
    self.snake.insert(0, new_head)

    # Kiểm tra ăn mồi
    if new_head == self.food:
      self.score += 10
      self.spawn_food()
    else:
      self.snake.pop()

  def draw(self):
    self.screen.fill(COLOR_BG)

    # Vẽ đường lưới nền
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
      pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
      pygame.draw.line(self.screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

    # Vẽ mồi
    food_rect = pygame.Rect(
        self.food[0] * GRID_SIZE,
        self.food[1] * GRID_SIZE,
        GRID_SIZE - 2,
        GRID_SIZE - 2,
    )
    pygame.draw.rect(self.screen, COLOR_FOOD, food_rect, border_radius=4)

    # Vẽ rắn
    for i, (segment_x, segment_y) in enumerate(self.snake):
      rect = pygame.Rect(
          segment_x * GRID_SIZE,
          segment_y * GRID_SIZE,
          GRID_SIZE - 2,
          GRID_SIZE - 2,
      )
      color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
      pygame.draw.rect(self.screen, color, rect, border_radius=4)

    # Vẽ điểm số
    score_surface = self.font_score.render(
        f"Điểm: {self.score}", True, COLOR_TEXT
    )
    self.screen.blit(score_surface, (15, 10))

    # Vẽ thông báo Game Over
    if self.game_over:
      overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
      overlay.fill((0, 0, 0, 180))
      self.screen.blit(overlay, (0, 0))

      msg1 = self.font_over.render("GAME OVER", True, (239, 68, 68))
      msg2 = self.font_score.render(
          f"Tổng điểm: {self.score}", True, COLOR_TEXT
      )
      msg3 = self.font_score.render(
          "Nhấn [SPACE] để chơi lại", True, (148, 163, 184)
      )

      self.screen.blit(
          msg1, msg1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
      )
      self.screen.blit(
          msg2, msg2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
      )
      self.screen.blit(
          msg3, msg3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
      )

    pygame.display.flip()

  def run(self):
    while True:
      self.handle_input()
      self.update()
      self.draw()
      # Khống chế tốc độ khung hình (10 FPS = tốc độ di chuyển rắn)
      self.clock.tick(10)


if __name__ == "__main__":
  game = SnakeGame()
  game.run()
