import pygame

class Ataque(pygame.sprite.Sprite):
    def __init__(self, pos, escala, dano, duracao_ataque, cooldown_ataque, sprite_invisivel, sprites_animacao, frame_rate):
        super().__init__()

        #objeto e sua posicao
        self.pos = pos
        self.escala = escala
        self.sprite_invisivel = pygame.transform.scale(pygame.image.load(sprite_invisivel), self.escala)

        # BUG - ERRO NA INVERSÃO DO SPRITE
        self.sprites_animacao = [pygame.transform.scale(pygame.image.load(sprite), self.escala) for sprite in sprites_animacao]

        #atributos do ataque
        self.dano = dano
        self.duracao_ataque = duracao_ataque * 1000 #convertendo para milisegundos
        self.cooldown_ataque = cooldown_ataque * 1000 #convertendo para milisegundos

        #atributos de animacao e hitbox
        self.frame_rate = 1000 // frame_rate
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.ultimo_hit = pygame.time.get_ticks()
        self.ultimo_ataque = pygame.time.get_ticks()
        self.ultimo_dano = pygame.time.get_ticks()
        self.ultimo_ataque_a_inimigo = {} # dicionario utilizado para rastrear o ultimo ataque a um inimigo, pois o ataque recebe um inimigo de cada vez, mais otimizado.
        self.ataque_executado = False

        self.image = self.sprites_animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def dar_dano(self, inimigo):
        tempo_atual = pygame.time.get_ticks()
        #verifica se o ataque atingiu o inimigo
        if self.rect.colliderect(inimigo.hitbox) and self.ataque_executado:
            #verifica se o inimigo reecbeu hit e se o tempo do ultimo ataque a ele foi + que 1 segundo
            if inimigo not in self.ultimo_ataque_a_inimigo or tempo_atual - self.ultimo_ataque_a_inimigo[inimigo] >= 1000:
                # Aplica o dano e atualiza o tempo do último ataque a este inimigo
                self.ultimo_ataque_a_inimigo.update({inimigo: tempo_atual})
                if self.dano // inimigo.defesa >= 1:
                    return self.dano // inimigo.defesa
                else:
                    return 1  # Dano mínimo de 1
        return 0  # Nenhum dano se não houver colisão ou se o ataque não foi executado
    
    #a segunda funcao ira realizar o ataque, e ira retornar a variavel ataque_executado como true ou false, no intervalo definido pelo cooldown e duracao de ataque.
    def atacar(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_hit < self.cooldown_ataque: #tempo atual - ultimo hit < cooldown_ataque, entao nao executa ataque
            self.ataque_executado = False
        else:
            if tempo_atual - self.ultimo_hit < self.duracao_ataque + self.cooldown_ataque: #tempo atual - ultimo hit < duracao_ataque + cooldown_ataque, entao executa ataque
                self.ataque_executado = True
            else:
                self.ataque_executado = False
                self.ultimo_hit = tempo_atual
        return self.ataque_executado
        
    #a terceira funcao eh responsavel por animar o ataque, e ira atualizar o frame do ataque, e a imagem do ataque
    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks() 

        if tick_atual - self.ultimo_tick > self.frame_rate and self.ataque_executado: #se o tempo atual - o ultimo tick for maior que o frame rate, entao atualizamos o frame
            self.ultimo_tick = tick_atual #atualizamos o ultimo tick
            self.frame = (self.frame + 1) % len(self.sprites_animacao) #atualizamos o frame
            self.image = self.sprites_animacao[self.frame] #atualizamos a imagem
        elif not self.ataque_executado:
            self.image = self.sprite_invisivel

        self.rect = self.image.get_rect() #atualizamos a hitbox
        self.rect.center = self.pos #atualizamos a posicao da hitbox

    def atualizar_posicao(self, pos_jogador, direcao_jogador, offset): #funcao para adicionar um offset para ataques especificos
        if direcao_jogador == 'direita':
            self.pos = pos_jogador + pygame.math.Vector2(offset, 0)
        elif direcao_jogador == 'esquerda':
            self.pos = pos_jogador - pygame.math.Vector2(offset, 0)

class Slash(Ataque):
    def __init__(self, pos):

        escala = pygame.math.Vector2(150, 120)
        sprite_invisivel = 'Sprites/Ataques/ataque_invisivel.png'

        #BUG - ERRO NA INVERSÃO DO SPRITE
        sprites_animacao = [f"Sprites/Ataques/Slash_chicote/ataque_chicote_{i+1}.png" for i in range(4)]


        dano = 50
        duracao_ataque = 1
        cooldown_ataque = 0.5

        frame_rate = 8

        super().__init__(pos, escala, dano, duracao_ataque, cooldown_ataque, sprite_invisivel, sprites_animacao, frame_rate)