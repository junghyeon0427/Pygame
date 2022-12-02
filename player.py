import pygame


class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (64, 64))

        # [미션 2] 비행기가 총알에 맞았을 때 터지는 그림효과가 나타나게 한다.
        self.boom_image = pygame.image.load('boom.png')
        self.boom_image = pygame.transform.scale(self.boom_image, (80, 80))

        # [미션1] 비행기가 총알에 맞았을 때 효과음이 발생하도록 한다.
        self.soundObj = pygame.mixer.Sound('boom.mp3')

        # [미션 2], [미션 4] 터지는 그림효과와 무적을 위한 변수 설정
        self.unbeatable_flag = 0
        self.unbeatable_time = 0
        self.boom_flag = 0
        self.boom_time = 0

        # [미션6] 남은 생명력을 막대기와 숫자로 표현
        self.life = 5
        self.life_stk = '█████'
        
        self.pos = [x, y]
        self.to = [0, 0]
        self.angle = 0

    def goto(self, x, y):
        self.to[0] += x
        self.to[1] += y

    def update(self, dt, screen):
        width, height = screen.get_size()
        phw = self.image.get_width() / 2
        phh = self.image.get_height() / 2
        self.pos[0] = self.pos[0] + dt * self.to[0]
        self.pos[1] = self.pos[1] + dt * self.to[1]
        self.pos[0] = min(max(self.pos[0], phw), width-phw)
        self.pos[1] = min(max(self.pos[1], phh), height-phh)

        # [미션 4] 일정시간 후에 flag를 0으로 변경해서 무적이 끝나게끔 한다.
        self.unbeatable_time -= dt
        if self.unbeatable_time < 0:
            self.unbeatable_flag = 0

        # [미션 2] 일정시간 후에 flag를 0으로 변경해서 비행기 모양이 나오게끔 한다.
        self.boom_time -= dt
        if self.boom_time < 0:
            self.boom_flag = 0

    def boom(self, num):
        # flag == 0 -> 무적이 아니다
        # flag == 1 -> 무적이기 때문에 boom 함수가 실행 되어도 아무 일도 일어나지 않는다.
        if self.unbeatable_flag == 0:

            # [미션1] 충돌시 효과음 재생
            self.soundObj.play()

            # 변수로 받은 num가 총알의 종류를 의미한다. -> 차감되는 생명력을 다르게 한다.
            if num == 2:
                self.life -= 2
                self.life_stk = self.life_stk[:-2]
            else:
                self.life -= 1
                self.life_stk = self.life_stk[:-1]

            # 무적을 위해 flag를 1로 설정하고 시간도 설정
            self.unbeatable_flag = 1
            self.unbeatable_time = 700

            # 터지는 효과를 위해 flag를 1로 설정하고 시간도 설정
            self.boom_flag = 1
            self.boom_time = 700
        
    def draw(self, screen):

        if self.to == [-1, -1]:
            self.angle = 45
        elif self.to == [-1, 0]:
            self.angle = 90
        elif self.to == [-1, 1]:
            self.angle = 135
        elif self.to == [0, 1]:
            self.angle = 180
        elif self.to == [1, 1]:
            self.angle = 225
        elif self.to == [1, 0]:
            self.angle = 270
        elif self.to == [1, -1]:
            self.angle = 315
        elif self.to == [0, -1]:
            self.angle = 0
   
        # [미션 2] 총알에 맞지 않았을때는 기존의 비행기 모습을 그린다.
        if self.boom_flag == 0:
            rotated = pygame.transform.rotate(self.image, self.angle)
            calib_pos = (self.pos[0] - rotated.get_width() / 2,
                         self.pos[1] - rotated.get_height() / 2)
            screen.blit(rotated, calib_pos)
        # [미션 2] 비행기가 총알에 맞았을 때 터지는 그림을 그린다.
        else:
            calib_pos = (self.pos[0] - self.boom_image.get_width() / 2,
                         self.pos[1] - self.boom_image.get_height() / 2)
            # [미션 5] 무적시간 동안에는 2dt 마다 한번씩만 그림으로써 반짝이는 효과를 구현
            if self.unbeatable_flag == 1:
                if self.unbeatable_time % 2 == 0:
                    screen.blit(self.boom_image, calib_pos)
            else:
                screen.blit(self.boom_image, calib_pos)
