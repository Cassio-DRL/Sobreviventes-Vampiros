from personagems import BichoChicote
from inimigos import Texugo
from coletaveis import Moeda, Cura, CristalXp
import pygame
import random

class Camera:
    def __init__(self, largura, altura):
        # Cria um Rect representando a câmera
        self.camera = pygame.Rect(0, 0, largura, altura)
        self.largura = largura
        self.altura = altura

    def mover_objeto(self, objeto):
        # Move o objeto em relação à posição atual da câmera e retorna a nova posição do objeto
        return objeto.rect.move(self.camera.topleft)

    def movimento(self, centro):
        # Calcula a nova posição x da câmera de forma que o centro do jogador esteja no centro horizontal da tela
        x = -centro.rect.centerx + int(self.largura / 2)
        # Calcula a nova posição y da câmera de forma que o centro do jogador esteja no centro vertical da tela
        y = -centro.rect.centery + int(self.altura / 2)

        # Atualiza a posição da câmera com as novas coordenadas
        self.camera = pygame.Rect(x, y, self.largura, self.altura)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_loaded):
        super().__init__()
        self.image = sprite_loaded
        self.rect = self.image.get_rect(topleft=pos)

    def jogador_presente(self, jogador):
        # Se o jogador estiver neste tile, encontra as coordenadas para desenhar tiles ao redor do tile
        if self.rect.colliderect(jogador.rect):
            largura, altura = self.rect.size
            coord_multiplicador = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
            return {(self.rect.x + largura * x, self.rect.y + altura * y) for x, y in coord_multiplicador}
        return set()


pygame.init()

# Música do Nível
pygame.mixer_music.load('Audio/Musica_de_batalha_muito_top_SOULKNIGHT.mp3')
pygame.mixer_music.play(10000)

# Constantes
LARGURA = 1200
ALTURA = 800
FPS = 120

# Cores
BRANCO = (255, 255, 255)

# Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Vampiro Sobreviventes')

# Imagens
Grama_Tile = pygame.image.load('Sprites/Grama_Tile.png').convert_alpha()

# Fontes
fonte_none = pygame.font.Font(None, 30)

# Stats do jogo
total_moedas = 0

# Grupos de sprite
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
items = pygame.sprite.Group()
tiles = pygame.sprite.Group(Tile(pygame.math.Vector2(0, 0), Grama_Tile))

# Sistema
camera = Camera(LARGURA, ALTURA)
clock = pygame.time.Clock()

# GERAR SPRITES TESTE --------------------------------------------------------------------------------------------------
for i in range(10):
    moeda = Moeda(pygame.math.Vector2(random.randint(100, 1101), random.randint(100, 701)))
    todos_sprites.add(moeda)
    items.add(moeda)

cura = Cura(pygame.math.Vector2(550, 550))
todos_sprites.add(cura)
items.add(cura)

jogador = BichoChicote(pygame.math.Vector2(600, 400))
todos_sprites.add(jogador)

for i in range(10):
    obstagoon = Texugo(pygame.math.Vector2(random.randint(100, 1101), random.randint(100, 701)))
    todos_sprites.add(obstagoon)
    inimigos.add(obstagoon)
# ----------------------------------------------------------------------------------------------------------------------

# Main Game Loop
while True:
    clock.tick(FPS)
    delta_time = clock.tick(FPS) / 10  # Para multiplicar velocidade de objetos para garantir que a velocidade não seja afetada pelo FPS

    # Jogador
    jogador.movimento(delta_time)
    jogador.animar_sprite()
    jogador.nivel_update()

    camera.movimento(jogador)

    # Gerar background
    for tile in tiles:
        novo_tile_group = pygame.sprite.Group(Tile(pygame.math.Vector2(coords[0], coords[1]), Grama_Tile) for coords in tile.jogador_presente(jogador))
        if novo_tile_group:
            tiles = novo_tile_group
            break

    # Desenha sprites
    for tile in tiles:
        tela.blit(tile.image, camera.mover_objeto(tile))
    for sprite in todos_sprites:
        tela.blit(sprite.image, camera.mover_objeto(sprite))

    # Inimigo
    for inimigo in inimigos:
        inimigo.movimento(jogador.pos, delta_time)
        inimigo.animar_sprite()
        jogador.hit_points_atuais -= inimigo.dar_dano(jogador)
        if isinstance(inimigo, Texugo):
            drop = CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], [40, 3, 1], k=1)[0])
            inimigo.checar_hp(drop, items, todos_sprites)

    # Items
    for item in items:
        item.animar_sprite()
        if isinstance(item, Moeda):
            total_moedas += item.checar_colisao(jogador)
        elif isinstance(item, Cura):
            jogador.inventario['Poção'] += item.checar_colisao(jogador)
        elif isinstance(item, CristalXp):
            jogador.exp += item.checar_colisao(jogador)

    # UI
    FPS_ui = fonte_none.render(f"FPS: {clock.get_fps():.1f}", False, BRANCO)
    MOEDAS_ui = fonte_none.render(f"Moedas: {total_moedas}", False, BRANCO)
    HP_ui = fonte_none.render(f"Vida do Jogador: {jogador.hit_points_atuais}/{jogador.hit_point_max}", False, BRANCO)
    LEVEL_ui = fonte_none.render(f"Nível do Jogador: {jogador.nivel}", False, BRANCO)
    XP_ui = fonte_none.render(f"XP: {jogador.exp}/{jogador.exp_para_proximo_nivel}", False, BRANCO)
    POCOES_ui = fonte_none.render(f"Poções: {jogador.inventario['Poção']}", False, BRANCO)

    tela.blit(FPS_ui, FPS_ui.get_rect(center=(800, 20)))
    tela.blit(MOEDAS_ui, MOEDAS_ui.get_rect(center=(1000, 20)))
    tela.blit(HP_ui, HP_ui.get_rect(center=(150, 20)))
    tela.blit(LEVEL_ui, LEVEL_ui.get_rect(center=(121, 50)))
    tela.blit(XP_ui,  XP_ui.get_rect(center=(121, 70)))
    tela.blit(POCOES_ui, POCOES_ui.get_rect(center=(500, 20)))

    for evento in pygame.event.get():

        # Fechar o jogo caso aperte o botão na janela
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Checar se alguma tecla relevante foi apertada
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_q:  # Beber poção caso aperte Q
                jogador.beber_pocao()

    # Atualiza a tela
    pygame.display.update()

