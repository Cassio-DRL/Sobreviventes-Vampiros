import pygame
class Ataque(pygame.sprite.Sprite):
    def __init__(self, escala, dano, duracao_ataque, cooldown_ataque, sprite_invisivel, sprites_animacao, frame_rate, offset):
        super().__init__()

        # Sprite
        self.sprite_invisivel = pygame.transform.scale(sprite_invisivel, escala)
        self.sprites_animacao = [pygame.transform.scale(sprite, escala) for sprite in sprites_animacao]
        self.image = self.sprites_animacao[0]
        self.direcao = 'direita'

        # Objeto
        self.pos = pygame.math.Vector2(0, 0)
        self.rect = self.image.get_rect(center=self.pos)
        self.offset = offset

        # Stats
        self.dano = dano
        self.duracao_ataque = duracao_ataque * 1000  # convertendo para milisegundos
        self.cooldown_ataque = cooldown_ataque * 1000  # convertendo para milisegundos

        # Animação
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate = 1000 // frame_rate

        # Dano
        self.ultimo_hit = pygame.time.get_ticks()
        self.ultimo_ataque_a_inimigo = {}  # dicionario utilizado para rastrear o ultimo ataque a um inimigo, pois o ataque recebe um inimigo de cada vez, mais otimizado.
        self.ataque_executado = False

    def dar_dano(self, inimigo, jogador):
        tempo_atual = pygame.time.get_ticks()
        # verifica se o ataque atingiu o inimigo
        if self.rect.colliderect(inimigo.hitbox) and self.ataque_executado:
            # verifica se o inimigo reecbeu hit e se o tempo do ultimo ataque a ele foi + que 1 segundo
            if inimigo not in self.ultimo_ataque_a_inimigo or tempo_atual - self.ultimo_ataque_a_inimigo[inimigo] >= 1000:
                # Aplica o dano e atualiza o tempo do último ataque a este inimigo
                self.ultimo_ataque_a_inimigo[inimigo] = tempo_atual
                return max(self.dano * jogador.ataque // inimigo.defesa, 1)  # Dano mínimo de 1
        return 0

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

        elif not self.ataque_executado:
            self.image = self.sprite_invisivel

        # Atualizar hitbox
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self, jogador):  # funcao para adicionar um offset para ataques especificos
        offset_vec = pygame.math.Vector2(self.offset, 0)
        self.pos = jogador.pos + offset_vec if jogador.direcao == 'direita' else jogador.pos - offset_vec

        # Compara a direção do ataque com a direção do player e inverte o sprite se for diferente
        if self.direcao != jogador.direcao:
            self.direcao = jogador.direcao
            self.sprites_animacao = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites_animacao]

        self.rect.center = self.pos


# Carregar sprites
Sprite_Invisivel = pygame.image.load('Sprites/Ataques/ataque_invisivel.png')
Slash_Sprites = [pygame.image.load(f"Sprites/Ataques/Slash_chicote/ataque_chicote_{i+1}.png") for i in range(4)]

class Slash(Ataque):
    def __init__(self):
        escala = pygame.math.Vector2(150, 120)
        sprite_invisivel = Sprite_Invisivel
        sprites_animacao = [sprite.convert_alpha() for sprite in Slash_Sprites]

        # Stats
        dano = 10
        duracao_ataque = 1
        cooldown_ataque = 0.5

        # Animação
        frame_rate = 8

        # Offset em relação ao jogador
        offset = 100

        super().__init__(escala, dano, duracao_ataque, cooldown_ataque, sprite_invisivel, sprites_animacao, frame_rate, offset)
