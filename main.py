from UIs import *
from personagems import *
from inimigos import *
from coletaveis import *
from ataques import *
import random
import math
import sys

class Camera:
    # Cria um Rect representando a câmera
    def __init__(self, largura, altura):
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

def pontos_ao_redor(jogador, raio):
    # Função para achar pontos aleatórios na circunferência de um circulo ao redor do jogador
    angulo = math.radians(random.randint(0, 361))
    x = jogador.rect.centerx + raio * math.cos(angulo)
    y = jogador.rect.centery + raio * math.sin(angulo)
    return pygame.math.Vector2(x, y)

# Inicializar pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.mixer_music.load('Audio/0106 - Vempair Survaivors.mp3')

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Dimensões da tela
LARGURA = 1280
ALTURA = 800
FPS = 60

# Inicializando a tela
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Vampiro Sobreviventes')

# Fontes
FONTE_NONE = pygame.font.Font(None, 30)
FONTE_NONE_MEDIA = pygame.font.Font(None, 74)
FONTE_NONE_GRANDE = pygame.font.Font(None, 150)

# Imagens
GRAMA_TILE = pygame.image.load('Sprites/Grama_Tile.png').convert_alpha()

# Menu pausa
CONTINUAR_botao_pausa = Botao(pygame.math.Vector2(200, 700), 200, 50, "Continuar", FONTE_NONE, (100, 100, 100))
REINICIAR_botao_pausa = Botao(pygame.math.Vector2(500, 700), 200, 50, "Reiniciar", FONTE_NONE, (100, 100, 100))
MENU_PRINCIPAL_botao = Botao(pygame.math.Vector2(800, 700), 200, 50, "Menu Principal", FONTE_NONE, (100, 100, 100))
botoes_menu_pausa = (CONTINUAR_botao_pausa, REINICIAR_botao_pausa, MENU_PRINCIPAL_botao)

# Tela morte
REINICIAR_botao_morte = Botao(pygame.math.Vector2(200, 700), 200, 50, "Reiniciar", FONTE_NONE, (100, 100, 100))
MENU_PRINCIPAL_botao_morte = Botao(pygame.math.Vector2(900, 700), 200, 50, "Menu Principal", FONTE_NONE, (100, 100, 100))
botoes_tela_morte = (REINICIAR_botao_morte, MENU_PRINCIPAL_botao_morte)

# Sistema
camera = Camera(LARGURA, ALTURA)
clock = pygame.time.Clock()

def iniciar_jogo(start_ticks):

    # Música do Nível
    pygame.mixer_music.play(-1)

    # Contagem
    total_moedas = 0
    total_cristais = 0
    total_inimigos_mortos = 0

    # Cooldowns
    cooldown_spawnar_inimigos = -10000
    cooldown_spawnar_items = -15000
    dobro_xp_usado = -10000
    pocao_velocidade_usada = -10000

    # Tempo
    tempo_pausado_total = 0

    # Grupos de sprite
    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    items = pygame.sprite.Group()
    ataques = pygame.sprite.Group()
    tiles = pygame.sprite.Group(Tile(pygame.math.Vector2(0, 0), GRAMA_TILE))

    # Gerar jogador e ataque
    jogador = BichoChicote(pygame.math.Vector2(0, 0))
    hp_bar = BarraVida(70, 10, (0, 50))
    xp_bar = BarraExp(LARGURA, 30, (0, 0))
    ataque_chicote = Slash()
    todos_sprites.add(jogador, ataque_chicote)
    ataques.add(ataque_chicote)

    # Main Game Loop
    jogo_tela_morte = False
    jogo_pausado = False
    jogo_rodando = True
    menu_principal_ativo = False

    while jogo_rodando:
        # Menu Principal
        if menu_principal_ativo:
            menu_principal()
            menu_principal_ativo = False
            continue

        clock.tick(FPS)
        delta_time = clock.get_time() / 20  # Para multiplicar velocidade de objetos para garantir que a velocidade não seja afetada pelo FPS

        if not (jogo_pausado or jogo_tela_morte):
            # Timer
            ticks_passados = pygame.time.get_ticks() - start_ticks - tempo_pausado_total
            segundos_passados = ticks_passados // 1000

            # Atualizar modificadores
            modificador_player_speed = 3 if ticks_passados - pocao_velocidade_usada < 10000 else 1  # Dura 10 segundos
            modificador_xp_yield = 2 if ticks_passados - dobro_xp_usado < 10000 else 1  # Dura 10 segundos

            # Jogador
            jogador.movimento(delta_time, modificador_player_speed)
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

            TELA.blit(hp_bar.image, camera.mover_objeto(hp_bar))
            TELA.blit(xp_bar.image, (0, 0))

            if jogador.hit_points_atuais <= 0 and not jogo_tela_morte:
                jogo_tela_morte = True
                tela_morte(LARGURA, ALTURA, TELA, FONTE_NONE_GRANDE, botoes_tela_morte, BRANCO)

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

            for item in items:
                item.animar_sprite()
                item.magnetismo(jogador, delta_time)

                # Recurso coletado dependendo do tipo de item
                if isinstance(item, Moeda):
                    total_moedas += item.checar_colisao(jogador)

                elif isinstance(item, Cura):
                    jogador.inventario['Poção Cura'] += item.checar_colisao(jogador)
                elif isinstance(item, Velocidade):
                    jogador.inventario['Poção Velocidade'] += item.checar_colisao(jogador)
                elif isinstance(item, Bomba):
                    jogador.inventario['Bomba'] += item.checar_colisao(jogador)
                elif isinstance(item, DobroXp):
                    jogador.inventario['Dobro XP'] += item.checar_colisao(jogador)

                elif isinstance(item, CristalXp):
                    jogador.xp += item.checar_colisao(jogador) * modificador_xp_yield
                    total_cristais += item.checar_colisao(jogador)//max(item.checar_colisao(jogador), 1)

            # Spawnar inimigos (Spawna 10 a cada 10 segundos) (Max = 40)
            if ticks_passados - cooldown_spawnar_inimigos >= 10000 and len(inimigos) <= 40:
                cooldown_spawnar_inimigos = ticks_passados
                for i in range(10):
                    inimigo_tipo = random.choice([Texugo])
                    inimigo_spawanado = inimigo_tipo(pontos_ao_redor(jogador, 900))
                    todos_sprites.add(inimigo_spawanado)
                    inimigos.add(inimigo_spawanado)

            # Spawnar items (Spawna 15 a cada 15 segundos) (Max = 30)
            if ticks_passados - cooldown_spawnar_items >= 15000 and len(items) <= 30:
                cooldown_spawnar_items = ticks_passados
                for i in range(15):
                    item_tipo = random.choice([Moeda, Cura, Bomba, DobroXp, Velocidade])
                    item_spawnado = item_tipo(pontos_ao_redor(jogador, 900))
                    todos_sprites.add(item_spawnado)
                    items.add(item_spawnado)

            # UI
            if not jogo_tela_morte:
                ui_jogo(total_moedas, total_cristais, jogador.nivel, jogador.xp, jogador.xp_para_proximo_nivel,
                jogador.inventario['Poção Cura'], total_inimigos_mortos, segundos_passados,
                FONTE_NONE, BRANCO, TELA, jogador.inventario['Poção Velocidade'], jogador.inventario['Bomba'],
                jogador.inventario['Dobro XP'], xp_bar, jogador, hp_bar)

        # Eventos
        for evento in pygame.event.get():
            # Fechar o jogo caso aperte o botão na janela
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Checar se alguma tecla relevante foi apertada
            if evento.type == pygame.KEYDOWN and not jogo_tela_morte:
                if evento.key == pygame.K_ESCAPE:  # Pausar ou despausar jogo se apertar ESC
                    if not jogo_pausado:
                        jogo_pausado = True
                        contar_tempo_pausado = pygame.time.get_ticks()
                        menu_pausa(LARGURA, ALTURA, TELA, FONTE_NONE_GRANDE, botoes_menu_pausa, BRANCO)
                    else:
                        tempo_pausado_total += pygame.time.get_ticks() - contar_tempo_pausado
                        jogo_pausado = False

                if not jogo_pausado:
                    if evento.key == pygame.K_z and jogador.usar_item('Poção Cura'): # Beber poção de cura caso aperte Z
                        jogador.hit_points_atuais = min(jogador.hit_points_atuais + 25, jogador.hit_point_max)

                    if evento.key == pygame.K_x and ticks_passados - pocao_velocidade_usada >= 10000 and jogador.usar_item('Poção Velocidade'):  # Beber poção de velocidade caso aperte X (Cooldown = 10s)
                        pocao_velocidade_usada = ticks_passados

                    if evento.key == pygame.K_c and jogador.usar_item('Bomba'):  # Usar bomba  caso aperte C
                        for inimigo in inimigos:
                            inimigo.hit_points_atuais = 0

                    if evento.key == pygame.K_v and ticks_passados - dobro_xp_usado >= 10000:  # Usar dobro xp caso aperte V (Cooldown = 10s)
                        if jogador.usar_item('Dobro XP'):
                            dobro_xp_usado = ticks_passados

            if jogo_pausado:
                for botao in botoes_menu_pausa:  # Apertos de botão na tela de pausa
                    if botao.mouse_interacao(evento):
                        if botao == CONTINUAR_botao_pausa:
                            tempo_pausado_total += pygame.time.get_ticks() - contar_tempo_pausado
                            jogo_pausado = False
                        elif botao == MENU_PRINCIPAL_botao:
                            menu_principal_ativo = True
                            jogo_pausado = False
                        elif botao == REINICIAR_botao_pausa:
                            iniciar_jogo(pygame.time.get_ticks())
                            jogo_pausado = False

            if jogo_tela_morte:
                for botao in botoes_tela_morte:  # Apertos de botão na tela de morte
                    if botao.mouse_interacao(evento):
                        if botao == REINICIAR_botao_morte:
                            iniciar_jogo(pygame.time.get_ticks())
                            jogo_tela_morte = False
                        elif botao == MENU_PRINCIPAL_botao_morte:
                            menu_principal_ativo = True
                            jogo_tela_morte = False

        # Atualiza a tela
        pygame.display.update()

# Função para abrir as configurações
def abrir_configuracoes():
    configuracoes = True
    volume = 0.5

    while configuracoes:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    configuracoes = False
                elif evento.key == pygame.K_UP:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif evento.key == pygame.K_DOWN:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)

        TELA.fill(PRETO)
        texto = FONTE_NONE_MEDIA.render("Configurações", True, BRANCO)
        TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - 100))
        texto_volume = FONTE_NONE_MEDIA.render(f"Volume: {int(volume * 100)}%", True, BRANCO)
        TELA.blit(texto_volume, (LARGURA // 2 - texto_volume.get_width() // 2, ALTURA // 2))
        texto_voltar = FONTE_NONE_MEDIA.render("Pressione ESC para voltar", True, BRANCO)
        TELA.blit(texto_voltar, (LARGURA // 2 - texto_voltar.get_width() // 2, ALTURA // 2 + 100))
        pygame.display.flip()

# Função para mostrar o menu principal
def menu_principal():
    pygame.mixer_music.stop()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if botao_iniciar.collidepoint(x, y):
                    iniciar_jogo(pygame.time.get_ticks())
                elif botao_configuracoes.collidepoint(x, y):
                    abrir_configuracoes()
                elif botao_sair.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

        TELA.fill(PRETO)

        texto_iniciar = FONTE_NONE_MEDIA.render("Iniciar Jogo", True, BRANCO)
        botao_iniciar = texto_iniciar.get_rect(center=(LARGURA // 2, ALTURA // 2 - 100))
        TELA.blit(texto_iniciar, botao_iniciar.topleft)

        texto_configuracoes = FONTE_NONE_MEDIA.render("Configurações", True, BRANCO)
        botao_configuracoes = texto_configuracoes.get_rect(center=(LARGURA // 2, ALTURA // 2))
        TELA.blit(texto_configuracoes, botao_configuracoes.topleft)

        texto_sair = FONTE_NONE_MEDIA.render("Sair do Jogo", True, BRANCO)
        botao_sair = texto_sair.get_rect(center=(LARGURA // 2, ALTURA // 2 + 100))
        TELA.blit(texto_sair, botao_sair.topleft)

        pygame.display.update()


menu_principal()
