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
        self.nivel = 0

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

        if tempo_atual - self.ultimo_hit >= self.cooldown_ataque and self.nivel != 0:  # Checa se o tempo decorrido desde o último ataque >= cooldown e so nível > 0
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
Bola_Sprites = [pygame.image.load(f"Sprites/Ataques/ataque_rotatorio.png")]
Adaga_Sprites = [pygame.image.load('Sprites/Ataques/adaga.png')]
Machado_Sprites = [pygame.image.load('Sprites/Ataques/machado.png')]
Chicote_Icone = pygame.image.load('Sprites/Ataques/chicote.png')

class Chicote(Ataque):
    def __init__(self, offset, direcao):
        escala = pygame.math.Vector2(300, 200)
        sprite_invisivel = Sprite_Invisivel
        sprites_animacao = [sprite.convert_alpha() for sprite in Slash2_Sprites]
        self.icone = pygame.transform.scale(Chicote_Icone.convert_alpha(), (119, 119))

        # Stats
        self.nome = "CHICOTE"
        self.dano_base = 8
        self.duracao_ataque_base = 0.4 # em segundos
        self.cooldown_ataque_base = 1.35  # em segundos
        self.knockback_base = 20

        # Animação
        frame_rate = 11

        super().__init__(escala, self.dano_base, self.duracao_ataque_base, self.cooldown_ataque_base, sprite_invisivel, sprites_animacao, frame_rate, offset, self.knockback_base, direcao)

        # Dicionário dos upgrades a cada level up
        self.level_up_dict = {
            1: "Atinge inimigos próximos ao jogador",
            2: "Adiciona Projétil",
            3: "Duração do ataque + 50%. Cooldown - 33%",
            4: "Aumenta o dano em 60%",
            5: "Aumenta o dano em 60%",
            6: "Dano + 40%. Duração + 40%",
            7: "Adiciona projétil",
            8: "Reduz cooldown em 50%",
            9: "Aumenta dano em 100%",
            10: "Adiciona projétil"
        }

    def ajustar_nivel(self, grupo_ataques, grupo_todos):
        ajustes = {
            1: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 1000},
            2: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 1000},
            3: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1.5 * 1000, 'cooldown': self.cooldown_ataque_base / 1.5 * 1000},
            4: {'dano': self.dano_base * 1.6, 'duracao': self.duracao_ataque_base * 1.5 * 1000, 'cooldown': self.cooldown_ataque_base / 1.5 * 1000},
            5: {'dano': self.dano_base * 1.6 * 1.6, 'duracao': self.duracao_ataque_base * 1.5 * 1000, 'cooldown': self.cooldown_ataque_base / 1.5 * 1000},
            6: {'dano': self.dano_base * 1.6 * 1.6 * 1.4, 'duracao': self.duracao_ataque_base * 2.1 * 1000, 'cooldown': self.cooldown_ataque_base / 1.5 * 1000},
            7: {'dano': self.dano_base * 1.6 * 1.6 * 1.4, 'duracao': self.duracao_ataque_base * 2.1 * 1000, 'cooldown': self.cooldown_ataque_base / 1.5 * 1000},
            8: {'dano': self.dano_base * 1.6 * 1.6 * 1.4, 'duracao': self.duracao_ataque_base * 2.1 * 1000, 'cooldown': self.cooldown_ataque_base / (1.5 * 2) * 1000},
            9: {'dano': self.dano_base * 1.6 * 1.6 * 1.4 * 2, 'duracao': self.duracao_ataque_base * 2.1 * 1000, 'cooldown': self.cooldown_ataque_base / (1.5 * 2) * 1000},
            10: {'dano': self.dano_base * 1.6 * 1.6 * 1.4 * 2, 'duracao': self.duracao_ataque_base * 2.1 * 1000, 'cooldown': self.cooldown_ataque_base / (1.5 * 2) * 1000}
        }

        # Aplicar ajustes baseados no nível
        if self.nivel in ajustes:
            ajustes_nivel = ajustes[self.nivel]
            self.dano = ajustes_nivel['dano']
            self.duracao_ataque = ajustes_nivel['duracao']
            self.cooldown_ataque = ajustes_nivel['cooldown']

            # Adiciona projéteis conforme o nível
            if self.nivel in (2, 7, 10):
                num_projetis_max = {2: 2, 7: 3, 10: 4}[self.nivel]
                posicao_chicote = {2: ((-160, 0), 'esquerda'), 7: ((160, -100), 'direita'), 10: ((-160, 100), 'esquerda')}[self.nivel]
                flip = {2: (False, True), 7: (False, False), 10: (False, True)}[self.nivel]
                ataque_chicote = Chicote(*posicao_chicote)
                ataque_chicote.sprites_animacao = [pygame.transform.flip(sprite, *flip) for sprite in ataque_chicote.sprites_animacao]
                if sum(1 for sprite in grupo_ataques if isinstance(sprite, Chicote)) < num_projetis_max:
                    grupo_ataques.add(ataque_chicote)
                    grupo_todos.add(ataque_chicote)

class Rotacao(Ataque):
    def __init__(self, offset, angulo):
        escala = pygame.math.Vector2(80, 80)
        sprite_invisivel = Sprite_Invisivel
        sprites_animacao = [sprite.convert_alpha() for sprite in Bola_Sprites]
        self.icone = pygame.transform.scale(Bola_Sprites[0].convert_alpha(), (119, 119))

        # Stats
        self.nome = "ESFERA DE ENERGIA"
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

        # Dicionário dos upgrades a cada level up
        self.level_up_dict = {
            1: "Gira ao redor do jogador",
            2: "Adiciona Projétil",
            3: "Aumneta duração em 50%",
            4: "Aumenta o dano em 100%",
            5: "Diminui cooldown em 50%",
            6: "Adiciona projétil e aumenta dano em 70%",
            7: "Aumenta duração em 50%",
            8: "Adiciona projétil e aumenta dano em 70%",
            9: "Aumenta duração em 50%",
            10: "Ataque dura perpetualmente"
        }

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
        ajustes = {
            1: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 1000},
            2: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 1000},
            3: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000 * 1.5, 'cooldown': self.cooldown_ataque_base * 1000},
            4: {'dano': self.dano_base * 2, 'duracao': self.duracao_ataque_base * 1000 * 1.5, 'cooldown': self.cooldown_ataque_base * 1000},
            5: {'dano': self.dano_base * 2, 'duracao': self.duracao_ataque_base * 1000 * 1.5, 'cooldown': self.cooldown_ataque_base * 1000 * 0.5},
            6: {'dano': self.dano_base * 2 * 1.7, 'duracao': self.duracao_ataque_base * 1000 * 1.5, 'cooldown': self.cooldown_ataque_base * 1000 * 0.5},
            7: {'dano': self.dano_base * 2 * 1.7, 'duracao': self.duracao_ataque_base * 1000 * 1.5 * 1.5, 'cooldown': self.cooldown_ataque_base * 1000 * 0.5},
            8: {'dano': self.dano_base * 2 * 1.7 * 1.7, 'duracao': self.duracao_ataque_base * 1000 * 1.5 * 1.5, 'cooldown': self.cooldown_ataque_base * 1000 * 0.5},
            9: {'dano': self.dano_base * 2 * 1.7 * 1.7, 'duracao': self.duracao_ataque_base * 1000 * 1.5 * 1.5 * 1.5, 'cooldown': self.cooldown_ataque_base * 1000 * 0.5},
            10: {'dano': self.dano_base * 2 * 1.7 * 1.7, 'duracao': float('inf'), 'cooldown': self.cooldown_ataque_base * 1000 * 0.5}
        }

        # Aplicar ajustes baseados no nível
        if self.nivel in ajustes:
            ajustes_nivel = ajustes[self.nivel]
            self.dano = ajustes_nivel['dano']
            self.duracao_ataque = ajustes_nivel['duracao']
            self.cooldown_ataque = ajustes_nivel['cooldown']

            # Adiciona projéteis conforme o nível
            if self.nivel in (2, 6, 8):
                num_projetis_max = {2: 2, 6: 3, 8: 4}[self.nivel]
                angulo_projetil = {2: 90, 6: 180, 8: 270}[self.nivel]
                ataque_rotacao = Rotacao(140, angulo_projetil)
                if sum(1 for sprite in grupo_ataques if isinstance(sprite, Rotacao)) < num_projetis_max:
                    grupo_ataques.add(ataque_rotacao)
                    grupo_todos.add(ataque_rotacao)

class Adaga(Ataque):
    def __init__(self, offset, direcao):
        escala = pygame.math.Vector2(75, 75)
        sprite_invisivel = Sprite_Invisivel
        sprites_animacao = [sprite.convert_alpha() for sprite in Adaga_Sprites]
        self.icone = pygame.transform.scale(Adaga_Sprites[0].convert_alpha(), (119, 119))

        # Stats
        self.nome = "ADAGA"
        self.dano_base = 5
        self.duracao_ataque_base = 5  # em segundos
        self.cooldown_ataque_base = 2  # em segundos
        self.knockback_base = 0
        self.limite_projeteis = 1

        # Animação
        frame_rate = 1

        super().__init__(escala, self.dano_base, self.duracao_ataque_base, self.cooldown_ataque_base, sprite_invisivel, sprites_animacao, frame_rate, offset, self.knockback_base, direcao)

        # Dicionário dos upgrades a cada level up
        self.level_up_dict = {
            1: "É lançando na direção do jogador",
            2: "Adiciona Projétil",
            3: "Aumenta duração do ataque em 100%",
            4: "Adiciona Projétil",
            5: "Aumenta o dano em 60%",
            6: "Adiciona Projétil",
            7: "Aumenta o dano em 60%",
            8: "Adiciona Projétil",
            9: "Aumenta dano em 60%",
            10: "Adiciona projétil"
        }

    def spawnar_projetil(self, grupo_ataques, grupo_todos):
        if self.ataque_executado and sum(1 for ataque in grupo_ataques if isinstance(ataque, Projetil_Adaga)) < self.limite_projeteis:
            projetil = Projetil_Adaga(self.sprites_animacao, self.pos + (0, random.randrange(-50, 50)), self.direcao, 15, self.dano, self.knockback)
            grupo_ataques.add(projetil)
            grupo_todos.add(projetil)

    def ajustar_nivel(self, grupo_ataques, grupo_todos):
        ajustes = {
            1: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 1000},
            2: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 1000},
            3: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000 * 2, 'cooldown': self.cooldown_ataque_base * 1000},
            4: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000 * 2, 'cooldown': self.cooldown_ataque_base * 1000},
            5: {'dano': self.dano_base * 1.6, 'duracao': self.duracao_ataque_base * 1000 * 2, 'cooldown': self.cooldown_ataque_base * 1000},
            6: {'dano': self.dano_base * 1.6, 'duracao': self.duracao_ataque_base * 1000 * 2, 'cooldown': self.cooldown_ataque_base * 1000},
            7: {'dano': self.dano_base * 1.6 * 1.6, 'duracao': self.duracao_ataque_base * 1000 * 2, 'cooldown': self.cooldown_ataque_base * 1000},
            8: {'dano': self.dano_base * 1.6 * 1.6, 'duracao': self.duracao_ataque_base * 1000 * 2, 'cooldown': self.cooldown_ataque_base * 1000},
            9: {'dano': self.dano_base * 1.6 * 1.6 * 1.6, 'duracao': self.duracao_ataque_base * 1000 * 2, 'cooldown': self.cooldown_ataque_base * 1000},
            10: {'dano': self.dano_base * 1.6 * 1.6 * 1.6, 'duracao': self.duracao_ataque_base * 1000 * 2, 'cooldown': self.cooldown_ataque_base * 1000}
        }

        # Aplicar ajustes baseados no nível
        if self.nivel in ajustes:
            ajustes_nivel = ajustes[self.nivel]
            self.dano = ajustes_nivel['dano']
            self.duracao_ataque = ajustes_nivel['duracao']
            self.cooldown_ataque = ajustes_nivel['cooldown']

        if self.nivel in (2, 4, 6, 8, 10):
            self.limite_projeteis = {2: 2, 4: 3, 6: 4, 8: 5, 10: 6}[self.nivel]


class Machado(Ataque):
    def __init__(self, offset, direcao):
        escala = pygame.math.Vector2(90, 90)
        sprite_invisivel = Sprite_Invisivel
        sprites_animacao = [sprite.convert_alpha() for sprite in Machado_Sprites]
        self.icone = pygame.transform.scale(Machado_Sprites[0].convert_alpha(), (119, 119))

        # Stats
        self.nome = "MACHADO"
        self.dano_base = 16
        self.duracao_ataque_base = 5 # em segundos
        self.cooldown_ataque_base = 3  # em segundos
        self.knockback_base = 5
        self.limite_projeteis = 1

        # Animação
        frame_rate = 11

        super().__init__(escala, self.dano_base, self.duracao_ataque_base, self.cooldown_ataque_base, sprite_invisivel, sprites_animacao, frame_rate, offset, self.knockback_base, direcao)

        # Dicionário dos upgrades a cada level up
        self.level_up_dict = {
            1: "Move-se em parabóla",
            2: "Adiciona projétil",
            3: "Reduz cooldown em 50%",
            4: "Aumenta o dano em 80%",
            5: "Adiciona projétil",
            6: "Cooldown - 50%. Dano + 80%",
            7: "Adiciona projétil",
            8: "Reduz cooldown em 50%",
            9: "Aumenta dano em 80%",
            10: "Adiciona projétil"
        }

    def ajustar_nivel(self, grupo_ataques, grupo_todos):
        ajustes = {
            1: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 1000},
            2: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 1000},
            3: {'dano': self.dano_base, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 0.5 * 1000},
            4: {'dano': self.dano_base * 1.8, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 0.5 * 1000},
            5: {'dano': self.dano_base * 1.8, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 0.5 * 1000},
            6: {'dano': self.dano_base * 1.8 * 1.8, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 0.5 * 0.5 * 1000},
            7: {'dano': self.dano_base * 1.8 * 1.8, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 0.5 * 0.5 * 1000},
            8: {'dano': self.dano_base * 1.8 * 1.8, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 0.5 * 0.5 * 0.5 * 1000},
            9: {'dano': self.dano_base * 1.8 * 1.8 * 1.8, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 0.5 * 0.5 * 0.5 * 1000},
            10: {'dano': self.dano_base * 1.8 * 1.8 * 1.8, 'duracao': self.duracao_ataque_base * 1000, 'cooldown': self.cooldown_ataque_base * 0.5 * 0.5 * 0.5 * 1000}

        }

        # Aplicar ajustes baseados no nível
        if self.nivel in ajustes:
            ajustes_nivel = ajustes[self.nivel]
            self.dano = ajustes_nivel['dano']
            self.duracao_ataque = ajustes_nivel['duracao']
            self.cooldown_ataque = ajustes_nivel['cooldown']

        if self.nivel in (2, 5, 7, 10):
            self.limite_projeteis = {2: 2, 5: 3, 7: 4, 10: 5}[self.nivel]

    def spawnar_projetil(self, grupo_ataques, grupo_todos):
        direcao_oposta = 'direita' if self.direcao == 'esquerda' else 'esquerda'
        machados_possiveis = (
            Projetil_Machado(self.sprites_animacao, self.pos + (0, -20), self.direcao, 7, -9, self.dano, self.knockback),
            Projetil_Machado(self.sprites_animacao, self.pos + (0, -40), direcao_oposta, 7, -9, self.dano, self.knockback),
            Projetil_Machado(self.sprites_animacao, self.pos + (0, +40), self.direcao, 9, -9, self.dano, self.knockback),
            Projetil_Machado(self.sprites_animacao, self.pos + (0, +20), direcao_oposta, 9, -9, self.dano, self.knockback),
            Projetil_Machado(self.sprites_animacao, self.pos + (0, +60), self.direcao, 9, -9, self.dano, self.knockback)
        )

        if self.ataque_executado and sum(1 for ataque in grupo_ataques if isinstance(ataque, Projetil_Machado)) < self.limite_projeteis:
            grupo_ataques.add(machados_possiveis[:self.limite_projeteis])
            grupo_todos.add(machados_possiveis[:self.limite_projeteis])

class Projetil(pygame.sprite.Sprite):
    def __init__(self, sprites_animacao, pos, direcao, velocidade, dano, knockback):
        super().__init__()
        # Objeto
        self.image = sprites_animacao[0]
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.ataque_executado = True

        # Posição e movimento
        self.pos = pygame.math.Vector2(pos)
        self.direcao = direcao
        self.velocidade = pygame.math.Vector2(velocidade)

        # Stats
        self.dano = dano
        self.knockback = knockback

        # Animação
        self.sprites_animacao = sprites_animacao
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate = 1000 // 1

    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()
        if tick_atual - self.ultimo_tick > self.frame_rate:
            self.ultimo_tick = tick_atual
            self.frame = (self.frame + 1) % len(self.sprites_animacao)
            self.image = self.sprites_animacao[self.frame]
            self.mask = pygame.mask.from_surface(self.image)  # Atualiza mask
        self.rect = self.image.get_rect(center=self.pos)

    def verificar_distancia(self, jogador):
        direcao_x = jogador.pos.x - self.pos.x
        direcao_y = jogador.pos.y - self.pos.y
        distancia = (direcao_x ** 2 + direcao_y ** 2) ** 0.5
        if distancia > 1000:  # Se o jogador estiver muito longe do ataque, deleta o ataque
            self.kill()


class Projetil_Adaga(Projetil):
    def __init__(self, sprites_animacao, pos, direcao, velocidade, dano, knockback):
        super().__init__(sprites_animacao, pos, direcao, (velocidade, 0), dano, knockback)

    def atualizar(self, jogador, dt):
        # Move o projétil na direção do jogador
        if self.direcao == 'direita':
            self.pos.x += self.velocidade.x * dt
        else:
            self.pos.x -= self.velocidade.x * dt

        # Animar o projétil
        self.animar_sprite()

        # Checar distância do jogador
        self.verificar_distancia(jogador)


class Projetil_Machado(Projetil):
    def __init__(self, sprites_animacao, pos, direcao, velocidade_x, velocidade_y, dano, knockback):
        super().__init__(sprites_animacao, pos, direcao, (velocidade_x, velocidade_y), dano, knockback)
        self.gravidade = 0.4

    def atualizar(self, jogador, dt):
        # Move o projétil numa parábola
        if self.direcao == 'direita':
            self.pos.x += self.velocidade.x * dt
        else:
            self.pos.x -= self.velocidade.x * dt
        self.pos.y += self.velocidade.y * dt
        self.velocidade.y += self.gravidade

        # Animar o projétil
        self.animar_sprite()

        # Checar distância do jogador
        self.verificar_distancia(jogador)
