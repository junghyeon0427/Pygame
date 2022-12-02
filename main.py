import time
import pygame
import random as rnd
from player import Player
from bullet import Bullet, Bullet2


def collision(obj1, obj2):
    dist = ((obj1.pos[0] - obj2.pos[0]) ** 2 + (obj1.pos[1] - obj2.pos[1]) ** 2) ** 0.5
    return dist < 20


def draw_text(txt, size, pos, color):
    # 폰트 변경
    font = pygame.font.Font('VCR_OSD_MONO.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)


# [미션 9] 사용자의 가장 오래 버틴 생존시간을 기록
def record(result, result_tmp):
    # 먼저 기존의 기록된 값을 가져와서 tmp 배열에 저장
    with open('result.txt', 'r') as f:
        result_tmp = f.readlines()
    f.close()

    # 맨 마지막 '\n'을 제외한 스트링을 result 배열에 저장
    for i in result_tmp:
        result.append(i[:-1])

    # 현재 점수를 result 배열에 저장 후 내림차순으로 정렬
    result.append(str(round(score, 5)))

    result.sort(reverse=True, key=float)

    # 만약 길이가 10을 넘는다면 (기록된 시간이 10을 넘는다는 뜻) 10개까지만 슬라이싱 해서 저장
    if len(result) > 10:
        result = result[:10]

    # 파일에 저장할때 줄을 띄우기 위해 배열애 '\n'을 추가
    for i in range(len(result)):
        result[i] = result[i] + '\n'

    # I/O 입출력 open 명령어로 result.txt에 상위 10개의 기록을 저장
    with open('result.txt', 'w') as f:
        f.writelines(result)
    f.close()


pygame.init()
WIDTH, HEIGHT = 1000, 800
flag = 0

pygame.display.set_caption("총알 피하기")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60

pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)

bg_image = pygame.image.load('bg.jpg')
image_width = 2053
image_height = 1500
bg_pos_x = 0
bg_pos_y = 0

# [미션3]를 위한 초깃값 설정
bg_pos = (image_width / 2, image_height / 2)

player = Player(WIDTH / 2, HEIGHT / 2)

result_stk = []
result_tmp_stk = []
top10 = []
top10_tmp = []

bullets = []
bullets2 = []

for i in range(1):
    bullets.append(Bullet(0, rnd.random() * HEIGHT, rnd.random() - 0.5, rnd.random() - 0.5))

for i in range(1):
    bullets2.append(Bullet2(0, rnd.random() * HEIGHT, rnd.random() - 0.5, rnd.random() - 0.5))

time_for_adding_bullets = 0
time_for_adding_bullets2 = 0

start_time = time.time()

gameover = False
running = True

while running:
    dt = clock.tick(FPS)

    time_for_adding_bullets += dt
    time_for_adding_bullets2 += dt

    # 이벤트 받는 부분
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.goto(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(1, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, -1)
            elif event.key == pygame.K_DOWN:
                player.goto(0, 1)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.goto(1, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(-1, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, 1)
            elif event.key == pygame.K_DOWN:
                player.goto(0, -1)

    player.update(dt, screen)

    bg_player_to_go = player.to

    # [미션 6] 플레이어의 현재 위치를 얻어와서 움직인 값과 현재 이미지의 위치를 더한다.
    bg_pos = (bg_pos[0] + bg_player_to_go[0] * dt * -0.05, bg_pos[1] + bg_player_to_go[1] * dt * -0.05)
    # [미션 6] 플레이어가 배경 사진을 넘어갈경우에 플레이어 이미지와 총알들이 겹쳐서 그려지는 것을 방지
    bg_pos = (max(min(0, bg_pos[0]), WIDTH - image_width), max(min(0, bg_pos[1]), HEIGHT - image_height))

    # 화면 갱신
    screen.blit(bg_image, bg_pos)
    player.draw(screen)

    # 총알 1 을 그린다.
    for b in bullets:
        b.update_and_draw(dt, screen)

    # 총알 2 를 그린다.
    for b2 in bullets2:
        b2.update_and_draw(dt, screen)

    for b in bullets:
        if collision(b, player):
            # [미션8] 빨간 총알(bullet 1)에 부딪혔을때는 생명력이 2개 감소
            player.boom(2)
            if player.life < 1:
                gameover = True

    for b2 in bullets2:
        if collision(b2, player):
            # [미션8] 노란 총알(bullet 2)에 부딪혔을때는 생명력이 1개 감소
            player.boom(1)
            if player.life < 1:
                gameover = True

    if gameover:
        draw_text("GAME OVER", 100, (WIDTH / 2 - 280, HEIGHT / 2 - 320), (255, 255, 255))
        txt = f"Time: {score:.5f}, Bullets: {len(bullets) + len(bullets2)}"
        draw_text(txt, 32, (WIDTH / 2 - 265, HEIGHT / 2 - 200), (255, 255, 255))

        # 게임 오버시에 result.txt에서 기록을 읽어오고, 배열에 저장
        with open('result.txt', 'r') as f:
            top10_tmp = f.readlines()
        f.close()

        for i in top10_tmp:
            top10.append(i[:-1])

        # flag를 이용해서 배열에 한번만 접근하게끔 설정 (처음에 실행하고 나면 flag가 1이 되어 다시 실행되지 않는다)
        if flag == 0:
            # 현재 점수를 배열에 추가하고 내림차순(오래버틴 시간)으로 정렬
            top10.append(str(round(score, 5)))
            top10.sort(reverse=True, key=float)
            flag = 1

        draw_text('* Top 10 List *', 40, (WIDTH / 2 - 180, HEIGHT / 2 - 100), (255, 255, 255))

        # [미션 10] 게임 오버시에 파일에 기록된 생존시간을 출력
        for i in range(len(top10)):
            # [미션 11] 오래버틴 10개의 기록 내에 현재 기록이 있을 경우에는 색깔을 노란색으로 표현
            if top10[i] == str(round(score, 5)):
                draw_text(str(i + 1) + ' : ' + top10[i] + ' <- Your Score !!!', 32,
                          (WIDTH / 2 - 200, HEIGHT / 2 + (i * 30)), (255, 255, 0))
            else:
                draw_text(str(i + 1) + ' : ' + top10[i], 32, (WIDTH / 2 - 180, HEIGHT / 2 + (i * 30)), (255, 255, 255))
            # 상위 10개만 출력
            if i == 9:
                break

    else:
        score = time.time() - start_time
        # [미션6] 남은 생명력을 막대기와 숫자로 표현
        txt = f"Time: {score:.2f}"
        txt2 = f"Bullets: {len(bullets) + len(bullets2)}, Lifes: {player.life}"
        txt3 = f"Life Stack: {player.life_stk}"
        draw_text(txt, 32, (10, 10), (255, 255, 255))
        draw_text(txt2, 32, (10, 45), (255, 255, 255))
        draw_text(txt3, 32, (10, 80), (0, 255, 255))

        if time_for_adding_bullets > 1000:
            bullets.append(Bullet(0, rnd.random() * HEIGHT, rnd.random() - 0.5, rnd.random() - 0.5))
            time_for_adding_bullets -= 1000

        if time_for_adding_bullets2 > 1000:
            bullets2.append(Bullet2(0, rnd.random() * HEIGHT, rnd.random() - 0.5, rnd.random() - 0.5))
            time_for_adding_bullets2 -= 1000

    pygame.display.update()

# 플레이어의 생존 시간을 기록
record(result_stk, result_tmp_stk)
