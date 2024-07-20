import pygame
class coletavel(pygame.sprite.Sprite):
    def __init__(self, pos, escala, sprites, qt_recurso, frame_rate):
        super().__init__()

        # Sprite
        self.escala = escala  # Dimensões do sprite (x, y)
        self.sprites = [pygame.transform.scale(pygame.image.load(sprite), self.escala) for sprite in sprites]  # Lista de frames do sprite
        self.image = self.sprites[0]  # Imagem a ser desenhada na tela

        # Objeto
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = self.pos

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
        if jogador.hitbox.colliderect(self.rect):  # Caso o jogador toque no item
            self.kill()  # Remove o item
            return self.qt_recurso  # Retorna o valor a ser adicionado a contagem do item coletado
        return 0

class Moeda(coletavel):
    def __init__(self, pos):
        escala = (25, 25)
        sprites = [f"Sprites/Moeda_girando_{i+1}.png" for i in range(7)]
        dinheiro = 1
        frame_rate = 11
        super().__init__(pos, escala, sprites, dinheiro, frame_rate)

class Cura(coletavel):
    def __init__(self, pos):
        escala = (25, 25)
        sprites = ["Sprites/pocao grande.png"]
        pocoes = 1
        frame_rate = 1
        super().__init__(pos, escala, sprites, pocoes, frame_rate)

class CristalXp(coletavel):
    def __init__(self, pos, tipo):
        escala = (50, 50)
        sprites = [f"Sprites/Cristais/{tipo}/{tipo.lower()}_crystal_000{i}.png" for i in range(4)]
        xp = 10 if tipo == 'Blue' else 40 if tipo == 'Green' else 80
        frame_rate = 11
        super().__init__(pos, escala, sprites, xp, frame_rate)
