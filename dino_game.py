import random
import math
from pygame import Rect

WIDTH = 600
HEIGHT = 400

game_state = "menu"
player_won = False
umbrella_collected = False

platforms = [
    Rect(0, 380, 600, 20),      # chao
    Rect(0, 300, 80, 16),
    Rect(100, 250, 120, 16),
    Rect(480, 280, 120, 16),
    Rect(510, 220, 120, 16),
    Rect(400, 170, 50, 16),
    Rect(250, 170, 80, 16),
    Rect(0, 110, 200, 16),
    Rect(280, 50, 350, 16),
]

class Hero(Actor):
    def __init__(self):
        super().__init__('idle1_right')
        self.pos = (100, 320)
        self.vel_y = 0
        self.speed = 4
        self.on_ground = True
        self.score = 0

        # animacao
        self.anim_timer = 0
        self.idle_frame = 0
        self.run_frame = 0
        self.direction = "right"
        self.is_moving = False

    def update(self):
        self.is_moving = False
        if keyboard.right:
            self.x += self.speed
            self.direction = "right"
            self.is_moving = True
        if keyboard.left:
            self.x -= self.speed
            self.direction = "left"
            self.is_moving = True

        # limita-se a tela
        self.x = max(20, min(WIDTH - 20, self.x))

        # pulo
        if keyboard.up and self.on_ground:
            self.vel_y = -10
            self.on_ground = False
            if not mute:
                sounds.jump.play()

        # gravidade
        self.vel_y += 0.5
        self.y += self.vel_y

        # colisao plataformas
        self.on_ground = False

        for plat in platforms:
            if (self.colliderect(plat) and
                self.vel_y >= 0 and
                self.bottom >= plat.top and
                self.y < plat.top + 10):

                self.bottom = plat.top
                self.vel_y = 0
                self.on_ground = True
                break

        # caiu fora
        if self.top > HEIGHT:
            self.pos = (100, 320)
            self.vel_y = 0
            self.on_ground = True

        # troca sprite
        self.anim_timer += 1

        if self.is_moving:
            if self.anim_timer % 6 == 0:
                self.run_frame = (self.run_frame + 1) % 6
            self.image = f'run{self.run_frame + 1}_{self.direction}'
        else:
            if self.anim_timer % 12 == 0:
                self.idle_frame = (self.idle_frame + 1) % 3
            self.image = f'idle{self.idle_frame + 1}_{self.direction}'

class Enemy(Actor):
    def __init__(self, platform):
        super().__init__('enemy_walk1_left')
        self.platform = platform
        self.bottom = platform.top
        self.x = platform.left + 20
        self.direction = 1
        self.anim_timer = 0
        self.frame = 0
        self.speed = 0.7  # inimigo +devagar

    def update(self):
        # vai e volta
        self.x += self.direction * self.speed

        if self.x > self.platform.right - 20:
            self.direction = -1
        if self.x < self.platform.left + 20:
            self.direction = 1

        # anima
        self.anim_timer += 1
        if self.anim_timer % 8 == 0:
            self.frame = (self.frame + 1) % 4

        direction = "right" if self.direction == 1 else "left"
        self.image = f'enemy_walk{self.frame + 1}_{direction}'

class Coin(Actor):
    def __init__(self, x, y):
        super().__init__('coin1', (x, y))
        self.collected = False
        self.anim_timer = 0
        self.frame = 0

    def update(self):
        if not self.collected:
            self.anim_timer += 1
            if self.anim_timer % 4 == 0:
                self.frame = (self.frame + 1) % 12
                self.image = f'coin{self.frame + 1}'


class Meteoro(Actor):
    def __init__(self):
        super().__init__('meteoro', (random.randint(20, WIDTH-20), -30))
        self.speed = random.uniform(1.5, 3.0)  # cai devagar
        self.rotation = random.uniform(-2, 2)  # gira um pouco

    def update(self):
        self.y += self.speed
        #self.angle += self.rotation  # gira enquanto cai

        if self.top > HEIGHT + 50:
            self.x = random.randint(20, WIDTH-20)
            self.y = -30
            self.speed = random.uniform(1.5, 3.0)

    def draw(self):
        super().draw()

# cria tudo
player = Hero()

# inimigos em algumass plataformas
enemies = [
    Enemy(platforms[2]),  # plataforma 2
    Enemy(platforms[7]),  # plataforma 7
    Enemy(platforms[3]),  # plataforma 3
]

# moedas
coins = [
    Coin(40, 284),
    Coin(160, 234),
    Coin(130, 234),
    Coin(540, 264),
    Coin(510, 264),
    Coin(570, 204),
    Coin(540, 204),
    Coin(425, 154),
    Coin(290, 154),
    Coin(50, 94),
    Coin(100, 94),
    Coin(150, 94),
    Coin(320, 34),
    Coin(450, 34),
    Coin(580, 34),
    Coin(200, 200),
    Coin(350, 100),
]

meteoros = []
for _ in range(4):  # 4 meteoros
    meteoros.append(Meteoro())

# botoes menu
BTN_W, BTN_H = 180, 40
btn_start = Rect(210, 200, BTN_W, BTN_H)
btn_mute = Rect(210, 260, BTN_W, BTN_H)
btn_exit = Rect(210, 320, BTN_W, BTN_H)

mute = False
music_playing = False

def play_music():
    global music_playing
    if not mute and not music_playing:
        sounds.music.play(-1)
        music_playing = True

def stop_music():
    global music_playing
    sounds.music.stop()
    music_playing = False

def draw_menu():
    screen.clear()
    screen.fill((40, 40, 60))

    screen.draw.text("DINO GAME", center=(300, 100), fontsize=64, color="white")
    screen.draw.text("SETA: anda e pula", center=(300, 150), fontsize=24, color="lightblue")

    # botoes
    screen.draw.filled_rect(btn_start, "green")
    screen.draw.filled_rect(btn_mute, "blue")
    screen.draw.filled_rect(btn_exit, "red")

    screen.draw.text("COMECAR", center=btn_start.center, fontsize=28, color="white")
    mute_text = "MUDO: SIM" if mute else "MUDO: NAO"
    screen.draw.text(mute_text, center=btn_mute.center, fontsize=28, color="white")
    screen.draw.text("SAIR", center=btn_exit.center, fontsize=28, color="white")

def on_mouse_down(pos):
    global game_state, mute, player_won, umbrella_collected

    if game_state == "menu":
        if btn_start.collidepoint(pos):
            game_state = "game"
            player_won = False
            umbrella_collected = False
            # reseta moedas
            for coin in coins:
                coin.collected = False
            player.pos = (100, 320)
            player.score = 0
            play_music()
        elif btn_mute.collidepoint(pos):
            mute = not mute
            if mute: stop_music()
            else: play_music()
        elif btn_exit.collidepoint(pos):
            quit()

def draw():
    screen.clear()

    if game_state == "menu":
        draw_menu()
    elif player_won:  # tela de vitoria
        screen.fill((50, 200, 50))
        screen.draw.text("VITORIA!", center=(300, 150), fontsize=72, color="gold")
        screen.draw.text("Voce sobreviveuu!!! :)", center=(300, 220), fontsize=32, color="white")
    else:
        # jogo
        screen.fill((135, 206, 250))

        for y in range(0, HEIGHT, 750):
            screen.blit('bg', (0, y))

        # plataformas
        for plat in platforms:
            tile_size = 16
            for x in range(plat.x, plat.x + plat.width, tile_size):
                for y in range(plat.y, plat.y + plat.height, tile_size):
                    if x < plat.x + plat.width and y < plat.y + plat.height:
                        screen.blit('grass', (x, y))

        collected = sum(1 for c in coins if c.collected)
        if collected == len(coins):
            screen.blit('umbrella', (570, 204))


        # moedas
        for coin in coins:
            if not coin.collected:
                coin.draw()

        # personagens
        player.draw()
        for enemy in enemies:
            enemy.draw()

        # meteoros
        collected = sum(1 for c in coins if c.collected)
        if collected == len(coins):  # só desenha se pegou todas moedas
            for meteoro in meteoros:
                meteoro.draw()

        # mostra pontos
        collected = sum(1 for c in coins if c.collected)
        screen.draw.text(f"PONTOS: {player.score}", (10, 10), fontsize=28, color="white")
        screen.draw.text(f"MOEDAS: {collected}/{len(coins)}", (10, 40), fontsize=28, color="gold")

def update():
    global game_state, player_won, umbrella_collected

    if game_state == "game" and not player_won:
        player.update()

        # inimigos
        for enemy in enemies:
            enemy.update()
            if player.colliderect(enemy):
                if not mute:
                    sounds.hurt.play()
                player.pos = (100, 320)
                player.vel_y = 0
                player.on_ground = True

        # verifica moedas
        all_collected = True
        for coin in coins:
            if not coin.collected:
                coin.update()
                if player.colliderect(coin):
                    coin.collected = True
                    player.score += 10
                    if not mute:
                        sounds.coin.play()
            if not coin.collected:
                all_collected = False

        # meteoros só caem se pegou todas moedas
        for meteoro in meteoros:
            if all_collected:
                meteoro.update()
                if player.colliderect(meteoro):
                    if not mute:
                        sounds.hurt.play()
                    player.pos = (100, 320)
                    player.vel_y = 0
                    player.on_ground = True

        # VITORIA
        if all_collected and not umbrella_collected:
            umbrella_rect = Rect(570, 204, 16, 16)
            if player.colliderect(umbrella_rect):
                umbrella_collected = True
                player_won = True
                clock.schedule_unique(volta_menu, 3.0)

def volta_menu():
    global game_state, player_won
    game_state = "menu"
    player_won = False
    stop_music()

def on_key_down(key):
    global game_state
    if key == keys.ESCAPE and game_state == "game":
        game_state = "menu"
        stop_music()
