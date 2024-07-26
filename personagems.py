import pygame
class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade, frame_rate, nome):
        super().__init__()

        # Sprite
        self.sprite_idle = pygame.transform.scale(sprite_idle, escala)
        self.sprite_andando = [pygame.transform.scale(sprite, escala) for sprite in sprite_andando]
        self.image = self.sprite_idle  # Imagem a ser desenhada na tela
        self.direcao = "direita"  # Direção para qual o sprite está indo

        # Objeto
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Mask para ser usada como hitbox
        self.pos = pos

        # Stats originais para calcular novos stats a cada nível
        self.ataque_original = ataque
        self.defesa_orginal = defesa

        # Stats iniciais
        self.nome = nome
        self.nivel = 1
        self.xp = 0
        self.xp_para_proximo_nivel = int(100 * (1 + self.nivel ** 1.1))
        self.hit_point_max = hp * (1 + self.nivel * 0.2)
        self.hit_points_atuais = self.hit_point_max
        self.ataque = ataque * (1 + self.nivel * 0.2)
        self.defesa = defesa * (1 + self.nivel * 0.2)
        self.velocidade_movimento = velocidade

        # Dicionários
        self.inventario = {'Poção Cura': 0, 'Poção Velocidade': 0, 'Bomba': 0, 'Dobro XP': 0}
        self.dicionario = {'Nome': nome, 'HP': hp, 'ATK': ataque, 'DEF': defesa, 'SPD': velocidade}  # Para mostrar os stats no menu inicial

        # Animação
        self.andando = False
        self.frame = 0  # Frame Atual
        self.ultimo_tick = pygame.time.get_ticks()  # Contagem de ticks quando o frame foi atualizado pela última vez
        self.frame_rate_animacao = 1000 // frame_rate  # Frame rate da animação do sprite

    def movimento(self, dt, mod):
        keys = pygame.key.get_pressed()
        self.andando = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos.x -= self.velocidade_movimento * dt * mod
            if self.direcao != 'esquerda':
                self.direcao = 'esquerda'
                self.sprite_idle = pygame.transform.flip(self.sprite_idle, True, False)
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
            self.andando = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos.x += self.velocidade_movimento * dt * mod
            if self.direcao != 'direita':
                self.direcao = 'direita'
                self.sprite_idle = pygame.transform.flip(self.sprite_idle, True, False)
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
            self.andando = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pos.y -= self.velocidade_movimento * dt * mod
            self.andando = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pos.y += self.velocidade_movimento * dt * mod
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

        # Atualiza rect e mask
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)

    def nivel_update(self):
        if self.xp >= self.xp_para_proximo_nivel:
            self.xp -= self.xp_para_proximo_nivel
            self.nivel += 1
            self.xp_para_proximo_nivel = int(100 * (1 + self.nivel ** 1.1))
            self.ataque = self.ataque_original * (1 + self.nivel * 0.2)
            self.defesa = self.defesa_orginal * (1 + self.nivel * 0.2)

    def usar_item(self, item):
        if self.inventario[item] > 0:
            self.inventario[item] -= 1
            return True
        return False


# Carregar sprites
Sprite_BichoChicote_Idle = pygame.image.load("Sprites/personagens/bicho_chicote_idle.png")
Sprite_BichoChicote_Andando = [pygame.image.load(f"Sprites/personagens/bicho_chicote_{i+1}.png") for i in range(3)]

Sprite_BichoAdaga_Idle = pygame.image.load(f"Sprites/personagens/bicho_adaga_idle.png")
Sprite_BichoAdaga_Andando = [pygame.image.load(f"Sprites/personagens/bicho_adaga_{i+1}.png") for i in range(3)]

Sprite_BichoCajado_Idle = pygame.image.load(f"Sprites/personagens/bicho_cajado_idle.png")
Sprite_BichoCajado_Andando = [pygame.image.load(f"Sprites/personagens/bicho_cajado_{i+1}.png") for i in range(3)]

Sprite_BichoMachado_Idle = pygame.image.load(f"Sprites/personagens/bicho_machado_idle.png")
Sprite_BichoMachado_Andando = [pygame.image.load(f"Sprites/personagens/bicho_machado_{i+1}.png") for i in range(3)]

class BichoChicote(Jogador):
    def __init__(self, pos):
        nome = 'Bicho Chicote'
        escala = pygame.math.Vector2(66, 66)
        sprite_idle = Sprite_BichoChicote_Idle.convert_alpha()
        sprite_andando = [sprite.convert_alpha() for sprite in Sprite_BichoChicote_Andando]

        # Stats
        hp = 50
        ataque = 6
        defesa = 6
        velocidade_movimento = 3

        # Animação
        frame_rate = 9

        super().__init__(pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate, nome)

class BichoAdaga(Jogador):
    def __init__(self, pos):
        nome = 'Bicho Adaga'
        escala = pygame.math.Vector2(66, 66)
        sprite_idle = Sprite_BichoAdaga_Idle.convert_alpha()
        sprite_andando = [sprite.convert_alpha() for sprite in Sprite_BichoAdaga_Andando]

        # Stats
        hp = 50
        ataque = 8
        defesa = 4
        velocidade_movimento = 4

        # Animação
        frame_rate = 9

        super().__init__(pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate, nome)

class BichoCajado(Jogador):
    def __init__(self, pos):
        nome = 'Bicho Cajado'
        escala = pygame.math.Vector2(66, 66)
        sprite_idle = Sprite_BichoCajado_Idle.convert_alpha()
        sprite_andando = [sprite.convert_alpha() for sprite in Sprite_BichoCajado_Andando]

        # Stats
        hp = 40
        ataque = 10
        defesa = 3
        velocidade_movimento = 5

        # Animação
        frame_rate = 9

        super().__init__(pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate, nome)

class BichoMachado(Jogador):
    def __init__(self, pos):
        nome = 'Bicho Machado'
        escala = pygame.math.Vector2(66, 66)
        sprite_idle = Sprite_BichoMachado_Idle.convert_alpha()
        sprite_andando = [sprite.convert_alpha() for sprite in Sprite_BichoMachado_Andando]

        # Stats
        hp = 75
        ataque = 8
        defesa = 8
        velocidade_movimento = 2

        # Animação
        frame_rate = 9

        super().__init__(pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate, nome)




