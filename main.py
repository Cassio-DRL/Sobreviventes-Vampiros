from UIs import *
from personagems import *
from inimigos import *
from coletaveis import *
from ataques import *
import sys
import pickle

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
pygame.mixer.music.set_volume(0.5)

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
pygame.display.set_icon(pygame.image.load('Sprites/morcego.png'))

# Imagens
GRAMA_TILE = pygame.transform.scale(pygame.image.load('Sprites/Grama_Tile_Menor.png').convert_alpha(), (640, 640))
BOTAO_VERDE = pygame.image.load('Sprites/UI/botao_verde.png').convert_alpha()
BOTAO_VERMELHO = pygame.image.load('Sprites/UI/botao_vermelho.png').convert_alpha()
BOTAO_AZUL = pygame.image.load('Sprites/UI/botao_azul.png').convert_alpha()
BOTAO_CINZA = pygame.image.load('Sprites/UI/botao_cinza.png').convert_alpha()
mais = pygame.transform.scale(pygame.image.load('Sprites/UI/mais_icone.png').convert_alpha(), (50, 50))
menos = pygame.transform.scale(pygame.image.load('Sprites/UI/menos_icone.png').convert_alpha(), (50, 140))
arco_iris = pygame.image.load('Sprites/rainbow.png')

# Menu pausa
CONTINUAR_botao_pausa = Botao(pygame.math.Vector2(200, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Continuar", pygame.font.Font(None, 30), cor=None, imagem=BOTAO_CINZA)
REINICIAR_botao_pausa = Botao(pygame.math.Vector2(567, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Reiniciar", pygame.font.Font(None, 30), cor=None, imagem=BOTAO_CINZA)
MENU_PRINCIPAL_botao = Botao(pygame.math.Vector2(934, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Menu Principal", pygame.font.Font(None, 24), cor=None, imagem=BOTAO_CINZA)
botoes_menu_pausa = (CONTINUAR_botao_pausa, REINICIAR_botao_pausa, MENU_PRINCIPAL_botao)

# Tela morte
REINICIAR_botao_morte = Botao(pygame.math.Vector2(200, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Reiniciar", pygame.font.Font(None, 30), cor=None, imagem=BOTAO_CINZA)
MENU_PRINCIPAL_botao_morte = Botao(pygame.math.Vector2(934, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Menu Principal", pygame.font.Font(None, 24), cor=None, imagem=BOTAO_CINZA)
botoes_tela_morte = (REINICIAR_botao_morte, MENU_PRINCIPAL_botao_morte)

# Menu principal
JOGAR_botao = Botao(pygame.math.Vector2(568, 347), BOTAO_VERDE.get_width(), BOTAO_VERDE.get_height(), "JOGAR", pygame.font.Font(None, 40), cor=None, imagem=BOTAO_VERDE)
SAIR_botao = Botao(pygame.math.Vector2(568, 437), BOTAO_VERMELHO.get_width(), BOTAO_VERMELHO.get_height(), "SAIR", pygame.font.Font(None, 40), cor=None, imagem=BOTAO_VERMELHO)
MAIS_botao = Botao(pygame.math.Vector2(780, 585), mais.get_width(), mais.get_height(), "", pygame.font.Font(None, 30), cor=None, imagem=mais)
MENOS_botao = Botao(pygame.math.Vector2(450, 540), menos.get_width(), menos.get_height(), "", pygame.font.Font(None, 30), cor=None, imagem=menos)
SALVAR_botao = Botao(pygame.math.Vector2(5, 740), BOTAO_AZUL.get_width(), BOTAO_AZUL.get_height(), "SALVAR", pygame.font.Font(None, 30), cor=None, imagem=BOTAO_AZUL)
RESETAR_botao = Botao(pygame.math.Vector2(1129, 740), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "RESET", pygame.font.Font(None, 30), cor=None, imagem=BOTAO_CINZA)
botoes_menu_principal = (JOGAR_botao, SAIR_botao, MAIS_botao, MENOS_botao, SALVAR_botao, RESETAR_botao)

# Tela de level up
CONTINUAR_botao_level_up = Botao(pygame.math.Vector2(640, 700), BOTAO_CINZA.get_width(), BOTAO_CINZA.get_height(), "Continuar", pygame.font.Font(None, 30), cor=None, imagem=BOTAO_CINZA)
botoes_level_up = (CONTINUAR_botao_level_up, CONTINUAR_botao_level_up)

# Sistema
camera = Camera(LARGURA, ALTURA)
clock = pygame.time.Clock()
moedas_acumuladas = 4000

# Personagens
personagem_tupla = (BichoChicote, BichoCajado, BichoMachado, BichoAdaga)
personagems_comprados = [False for i in range(len(personagem_tupla))]

# Carregar dados salvos
with open('save.pkl', 'rb') as file:
    moedas_acumuladas, personagems_comprados = pickle.load(file)

def iniciar_jogo(start_ticks, personagem_selecionado):

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

    # Ataques
    ataques_tupla = (Slash(pygame.math.Vector2(300, 0), 'direita'), Rotacao(140, 0))

    # Grupos de sprite
    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    items = pygame.sprite.Group()
    ataques = pygame.sprite.Group()
    tiles = pygame.sprite.Group(Tile(pygame.math.Vector2(0, 0), GRAMA_TILE))

    # Gerar jogador e ataques
    jogador = personagem_selecionado(pygame.math.Vector2(0, 0), 0)
    hp_bar = BarraVida(70, 10, (0, 50))
    xp_bar = BarraFixa(LARGURA, 30, (0, 0))

    todos_sprites.add(jogador, *ataques_tupla)
    ataques.add(*ataques_tupla)

    # Main Game Loop
    jogo_tela_level_up = False
    jogo_tela_morte = False
    jogo_pausado = False
    jogo_rodando = True

    while jogo_rodando:
        clock.tick(FPS)
        delta_time = clock.get_time() / 20  # Para multiplicar velocidade de objetos para garantir que a velocidade não seja afetada pelo FPS

        if not (jogo_pausado or jogo_tela_morte or jogo_tela_level_up):
            # Timer
            ticks_passados = pygame.time.get_ticks() - start_ticks - tempo_pausado_total
            segundos_passados = ticks_passados // 1000

            # DESENHAR ELEMENTOS GRÁFICOS ##############################################################################
            # Desenha sprites
            for group in (tiles, todos_sprites):
                for sprite in group:
                    TELA.blit(sprite.image, camera.mover_objeto(sprite))

            for inimigo in inimigos:
                for dano in inimigo.textos_dano:
                    TELA.blit(dano.image, camera.mover_objeto(dano))
                    dano.update(ticks_passados, 200)

            TELA.blit(hp_bar.image, camera.mover_objeto(hp_bar))
            TELA.blit(xp_bar.image, (0, 0))

            # Desenha UI
            ui_jogo(total_moedas, total_cristais, jogador.nivel, jogador.xp, jogador.xp_para_proximo_nivel,
                    jogador.inventario['Poção Cura'], total_inimigos_mortos, segundos_passados,
                    pygame.font.Font(None, 30), BRANCO, TELA, jogador.inventario['Poção Velocidade'],
                    jogador.inventario['Bomba'],
                    jogador.inventario['Dobro XP'])

            # Mostra tela de morte se o hp do jogador chegar a 0
            if jogador.hit_points_atuais <= 0 and not jogo_tela_morte:
                jogo_tela_morte = True
                moedas_ganhas = tela_morte(LARGURA, ALTURA, TELA, FONTE_NONE_GRANDE, botoes_tela_morte, BRANCO, total_inimigos_mortos, total_cristais, total_moedas)

            # ATUALIZAR JOGO ###########################################################################################
            # Atualizar modificadores
            if ticks_passados - pocao_velocidade_usada < 10000:  # Dura 10 segundos
                modificador_player_speed = 3
                TELA.blit(arco_iris, arco_iris.get_rect(topleft=(79, 726)))
            else:
                modificador_player_speed = 1

            if ticks_passados - dobro_xp_usado < 10000:  # Dura 10 segundos
                modificador_xp_yield = 2
                TELA.blit(arco_iris, arco_iris.get_rect(topleft=(230, 726)))
            else:
                modificador_xp_yield = 1
            # Atualizar jogador
            jogador.movimento(delta_time, modificador_player_speed)
            jogador.levar_dano(inimigos, ticks_passados)
            jogador.animar_sprite(ticks_passados)

            hp_bar.atualizar(jogador)
            xp_bar.atualizar(jogador.xp, jogador.xp_para_proximo_nivel, (0, 0, 255))

            camera.movimento(jogador)

            # Atualizar ataques
            for ataque in ataques:
                ataque.ajustar_nivel(ataques, todos_sprites)
                ataque.animar_sprite()
                ataque.atacar()
                ataque.atualizar_posicao(jogador)

            # Gerar background
            for tile in tiles:
                novo_tile_group = pygame.sprite.Group(Tile(pygame.math.Vector2(x, y), GRAMA_TILE) for x, y in tile.jogador_presente(jogador))
                if novo_tile_group:
                    tiles = novo_tile_group
                    break

            # Atualizar inimigos
            for inimigo in inimigos:

                inimigo.movimento(jogador, inimigos, delta_time)
                inimigo.levar_dano(ataques, jogador, ticks_passados, delta_time)
                inimigo.animar_sprite(ticks_passados)

                # Drops dependendo do tipo de inimigo
                if isinstance(inimigo, Texugo):
                    drop = CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], [40, 5, 1], k=1)[0])
                    total_inimigos_mortos += inimigo.checar_hp(drop, items, todos_sprites, ticks_passados)
                if isinstance(inimigo, Eisquelto):
                    drop = CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], [8, 1, 0], k=1)[0])
                    total_inimigos_mortos += inimigo.checar_hp(drop, items, todos_sprites, ticks_passados)
                if isinstance(inimigo, Minhocao):
                    drop = CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], [5, 5, 10], k=1)[0])
                    total_inimigos_mortos += inimigo.checar_hp(drop, items, todos_sprites, ticks_passados)
                if isinstance(inimigo, LoboPidao):
                    drop = CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], [20, 10, 1], k=1)[0])
                    total_inimigos_mortos += inimigo.checar_hp(drop, items, todos_sprites, ticks_passados)
                if isinstance(inimigo, Zumbi):
                    drop = CristalXp(inimigo.pos, random.choices(['Blue', 'Green', 'Red'], [10, 50, 0], k=1)[0])
                    total_inimigos_mortos += inimigo.checar_hp(drop, items, todos_sprites, ticks_passados)

            # Atualizar coletáveis
            for item in items:
                item.animar_sprite()
                item.magnetismo(jogador, delta_time)

                # Recurso coletado dependendo do tipo de item
                if isinstance(item, Moeda):
                    total_moedas += item.checar_colisao(jogador)

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
                {'Fase': (0, 60), 'Pesos': [1, 0, 0, 0, 0, 0], 'Numero Spawn': 10, 'Intervalo': 15000},
                {'Fase': (60, 120), 'Pesos': [5, 1, 0, 0, 0, 0], 'Numero Spawn': 10, 'Intervalo': 13000},
                {'Fase': (120, 180), 'Pesos': [1, 1, 1, 0, 0, 0], 'Numero Spawn': 10, 'Intervalo': 10000},
                {'Fase': (180, 240), 'Pesos': [1, 3, 10, 0, 0, 0], 'Numero Spawn': 10, 'Intervalo': 7000},
                {'Fase': (240, 300), 'Pesos': [2, 5, 20, 0, 0, 0], 'Numero Spawn': 10, 'Intervalo': 5000},
                {'Fase': (300, 360), 'Pesos': [1, 1, 2, 2, 0, 0], 'Numero Spawn': 10, 'Intervalo': 5000},
                {'Fase': (360, 420), 'Pesos': [1, 3, 2, 1, 0, 0], 'Numero Spawn': 10, 'Intervalo': 4000},
                {'Fase': (420, 480), 'Pesos': [0, 1, 2, 6, 1, 0], 'Numero Spawn': 10, 'Intervalo': 3000},
                {'Fase': (480, 600), 'Pesos': [0, 0, 0, 1, 3, 0], 'Numero Spawn': 10, 'Intervalo': 2000},
                {'Fase': (600, 900), 'Pesos': [1, 1, 1, 5, 20, 0], 'Numero Spawn': 10, 'Intervalo': 1000},
                {'Fase': (900, 10000), 'Pesos': [0, 0, 0, 0, 0, 1], 'Numero Spawn': 10, 'Intervalo': 1000}
            )

            for fase in fases_spawn_inimigo:
                if segundos_passados in range(fase['Fase'][0], fase['Fase'][1]):
                    pesos = fase['Pesos']
                    numero_spawn = fase['Numero Spawn']
                    intervalo = fase['Intervalo']

            # Spawnar inimigos (Max = 50)
            if ticks_passados - cooldown_spawnar_inimigos >= intervalo and len(inimigos) <= 50:
                cooldown_spawnar_inimigos = ticks_passados
                tipos_de_inimigo = random.choices([Eisquelto, Texugo, Zumbi, LoboPidao, Minhocao, Morte], pesos, k=numero_spawn)
                for inimigo_classe in tipos_de_inimigo:
                    inimigo_spawanado = inimigo_classe(pontos_ao_redor(jogador, 900), ticks_passados, jogador)
                    todos_sprites.add(inimigo_spawanado)
                    inimigos.add(inimigo_spawanado)

            # Spawnar items (Spawna 15 a cada 15 segundos) (Max = 30)
            if ticks_passados - cooldown_spawnar_items >= 15000 and len(items) <= 30:
                cooldown_spawnar_items = ticks_passados
                for i in range(15):
                    item_tipo = random.choices([Moeda, Cura, Bomba, DobroXp, Velocidade], [20, 2, 0.01, 2, 2], k=1)[0]
                    item_spawnado = item_tipo(pontos_ao_redor(jogador, 900))
                    todos_sprites.add(item_spawnado)
                    items.add(item_spawnado)

            subiu_de_nivel = jogador.nivel_update()
            if subiu_de_nivel:
                jogo_tela_level_up = True
                contar_tempo_pausado = pygame.time.get_ticks()
                tela_level_up()

        # EVENTOS ######################################################################################################
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
                    if evento.key == pygame.K_z and jogador.usar_item('Poção Cura'):  # Beber poção de cura caso aperte Z
                        jogador.hit_points_atuais = min(jogador.hit_points_atuais + jogador.hit_point_max//4, jogador.hit_point_max)

                    if evento.key == pygame.K_x and ticks_passados - pocao_velocidade_usada >= 10000 and jogador.usar_item('Poção Velocidade'):  # Beber poção de velocidade caso aperte X (Cooldown = 10s)
                        pocao_velocidade_usada = ticks_passados

                    if evento.key == pygame.K_c and jogador.usar_item('Bomba'):  # Usar bomba caso aperte C
                        for inimigo in inimigos:
                            inimigo.hit_points_atuais = 0

                    if evento.key == pygame.K_v and ticks_passados - dobro_xp_usado >= 10000:  # Usar dobro xp caso aperte V (Cooldown = 10s)
                        if jogador.usar_item('Dobro XP'):
                            dobro_xp_usado = ticks_passados

                    if evento.key == pygame.K_p:
                        for ataque in ataques_tupla:
                            ataque.nivel += 1
                            for ataques_derivados in ataques:
                                if isinstance(ataques_derivados, type(ataque)):
                                    ataques_derivados.nivel = ataque.nivel

            # Apertos de botão na tela de pausa
            if jogo_pausado:
                for botao in botoes_menu_pausa:
                    if botao.mouse_interacao(evento):
                        if botao == CONTINUAR_botao_pausa:
                            tempo_pausado_total += pygame.time.get_ticks() - contar_tempo_pausado
                            jogo_pausado = False
                        elif botao == MENU_PRINCIPAL_botao:
                            return False, 0
                        elif botao == REINICIAR_botao_pausa:
                            return True, 0

            # Apertos de botão na tela de morte
            if jogo_tela_morte:
                for botao in botoes_tela_morte:
                    if botao.mouse_interacao(evento):
                        if botao == REINICIAR_botao_morte:
                            return True, moedas_ganhas
                        elif botao == MENU_PRINCIPAL_botao_morte:
                            return False, moedas_ganhas

            if jogo_tela_level_up:
                for botao in botoes_level_up:
                    if botao.mouse_interacao(evento):
                        if botao == CONTINUAR_botao_level_up:
                            tempo_pausado_total += pygame.time.get_ticks() - contar_tempo_pausado
                            jogo_tela_level_up = False


        # Atualiza a tela
        pygame.display.flip()

# Função para mostrar o menu principal
def menu_principal(moedas_acumuladas, personagems_comprados):
    pygame.mixer_music.stop()

    volume_barra = BarraFixa(240, 30, (520, 595))

    frames = [PersonagemFrame((coord_x, 124), personagem_tupla[i], 1000) for i, coord_x in enumerate((365, 505, 645, 785))]

    personagem_selecionado = None

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or SAIR_botao.mouse_interacao(evento):
                pygame.quit()
                sys.exit()

            if JOGAR_botao.mouse_interacao(evento) and personagem_selecionado:
                return personagem_selecionado, moedas_acumuladas, personagems_comprados

            if MAIS_botao.mouse_interacao(evento):
                pygame.mixer.music.set_volume(min(1, pygame.mixer.music.get_volume() + 0.1))

            if MENOS_botao.mouse_interacao(evento):
                pygame.mixer.music.set_volume(max(0, pygame.mixer.music.get_volume() - 0.1))

            if SALVAR_botao.mouse_interacao(evento):
                with open('save.pkl', 'wb') as file:
                    pickle.dump((moedas_acumuladas, personagems_comprados), file)

            if RESETAR_botao.mouse_interacao(evento):
                moedas_acumuladas = 1000
                personagem_selecionado = None
                personagems_comprados = [False for _ in range(len(personagem_tupla))]

            for frame in frames:
                moedas_acumuladas, personagem_selecionado, comprou = frame.comprar(moedas_acumuladas, personagem_selecionado, evento)
                if comprou:
                    personagems_comprados[frames.index(frame)] = True

        TELA.blit(background.convert_alpha(), background.get_rect(topleft=(0, 0)))

        # Caixa para barra de volume. Possivelmente opções de mudo e fullscreen?
        TELA.blit(box_config.convert_alpha(), box_config.get_rect(topleft=(408, 538)))

        # Barra de Volume
        volume_texto = pygame.font.Font(None, 45).render(f"VOLUME", True, BRANCO)
        TELA.blit(volume_texto, volume_texto.get_rect(center=(640, 568)))
        volume_barra.atualizar(pygame.mixer.music.get_volume(), 1, (255, 255, 255))
        TELA.blit(volume_barra.image, volume_barra.rect)

        # Titulo do Jogo
        titulo_texto = pygame.font.Font(None, 100).render(f"VAMPIRO SOBREVIVENTES", True, BRANCO)
        TELA.blit(titulo_texto, titulo_texto.get_rect(center=(640, 85)))

        # Contagem de moedas
        TELA.blit(moedas_conta.convert_alpha(), moedas_conta.get_rect(topleft=(483, 0)))
        moedas_texto = pygame.font.Font(None, 46).render(f"{moedas_acumuladas}", True, BRANCO)
        TELA.blit(moedas_texto, moedas_texto.get_rect(center=(640, 20)))
        TELA.blit(moeda.convert_alpha(), moeda.get_rect(topright=(570, 5)))

        # Botões
        for botao in botoes_menu_principal:
            botao.desenhar(TELA)

        # Desenhar frames de personagem de acordo se eles estão bloqueados ou não
        for i, frame in enumerate(frames):
            frame.desbloqueado_variavel = personagems_comprados[i]
            frame.desenhar(TELA)

        pygame.display.update()


def tela_level_up():
    # Camada sobre a tela que permite que coisas sejam desenhadas com opacidade reduzida
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    pygame.draw.rect(camada, (20, 50, 50, 150), (0, 0, LARGURA, ALTURA))
    TELA.blit(camada, (0, 0))

    texto_morte = pygame.font.Font(None, 100).render(f"SUBIU DE NÍVEL!!!", True, BRANCO)
    TELA.blit(texto_morte, (LARGURA // 2 - texto_morte.get_width() // 2, ALTURA // 2 - 300))
    for botao in botoes_level_up:
        botao.desenhar(TELA)

while True:
    personagem_selecionado, moedas_acumuladas, personagems_comprados = menu_principal(moedas_acumuladas, personagems_comprados)
    while True:
        reiniciar, moedas_ganhas = iniciar_jogo(pygame.time.get_ticks(), personagem_selecionado)
        moedas_acumuladas += moedas_ganhas
        if not reiniciar:
            break
