import pygame
class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade, frame_rate):
        super().__init__()

        # Sprite
        self.sprite_idle = pygame.transform.scale(sprite_idle, escala)
        self.sprite_andando = [pygame.transform.scale(sprite, escala) for sprite in sprite_andando]
        self.image = self.sprite_idle  # Imagem a ser desenhada na tela
        self.direcao = "direita"  # Direção para qual o sprite está indo

        # Objeto
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(pos.x / 4, pos.y / 4, escala.x / 2, escala.y / 2)  # Hitbox posicionada no centro do rect e com metade do tamanho
        self.pos = pos

        # Stats
        self.hit_point_max = hp
        self.hit_points_atuais = self.hit_point_max
        self.ataque = ataque
        self.defesa = defesa
        self.velocidade_movimento = velocidade
        self.nivel = 1
        self.exp = 0
        self.exp_para_proximo_nivel = int(100 * (1 + self.nivel ** 1.1))

        # Inventário
        self.inventario = {'Poção': 0}

        # Animação
        self.andando = False
        self.frame = 0  # Frame Atual
        self.ultimo_tick = pygame.time.get_ticks()  # Contagem de ticks quando o frame foi atualizado pela última vez
        self.frame_rate_animacao = 1000 // frame_rate  # Frame rate da animação do sprite

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

    def beber_pocao(self):
        if self.inventario['Poção'] > 0:
            self.inventario['Poção'] -= 1
            self.hit_points_atuais += 25
            self.hit_points_atuais = min(self.hit_points_atuais, self.hit_point_max)


# Carregar sprites
Sprite_BichoChicote_Idle = pygame.image.load("Sprites/Player_Idle.png")
Sprite_BichoChicote_Andando = [pygame.image.load(f"Sprites/Player_andando_{i+1}.png") for i in range(3)]

class BichoChicote(Jogador):
    def __init__(self, pos):
        escala = pygame.math.Vector2(66, 66)
        sprite_idle = Sprite_BichoChicote_Idle.convert_alpha()
        sprite_andando = [sprite.convert_alpha() for sprite in Sprite_BichoChicote_Andando]

        # Stats
        hp = 100
        ataque = 5
        defesa = 5
        velocidade_movimento = 3

        # Animação
        frame_rate = 9

        super().__init__(pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate)
