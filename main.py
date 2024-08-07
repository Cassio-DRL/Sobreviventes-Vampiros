from UIs import *
from personagems import *
from inimigos import *
from coletaveis import *
from ataques import *

import pygame
import random
import math
import sys
import pickle
from datetime import datetime, timedelta

class Camera:
    # Cria um Rect representando a câmera
    def __init__(self, largura, altura):
        self.camera = pygame.Rect(0, 0, largura, altura)
        self.largura = largura
        self.altura = altura

    def movimento(self, jogador):
        # Calcula a nova posição x e y da câmera de forma que o centro do jogador esteja no centro da tela
        x = int(self.largura / 2) - jogador.rect.centerx
        y = int(self.altura / 2) - jogador.rect.centery
        # Atualiza a posição da câmera com as novas coordenadas
        self.camera.center = (x, y)

    def mover_objeto(self, objeto):
        # Move um objeto em relação à posição atual da câmera e retorna a nova posição do objeto
        return objeto.rect.move(self.camera.center)

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
pygame.mixer.music.set_volume(0.5)

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fonte
fonte_titulo = "fonte/fonteboa.ttf"
fonte = "fonte/Silkscreen-Regular.ttf"

# Dimensões da tela
LARGURA = 1280
ALTURA = 800
FPS = 60

# Inicializando a tela
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Vampiro Sobreviventes')
pygame.display.set_icon(pygame.image.load('Sprites/morcego.png'))

# Imagens
GRAMA_TILE = pygame.transform.scale(pygame.image.load('Sprites/Grama_Tile_Menor.png').convert_alpha(), (640, 640))
BOTAO_VERDE = pygame.image.load('Sprites/UI/botao_verde.png').convert_alpha()
BOTAO_VERMELHO = pygame.image.load('Sprites/UI/botao_vermelho.png').convert_alpha()
BOTAO_AZUL = pygame.image.load('Sprites/UI/botao_azul.png').convert_alpha()
BOTAO_CINZA = pygame.image.load('Sprites/UI/botao_cinza.png').convert_alpha()
ARCO_IRIS_QUADRADO = pygame.image.load('Sprites/rainbow.png').convert_alpha()

# Imagens Tela Inicial
background = pygame.image.load('Sprites/UI/Background.png')
moedas_conta = pygame.image.load('Sprites/UI/coin_count_frame.png')
box_config = pygame.image.load('Sprites/UI/box.png')
SIMBOLO_MAIS = pygame.transform.scale(pygame.image.load('Sprites/UI/mais_icone.png').convert_alpha(), (50, 50))
SIMBOLO_MENOS = pygame.transform.scale(pygame.image.load('Sprites/UI/menos_icone.png').convert_alpha(), (50, 140))
SETA_PRA_CIMA = pygame.image.load('Sprites/UI/setinha pra cima.png').convert_alpha()
SETA_PRA_BAIXO = pygame.image.load('Sprites/UI/setinha pra baixo.png').convert_alpha()

# Menu pausa
CONTINUAR_botao_pausa = Botao(pygame.math.Vector2(200, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Continuar", pygame.font.Font(fonte, 30), cor=None, imagem=BOTAO_CINZA)
REINICIAR_botao_pausa = Botao(pygame.math.Vector2(567, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Reiniciar", pygame.font.Font(fonte, 30), cor=None, imagem=BOTAO_CINZA)
MENU_PRINCIPAL_botao = Botao(pygame.math.Vector2(934, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Menu Principal", pygame.font.Font(fonte, 20), cor=None, imagem=BOTAO_CINZA)
botoes_menu_pausa = (CONTINUAR_botao_pausa, REINICIAR_botao_pausa, MENU_PRINCIPAL_botao)

# Tela morte
REINICIAR_botao_morte = Botao(pygame.math.Vector2(200, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Reiniciar", pygame.font.Font(fonte, 30), cor=None, imagem=BOTAO_CINZA)
MENU_PRINCIPAL_botao_morte = Botao(pygame.math.Vector2(934, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Menu Principal", pygame.font.Font(fonte, 20), cor=None, imagem=BOTAO_CINZA)
botoes_tela_morte = (REINICIAR_botao_morte, MENU_PRINCIPAL_botao_morte)
inicio_tela_morte = None

# Menu principal
JOGAR_botao = Botao(pygame.math.Vector2(568, 347), BOTAO_VERDE.get_width(), BOTAO_VERDE.get_height(), "JOGAR", pygame.font.Font(fonte, 40), cor=None, imagem=BOTAO_VERDE)
SAIR_botao = Botao(pygame.math.Vector2(568, 437), BOTAO_VERMELHO.get_width(), BOTAO_VERMELHO.get_height(), "SAIR", pygame.font.Font(fonte, 40), cor=None, imagem=BOTAO_VERMELHO)
MAIS_botao = Botao(pygame.math.Vector2(780, 585), SIMBOLO_MAIS.get_width(), SIMBOLO_MAIS.get_height(), "", pygame.font.Font(fonte, 30), cor=None, imagem=SIMBOLO_MAIS)
MENOS_botao = Botao(pygame.math.Vector2(450, 540), SIMBOLO_MENOS.get_width(), SIMBOLO_MENOS.get_height(), "", pygame.font.Font(fonte, 30), cor=None, imagem=SIMBOLO_MENOS)
SALVAR_botao = Botao(pygame.math.Vector2(5, 700), BOTAO_AZUL.get_width(), BOTAO_AZUL.get_height(), "SALVAR", pygame.font.Font(fonte, 30), cor=None, imagem=BOTAO_AZUL)
RESETAR_botao = Botao(pygame.math.Vector2(1129, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "RESET", pygame.font.Font(fonte, 30), cor=None, imagem=BOTAO_CINZA)
SETA_CIMA_botao = Botao(pygame.math.Vector2(741, 653), 15, 15, "", pygame.font.Font(fonte, 30), cor=None, imagem=SETA_PRA_CIMA)
SETA_BAIXO_botao = Botao(pygame.math.Vector2(741, 677), 15, 15, "", pygame.font.Font(fonte, 30), cor=None, imagem=SETA_PRA_BAIXO)
botoes_menu_principal = (JOGAR_botao, SAIR_botao, MAIS_botao, MENOS_botao, SALVAR_botao, RESETAR_botao, SETA_CIMA_botao, SETA_BAIXO_botao)


# Tela de level up
box_upgrade = pygame.image.load('Sprites/UI/box_level_up.png')
CONTINUAR_botao_level_up = Botao(pygame.math.Vector2(567, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Continuar", pygame.font.Font(fonte, 30), cor=None, imagem=BOTAO_CINZA)
botoes_level_up = (CONTINUAR_botao_level_up,)

# Sistema
camera = Camera(LARGURA, ALTURA)
clock = pygame.time.Clock()

# Game Data
personagem_tupla = (BichoChicote, BichoCajado, BichoMachado, BichoAdaga)
personagems_comprados = [False for i in range(len(personagem_tupla))]
moedas_acumuladas = 1000
moedas_ganhas = 0

# Carregar dados salvos
try:
    with open('save.pkl', 'rb') as file:
        moedas_acumuladas, personagems_comprados = pickle.load(file)
except FileNotFoundError:
    pass

def iniciar_jogo(start_ticks, personagem_selecionado, tempo_jogo):

    # Música do Nível
    pygame.mixer_music.load(random.choice(('Audio/0202 - Forest Night Fever.mp3', 'Audio/0106 - Vempair Survaivors.mp3', 'Audio/Musica_de_batalha_muito_top_SOULKNIGHT.mp3')))
    pygame.mixer_music.play(-1)

    # Contagem
    total_moedas = 0
    total_cristais = 0
    total_inimigos_mortos = 0

    # Cooldowns
    cooldown_spawnar_inimigos = -15000
    cooldown_spawnar_items = -15000
    dobro_xp_usado = -10000
    pocao_velocidade_usada = -10000

    # Tempo
    tempo_pausado_total = 0

    # Grupos de sprite
    todos_sprites = pygame.sprite.Group()
    inimigos_sprite_group = pygame.sprite.Group()
    items_sprite_group = pygame.sprite.Group()
    ataques_sprite_group = pygame.sprite.Group()
    tiles = pygame.sprite.Group(Tile(pygame.math.Vector2(0, 0), GRAMA_TILE))

    # Gerar jogador e ataques
    ataque_lista = [Chicote(pygame.math.Vector2(160, 0), 'direita'), Rotacao(140, 0), Adaga((0, 0), 'direita'), Machado((0, 0), 'direita')]
    jogador = personagem_selecionado(pygame.math.Vector2(0, 0), 0)

    # Classe do personagem associada a uma classe de ataque inicial
    ataques_inicias = {
        BichoChicote: Chicote,
        BichoAdaga: Adaga,
        BichoCajado: Rotacao,
        BichoMachado: Machado
    }

    # Inicia um dos ataques no nível 1 dependendo do personagem selecionado
    for jogador_classe, ataque_classe in ataques_inicias.items():
        if isinstance(jogador, jogador_classe):
            for ataque in ataque_lista:
                if isinstance(ataque, ataque_classe):
                    ataque.nivel = 1

    # Inicializa barras de HP e XP
    hp_bar = BarraVida(70, 10, (0, 50))
    xp_bar = BarraFixa(LARGURA, 30, (0, 0))

    # Adiciona o jogador e os ataques aos sprite groups
    todos_sprites.add(jogador, *ataque_lista)
    ataques_sprite_group.add(*ataque_lista)

    # Estados do jogo
    jogo_tela_morte = False
    jogo_pausado = False
    jogo_rodando = True

    while jogo_rodando:

        clock.tick(FPS)
        delta_time = clock.get_time() / 20  # Para multiplicar velocidade de objetos para garantir que a velocidade não seja afetada pelo FPS
        if not (jogo_pausado or jogo_tela_morte):
            # Timer
            
            ticks_passados = pygame.time.get_ticks() - start_ticks - tempo_pausado_total
            segundos_passados = ticks_passados // 1000

            ############################################################################################################
            # DESENHAR ELEMENTOS GRÁFICOS ##############################################################################
            ############################################################################################################

            # Desenha sprites
            for group in (tiles, todos_sprites):
                for sprite in group:
                    # Não mostra a instância original do ataque adaga ou machado mas ainda irá mostrar os projetéis spawnados
                    if not (isinstance(sprite, Adaga) or isinstance(sprite, Machado)):
                        TELA.blit(sprite.image, camera.mover_objeto(sprite))

            TELA.blit(hp_bar.image, camera.mover_objeto(hp_bar))
            TELA.blit(xp_bar.image, (0, 0))

            # Desenha HUD
            hud(total_moedas, total_cristais, jogador.nivel, jogador.xp, jogador.xp_para_proximo_nivel,
                jogador.inventario['Poção Cura'], total_inimigos_mortos, segundos_passados,
                pygame.font.Font(fonte, 30), BRANCO, TELA, jogador.inventario['Poção Velocidade'],
                jogador.inventario['Bomba'], jogador.inventario['Dobro XP'])

            # Mostra tela de morte se o hp do jogador chegar a 0
            if (jogador.hit_points_atuais <= 0 and not jogo_tela_morte) or jogo_tela_morte:
                inicio_tela_morte = datetime.now()
                jogo_tela_morte = True

                pygame.mixer_music.load("Audio/death_sound.mp3")
                pygame.mixer_music.play()


            ############################################################################################################
            # ATUALIZAR JOGO ###########################################################################################
            ############################################################################################################

            # GERAR BACKGROUND INFINITO ################################################################################
            for tile in tiles:
                novo_tile_group = pygame.sprite.Group(Tile(pygame.math.Vector2(x, y), GRAMA_TILE) for x, y in tile.jogador_presente(jogador))
                if novo_tile_group:
                    tiles = novo_tile_group
                    break

            # ATUALIZAR MODIFICADORES ##################################################################################
            if ticks_passados - pocao_velocidade_usada < 10000:  # Velocidade dura 10 segundos
                modificador_player_speed = 3
                TELA.blit(ARCO_IRIS_QUADRADO, ARCO_IRIS_QUADRADO.get_rect(topleft=(79, 726)))
            else:
                modificador_player_speed = 1

            if ticks_passados - dobro_xp_usado < 10000:  # Dobro XP dura 10 segundos
                modificador_xp_yield = 2
                TELA.blit(ARCO_IRIS_QUADRADO, ARCO_IRIS_QUADRADO.get_rect(topleft=(230, 726)))
            else:
                modificador_xp_yield = 1

            # ATUALIZAR JOGADOR ########################################################################################
            jogador.movimento(delta_time, modificador_player_speed)
            jogador.levar_dano(inimigos_sprite_group, ticks_passados)
            jogador.animar_sprite(ticks_passados)
            subiu_de_nivel = jogador.nivel_update()

            if subiu_de_nivel:
                contar_tempo_pausado = pygame.time.get_ticks()

                # Chama a função da tela de level up que retorna o upgrade selecionado
                selecionado = tela_level_up(ataque_lista)

                if selecionado is not None:
                    # Atualiza os ataques na lista inicial de ataques
                    for ataque_origem in ataque_lista:
                        if ataque_origem == selecionado:
                            ataque_origem.nivel += 1

                            # Atualiza o nível de todas as instâncias dos ataques (Relevante para Chicote e Rotação)
                            for _ in range(2):
                                for ataques_derivados in ataques_sprite_group:
                                    if isinstance(ataques_derivados, type(ataque_origem)):
                                        ataques_derivados.ajustar_nivel(ataques_sprite_group, todos_sprites)
                                        ataques_derivados.nivel = ataque_origem.nivel

                tempo_pausado_total += pygame.time.get_ticks() - contar_tempo_pausado

            hp_bar.atualizar(jogador)
            xp_bar.atualizar(jogador.xp, jogador.xp_para_proximo_nivel, (0, 0, 255))

            camera.movimento(jogador)

            # ATUALIZAR ATAQUES ########################################################################################
            for ataque in ataques_sprite_group:
                if isinstance(ataque, Projetil):
                    ataque.atualizar(jogador, delta_time)
                else:
                    ataque.animar_sprite()
                    ataque.atacar()
                    ataque.atualizar_posicao(jogador)
                    ataque.ajustar_nivel(ataques_sprite_group, todos_sprites)
                    if isinstance(ataque, Adaga) or isinstance(ataque, Machado):
                        ataque.spawnar_projetil(ataques_sprite_group, todos_sprites)

            # ATUALIZAR INIMIGOS #######################################################################################
            for inimigo in inimigos_sprite_group:

                inimigo.movimento(jogador, inimigos_sprite_group, delta_time)
                inimigo.animar_sprite(ticks_passados)
                inimigo.levar_dano(ataques_sprite_group, jogador, ticks_passados, delta_time, Projetil_Adaga)

                # Mostrar texto de dano
                for dano in inimigo.textos_dano:
                    TELA.blit(dano.image, camera.mover_objeto(dano))
                    dano.update(ticks_passados, 200)

                # Drops dependendo do tipo de inimigo
                drop_probabilities = {
                    Morguesso: [1, 0, 0],
                    Eisquelto: [8, 1, 0],
                    Texugo: [8, 1, 0.2],
                    Abobora: [0, 1, 0],
                    Zumbi: [1, 5, 0],
                    LoboPidao: [2, 1, 0.5],
                    Minhocao: [5, 5, 10],
                    Hidra: [0, 1, 2],
                    Centopeia: [0, 0, 1],
                    Morte: [0, 0, 1]
                }

                for inimigo_classe, peso in drop_probabilities.items():
                    if isinstance(inimigo, inimigo_classe):
                        drop = CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], peso, k=1)[0])
                        total_inimigos_mortos += inimigo.checar_hp(drop, items_sprite_group, todos_sprites, ticks_passados)

            # ATUALIZAR ITEMS ##########################################################################################
            for item in items_sprite_group:
                item.animar_sprite()
                item.magnetismo(jogador, delta_time)

                # Recurso coletado dependendo do tipo de item
                if isinstance(item, Moeda):
                    total_moedas += item.checar_colisao(jogador)

                # Items utilizáveis do inventário com limite de 3 pra cada
                elif isinstance(item, Cura):
                    jogador.inventario['Poção Cura'] = min(jogador.inventario['Poção Cura'] + item.checar_colisao(jogador), 3)
                elif isinstance(item, Velocidade):
                    jogador.inventario['Poção Velocidade'] = min(jogador.inventario['Poção Velocidade'] + item.checar_colisao(jogador), 3)
                elif isinstance(item, Bomba):
                    jogador.inventario['Bomba'] = min(jogador.inventario['Bomba'] + item.checar_colisao(jogador), 3)
                elif isinstance(item, DobroXp):
                    jogador.inventario['Dobro XP'] = min(jogador.inventario['Dobro XP'] + item.checar_colisao(jogador), 3)

                elif isinstance(item, CristalXp):
                    ganho = item.checar_colisao(jogador)
                    jogador.xp += ganho * modificador_xp_yield
                    total_cristais += ganho//max(ganho, 1)

            # SPAWNS ALEATÓRIOS ########################################################################################
            # Pesos para o spawn de cada tipo de inimigo, além de número pra spawnar a cada intervalo em milisegundos dependendo de quanto tempo se passou em segundos
            fases_spawn_inimigo = (
                {'Fase': (0, tempo_jogo*(1/15)), 'Pesos': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Numero Spawn': 10, 'Intervalo': 7000},
                {'Fase': (tempo_jogo*(1/15), tempo_jogo*(2/15)), 'Pesos': [8, 1, 0, 0, 0, 0, 0, 0, 0, 0], 'Numero Spawn': 15, 'Intervalo': 6000},
                {'Fase': (tempo_jogo*(2/15), tempo_jogo*(3/15)), 'Pesos': [6, 2, 1, 0, 0, 0, 0, 0, 0, 0], 'Numero Spawn': 15, 'Intervalo': 5000},
                {'Fase': (tempo_jogo*(3/15), tempo_jogo*(4/15)), 'Pesos': [3, 3, 2, 0, 0, 0, 0, 0, 0, 0], 'Numero Spawn': 15, 'Intervalo': 4000},
                {'Fase': (tempo_jogo*(4/15), tempo_jogo*(5/15)), 'Pesos': [0, 2, 3, 0, 1, 0, 0, 0, 0, 0], 'Numero Spawn': 15, 'Intervalo': 3000},
                {'Fase': (tempo_jogo*(5/15), tempo_jogo*(6/15)), 'Pesos': [0, 0, 0, 5, 10, 0, 0, 0, 0, 0], 'Numero Spawn': 15, 'Intervalo': 2000},
                {'Fase': (tempo_jogo*(6/15), tempo_jogo*(7/15)), 'Pesos': [0, 0, 0, 6, 4, 6, 0, 0, 0, 0], 'Numero Spawn': 15, 'Intervalo': 2000},
                {'Fase': (tempo_jogo*(7/15), tempo_jogo*(8/15)), 'Pesos': [0, 0, 12, 0, 0, 6, 6, 0, 0, 0], 'Numero Spawn': 15, 'Intervalo': 2000},
                {'Fase': (tempo_jogo*(8/15), tempo_jogo*(9/15)), 'Pesos': [0, 0, 0, 0, 1, 1, 4, 6, 0, 0], 'Numero Spawn': 15, 'Intervalo': 1000},
                {'Fase': (tempo_jogo*(9/15), tempo_jogo*(10/15)), 'Pesos': [0, 0, 0, 0, 0, 2, 3, 6, 0, 0], 'Numero Spawn': 15, 'Intervalo': 1000},
                {'Fase': (tempo_jogo*(10/15), tempo_jogo*(11/15)), 'Pesos': [0, 0, 0, 0, 0, 2, 8, 3, 0, 0], 'Numero Spawn': 15, 'Intervalo': 1000},
                {'Fase': (tempo_jogo*(11/15), tempo_jogo*(12/15)), 'Pesos': [0, 0, 0, 0, 0, 0, 0, 10, 2, 0], 'Numero Spawn': 15, 'Intervalo': 1000},
                {'Fase': (tempo_jogo*(12/15), tempo_jogo*(13/15)), 'Pesos': [0, 0, 0, 0, 0, 0, 0, 4, 4, 0], 'Numero Spawn': 15, 'Intervalo': 1000},
                {'Fase': (tempo_jogo*(13/15), tempo_jogo*(14/15)), 'Pesos': [0, 0, 0, 0, 0, 0, 0, 1, 5, 0], 'Numero Spawn': 15, 'Intervalo': 1000},
                {'Fase': (tempo_jogo*(14/15), tempo_jogo), 'Pesos': [1, 1, 1, 1, 1, 2, 4, 6, 12, 0], 'Numero Spawn': 15, 'Intervalo': 1000},
                {'Fase': (tempo_jogo, 100000), 'Pesos': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 'Numero Spawn': 20, 'Intervalo': 1000}
            )

            for fase in fases_spawn_inimigo:
                if segundos_passados in range(int(fase['Fase'][0]), int(fase['Fase'][1])):
                    pesos = fase['Pesos']
                    numero_spawn = fase['Numero Spawn']
                    intervalo = fase['Intervalo']

            # SPAWNAR INIMIGOS (Max = 50)
            if ticks_passados - cooldown_spawnar_inimigos >= intervalo and len(inimigos_sprite_group) <= 50:
                cooldown_spawnar_inimigos = ticks_passados
                tipos_de_inimigo = random.choices([Morguesso, Eisquelto, Texugo, Abobora, Zumbi, LoboPidao, Minhocao, Hidra, Centopeia, Morte], pesos, k=numero_spawn)
                for inimigo_classe in tipos_de_inimigo:
                    inimigo_spawanado = inimigo_classe(pontos_ao_redor(jogador, 900), ticks_passados, jogador)
                    todos_sprites.add(inimigo_spawanado)
                    inimigos_sprite_group.add(inimigo_spawanado)

            # SPAWNAR ITEMS (Spawna 15 a cada 15 segundos) (Max = 30)
            if ticks_passados - cooldown_spawnar_items >= 15000 and len(items_sprite_group) <= 30:
                cooldown_spawnar_items = ticks_passados
                tipos_de_item = random.choices([Moeda, Cura, Bomba, DobroXp, Velocidade], [20, 2, 0.01, 2, 2], k=15)
                for item_classe in tipos_de_item:
                    item_spawnado = item_classe(pontos_ao_redor(jogador, 900))
                    todos_sprites.add(item_spawnado)
                    items_sprite_group.add(item_spawnado)
        
        elif jogo_tela_morte: # para escurecer a tela
                escurecer_duracao = timedelta(seconds=20)
                tempo_atual = datetime.now()
                tempo_decorrido = tempo_atual - inicio_tela_morte
            
                if tempo_decorrido < escurecer_duracao:
                    intensidade = int((tempo_decorrido / escurecer_duracao) * 255)
                else:
                    intensidade = 255

                moedas_ganhas = tela_morte(total_inimigos_mortos, total_cristais, total_moedas, intensidade)
                

        ################################################################################################################
        # EVENTOS ######################################################################################################
        ################################################################################################################

        for evento in pygame.event.get():
            # Fechar o jogo caso aperte o botão na janela
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Checar se alguma tecla relevante foi apertada
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:  # Screenshot se apertar P
                    hora = datetime.now()
                    pygame.image.save(TELA, f'Screenshots/screenshot_{hora.strftime("%Y_%m_%d_%H_%M_%S")}.png')

                if not jogo_tela_morte:
                    if evento.key == pygame.K_ESCAPE:  # Pausar ou despausar jogo se apertar ESC
                        if not jogo_pausado:
                            jogo_pausado = True
                            contar_tempo_pausado = pygame.time.get_ticks()
                            menu_pausa()
                        else:
                            tempo_pausado_total += pygame.time.get_ticks() - contar_tempo_pausado
                            jogo_pausado = False

                    if not jogo_pausado:
                        # Uso de items do inventário
                        if evento.key == pygame.K_z and jogador.usar_item('Poção Cura'):  # Beber poção de cura caso aperte Z
                            jogador.hit_points_atuais = min(jogador.hit_points_atuais + jogador.hit_point_max//4, jogador.hit_point_max)

                        if evento.key == pygame.K_x and ticks_passados - pocao_velocidade_usada >= 10000 and jogador.usar_item('Poção Velocidade'):  # Beber poção de velocidade caso aperte X (Cooldown = 10s)
                            pocao_velocidade_usada = ticks_passados

                        if evento.key == pygame.K_c and jogador.usar_item('Bomba'):  # Usar bomba caso aperte C
                            for inimigo in inimigos_sprite_group:
                                inimigo.hit_points_atuais = 0

                        if evento.key == pygame.K_v and ticks_passados - dobro_xp_usado >= 10000 and jogador.usar_item('Dobro XP'):  # Usar dobro xp caso aperte V (Cooldown = 10s)
                                dobro_xp_usado = ticks_passados

            # Apertos de botão na tela de pausa
            if jogo_pausado:
                if CONTINUAR_botao_pausa.mouse_interacao(evento):
                    tempo_pausado_total += pygame.time.get_ticks() - contar_tempo_pausado
                    jogo_pausado = False

                elif MENU_PRINCIPAL_botao.mouse_interacao(evento):
                    return False, 0

                elif REINICIAR_botao_pausa.mouse_interacao(evento):
                    return True, 0

            # Apertos de botão na tela de morte
            if jogo_tela_morte:
                if REINICIAR_botao_morte.mouse_interacao(evento):
                    return True, moedas_ganhas

                elif MENU_PRINCIPAL_botao_morte.mouse_interacao(evento):
                    return False, moedas_ganhas

        # Atualiza a tela
        pygame.display.flip()

########################################################################################################################
# FUNÇÕES PARA DIFERENTES TELAS ########################################################################################
########################################################################################################################

# Função para mostrar o menu principal
def menu_principal(moedas_acumuladas, personagems_comprados):
    pygame.mixer_music.stop()

    molduras = [PersonagemFrame((coord_x, 124), personagem_tupla[i], 1000) for i, coord_x in enumerate((365, 505, 645, 785))]
    volume_barra = BarraFixa(240, 30, (520, 595))

    personagem_selecionado = None
    tempo_de_jogo_minutos = 15

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or SAIR_botao.mouse_interacao(evento):
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:  # Screenshot se apertar P
                    hora = datetime.now()
                    pygame.image.save(TELA, f'Screenshots/screenshot_{hora.strftime("%Y_%m_%d_%H_%M_%S")}.png')

            if JOGAR_botao.mouse_interacao(evento) and personagem_selecionado:
                return personagem_selecionado, moedas_acumuladas, personagems_comprados, tempo_de_jogo_minutos

            # Controle de volume
            if MAIS_botao.mouse_interacao(evento):
                pygame.mixer.music.set_volume(min(1, pygame.mixer.music.get_volume() + 0.1))
            elif MENOS_botao.mouse_interacao(evento):
                pygame.mixer.music.set_volume(max(0, pygame.mixer.music.get_volume() - 0.1))

            # Controle de duração de rodada
            if SETA_CIMA_botao.mouse_interacao(evento):
                tempo_de_jogo_minutos = min(15, tempo_de_jogo_minutos + 1)
            elif SETA_BAIXO_botao.mouse_interacao(evento):
                tempo_de_jogo_minutos = max(3, tempo_de_jogo_minutos - 1)

            if SALVAR_botao.mouse_interacao(evento):
                with open('save.pkl', 'wb') as file:
                    pickle.dump((moedas_acumuladas, personagems_comprados), file)

            if RESETAR_botao.mouse_interacao(evento):
                moedas_acumuladas = 1000
                personagem_selecionado = None
                personagems_comprados = [False for _ in range(len(personagem_tupla))]

            for frame in molduras:
                moedas_acumuladas, personagem_selecionado, comprou = frame.comprar(moedas_acumuladas, personagem_selecionado, evento)
                if comprou:
                    personagems_comprados[molduras.index(frame)] = True

        TELA.blit(background.convert_alpha(), background.get_rect(topleft=(0, 0)))

        # Caixa para barra de volume e configuração do tempo de jogo
        TELA.blit(box_config.convert_alpha(), box_config.get_rect(topleft=(408, 538)))

        # Configuração do tempo de jogo
        quadrado = pygame.rect.Rect(667, 638, 67, 67)
        pygame.draw.rect(TELA, BRANCO, quadrado)
        tempo_de_jogo_texto = pygame.font.Font(fonte, 65).render(f"{tempo_de_jogo_minutos}", True, PRETO)
        TELA.blit(tempo_de_jogo_texto, tempo_de_jogo_texto.get_rect(center=quadrado.center))
        limite_de_tempo_texto = pygame.font.Font(fonte, 17).render(f"LIMITE DE TEMPO", True, BRANCO)
        TELA.blit(limite_de_tempo_texto, limite_de_tempo_texto.get_rect(topleft=(530, 666)))

        # Barra de Volume
        volume_texto = pygame.font.Font(fonte, 45).render(f"VOLUME", True, BRANCO)
        TELA.blit(volume_texto, volume_texto.get_rect(center=(640, 568)))
        volume_barra.atualizar(pygame.mixer.music.get_volume(), 1, (255, 255, 255))
        TELA.blit(volume_barra.image, volume_barra.rect)

        # Titulo do Jogo
        titulo_texto = pygame.font.Font(fonte_titulo, 85).render(f"VAMPIRO  SOBREVIVENTES", True, BRANCO)
        TELA.blit(titulo_texto, titulo_texto.get_rect(center=(640, 90)))

        # Contagem de moedas
        TELA.blit(moedas_conta.convert_alpha(), moedas_conta.get_rect(topleft=(483, 0)))
        moedas_texto = pygame.font.Font(fonte, 46).render(f"{moedas_acumuladas}", True, BRANCO)
        TELA.blit(moedas_texto, moedas_texto.get_rect(center=(640, 20)))
        TELA.blit(moeda.convert_alpha(), moeda.get_rect(topright=(570, 5)))

        # Botões
        for botao in botoes_menu_principal:
            botao.desenhar(TELA)

        # Desenhar frames de personagem de acordo se eles estão bloqueados ou não
        for i, frame in enumerate(molduras):
            frame.desbloqueado_variavel = personagems_comprados[i]
            frame.desenhar(TELA)

        pygame.display.update()

# Função para mostrar a tela de level up
def tela_level_up(ataque_lista):
    ataques_upgradaveis = pygame.sprite.Group()

    # Cria uma lista em ordem aleatória dos ataques
    ataques_randomizados = ataque_lista.copy()
    random.shuffle(ataques_randomizados)

    # Cria até 3 opções de upgrade pra ataques abaixo do nível 10
    for ataque, coord_y in zip(ataques_randomizados, [270, 420, 570]):
        if ataque.nivel < 10:
            ataques_upgradaveis.add(MolduraAtaqueLevelUP((640, coord_y), ataque))

    # Camada sobre a tela que permite que coisas sejam desenhadas com opacidade reduzida
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    pygame.draw.rect(camada, (20, 50, 50, 150), (0, 0, LARGURA, ALTURA))
    TELA.blit(camada, (0, 0))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:  # Screenshot se apertar P
                    hora = datetime.now()
                    pygame.image.save(TELA, f'Screenshots/screenshot_{hora.strftime("%Y_%m_%d_%H_%M_%S")}.png')

            # Apertar continuar permite que o jogador avance sem escolher nenhum upgrade
            if CONTINUAR_botao_level_up.mouse_interacao(evento):
                return None

            # Checa se algum dos botões de selecionar foi apertado
            for ataque in ataques_upgradaveis:
                upgrade_selecionado = ataque.selecionar_upgrade(evento)
                if upgrade_selecionado is not None:
                    return upgrade_selecionado

        # Texto grande na tela
        texto_morte = pygame.font.Font(fonte, 100).render(f"SUBIU DE NÍVEL", True, BRANCO)
        TELA.blit(texto_morte, (LARGURA // 2 - texto_morte.get_width() // 2, ALTURA // 2 - 340))

        # Caixa com as molduras de ataque
        TELA.blit(box_upgrade, box_upgrade.get_rect(center=(640, 420)))

        # Botões
        for botao in botoes_level_up:
            botao.desenhar(TELA)

        # Desenhar os ataques
        for ataque in ataques_upgradaveis:
            ataque.desenhar(TELA)

        pygame.display.update()

# Função para mostrar a tela de pausa
def menu_pausa():

    # Camada sobre a tela que permite que coisas sejam desenhadas com opacidade reduzida
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    pygame.draw.rect(camada, (20, 50, 50, 150), (0, 0, LARGURA, ALTURA))
    TELA.blit(camada, (0, 0))

    # Texto grande no meio da tela
    texto_pausa = pygame.font.Font(fonte, 100).render(f"JOGO PAUSADO", False, BRANCO)
    TELA.blit(texto_pausa, (LARGURA // 2 - texto_pausa.get_width() // 2, ALTURA // 2 - 100))

    # Desenha cada botão
    for botao in botoes_menu_pausa:
        botao.desenhar(TELA)

# Função para mostrar a tela de morte
def tela_morte(total_inimigos_mortos, total_cristais, total_moedas, intensidade):
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    TELA.blit(camada, (0, 0))

    pygame.draw.rect(camada, (0, 0, 0, intensidade), (0, 0, LARGURA, ALTURA))
    TELA.blit(camada, (0, 0))

    # Texto grande no meio da tela
    texto_morte = pygame.font.Font(fonte, 100).render(f"VOCÊ MORREU!", True, (255, 10, 10))
    TELA.blit(texto_morte, (LARGURA // 2 - texto_morte.get_width() // 2, ALTURA // 2 - 300))

    # Sumário do jogo
    inimigos = pygame.font.Font(fonte, 30).render(f"Inimigos Mortos: {total_inimigos_mortos}", True, BRANCO)
    cristais = pygame.font.Font(fonte, 30).render(f"Cristais Coletados: {total_cristais}", True, BRANCO)
    moedas = pygame.font.Font(fonte, 30).render(f"Moedas Coletadas: {total_moedas}", True, BRANCO)

    # Coneversão para moedas
    contagem_inimigos = pygame.font.Font(fonte, 30).render(f"{total_inimigos_mortos // 2}", True, BRANCO)
    contagem_cristais = pygame.font.Font(fonte, 30).render(f"{total_cristais // 4}", True, BRANCO)
    contagem_moedas = pygame.font.Font(fonte, 30).render(f"{total_moedas}", True, BRANCO)
    total = pygame.font.Font(fonte, 30).render(f"{total_moedas + total_cristais // 4 + total_inimigos_mortos // 2}", True, BRANCO)

    # Exibir textos na tela
    TELA.blit(inimigos, inimigos.get_rect(topleft=(300, 250)))
    TELA.blit(cristais, cristais.get_rect(topleft=(300, 300)))
    TELA.blit(moedas, moedas.get_rect(topleft=(300, 350)))

    TELA.blit(contagem_inimigos, contagem_inimigos.get_rect(topright=(800, 250)))
    TELA.blit(contagem_cristais, contagem_cristais.get_rect(topright=(800, 300)))
    TELA.blit(contagem_moedas, contagem_moedas.get_rect(topright=(800, 350)))
    TELA.blit(total, total.get_rect(topright=(800, 400)))

    # Desenhar ícones das moedas
    for i in (251, 301, 351):
        TELA.blit(moeda.convert_alpha(), moeda.get_rect(topright=(840, i)))

    # Desenha cada botão
    for botao in botoes_tela_morte:
        botao.desenhar(TELA)
    
    return total_moedas + total_cristais // 4 + total_inimigos_mortos // 2


########################################################################################################################
# MAIN GAME LOOP #######################################################################################################
########################################################################################################################
while True:
    personagem_selecionado, moedas_acumuladas, personagems_comprados, tempo_jogo = menu_principal(moedas_acumuladas, personagems_comprados)
    while True:
        reiniciar, moedas_ganhas = iniciar_jogo(pygame.time.get_ticks(), personagem_selecionado, tempo_jogo * 60)
        moedas_acumuladas += moedas_ganhas
        if not reiniciar:
            break
