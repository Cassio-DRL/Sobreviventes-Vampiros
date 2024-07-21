from personagems import BichoChicote
from inimigos import Texugo
from coletaveis import Moeda, Cura, CristalXp
from ataques import Slash
import pygame
import random
import math

class Camera:
    def __init__(self, largura, altura):
        # Cria um Rect representando a câmera
        self.camera = pygame.Rect(0, 0, largura, altura)
        self.largura = largura
        self.altura = altura

    def mover_objeto(self, objeto):
        # Move um objeto em relação à posição atual da câmera e retorna a nova posição do objeto
        return objeto.rect.move(self.camera.topleft)

    def movimento(self, jogador):
        # Calcula a nova posição x e y da câmera de forma que o centro do jogador esteja no centro da tela
        x = int(self.largura / 2) - jogador.rect.centerx
        y = int(self.altura / 2) - jogador.rect.centery

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
            coord_multiplicador = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))
            return {(self.rect.x + largura * x, self.rect.y + altura * y) for x, y in coord_multiplicador}
        return set()

def spawnar_ao_redor(jogador, raio):
    # Função para gerar objetos em pontos aleatórios na circunferência de um circulo ao redor do jogador
    angulo = math.radians(random.randint(0, 361))
    x = jogador.rect.centerx + raio * math.cos(angulo)
    y = jogador.rect.centery + raio * math.sin(angulo)
    return pygame.math.Vector2(x, y)


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
total_inimigos_mortos = 0
cooldown_spawnar_inimigos = 0
cooldown_spawnar_items = 0

# Grupos de sprite
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
items = pygame.sprite.Group()
ataques = pygame.sprite.Group()
tiles = pygame.sprite.Group(Tile(pygame.math.Vector2(0, 0), Grama_Tile))

# Sistema
camera = Camera(LARGURA, ALTURA)
clock = pygame.time.Clock()

# Gerar jogador e ataque
jogador = BichoChicote(pygame.math.Vector2(0, 0))
todos_sprites.add(jogador)

ataque_chicote = Slash()
todos_sprites.add(ataque_chicote)
ataques.add(ataque_chicote)

# Main Game Loop
while True:
    clock.tick(FPS)
    delta_time = clock.tick(FPS) / 10  # Para multiplicar velocidade de objetos para garantir que a velocidade não seja afetada pelo FPS

    # Jogador
    jogador.movimento(delta_time)
    jogador.animar_sprite()
    jogador.nivel_update()

    camera.movimento(jogador)

    # Ataques (No momento só existe 1 tipo de ataque mas é bom já ter essa estrutura pra adicionar mais depois)
    for ataque in ataques:
        ataque.animar_sprite()
        ataque.atacar()
        ataque.atualizar_posicao(jogador)

    # Gerar background
    for tile in tiles:
        novo_tile_group = pygame.sprite.Group(Tile(pygame.math.Vector2(x, y), Grama_Tile) for x, y in tile.jogador_presente(jogador))
        if novo_tile_group:
            tiles = novo_tile_group
            break

    # Desenha sprites
    for group in (tiles, todos_sprites):
        for sprite in group:
            tela.blit(sprite.image, camera.mover_objeto(sprite))

    # Inimigo
    for inimigo in inimigos:
        inimigo.movimento(jogador, delta_time)
        inimigo.animar_sprite()
        jogador.hit_points_atuais -= inimigo.dar_dano(jogador)

        # Verificação de dano contra o inimigo se um ataque estiver sendo executado e tocando no inimigo
        for ataque in ataques:
            inimigo.hit_points_atuais -= ataque.dar_dano(inimigo, jogador)

        # Drops dependendo do tipo de inimigo
        if isinstance(inimigo, Texugo):
            drop = CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], [40, 3, 1], k=1)[0])
            total_inimigos_mortos += inimigo.checar_hp(drop, items, todos_sprites)

    # Items
    for item in items:
        item.animar_sprite()
        item.deletar_se_longe(jogador)

        # Recurso coletado dependendo do tipo de item
        if isinstance(item, Moeda):
            total_moedas += item.checar_colisao(jogador)
        elif isinstance(item, Cura):
            jogador.inventario['Poção'] += item.checar_colisao(jogador)
        elif isinstance(item, CristalXp):
            jogador.exp += item.checar_colisao(jogador)

    # Spawnar inimigos (Spawna 10 a cada 10 segundos) (Max = 40)
    if pygame.time.get_ticks() >= cooldown_spawnar_inimigos and len(inimigos) <= 40:
        for i in range(10):
            inimigo_tipo = random.choice([Texugo])
            inimigo_spawanado = inimigo_tipo(spawnar_ao_redor(jogador, 900))
            todos_sprites.add(inimigo_spawanado)
            inimigos.add(inimigo_spawanado)

        cooldown_spawnar_inimigos += 10000

    # Spawnar items (Spawna 5 a cada 15 segundos) (Max = 20)
    if pygame.time.get_ticks() >= cooldown_spawnar_items and len(items) <= 20:
        for i in range(5):
            item_tipo = random.choice([Moeda, Cura])
            item_spawnado = item_tipo(spawnar_ao_redor(jogador, 900))
            todos_sprites.add(item_spawnado)
            items.add(item_spawnado)

        cooldown_spawnar_items += 15000

    # UI
    FPS_ui = fonte_none.render(f"FPS: {clock.get_fps():.1f}", False, BRANCO)
    MOEDAS_ui = fonte_none.render(f"Moedas: {total_moedas}", False, BRANCO)
    HP_ui = fonte_none.render(f"Vida do Jogador: {jogador.hit_points_atuais}/{jogador.hit_point_max}", False, BRANCO)
    LEVEL_ui = fonte_none.render(f"Nível do Jogador: {jogador.nivel}", False, BRANCO)
    XP_ui = fonte_none.render(f"XP: {jogador.exp}/{jogador.exp_para_proximo_nivel}", False, BRANCO)
    POCOES_ui = fonte_none.render(f"Poções: {jogador.inventario['Poção']}", False, BRANCO)
    KILLCOUNT_ui = fonte_none.render(f"Inimigos Mortos: {total_inimigos_mortos}", False, BRANCO)

    tela.blit(FPS_ui, FPS_ui.get_rect(topleft=(880, 20)))
    tela.blit(MOEDAS_ui, MOEDAS_ui.get_rect(topleft=(1050, 20)))
    tela.blit(HP_ui, HP_ui.get_rect(topleft=(20, 20)))
    tela.blit(LEVEL_ui, LEVEL_ui.get_rect(topleft=(20, 50)))
    tela.blit(XP_ui,  XP_ui.get_rect(topleft=(20, 80)))
    tela.blit(POCOES_ui, POCOES_ui.get_rect(topleft=(320, 20)))
    tela.blit(KILLCOUNT_ui, KILLCOUNT_ui.get_rect(topleft=(20, 760)))

    # Eventos
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

