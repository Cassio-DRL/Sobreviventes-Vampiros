import pygame

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, pos, sprites_walking, escala, hit_points, ataque, defesa, velocidade_movimento, frame_rate):
        super().__init__()
        self.ultimo_hit = pygame.time.get_ticks()
        self.escala = escala
        self.sprite_andando = [pygame.transform.scale(pygame.image.load(sprite), self.escala) for sprite in sprites_walking]
        self.image = self.sprite_andando[0]
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(pos.x / 4, pos.y / 4, self.escala.x / 2, self.escala.y / 2)
        self.pos = pygame.math.Vector2(pos.x, pos.y)
        self.direcao = 'direita'

        # Stats
        self.hit_point_max = hit_points
        self.hit_points_atuais = self.hit_point_max
        self.ataque = ataque
        self.defesa = defesa
        self.velocidade_movimento = velocidade_movimento

        # Animação
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate_animacao = frame_rate

    def movimento(self, pos_jogador, dt):
        direcao_x = pos_jogador.x - self.pos.x
        direcao_y = pos_jogador.y - self.pos.y

        distancia = (direcao_x ** 2 + direcao_y ** 2) ** (1 / 2)
        direcao_x /= distancia
        direcao_y /= distancia

        self.pos.x += direcao_x * self.velocidade_movimento * dt
        self.pos.y += direcao_y * self.velocidade_movimento * dt

        if direcao_x > 0:
            if self.direcao != 'direita':
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.direcao = 'direita'
        else:
            if self.direcao != 'esquerda':
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.direcao = 'esquerda'

    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()
        if tick_atual - self.ultimo_tick > self.frame_rate_animacao:
            self.ultimo_tick = tick_atual
            self.frame = (self.frame + 1) % len(self.sprite_andando)
            self.image = self.sprite_andando[self.frame]

        self.rect.center = self.pos
        self.hitbox.center = self.rect.center

    def dar_dano(self, jogador):
        tick_atual = pygame.time.get_ticks()
        if self.hitbox.colliderect(jogador.rect) and tick_atual - self.ultimo_hit >= 1000:  # Cooldown de 1s
            self.ultimo_hit = tick_atual
            return self.ataque // jogador.defesa
        return 0

    def checar_hp(self):
        if self.hit_points_atuais <= 0:
            self.kill()


class Texugo(Inimigo):
    def __init__(self, pos):
        escala = pygame.math.Vector2(66, 66)
        sprite_andando = [f"Sprites/Texugo_Andando_{i+1}.png" for i in range(3)]

        # Stats
        hp = 20
        ataque = 50
        defesa = 5
        velocidade_movimento = 2

        # Animação
        frame_rate = 1000 // 9

        super().__init__(pos, sprite_andando, escala, hp, ataque, defesa, velocidade_movimento, frame_rate)

