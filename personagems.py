import pygame
class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos_x_jogador, pos_y_jogador, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade, frame_rate):
        super().__init__()
        self.escala = escala
        self.sprite_idle = pygame.transform.scale(pygame.image.load(sprite_idle), self.escala)
        self.sprite_andando = [pygame.transform.scale(pygame.image.load(sprite), self.escala) for sprite in sprite_andando]
        self.image = self.sprite_idle
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(pos_x_jogador/4, pos_y_jogador/4, 33, 33)
        self.pos = pygame.math.Vector2(pos_x_jogador, pos_y_jogador)
        self.direcao = "direita"

        # Stats
        self.hit_point_max = hp
        self.hit_points_atuais = self.hit_point_max
        self.ataque = ataque
        self.defesa = defesa
        self.velocidade_movimento = velocidade
        self.nivel = 1
        self.exp = 0
        self.exp_para_proximo_nivel = int(100 * (1 + self.nivel ** 1.1))

        # Animação
        self.andando = False
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate_animacao = frame_rate

    def movimento(self, dt):
        keys = pygame.key.get_pressed()
        self.andando = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos.x -= self.velocidade_movimento * dt
            if self.direcao != 'esquerda':
                self.direcao = 'esquerda'
                self.sprite_idle = pygame.transform.flip(self.sprite_idle, True, False)
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
            self.andando = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos.x += self.velocidade_movimento * dt
            if self.direcao != 'direita':
                self.direcao = 'direita'
                self.sprite_idle = pygame.transform.flip(self.sprite_idle, True, False)
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
            self.andando = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pos.y -= self.velocidade_movimento * dt
            self.andando = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pos.y += self.velocidade_movimento * dt
            self.andando = True

    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()
        if self.andando:
            if tick_atual - self.ultimo_tick > self.frame_rate_animacao:
                self.ultimo_tick = tick_atual
                self.frame = (self.frame + 1) % len(self.sprite_andando)
                self.image = self.sprite_andando[self.frame]
        else:
            self.image = self.sprite_idle

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def nivel_update(self):
        if self.exp >= self.exp_para_proximo_nivel:
            self.exp -= self.exp_para_proximo_nivel
            self.nivel += 1
            self.exp_para_proximo_nivel = int(100 * (1 + self.nivel ** 1.1))

class Chicote(Jogador):
    def __init__(self, pos_x, pos_y):
        escala = (66, 66)
        sprite_idle = "Sprites/Player_Idle.png"
        sprite_andando = [f"Sprites/Player_andando_{i+1}.png" for i in range(3)]

        # Stats
        hp = 100
        ataque = 5
        defesa = 5
        velocidade_movimento = 3

        # Animação
        frame_rate = 1000 // 9

        super().__init__(pos_x, pos_y, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate)




