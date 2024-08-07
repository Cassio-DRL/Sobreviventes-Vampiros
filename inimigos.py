import random
import pygame
class DanoTexto(pygame.sprite.Sprite):
    def __init__(self, pos, dano, tempo):
        super().__init__()
        self.image = pygame.font.Font("fonte/Silkscreen-Regular.ttf", 56).render(str(int(dano)), True, (255, 0, 0))
        self.rect = self.image.get_rect(center=pos + (random.randrange(-20, 20), random.randrange(-20, 20)))
        self.criado = tempo

    def update(self, tempo, cooldown):
        # Remover o texto após certo período de tempo
        if tempo - self.criado > cooldown:
            self.kill()

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, pos, sprites_walking, escala, hit_points, dano, defesa, velocidade_movimento, frame_rate, sprites_branco, tempo, jogador):
        super().__init__()

        # Sprite
        self.escala = escala
        self.sprite_andando = [pygame.transform.scale(sprite, escala) for sprite in sprites_walking]  # Lista de frames do sprite
        self.sprite_branco = [pygame.transform.scale(sprite, escala) for sprite in sprites_branco]
        self.image = self.sprite_andando[0]  # Imagem a ser desenhada na tela
        self.direcao = 'direita'  # Direção para qual o sprite está indo

        # Objeto
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Mask para ser usada como hitbox
        self.pos = pos

        # Stats
        self.hit_point_max = hit_points * max(jogador.nivel/2, 1)
        self.hit_points_atuais = self.hit_point_max
        self.dano = dano
        self.defesa = defesa
        self.velocidade_movimento = velocidade_movimento

        # Animação
        self.frame = 0  # Frame Atual
        self.ultimo_tick = 0  # Contagem de ticks quando o frame foi atualizado pela última vez
        self.frame_rate_animacao = 1000 // frame_rate  # Frame rate da animação do sprite

        # Dano
        self.ultimo_hit = tempo  # Contagem de ticks quando o inimigo deu dano pela última vez
        self.cooldown = 100
        self.textos_dano = pygame.sprite.Group()

    def movimento(self, jogador, grupo_inimigos, dt):
        # Calcula direção do jogador e distância entre inimigo e jogador
        direcao_x = jogador.pos.x - self.pos.x
        direcao_y = jogador.pos.y - self.pos.y
        distancia = (direcao_x ** 2 + direcao_y ** 2) ** (1 / 2)
        if distancia > 2000:  # Se o jogador estiver muito longe do inimigo, deleta o inimigo
            self.kill()

        # Normaliza
        direcao_x /= distancia
        direcao_y /= distancia

        # Move o inimigo
        nova_pos_x = self.pos.x + direcao_x * self.velocidade_movimento * dt
        nova_pos_y = self.pos.y + direcao_y * self.velocidade_movimento * dt

        # Verifica colisão com outros inimigos
        for outro_inimigo in grupo_inimigos:

            if outro_inimigo != self:  # Evita verificar colisão consigo mesmo

                if self.mask.overlap(outro_inimigo.mask, (outro_inimigo.rect.left - self.rect.left, outro_inimigo.rect.top - self.rect.top)):
                    # Se o inimigo atual colide com outro inimigo, empurra o inimigo atual na direção oposta
                    empurra_x = nova_pos_x - outro_inimigo.pos.x
                    empurra_y = nova_pos_y - outro_inimigo.pos.y
                    empurra_dist = (empurra_x ** 2 + empurra_y ** 2) ** (1 / 2)

                    if empurra_dist != 0:  # Evita divisão por zero caso dois inimigos estejam exatamente na mesma posição
                        empurra_x /= empurra_dist
                        empurra_y /= empurra_dist
                    else:
                        empurra_x /= 60
                        empurra_y /= 60

                    # Atualiza a nova posição
                    nova_pos_x += empurra_x * self.velocidade_movimento * dt
                    nova_pos_y += empurra_y * self.velocidade_movimento * dt

        # Por algum motivo, depois do menu inicial aparecer os inimigos se moviam muito e eu não consegui achar a causa deste comportamento
        # A melhor solução que eu achei foi limitar a distância que inimigos podem mover-se por update
        if nova_pos_x - self.pos.x > 12 or nova_pos_x - self.pos.x < (- 12) or nova_pos_y - self.pos.y > 12 or nova_pos_y - self.pos.y < (- 12):
            self.pos.x = self.pos.x
            self.pos.y = self.pos.y
        else:
            # Atualiza posição do inimigo
            self.pos.x = nova_pos_x
            self.pos.y = nova_pos_y

        if direcao_x > 0:  # Movendo pra direita
            if self.direcao != 'direita':
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.sprite_branco = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_branco]
                self.direcao = 'direita'
        else:  # Movendo pra esquerda
            if self.direcao != 'esquerda':
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.sprite_branco = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_branco]
                self.direcao = 'esquerda'

    def animar_sprite(self, tempo):
        lista_sprites = self.sprite_andando if tempo - self.ultimo_hit >= self.cooldown else self.sprite_branco
        if tempo - self.ultimo_tick > self.frame_rate_animacao:  # Se já se passou o bastante para passar para o próximo frame
            self.ultimo_tick = tempo
            self.frame = (self.frame + 1) % len(lista_sprites)  # Incrementa o index do frame
            self.image = lista_sprites[self.frame]  # Atualiza a imagem a ser desenhada na tela
            self.mask = pygame.mask.from_surface(self.image)  # Atualiza a mask

        # Atualiza posição do rect e da hitbox
        self.rect.center = self.pos

    def levar_dano(self, armas_grupo, jogador, tempo, dt, Adaga):
        for arma in armas_grupo:
            if self.mask.overlap(arma.mask, (arma.rect.left - self.rect.left, arma.rect.top - self.rect.top)) and arma.ataque_executado:

                # Calcular Knockback
                direction_x = self.pos.x - jogador.pos.x
                direction_y = self.pos.y - jogador.pos.y
                knockback_distancia = (direction_x ** 2 + direction_y ** 2) ** 0.5

                if knockback_distancia != 0:
                    direction_x /= knockback_distancia
                    direction_y /= knockback_distancia

                # Aplicar knockback
                self.pos.x += direction_x * arma.knockback * dt
                self.pos.y += direction_y * arma.knockback * dt

                # Receber dano e criar texto de dano
                if tempo - self.ultimo_hit >= self.cooldown:
                    if self.hit_points_atuais > 0:
                        self.hit_points_atuais -= max(arma.dano * jogador.ataque / self.defesa, 1)
                        self.textos_dano.add(DanoTexto(self.pos + (0, -20), max(arma.dano * jogador.ataque / self.defesa, 1), tempo))
                        self.ultimo_hit = tempo
                        if isinstance(arma, Adaga):  # Deleta adagas quando elas colidem com o inimigo
                            arma.kill()

        if tempo - self.ultimo_hit >= self.cooldown:
            self.image = self.sprite_andando[self.frame]
        else:
            self.image = self.sprite_branco[self.frame]

    def checar_hp(self, drop, grupo_item, grupo_todos, tempo):
        # Função que checa se o HP do inimigo chegou a zero e retorna 1 para a contagem de inimigos mortos em uma partida se sim
        if self.hit_points_atuais <= 0 and tempo - self.ultimo_hit >= self.cooldown:  # Se o HP do inimigo chegar a zero
            # Adiciona o item dropado aos grupos definidos de sprites para ser desenhado
            grupo_item.add(drop)
            grupo_todos.add(drop)

            # Remove o inimigo
            self.kill()

            return 1
        return 0


# Carregar Sprites
Texugo_Sprites = [pygame.image.load(f"Sprites/Inimigos/Texugo_0{i}.png") for i in range(4)]
Texugo_Sprites_branco = [pygame.image.load(f"Sprites/Inimigos/Texugo_0{i}_hit.png") for i in range(4)]

Eisqueleto_Sprites = [pygame.image.load(f"Sprites/Inimigos/Esqueleto_0{i}.png") for i in range(4)]
Eisqueleto_Sprites_branco = [pygame.image.load(f"Sprites/Inimigos/Esqueleto_0{i}_hit.png") for i in range(4)]

Minhocao_Sprites = [pygame.image.load(f"Sprites/Inimigos/minhocao_0{i}.png") for i in range(4)]
Minhocao_Sprites_branco = [pygame.image.load(f"Sprites/Inimigos/minhocao_0{i}_hit.png") for i in range(4)]

Lobo_Sprites = [pygame.image.load(f"Sprites/Inimigos/lobo_0{i}.png") for i in range(4)]
Lobo_Sprites_branco = [pygame.image.load(f"Sprites/Inimigos/lobo_0{i}_hit.png") for i in range(4)]

Zumbi_Sprites = [pygame.image.load(f"Sprites/Inimigos/Zumbi_0{i}.png") for i in range(4)]
Zumbi_Sprites_branco = [pygame.image.load(f"Sprites/Inimigos/Zumbi_0{i}_hit.png") for i in range(4)]

Morguesso_Sprites = [pygame.image.load(f"Sprites/Inimigos/morguesso_0{i}.png") for i in range(2)]
Morguesso_Sprites_branco = [pygame.image.load(f"Sprites/Inimigos/morguesso_0{i}_hit.png") for i in range(2)]

Abobora_Sprites = [pygame.image.load(f"Sprites/Inimigos/pumpkin_0{i}.png") for i in range(4)]
Abobora_Sprites_branco = [pygame.image.load(f"Sprites/Inimigos/pumpkin_0{i}_hit.png") for i in range(4)]

Hidra_Sprites = [pygame.image.load(f"Sprites/Inimigos/hidra_0{i}.png") for i in range(4)]
Hidra_Sprites_branco = [pygame.image.load(f"Sprites/Inimigos/hidra_0{i}_hit.png") for i in range(4)]

Centopeia_Sprites = [pygame.image.load(f"Sprites/Inimigos/centopeia_0{i}.png") for i in range(6)]
Centopeia_Sprites_branco = [pygame.image.load(f"Sprites/Inimigos/centopeia_0{i}_hit.png") for i in range(6)]

Morte_Sprites = [pygame.image.load(f"Sprites/Inimigos/morte_0{i}.png") for i in range(5)]


class Morguesso(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(240, 240)
        sprite_andando = [sprite.convert_alpha() for sprite in Morguesso_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Morguesso_Sprites_branco]

        # Stats
        hp = 5
        dano = 70
        defesa = 5
        velocidade_movimento = 2.2

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)
class Eisquelto(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(59, 72)
        sprite_andando = [sprite.convert_alpha() for sprite in Eisqueleto_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Eisqueleto_Sprites_branco]

        # Stats
        hp = 10
        dano = 90
        defesa = 5
        velocidade_movimento = 1.9

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)

class Texugo(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(72, 72)
        sprite_andando = [sprite.convert_alpha() for sprite in Texugo_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Texugo_Sprites_branco]

        # Stats
        hp = 35
        dano = 110
        defesa = 8
        velocidade_movimento = 1.9

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)

class Abobora(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(72, 72)
        sprite_andando = [sprite.convert_alpha() for sprite in Abobora_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Abobora_Sprites_branco]

        # Stats
        hp = 35
        dano = 130
        defesa = 16
        velocidade_movimento = 1.9

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)

class Zumbi(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(65, 72)
        sprite_andando = [sprite.convert_alpha() for sprite in Zumbi_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Zumbi_Sprites_branco]

        # Stats
        hp = 120
        dano = 150
        defesa = 5
        velocidade_movimento = 1.9

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)

class LoboPidao(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(84, 86)
        sprite_andando = [sprite.convert_alpha() for sprite in Lobo_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Lobo_Sprites_branco]

        # Stats
        hp = 135
        dano = 170
        defesa = 10
        velocidade_movimento = 1.9

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)

class Minhocao(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(128, 128)
        sprite_andando = [sprite.convert_alpha() for sprite in Minhocao_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Minhocao_Sprites_branco]

        # Stats
        hp = 180
        dano = 190
        defesa = 25
        velocidade_movimento = 1.4

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)

class Hidra(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(128, 128)
        sprite_andando = [sprite.convert_alpha() for sprite in Hidra_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Hidra_Sprites_branco]

        # Stats
        hp = 210
        dano = 210
        defesa = 15
        velocidade_movimento = 2.1

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)

class Centopeia(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(130, 49)
        sprite_andando = [sprite.convert_alpha() for sprite in Centopeia_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Centopeia_Sprites_branco]

        # Stats
        hp = 256
        dano = 230
        defesa = 15
        velocidade_movimento = 2.3

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)

class Morte(Inimigo):
    def __init__(self, pos, tempo, jogador):
        escala = pygame.math.Vector2(200, 200)
        sprite_andando = [sprite.convert_alpha() for sprite in Morte_Sprites]
        sprite_atacado = [sprite.convert_alpha() for sprite in Morte_Sprites]

        # Stats
        hp = 99999999
        dano = 99999999
        defesa = 99999999
        velocidade_movimento = 5.1

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate, sprite_atacado, tempo, jogador)