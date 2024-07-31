import pygame
import math
import random

class Ataque(pygame.sprite.Sprite):
    def __init__(self, escala, dano, duracao_ataque, cooldown_ataque, sprite_invisivel, sprites_animacao, frame_rate, offset, knockback, direcao):
        super().__init__()

        # Sprite
        self.sprite_invisivel = pygame.transform.scale(sprite_invisivel, escala)
        self.sprites_animacao = [pygame.transform.scale(sprite, escala) for sprite in sprites_animacao]
        self.image = self.sprites_animacao[0]
        self.direcao = direcao

        # Objeto
        self.pos = pygame.math.Vector2(0, 0)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)  # Mask para ser usada como hitbox
        self.offset = offset

        # Stats
        self.dano = dano
        self.duracao_ataque = duracao_ataque * 1000  # convertendo para milisegundos
        self.cooldown_ataque = cooldown_ataque * 1000  # convertendo para milisegundos
        self.knockback = knockback
        self.nivel = 1

        # Animação
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate = 1000 // frame_rate

        # Dano
        self.ultimo_hit = pygame.time.get_ticks()
        self.ataque_executado = False

    # a segunda funcao ira realizar o ataque, e ira retornar a variavel ataque_executado como true ou false, no intervalo definido pelo cooldown e duracao de ataque.
    def atacar(self):
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - self.ultimo_hit >= self.cooldown_ataque:  # Checa se o tempo decorrido desde o último ataque >= cooldown
            # Checa se o ataque ainda está sendo executado
            self.ataque_executado = True if tempo_atual - self.ultimo_hit < self.duracao_ataque + self.cooldown_ataque else False
            if not self.ataque_executado:
                self.ultimo_hit = tempo_atual
        else:
            self.ataque_executado = False

        return self.ataque_executado

    # a terceira funcao eh responsavel por animar o ataque, e ira atualizar o frame do ataque, e a imagem do ataque
    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()

        if tick_atual - self.ultimo_tick > self.frame_rate and self.ataque_executado:  # se o tempo atual - o ultimo tick for maior que o frame rate, entao atualizamos o frame
            self.ultimo_tick = tick_atual  # atualizamos o ultimo tick
            self.frame = (self.frame + 1) % len(self.sprites_animacao)  # atualizamos o frame
            self.image = self.sprites_animacao[self.frame]
            self.mask = pygame.mask.from_surface(self.image)  # Atualiza mask

        elif not self.ataque_executado:
            self.image = self.sprite_invisivel
            #reseta a animacao e o frame
            self.frame = 0

        # Atualizar hitbox
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self, jogador):  # funcao para adicionar um offset para ataques especificos
        self.pos = jogador.pos + self.offset if jogador.direcao == 'direita' else jogador.pos - self.offset

        # Compara a direção do ataque com a direção do player e inverte o sprite se for diferente
        if self.direcao != jogador.direcao:
            self.direcao = jogador.direcao
            self.sprites_animacao = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites_animacao]

        self.rect.center = self.pos


# Carregar sprites
Sprite_Invisivel = pygame.image.load('Sprites/Ataques/ataque_invisivel.png')
Slash_Sprites = [pygame.image.load(f"Sprites/Ataques/Slash_chicote/ataque_chicote_{i+1}.png") for i in range(4)]
Slash2_Sprites = [pygame.image.load(f"Sprites/Ataques/Slash_chicote/ataque_chicote_02_0{i}.png") for i in range(4)]
Bola = [pygame.image.load(f"Sprites/Ataques/ataque_rotatorio.png")]

class Slash(Ataque):
    def __init__(self, offset, direcao):
        escala = pygame.math.Vector2(600, 300)
        sprite_invisivel = Sprite_Invisivel
        sprites_animacao = [sprite.convert_alpha() for sprite in Slash2_Sprites]

        # Stats
        self.dano_base = 8
        self.duracao_ataque_base = 1 # em segundos
        self.cooldown_ataque_base = 1.35  # em segundos
        self.knockback_base = 20

        # Animação
        frame_rate = 11

        super().__init__(escala, self.dano_base, self.duracao_ataque_base, self.cooldown_ataque_base, sprite_invisivel, sprites_animacao, frame_rate, offset, self.knockback_base, direcao)

    def ajustar_nivel(self, grupo_ataques, grupo_todos):
        # Usa os valores base para calcular os atributos com base no nível
        if self.nivel == 1:
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 2:  # Adiciona Projétil
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base

            ataque_chicote = Slash(pygame.math.Vector2(-300, 0), 'esquerda')
            ataque_chicote.sprites_animacao = [pygame.transform.flip(sprite, False, True) for sprite in ataque_chicote.sprites_animacao]
            if sum(1 for sprite in grupo_ataques if isinstance(sprite, Slash)) < 2:
                grupo_ataques.add(ataque_chicote)
                grupo_todos.add(ataque_chicote)

        elif self.nivel == 3:  # Aumenta duração do ataque em 50% e reduz cooldown por 33%
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1.5 * 1000
            self.cooldown_ataque = self.cooldown_ataque_base / 1.5 * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 4:  # Aumenta o dano em 20%
            self.dano = self.dano_base * 1.2
            self.duracao_ataque = self.duracao_ataque_base * 1.5 * 1000
            self.cooldown_ataque = self.cooldown_ataque_base / 1.5 * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 5:  # Aumenta knockback em 100%
            self.dano = self.dano_base * 1.2
            self.duracao_ataque = self.duracao_ataque_base * 1.5 * 1000
            self.cooldown_ataque = self.cooldown_ataque_base / 1.5 * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 6:  # Aumenta dano em 20% e aumenta duração em 40%
            self.dano = self.dano_base * 1.44  # 1.2 * 1.2
            self.duracao_ataque = self.duracao_ataque_base * 2.1 * 1000  # 1.5 * 1.4
            self.cooldown_ataque = self.cooldown_ataque_base / 1.5 * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 7:  # Adiciona projétil
            self.dano = self.dano_base * 1.44
            self.duracao_ataque = self.duracao_ataque_base * 2.1 * 1000
            self.cooldown_ataque = self.cooldown_ataque_base / 1.5 * 1000
            self.knockback = self.knockback_base

            ataque_chicote = Slash(pygame.math.Vector2(300, -100), 'direita')
            if sum(1 for sprite in grupo_ataques if isinstance(sprite, Slash)) < 3:
                grupo_ataques.add(ataque_chicote)
                grupo_todos.add(ataque_chicote)

        elif self.nivel == 8:  # Reduz cooldown em 50%, aumenta knockback em 50%
            self.dano = self.dano_base * 1.44
            self.duracao_ataque = self.duracao_ataque_base * 2.1 * 1000
            self.cooldown_ataque = self.cooldown_ataque_base / (1.5 * 2) * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 9:  # Aumenta dano em 40%
            self.dano = self.dano_base * 2.016  # 1.2 * 1.2 * 1.4
            self.duracao_ataque = self.duracao_ataque_base * 2.1 * 1000
            self.cooldown_ataque = self.cooldown_ataque_base / (1.5 * 2) * 1000
            self.knockback = self.knockback_base

        elif self.nivel >= 10:  # Adiciona projétil
            self.dano = self.dano_base * 2.016
            self.duracao_ataque = self.duracao_ataque_base * 2.1 * 1000
            self.cooldown_ataque = self.cooldown_ataque_base / (1.5 * 2) * 1000
            self.knockback = self.knockback_base

            ataque_chicote = Slash(pygame.math.Vector2(-300, 100), 'esquerda')
            ataque_chicote.sprites_animacao = [pygame.transform.flip(sprite, False, True) for sprite in ataque_chicote.sprites_animacao]
            if sum(1 for sprite in grupo_ataques if isinstance(sprite, Slash)) < 4:
                grupo_ataques.add(ataque_chicote)
                grupo_todos.add(ataque_chicote)

class Rotacao(Ataque):
    def __init__(self, offset, angulo):
        escala = pygame.math.Vector2(80, 80)
        sprite_invisivel = Sprite_Invisivel
        sprites_animacao = [sprite.convert_alpha() for sprite in Bola]

        # Stats
        self.dano_base = 8
        self.duracao_ataque_base = 3
        self.cooldown_ataque_base = 3
        self.knockback_base = 3

        self.angulo = angulo
        self.angulo_inicial = angulo
        self.speed = 3

        # Animação
        frame_rate = 6

        super().__init__(escala, self.dano_base, self.duracao_ataque_base, self.cooldown_ataque_base, sprite_invisivel, sprites_animacao, frame_rate, offset, self.knockback_base, direcao=None)

    def atualizar_posicao(self, jogador):
        if self.ataque_executado:
            self.angulo += self.speed
            self.pos.x = jogador.rect.centerx + self.offset * math.cos(math.radians(self.angulo))
            self.pos.y = jogador.rect.centery + self.offset * math.sin(math.radians(self.angulo))
            self.rect.center = self.pos

        else:
            self.angulo = self.angulo_inicial
            self.pos.x = jogador.rect.centerx + self.offset * math.cos(math.radians(self.angulo))
            self.pos.y = jogador.rect.centery + self.offset * math.sin(math.radians(self.angulo))
            self.rect.center = self.pos

    def ajustar_nivel(self, grupo_ataques, grupo_todos):
        if self.nivel == 1:
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 2:
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 3:
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 4:
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 5:
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 6:
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 7:
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base

        elif self.nivel == 8:
            self.dano = self.dano_base
            self.duracao_ataque = self.duracao_ataque_base * 1000
            self.cooldown_ataque = self.cooldown_ataque_base * 1000
            self.knockback = self.knockback_base
