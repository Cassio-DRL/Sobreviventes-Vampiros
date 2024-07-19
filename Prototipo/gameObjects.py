import pygame
class Coletavel:
    pass
class Inimigo:
    pass
class Ataque:
    pass
class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos_x_jogador, pos_y_jogador):
        super().__init__()
        self.escala = (66, 66)
        self.sprite_idle = pygame.transform.scale(pygame.image.load("Sprites/Player_Idle.png"), self.escala)
        self.sprite_andando = [
            pygame.transform.scale(pygame.image.load(f"Sprites/Player_andando_{i+1}.png"), self.escala) for i in range(3)]
        self.image = self.sprite_idle
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(pos_x_jogador, pos_y_jogador)
        self.rect.center = self.pos
        self.direcao = "direita"

        # Stats
        self.hit_point_max = 100
        self.hit_points_atuais = self.hit_point_max
        self.ataque = 5
        self.defesa = 5
        self.velocidade_movimento = 3
        self.nivel = 1

        # Animação
        self.andando = False
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate_animacao = 1000 // 9

    def movemento(self, dt):
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

class Moeda(pygame.sprite.Sprite, Coletavel):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.escala = (25, 25)
        self.sprite_girando = [
            pygame.transform.scale(pygame.image.load("Sprites/Moeda_girando_1.png"), self.escala),
            pygame.transform.scale(pygame.image.load("Sprites/Moeda_girando_2.png"), self.escala),
            pygame.transform.scale(pygame.image.load("Sprites/Moeda_girando_3.png"), self.escala),
            pygame.transform.scale(pygame.image.load("Sprites/Moeda_girando_4.png"), self.escala),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load("Sprites/Moeda_girando_3.png"), self.escala), True, False),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load("Sprites/Moeda_girando_2.png"), self.escala), True, False),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load("Sprites/Moeda_girando_1.png"), self.escala), True, False)
        ]
        self.image = self.sprite_girando[0]
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(pos_x, pos_y)
        self.rect.center = self.pos

        # Animação
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate_animacao = 1000 // 11

    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()
        if tick_atual - self.ultimo_tick > self.frame_rate_animacao:
            self.ultimo_tick = tick_atual
            self.frame = (self.frame + 1) % len(self.sprite_girando)
            self.image = self.sprite_girando[self.frame]

    def checar_colisao(self, jogador):
        contagem = 0
        if jogador.rect.contains(self.rect):
            contagem = 1
            self.kill()
        return contagem

class Cura(pygame.sprite.Sprite, Coletavel):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.escala = (25, 25)
        self.image = pygame.transform.scale(pygame.image.load("Sprites/pocao grande.png"), self.escala)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(pos_x, pos_y)
        self.rect.center = self.pos

    def checar_colisao(self, jogador):
        cura = 0
        if jogador.rect.contains(self.rect):
            cura = 25
            self.kill()
        return cura

class Badger(pygame.sprite.Sprite, Inimigo):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.ultimo_hit = pygame.time.get_ticks()
        self.escala = (66, 66)
        self.sprite_idle = pygame.transform.scale(pygame.image.load("Sprites/Badger_Idle.png"), self.escala)
        self.sprite_andando = [
            pygame.transform.scale(pygame.image.load(f"Sprites/Badger_Andando_{i+1}.png"), self.escala) for i in range(3)]
        self.image = self.sprite_idle
        self.rect = pygame.Rect(pos_x, pos_y, 33, 33)
        self.pos = pygame.math.Vector2(pos_x, pos_y)
        self.rect.center = self.pos
        self.direcao = 'direita'

        # Stats
        self.hit_point_max = 20
        self.hit_points_atuais = self.hit_point_max
        self.ataque = 50
        self.defesa = 5
        self.velocidade_movimento = 2

        # Animação
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate_animacao = 1000 // 9

    def movimento(self, pos_jogador, dt):
        direcao_x = pos_jogador.x - self.pos.x
        direcao_y = pos_jogador.y - self.pos.y

        distancia = (direcao_x**2 + direcao_y**2)**(1/2)
        direcao_x /= distancia
        direcao_y /= distancia

        self.pos.x += direcao_x * self.velocidade_movimento * dt
        self.pos.y += direcao_y * self.velocidade_movimento * dt

        if direcao_x > 0:
            if self.direcao != 'direita':
                pygame.transform.flip(self.sprite_idle, True, False)
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.direcao = 'direita'
        else:
            if self.direcao != 'esquerda':
                pygame.transform.flip(self.sprite_idle, True, False)
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.direcao = 'esquerda'

    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()
        if tick_atual - self.ultimo_tick > self.frame_rate_animacao:
            self.ultimo_tick = tick_atual
            self.frame = (self.frame + 1) % len(self.sprite_andando)
            self.image = self.sprite_andando[self.frame]

        self.rect.center = self.pos

    def dar_dano(self, jogador):
        tick_atual = pygame.time.get_ticks()
        if self.rect.colliderect(jogador.rect) and tick_atual - self.ultimo_hit >= 1000: # Cooldown de 1s
            self.ultimo_hit = tick_atual
            return self.ataque // jogador.defesa
        return 0

    def checar_hp(self):
        if self.hit_points_atuais <= 0:
            self.kill()

class Missel(pygame.sprite.Sprite, Ataque):  # BUGADO
    def __init__(self, jogador, inimigo):
        super().__init__()
        self.escala = (125, 125)
        self.sprites_movimento = [pygame.transform.scale(pygame.image.load(f"Sprites/Missel_magico/1_{i}.png"), self.escala) for i in range(30)]
        self.image = self.sprites_movimento[0]
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(jogador.rect.center)
        self.rect.center = self.pos

        # Direção e velocidade do míssil
        self.dano = jogador.ataque * 10
        self.velocidade = 3
        self.direcao = pygame.math.Vector2(inimigo.rect.center) - self.pos
        if self.direcao.length() > 0:
            self.direcao = self.direcao.normalize() * self.velocidade

        # Tempo de vida do míssil
        self.tempo_vida = 15000  # milissegundos
        self.criado_em = pygame.time.get_ticks()

        # Animação
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate_animacao = 1000 // 11

    def movimento(self, dt):
        # Mover o míssil na direção do inimigo
        self.pos += self.direcao * dt
        self.rect.center = self.pos

        # Verificar o tempo de vida do míssil
        if pygame.time.get_ticks() - self.criado_em > self.tempo_vida:
            self.kill()

    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()
        if tick_atual - self.ultimo_tick > self.frame_rate_animacao:
            self.ultimo_tick = tick_atual
            self.frame = (self.frame + 1) % len(self.sprites_movimento)
            self.image = self.sprites_movimento[self.frame]

        self.rect.center = self.pos

    def dar_dano(self, inimigo):
        if self.rect.colliderect(inimigo) and isinstance(inimigo, Badger):
            self.kill()
            return self.dano // inimigo.defesa
        return 0
