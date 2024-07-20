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
        # Calcula a nova posição x da câmera de forma que o centro do objeto esteja no centro horizontal da tela
        x = -centro.rect.centerx + int(self.largura / 2)
        # Calcula a nova posição y da câmera de forma que o centro do objeto esteja no centro vertical da tela
        y = -centro.rect.centery + int(self.altura / 2)

        # Atualiza a posição da câmera com as novas coordenadas.
        self.camera = pygame.Rect(x, y, self.largura, self.altura)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_loaded):
        super().__init__()

        # Sprite
        self.image = sprite_loaded
        self.largura = self.image.get_width()
        self.altura = self.image.get_height()

        # Objeto
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = self.pos

    def player_presente(self, jogador):
        # Se o jogador estiver neste tile, encontra as coordenadas para desenhar tiles ao redor do tile
        tiles_ao_redor = set()
        if self.rect.colliderect(jogador.rect):
            coord_multiplicador = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))
            for index in range(9):
                x = self.pos.x + self.largura * coord_multiplicador[index][0]
                y = self.pos.y + self.altura * coord_multiplicador[index][1]
                tiles_ao_redor.add((x, y))
        return tiles_ao_redor


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
moedas = pygame.sprite.Group()
pocoes = pygame.sprite.Group()
cristais = pygame.sprite.Group()
tiles = pygame.sprite.Group(Tile(pygame.math.Vector2(0, 0), Grama_Tile))

# Sistema
camera = Camera(LARGURA, ALTURA)
clock = pygame.time.Clock()

# GERAR SPRITES TESTE --------------------------------------------------------------------------------------------------
for i in range(10):
    moeda = Moeda(pygame.math.Vector2(random.randint(100, 1101), random.randint(100, 701)))
    todos_sprites.add(moeda)
    moedas.add(moeda)

cura = Cura(pygame.math.Vector2(550, 550))
todos_sprites.add(cura)
pocoes.add(cura)

for i in range(10):
    obstagoon = Texugo(pygame.math.Vector2(random.randint(100, 1101), random.randint(100, 701)))
    todos_sprites.add(obstagoon)
    inimigos.add(obstagoon)

jogador = BichoChicote(pygame.math.Vector2(600, 400))
todos_sprites.add(jogador)
# ----------------------------------------------------------------------------------------------------------------------

# Main Game Loop
while True:
    print(tiles)
    clock.tick(FPS)
    delta_time = clock.tick(FPS) / 10  # Para multiplicar velocidade de objetos para garantir que a velocidade não seja afetada pelo FPS

    # Jogador
    jogador.movimento(delta_time)
    jogador.animar_sprite()
    jogador.nivel_update()
    jogador.beber_pocao()

    camera.movimento(jogador)

    # Gerar background
    for tile in tiles:
        tiles_para_gerar = tile.player_presente(jogador)
        new_tiles_group = pygame.sprite.Group(Tile(pygame.math.Vector2(coords[0], coords[1]), Grama_Tile) for coords in tiles_para_gerar)
        if new_tiles_group:
            break

    tiles = new_tiles_group
    for tile in tiles:
        tela.blit(tile.image, camera.mover_objeto(tile))

    # Desenha sprites
    for sprite in todos_sprites:
        tela.blit(sprite.image, camera.mover_objeto(sprite))

    # Inimigo
    for inimigo in inimigos:
        inimigo.movimento(jogador.pos, delta_time)
        inimigo.animar_sprite()
        jogador.hit_points_atuais -= inimigo.dar_dano(jogador)
        inimigo.checar_hp(CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], [40, 3, 1], k=1)[0]), cristais, todos_sprites)

    # Moedas
    for coin in moedas:
        coin.animar_sprite()
        total_moedas += coin.checar_colisao(jogador)

    # Pocao
    for potion in pocoes:
        jogador.inventario['Poção'] += potion.checar_colisao(jogador)

    # Cristais
    for cristal in cristais:
        cristal.animar_sprite()
        jogador.exp += cristal.checar_colisao(jogador)

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

    # Fechar o jogo caso aperte X
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Atualiza a tela
    pygame.display.update()

