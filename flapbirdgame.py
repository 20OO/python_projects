import random
import sys
import pygame

# Khởi tạo Pygame
pygame.init()

# Cấu hình kích thước cửa sổ
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Màu sắc (RGB)
COLOR_BG = (135, 206, 235)  # Màu xanh trời
COLOR_GROUND = (222, 184, 135)  # Màu đất
COLOR_GROUND_LINE = (34, 139, 34)  # Đường cỏ xanh
COLOR_BIRD = (255, 215, 0)  # Vàng chim
COLOR_PIPE = (46, 139, 87)  # Xanh ống nước
COLOR_TEXT = (255, 255, 255)  # Trắng


class FlappyBirdGame:

  def __init__(self):
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird - Python Pro")
    self.clock = pygame.time.Clock()

    self.font_score = pygame.font.SysFont("Arial", 32, bold=True)
    self.font_over = pygame.font.SysFont("Arial", 40, bold=True)
    self.font_small = pygame.font.SysFont("Arial", 18, bold=True)

    self.reset_game()

  def reset_game(self):
    # Thông số chú chim
    self.bird_x = 80
    self.bird_y = SCREEN_HEIGHT // 2
    self.bird_radius = 15
    self.bird_velocity = 0
    self.gravity = 0.5
    self.jump_strength = -8.5

    # Thông số ống cống
    self.pipes = []
    self.pipe_width = 70
    self.pipe_gap = 160  # Khoảng trống giữa ống trên và ống dưới
    self.pipe_speed = 3.5

    self.score = 0
    self.game_over = False

    # Tạo ống đầu tiên
    self.spawn_pipe()

  def spawn_pipe(self):
    # Chiều cao ngẫu nhiên cho ống trên
    min_height = 50
    max_height = SCREEN_HEIGHT - self.pipe_gap - 150
    top_height = random.randint(min_height, max_height)

    # Lưu trữ [rect_top, rect_bottom, đã_tính_điểm]
    top_rect = pygame.Rect(SCREEN_WIDTH, 0, self.pipe_width, top_height)
    bottom_rect = pygame.Rect(
        SCREEN_WIDTH,
        top_height + self.pipe_gap,
        self.pipe_width,
        SCREEN_HEIGHT - (top_height + self.pipe_gap),
    )
    self.pipes.append([top_rect, bottom_rect, False])

  def handle_input(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          if self.game_over:
            self.reset_game()
          else:
            self.bird_velocity = self.jump_strength

  def update(self):
    if self.game_over:
      return

    # Cập nhật chuyển động chim
    self.bird_velocity += self.gravity
    self.bird_y += self.bird_velocity

    # Kiểm tra va chạm với mặt đất hoặc bay quá cao
    if (
        self.bird_y + self.bird_radius >= SCREEN_HEIGHT - 100
    ):  # 100 là chiều cao mặt đất
      self.bird_y = SCREEN_HEIGHT - 100 - self.bird_radius
      self.game_over = True
    if self.bird_y - self.bird_radius <= 0:
      self.bird_y = self.bird_radius

    # Di chuyển ống cống
    for pipe in self.pipes:
      pipe[0].x -= int(self.pipe_speed)
      pipe[1].x -= int(self.pipe_speed)

      # Kiểm tra chim vượt qua ống để tính điểm
      if not pipe[2] and pipe[0].x + self.pipe_width < self.bird_x:
        self.score += 1
        pipe[2] = True

    # Xóa ống đi khuất màn hình và tạo ống mới
    if self.pipes and self.pipes[0][0].x + self.pipe_width < 0:
      self.pipes.pop(0)

    # Tạo ống tiếp theo dựa vào khoảng cách
    if len(self.pipes) == 0 or self.pipes[-1][0].x < SCREEN_WIDTH - 220:
      self.spawn_pipe()

    # Kiểm tra va chạm giữa chim và ống
    bird_rect = pygame.Rect(
        self.bird_x - self.bird_radius,
        self.bird_y - self.bird_radius,
        self.bird_radius * 2,
        self.bird_radius * 2,
    )
    for pipe in self.pipes:
      if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
        self.game_over = True

  def draw(self):
    # Vẽ bầu trời nền
    self.screen.fill(COLOR_BG)

    # Vẽ ống cống
    for pipe in self.pipes:
      pygame.draw.rect(self.screen, COLOR_PIPE, pipe[0], border_radius=5)
      pygame.draw.rect(self.screen, COLOR_PIPE, pipe[1], border_radius=5)

    # Vẽ mặt đất
    ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
    pygame.draw.rect(self.screen, COLOR_GROUND, ground_rect)
    pygame.draw.line(
        self.screen,
        COLOR_GROUND_LINE,
        (0, SCREEN_HEIGHT - 100),
        (SCREEN_WIDTH, SCREEN_HEIGHT - 100),
        6,
    )

    # Vẽ chú chim
    pygame.draw.circle(
        self.screen,
        COLOR_BIRD,
        (int(self.bird_x), int(self.bird_y)),
        self.bird_radius,
    )
    # Mắt chim
    pygame.draw.circle(
        self.screen,
        (0, 0, 0),
        (int(self.bird_x) + 5, int(self.bird_y) - 4),
        3,
    )

    # Hiển thị điểm số khi đang chơi
    score_surface = self.font_score.render(str(self.score), True, COLOR_TEXT)
    self.screen.blit(
        score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 40)
    )

    # Giao diện Game Over
    if self.game_over:
      overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
      overlay.fill((0, 0, 0, 150))
      self.screen.blit(overlay, (0, 0))

      msg_over = self.font_over.render("GAME OVER", True, (239, 68, 68))
      msg_score = self.font_score.render(
          f"Điểm của bạn: {self.score}", True, COLOR_TEXT
      )
      msg_restart = self.font_small.render(
          "Nhấn [SPACE] để chơi lại", True, (200, 200, 200)
      )

      self.screen.blit(
          msg_over,
          msg_over.get_rect(
              center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
          ),
      )
      self.screen.blit(
          msg_score,
          msg_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
      )
      self.screen.blit(
          msg_restart,
          msg_restart.get_rect(
              center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
          ),
      )

    pygame.display.flip()

  def run(self):
    while True:
      self.handle_input()
      self.update()
      self.draw()
      self.clock.tick(60)  # Khóa tốc độ 60 FPS giúp game mượt mà


if __name__ == "__main__":
  game = FlappyBirdGame()
  game.run()
