import pygame
class coletavel(pygame.sprite.Sprite):
    def __init__(self, pos, escala, sprites, qt_recurso, frame_rate):
        super().__init__()

        # Sprite
        self.sprites = [pygame.transform.scale(sprite, escala) for sprite in sprites]  # Lista de frames do sprite
        self.image = self.sprites[0]  # Imagem a ser desenhada na tela

        # Objeto
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)  # Mask para ser usada como hitbox
        self.pos = pos

        # Animação
        self.frame = 0  # Frame Atual
        self.ultimo_tick = pygame.time.get_ticks()  # Contagem de ticks quando o frame foi atualizado pela última vez
        self.frame_rate_animacao = 1000 // frame_rate  # Frame rate da animação do sprite

        # Coleta de item
        self.qt_recurso = qt_recurso  # Número que vai ser somado a alguma contagem

    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()  # Contagem de ticks quando a função é chamada
        if tick_atual - self.ultimo_tick > self.frame_rate_animacao:  # Se já se passou o bastante para passar para o próximo frame
            self.ultimo_tick = tick_atual
            self.frame = (self.frame + 1) % len(self.sprites)  # Incrementa o index do frame
            self.image = self.sprites[self.frame]  # Atualiza a imagem a ser desenhada na tela

    def checar_colisao(self, jogador):
        if self.mask.overlap(jogador.mask, (jogador.rect.left - self.rect.left, jogador.rect.top - self.rect.top)):  # Caso o jogador toque no item
            self.kill()  # Remove o item
            return self.qt_recurso  # Retorna o valor a ser adicionado a contagem do item coletado
        return 0

    def magnetismo(self, jogador, dt):
        direcao_x = jogador.pos.x - self.pos.x
        direcao_y = jogador.pos.y - self.pos.y
        distancia = (direcao_x ** 2 + direcao_y ** 2) ** (1 / 2)
        if distancia > 2000:  # Se o jogador estiver muito longe do item, deleta o item
            self.kill()
        elif distancia < 150:   # Faz com que items dentro de uma certa distância se movam em direção ao jogador
            # Normaliza
            direcao_x /= distancia
            direcao_y /= distancia

            # Move o coletavel em direção ao jogador
            self.pos.x += direcao_x * dt * 10
            self.pos.y += direcao_y * dt * 10
            self.rect.topleft = self.pos


# Carregar sprites
Moeda_Sprites = [pygame.image.load(f"Sprites/Moeda_girando_{i+1}.png") for i in range(7)]
Cura_Sprites = [pygame.image.load("Sprites/pocao grande.png")]
Velocidade_Sprites = [pygame.image.load("Sprites/pocao pequena.png")]
Bomba_Sprites = [pygame.image.load("Sprites/bomba.png")]
Dobro_Xp = [pygame.image.load("Sprites/banana_dobro_xp.png")]

class Moeda(coletavel):
    def __init__(self, pos):
        escala = (25, 25)
        sprites = [sprite.convert_alpha() for sprite in Moeda_Sprites]
        dinheiro = 1
        frame_rate = 11
        super().__init__(pos, escala, sprites, dinheiro, frame_rate)

class Cura(coletavel):
    def __init__(self, pos):
        escala = (35, 35)
        sprites = [sprite.convert_alpha() for sprite in Cura_Sprites]
        pocoes = 1
        frame_rate = 1
        super().__init__(pos, escala, sprites, pocoes, frame_rate)

class Velocidade(coletavel):
    def __init__(self, pos):
        escala = (25, 31)
        sprites = [sprite.convert_alpha() for sprite in Velocidade_Sprites]
        pocoes_rapidas = 1
        frame_rate = 1
        super().__init__(pos, escala, sprites, pocoes_rapidas, frame_rate)

class Bomba(coletavel):
    def __init__(self, pos):
        escala = (25, 25)
        sprites = [sprite.convert_alpha() for sprite in Bomba_Sprites]
        bombas = 1
        frame_rate = 1
        super().__init__(pos, escala, sprites, bombas, frame_rate)

class DobroXp(coletavel):
    def __init__(self, pos):
        escala = (25, 25)
        sprites = [sprite.convert_alpha() for sprite in Dobro_Xp]
        bananas = 1
        frame_rate = 1
        super().__init__(pos, escala, sprites, bananas, frame_rate)

class CristalXp(coletavel):
    def __init__(self, pos, tipo):
        escala = (50, 50)
        sprites = [pygame.image.load(f"Sprites/Cristais/{tipo}/{tipo.lower()}_crystal_000{i}.png").convert_alpha() for i in range(4)]
        xp = 10 if tipo == 'Blue' else 40 if tipo == 'Green' else 80
        frame_rate = 11
        super().__init__(pos, escala, sprites, xp, frame_rate)

