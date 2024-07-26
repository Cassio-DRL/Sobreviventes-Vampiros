import pygame
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, pos, sprites_walking, escala, hit_points, dano, defesa, velocidade_movimento, frame_rate):
        super().__init__()

        # Sprite
        self.sprite_andando = [pygame.transform.scale(sprite, escala) for sprite in sprites_walking]  # Lista de frames do sprite
        self.image = self.sprite_andando[0]  # Imagem a ser desenhada na tela
        self.direcao = 'direita'  # Direção para qual o sprite está indo

        # Objeto
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Mask para ser usada como hitbox
        self.pos = pos

        # Stats
        self.hit_point_max = hit_points
        self.hit_points_atuais = self.hit_point_max
        self.dano = dano
        self.defesa = defesa
        self.velocidade_movimento = velocidade_movimento

        # Animação
        self.frame = 0  # Frame Atual
        self.ultimo_tick = pygame.time.get_ticks()  # Contagem de ticks quando o frame foi atualizado pela última vez
        self.frame_rate_animacao = 1000 // frame_rate  # Frame rate da animação do sprite

        # Dano
        self.ultimo_hit = pygame.time.get_ticks()  # Contagem de ticks quando o inimigo deu dano pela última vez

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


        # Atualiza posição do inimigo
        self.pos.x = nova_pos_x
        self.pos.y = nova_pos_y

        if direcao_x > 0:  # Movendo pra direita
            if self.direcao != 'direita':
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.direcao = 'direita'
        else:  # Movendo pra esquerda
            if self.direcao != 'esquerda':
                self.sprite_andando = [pygame.transform.flip(sprite, True, False) for sprite in self.sprite_andando]
                self.direcao = 'esquerda'

    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()  # Contagem de ticks quando a função é chamada
        if tick_atual - self.ultimo_tick > self.frame_rate_animacao:  # Se já se passou o bastante para passar para o próximo frame
            self.ultimo_tick = tick_atual
            self.frame = (self.frame + 1) % len(self.sprite_andando)  # Incrementa o index do frame
            self.image = self.sprite_andando[self.frame]  # Atualiza a imagem a ser desenhada na tela
            self.mask = pygame.mask.from_surface(self.image)  # Atualiza a mask

        # Atualiza posição do rect e da hitbox
        self.rect.center = self.pos

    def dar_dano(self, jogador):
        tick_atual = pygame.time.get_ticks()  # Contagem de ticks quando a função é chamada
        # Se o inimigo está encostando no jogador e já passou tempo o bastante do último ataque (cooldown de 1s)
        if self.mask.overlap(jogador.mask, (jogador.rect.left - self.rect.left, jogador.rect.top - self.rect.top)) and tick_atual - self.ultimo_hit >= 1000:
            self.ultimo_hit = tick_atual
            return max(self.dano // jogador.defesa, 1)  # Dano mínimo de 1
        return 0

    def checar_hp(self, drop, grupo_item, grupo_todos):
        # Função que checa se o HP do inimigo chegou a zero e retorna 1 para a contagem de inimigos mortos em uma partida se sim
        if self.hit_points_atuais <= 0:  # Se o HP do inimigo chegar a zero
            # Adiciona o item dropado aos grupos definidos de sprites para ser desenhado
            grupo_item.add(drop)
            grupo_todos.add(drop)

            # Remove o inimigo
            self.kill()

            return 1
        return 0


# Carregar Sprites
Texugo_Sprites = [pygame.image.load(f"Sprites/Inimigos/Texugo_0{i}.png") for i in range(4)]
Esqueleto_Sprites = [pygame.image.load(f"Sprites/Inimigos/Esqueleto_0{i}.png") for i in range(4)]
Minhocao_Sprites = [pygame.image.load(f"Sprites/Inimigos/minhocao_0{i}.png") for i in range(4)]
Lobo_Sprites = [pygame.image.load(f"Sprites/Inimigos/lobo_0{i}.png") for i in range(4)]
Zumbi_Sprites = [pygame.image.load(f"Sprites/Inimigos/Zumbi_0{i}.png") for i in range(4)]

class Texugo(Inimigo):
    def __init__(self, pos):
        escala = pygame.math.Vector2(72, 72)
        sprite_andando = [sprite.convert_alpha() for sprite in Texugo_Sprites]

        # Stats
        hp = 35
        dano = 70
        defesa = 8
        velocidade_movimento = 1.2

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate)

class Eisquelto(Inimigo):
    def __init__(self, pos):
        escala = pygame.math.Vector2(59, 72)
        sprite_andando = [sprite.convert_alpha() for sprite in Esqueleto_Sprites]

        # Stats
        hp = 20
        dano = 50
        defesa = 5
        velocidade_movimento = 1.2

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate)

class Minhocao(Inimigo):
    def __init__(self, pos):
        escala = pygame.math.Vector2(128, 128)
        sprite_andando = [sprite.convert_alpha() for sprite in Minhocao_Sprites]

        # Stats
        hp = 100
        dano = 120
        defesa = 15
        velocidade_movimento = 1.2

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate)

class LoboPidao(Inimigo):
    def __init__(self, pos):
        escala = pygame.math.Vector2(84, 86)
        sprite_andando = [sprite.convert_alpha() for sprite in Lobo_Sprites]

        # Stats
        hp = 80
        dano = 105
        defesa = 5
        velocidade_movimento = 1.2

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate)

class Zumbi(Inimigo):
    def __init__(self, pos):
        escala = pygame.math.Vector2(65, 72)
        sprite_andando = [sprite.convert_alpha() for sprite in Zumbi_Sprites]

        # Stats
        hp = 150
        dano = 50
        defesa = 5
        velocidade_movimento = 1.2

        # Animação
        frame_rate = 9

        super().__init__(pos, sprite_andando, escala, hp, dano, defesa, velocidade_movimento, frame_rate)


