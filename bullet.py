import pygame


# [미션 7] 종류별로 다른 총알 클래스 생성
class Bullet:
    def __init__(self, x, y, to_x, to_y):
        self.pos = [x, y]
        self.to = [to_x, to_y]
        self.radius = 8
        self.color = (255, 0, 0)

    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = (self.pos[0] + self.to[0] * dt) % width
        self.pos[1] = (self.pos[1] + self.to[1] * dt) % height
        pygame.draw.circle(screen, self.color, self.pos, self.radius)


# [미션 7] 종류별로 다른 총알 클래스 생성
class Bullet2:
    def __init__(self, x, y, to_x, to_y):
        self.pos = [x, y]
        self.to = [to_x, to_y]
        # 크기와 색깔을 구분
        self.radius = 5
        self.color = (255, 255, 0)

    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = (self.pos[0] + self.to[0] * dt) % width
        self.pos[1] = (self.pos[1] + self.to[1] * dt) % height
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
