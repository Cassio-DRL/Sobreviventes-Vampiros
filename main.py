from personagems import BichoChicote
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

class Botao:
    # Botão com texto que pode ser clicado pelo mouse
    def __init__(self, pos, largura, altura, texto, fonte, cor):
        self.rect = pygame.Rect(pos.x, pos.y, largura, altura)
        self.fonte = fonte
        self.texto = self.fonte.render(texto, False, (255, 255, 255))
        self.cor = cor

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)
        tela.blit(self.texto, self.texto.get_rect(center=self.rect.center))

    def mouse_interacao(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.rect.collidepoint(evento.pos):
                return True
        return False

def menu_pausa(largura, altura, tela, fonte, botoes, cor):
    # Função para desenhar todos os elementos da tela de pausa

    # Camada sobre a tela que permite que coisas sejam desenhadas com opacidade reduzida
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    pygame.draw.rect(camada, (20, 50, 50, 150), (0, 0, largura, altura))
    tela.blit(camada, (0, 0))

    # Texto grande no meio da tela
    texto_pausa = fonte.render(f"JOGO PAUSADO", False, cor)
    tela.blit(texto_pausa, texto_pausa.get_rect(center=(600, 400)))

    # Desenha cada botão
    for botao in botoes:
        botao.desenhar(tela)

def pontos_ao_redor(jogador, raio):
    # Função para achar pontos aleatórios na circunferência de um circulo ao redor do jogador
    angulo = math.radians(random.randint(0, 361))
    x = jogador.rect.centerx + raio * math.cos(angulo)
    y = jogador.rect.centery + raio * math.sin(angulo)
    return pygame.math.Vector2(x, y)


# Inicializar pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)  # Aparentemente faz o áudio ser melhor
pygame.init()

# Constantes
LARGURA = 1200
ALTURA = 800
FPS = 120

# Cores
BRANCO = (255, 255, 255)

# Tela
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Vampiro Sobreviventes')

# Imagens
GRAMA_TILE = pygame.image.load('Sprites/Grama_Tile.png').convert_alpha()

# Fontes
FONTE_NONE = pygame.font.Font(None, 30)
FONTE_NONE_GRANDE = pygame.font.Font(None, 150)

# Menu pausa
CONTINUAR_botao = Botao(pygame.math.Vector2(200, 700), 200, 50, "Continuar", FONTE_NONE, (100, 100, 100))
REINICIAR_botao = Botao(pygame.math.Vector2(500, 700), 200, 50, "Reiniciar", FONTE_NONE, (100, 100, 100))
MENU_PRINCIPAL_botao = Botao(pygame.math.Vector2(800, 700), 200, 50, "Menu Principal", FONTE_NONE, (100, 100, 100))
botoes_menu_pausa = (CONTINUAR_botao, REINICIAR_botao, MENU_PRINCIPAL_botao)

# Sistema
camera = Camera(LARGURA, ALTURA)
clock = pygame.time.Clock()

def main():
    # Música do Nível
    pygame.mixer_music.load('Audio/Musica_de_batalha_muito_top_SOULKNIGHT.mp3')
    pygame.mixer_music.play(10000)

    # Stats do jogo
    total_moedas = 0
    total_inimigos_mortos = 0
    cooldown_spawnar_inimigos = -10000
    cooldown_spawnar_items = -15000

    # Grupos de sprite
    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    items = pygame.sprite.Group()
    ataques = pygame.sprite.Group()
    tiles = pygame.sprite.Group(Tile(pygame.math.Vector2(0, 0), GRAMA_TILE))

    # Gerar jogador e ataque
    jogador = BichoChicote(pygame.math.Vector2(0, 0))
    todos_sprites.add(jogador)

    ataque_chicote = Slash()
    todos_sprites.add(ataque_chicote)
    ataques.add(ataque_chicote)

    # Main Game Loop
    jogo_pausado = False
    jogo_rodando = True

    while jogo_rodando:
        clock.tick(FPS)
        delta_time = clock.tick(FPS) / 10  # Para multiplicar velocidade de objetos para garantir que a velocidade não seja afetada pelo FPS

        if not jogo_pausado:
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
                novo_tile_group = pygame.sprite.Group(Tile(pygame.math.Vector2(x, y), GRAMA_TILE) for x, y in tile.jogador_presente(jogador))
                if novo_tile_group:
                    tiles = novo_tile_group
                    break

            # Desenha sprites
            for group in (tiles, todos_sprites):
                for sprite in group:
                    TELA.blit(sprite.image, camera.mover_objeto(sprite))

            # Inimigo
            for inimigo in inimigos:
                inimigo.movimento(jogador, delta_time)
                inimigo.animar_sprite()
                jogador.hit_points_atuais -= inimigo.dar_dano(jogador)

                # Verificação de dano contra o inimigo se um ataque estiver sendo executado e tocando no inimigo
                for ataque in ataques:
                    inimigo.hit_points_atuais -= ataque_chicote.dar_dano(inimigo, jogador)

                # Drops dependendo do tipo de inimigo
                if isinstance(inimigo, Texugo):
                    drop = CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], [40, 3, 1], k=1)[0])
                    total_inimigos_mortos += inimigo.checar_hp(drop, items, todos_sprites)

            # Items
            for item in items:
                item.animar_sprite()
                item.magnetismo(jogador, delta_time)

                # Recurso coletado dependendo do tipo de item
                if isinstance(item, Moeda):
                    total_moedas += item.checar_colisao(jogador)
                elif isinstance(item, Cura):
                    jogador.inventario['Poção'] += item.checar_colisao(jogador)
                elif isinstance(item, CristalXp):
                    jogador.exp += item.checar_colisao(jogador)

            # Spawnar inimigos (Spawna 10 a cada 10 segundos) (Max = 40)
            if pygame.time.get_ticks() - cooldown_spawnar_inimigos >= 10000 and len(inimigos) <= 40:
                cooldown_spawnar_inimigos = pygame.time.get_ticks()
                for i in range(10):
                    inimigo_tipo = random.choice([Texugo])
                    inimigo_spawanado = inimigo_tipo(pontos_ao_redor(jogador, 900))
                    todos_sprites.add(inimigo_spawanado)
                    inimigos.add(inimigo_spawanado)

            # Spawnar items (Spawna 5 a cada 15 segundos) (Max = 20)
            if pygame.time.get_ticks() - cooldown_spawnar_items >= 15000 and len(items) <= 20:
                cooldown_spawnar_items = pygame.time.get_ticks()
                for i in range(5):
                    item_tipo = random.choice([Moeda, Cura])
                    item_spawnado = item_tipo(pontos_ao_redor(jogador, 900))
                    todos_sprites.add(item_spawnado)
                    items.add(item_spawnado)

            # UI
            FPS_ui = FONTE_NONE.render(f"FPS: {clock.get_fps():.1f}", False, BRANCO)
            MOEDAS_ui = FONTE_NONE.render(f"Moedas: {total_moedas}", False, BRANCO)
            HP_ui = FONTE_NONE.render(f"Vida do Jogador: {jogador.hit_points_atuais}/{jogador.hit_point_max}", False, BRANCO)
            LEVEL_ui = FONTE_NONE.render(f"Nível do Jogador: {jogador.nivel}", False, BRANCO)
            XP_ui = FONTE_NONE.render(f"XP: {jogador.exp}/{jogador.exp_para_proximo_nivel}", False, BRANCO)
            POCOES_ui = FONTE_NONE.render(f"Poções: {jogador.inventario['Poção']}", False, BRANCO)
            KILLCOUNT_ui = FONTE_NONE.render(f"Inimigos Mortos: {total_inimigos_mortos}", False, BRANCO)

            TELA.blit(FPS_ui, FPS_ui.get_rect(topleft=(880, 20)))
            TELA.blit(MOEDAS_ui, MOEDAS_ui.get_rect(topleft=(1050, 20)))
            TELA.blit(HP_ui, HP_ui.get_rect(topleft=(20, 20)))
            TELA.blit(LEVEL_ui, LEVEL_ui.get_rect(topleft=(20, 50)))
            TELA.blit(XP_ui, XP_ui.get_rect(topleft=(20, 80)))
            TELA.blit(POCOES_ui, POCOES_ui.get_rect(topleft=(320, 20)))
            TELA.blit(KILLCOUNT_ui, KILLCOUNT_ui.get_rect(topleft=(20, 760)))

        # Eventos
        for evento in pygame.event.get():
            # Fechar o jogo caso aperte o botão na janela
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Checar se alguma tecla relevante foi apertada
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Pausar ou despausar jogo se apertar ESC
                    if not jogo_pausado:
                        jogo_pausado = True
                        menu_pausa(LARGURA, ALTURA, TELA, FONTE_NONE_GRANDE, botoes_menu_pausa, BRANCO)
                    else:
                        jogo_pausado = False

                if not jogo_pausado:
                    if evento.key == pygame.K_q:  # Beber poção caso aperte Q
                        jogador.beber_pocao()

            if jogo_pausado:
                for botao in botoes_menu_pausa:  # Apertos de botão na tela de pausa
                    if botao.mouse_interacao(evento):
                        if botao == CONTINUAR_botao:
                            jogo_pausado = False
                        elif botao == MENU_PRINCIPAL_botao:
                            pygame.quit()
                            exit()
                        elif botao == REINICIAR_botao:
                            jogo_rodando = False

        # Atualiza a tela
        pygame.display.update()


while True:
    main()
