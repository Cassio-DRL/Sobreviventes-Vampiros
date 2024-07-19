import pygame
class coletavel(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, escala, sprites, qt_recurso):
        super().__init__()
        self.escala = escala
        self.sprites = [pygame.transform.scale(sprite, self.escala) for sprite in sprites]
        self.recurso = qt_recurso

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(pos_x, pos_y)
        self.rect.center = self.pos

        # Animação
        self.frame = 0
        self.ultimo_tick = pygame.time.get_ticks()
        self.frame_rate_animacao = 1000 // 11

    def animar_sprite(self):
        tick_atual = pygame.time.get_ticks()
        if tick_atual - self.ultimo_tick > self.frame_rate_animacao:
            self.ultimo_tick = tick_atual
            self.frame = (self.frame + 1) % len(self.sprites)
            self.image = self.sprites[self.frame]

    def checar_colisao(self, jogador):
        if jogador.hitbox.colliderect(self.rect):
            self.kill()
            return self.recurso
        return 0

class Moeda(coletavel):
    def __init__(self, pos_x, pos_y):
        escala = (25, 25)
        sprites = [pygame.image.load(f"Sprites/Moeda_girando_{i+1}.png") for i in range(7)]
        dinheiro = 1
        super().__init__(pos_x, pos_y, escala, sprites, dinheiro)

class Cura(coletavel):
    def __init__(self, pos_x, pos_y):
        escala = (25, 25)
        sprites = [pygame.image.load("Sprites/pocao grande.png")]
        cura = 25
        super().__init__(pos_x, pos_y, escala, sprites, cura)

class CristalXp(coletavel):
    def __init__(self, pos_x, pos_y, tipo):
        escala = (50, 50)
        sprites = [pygame.image.load(f"Sprites/Cristais/{tipo}/{tipo.lower()}_crystal_000{i}.png") for i in range(4)]
        xp = 10 if tipo == 'Blue' else 20 if tipo == 'Green' else 30
        super().__init__(pos_x, pos_y, escala, sprites, xp)

