import pygame
class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade, frame_rate, nome, tempo, sprite_idle_apanhando, sprite_apanhando):
        super().__init__()

        # Sprite
        self.sprite_idle_apanhando = pygame.transform.scale(sprite_idle_apanhando, escala)
        self.sprite_apanhando = [pygame.transform.scale(sprite, escala) for sprite in sprite_apanhando]
        self.sprite_idle = pygame.transform.scale(sprite_idle, escala)
        self.sprite_andando = [pygame.transform.scale(sprite, escala) for sprite in sprite_andando]
        self.image = self.sprite_idle  # Imagem a ser desenhada na tela
        self.direcao = "direita"  # Direção para qual o sprite está indo

        # Objeto
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Mask para ser usada como hitbox
        self.pos = pos

        # Stats iniciais
        self.nome = nome
        self.nivel = 1
        self.xp = 0
        self.xp_para_proximo_nivel = int(50 * self.nivel ** 1.1)
        self.hit_point_max = hp
        self.hit_points_atuais = self.hit_point_max
        self.ataque = ataque
        self.defesa = defesa
        self.velocidade_movimento = velocidade

        # Dicionários
        self.inventario = {'Poção Cura': 0, 'Poção Velocidade': 0, 'Bomba': 0, 'Dobro XP': 0}
        self.dicionario = {'Nome': nome, 'HP': hp, 'ATK': ataque, 'DEF': defesa, 'SPD': velocidade}  # Para mostrar os stats no menu inicial

        # Animação
        self.andando = False
        self.frame = 0  # Frame Atual
        self.ultimo_tick = 0  # Contagem de ticks quando o frame foi atualizado pela última vez
        self.frame_rate_animacao = 1000 // frame_rate  # Frame rate da animação do sprite

        # Dano
        self.ultimo_hit = tempo

    def movimento(self, dt, mod):
        keys = pygame.key.get_pressed()
        self.andando = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos.x -= self.velocidade_movimento * dt * mod
            if self.direcao != 'esquerda':
                self.direcao = 'esquerda'
                self.sprite_idle = pygame.transform.flip(self.sprite_idle, True, False)
                self.sprite_idle_apanhando = pygame.transform.flip(self.sprite_idle_apanhando, True, False)
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.sprite_apanhando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_apanhando]
            self.andando = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos.x += self.velocidade_movimento * dt * mod
            if self.direcao != 'direita':
                self.direcao = 'direita'
                self.sprite_idle = pygame.transform.flip(self.sprite_idle, True, False)
                self.sprite_idle_apanhando = pygame.transform.flip(self.sprite_idle_apanhando, True, False)
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.sprite_apanhando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_apanhando]
            self.andando = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pos.y -= self.velocidade_movimento * dt * mod
            self.andando = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pos.y += self.velocidade_movimento * dt * mod
            self.andando = True

    def animar_sprite(self, tempo):
        lista_sprites = self.sprite_andando if tempo - self.ultimo_hit >= 100 else self.sprite_apanhando
        sprite_idle = self.sprite_idle if tempo - self.ultimo_hit >= 100 else self.sprite_idle_apanhando
        if self.andando:
            if tempo - self.ultimo_tick > self.frame_rate_animacao:
                self.ultimo_tick = tempo
                self.frame = (self.frame + 1) % len(lista_sprites)
                self.image = lista_sprites[self.frame]
        else:
            self.image = sprite_idle

        # Atualiza rect e mask
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)

    def levar_dano(self, inimigos_grupo, tempo):
        for inimigo in inimigos_grupo:
            if self.mask.overlap(inimigo.mask, (inimigo.rect.left - self.rect.left, inimigo.rect.top - self.rect.top)) and tempo - self.ultimo_hit >= 100:
                self.hit_points_atuais -= inimigo.dano/self.defesa
                self.ultimo_hit = tempo
                som = pygame.mixer.Sound('Audio/jogador_dano.mp3')
                pygame.mixer.Sound.set_volume(som, 0.3)
                pygame.mixer.Sound.play(som)

    def nivel_update(self):
        if self.xp >= self.xp_para_proximo_nivel:
            self.xp -= self.xp_para_proximo_nivel
            self.nivel += 1
            self.xp_para_proximo_nivel = int(50 * self.nivel ** 1.1)

    def usar_item(self, item):
        if self.inventario[item] > 0:
            self.inventario[item] -= 1
            return True
        return False


# Carregar Sprites
Sprite_BichoChicote_Idle = pygame.image.load("Sprites/personagens/bicho_chicote_idle.png")
Sprite_BichoChicote_Andando = [pygame.image.load(f"Sprites/personagens/bicho_chicote_{i+1}.png") for i in range(3)]
Sprite_BichoChicote_Apanhando_Idle = pygame.image.load("Sprites/personagens/bicho_chicote_idle_hit.png")
Sprite_BichoChicote_Apanhando = [pygame.image.load(f"Sprites/personagens/bicho_chicote_{i+1}_hit.png") for i in range(3)]

Sprite_BichoAdaga_Idle = pygame.image.load("Sprites/personagens/bicho_adaga_idle.png")
Sprite_BichoAdaga_Andando = [pygame.image.load(f"Sprites/personagens/bicho_adaga_{i+1}.png") for i in range(3)]
Sprite_BichoAdaga_Apanhando_Idle = pygame.image.load("Sprites/personagens/bicho_adaga_idle_hit.png")
Sprite_BichoAdaga_Apanhando = [pygame.image.load(f"Sprites/personagens/bicho_adaga_{i+1}_hit.png") for i in range(3)]

Sprite_BichoCajado_Idle = pygame.image.load("Sprites/personagens/bicho_cajado_idle.png")
Sprite_BichoCajado_Andando = [pygame.image.load(f"Sprites/personagens/bicho_cajado_{i+1}.png") for i in range(3)]
Sprite_BichoCajado_Apanhando_Idle = pygame.image.load("Sprites/personagens/bicho_cajado_idle_hit.png")
Sprite_BichoCajado_Apanhando = [pygame.image.load(f"Sprites/personagens/bicho_cajado_{i+1}_hit.png") for i in range(3)]

Sprite_BichoMachado_Idle = pygame.image.load("Sprites/personagens/bicho_machado_idle.png")
Sprite_BichoMachado_Andando = [pygame.image.load(f"Sprites/personagens/bicho_machado_{i+1}.png") for i in range(3)]
Sprite_BichoMachado_Apanhando_Idle = pygame.image.load("Sprites/personagens/bicho_machado_idle_hit.png")
Sprite_BichoMachado_Apanhando = [pygame.image.load(f"Sprites/personagens/bicho_machado_{i+1}_hit.png") for i in range(3)]

class BichoChicote(Jogador):
    def __init__(self, pos, tempo):
        nome = 'Bicho Chicote'
        escala = pygame.math.Vector2(66, 66)
        sprite_idle = Sprite_BichoChicote_Idle.convert_alpha()
        sprite_andando = [sprite.convert_alpha() for sprite in Sprite_BichoChicote_Andando]
        sprite_idle_apanhando = Sprite_BichoChicote_Apanhando_Idle.convert_alpha()
        sprite_apanhando = [sprite.convert_alpha() for sprite in Sprite_BichoChicote_Apanhando]

        # Stats
        hp = 600
        ataque = 6
        defesa = 6
        velocidade_movimento = 3

        # Animação
        frame_rate = 9

        super().__init__(pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate, nome, tempo, sprite_idle_apanhando, sprite_apanhando)

class BichoAdaga(Jogador):
    def __init__(self, pos, tempo):
        nome = 'Bicho Adaga'
        escala = pygame.math.Vector2(66, 66)
        sprite_idle = Sprite_BichoAdaga_Idle.convert_alpha()
        sprite_andando = [sprite.convert_alpha() for sprite in Sprite_BichoAdaga_Andando]
        sprite_idle_apanhando = Sprite_BichoAdaga_Apanhando_Idle.convert_alpha()
        sprite_apanhando = [sprite.convert_alpha() for sprite in Sprite_BichoAdaga_Apanhando]

        # Stats
        hp = 550
        ataque = 8
        defesa = 4
        velocidade_movimento = 4

        # Animação
        frame_rate = 9

        super().__init__(pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate, nome, tempo, sprite_idle_apanhando, sprite_apanhando)

class BichoCajado(Jogador):
    def __init__(self, pos, tempo):
        nome = 'Bicho Cajado'
        escala = pygame.math.Vector2(66, 66)
        sprite_idle = Sprite_BichoCajado_Idle.convert_alpha()
        sprite_andando = [sprite.convert_alpha() for sprite in Sprite_BichoCajado_Andando]
        sprite_idle_apanhando = Sprite_BichoCajado_Apanhando_Idle.convert_alpha()
        sprite_apanhando = [sprite.convert_alpha() for sprite in Sprite_BichoCajado_Apanhando]

        # Stats
        hp = 400
        ataque = 10
        defesa = 3
        velocidade_movimento = 5

        # Animação
        frame_rate = 9

        super().__init__(pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate, nome, tempo, sprite_idle_apanhando, sprite_apanhando)

class BichoMachado(Jogador):
    def __init__(self, pos, tempo):
        nome = 'Bicho Machado'
        escala = pygame.math.Vector2(66, 66)
        sprite_idle = Sprite_BichoMachado_Idle.convert_alpha()
        sprite_andando = [sprite.convert_alpha() for sprite in Sprite_BichoMachado_Andando]
        sprite_idle_apanhando = Sprite_BichoMachado_Apanhando_Idle.convert_alpha()
        sprite_apanhando = [sprite.convert_alpha() for sprite in Sprite_BichoMachado_Apanhando]

        # Stats
        hp = 750
        ataque = 8
        defesa = 8
        velocidade_movimento = 2

        # Animação
        frame_rate = 9

        super().__init__(pos, escala, sprite_idle, sprite_andando, hp, ataque, defesa, velocidade_movimento, frame_rate, nome, tempo, sprite_idle_apanhando, sprite_apanhando)




