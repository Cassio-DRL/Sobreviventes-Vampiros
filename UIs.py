import pygame
import sys

pygame.init()

# Fontes
FONTE_NONE_GRANDE = pygame.font.Font(None, 100)
FONTE_NONE_MEDIA = pygame.font.Font(None, 50)

# Tela Inicial
background = pygame.image.load('Sprites/UI/Background.png')
jogador_frame = pygame.image.load('Sprites/UI/Character_frame.png')
moedas_conta = pygame.image.load('Sprites/UI/coin_count_frame.png')
inventario = pygame.image.load('Sprites/UI/Inventário.png')
box_config = pygame.image.load('Sprites/UI/box.png')

# UI durante jogo
pocao = pygame.transform.scale(pygame.image.load('Sprites/pocao grande.png'), (45, 45))
velocidade = pygame.transform.scale(pygame.image.load('Sprites/pocao pequena.png'), (36, 45))
bomba = pygame.transform.scale(pygame.image.load('Sprites/bomba.png'), (45, 45))
dobroxp = pygame.transform.scale(pygame.image.load('Sprites/banana_dobro_xp.png'), (45, 45))
caveira = pygame.transform.scale(pygame.image.load('Sprites/UI/caveira.png'), (24, 26))
cristal = pygame.transform.scale(pygame.image.load(f"Sprites/Cristais/Pink/pink_crystal_0000.png"), (34, 34))
moeda = pygame.transform.scale(pygame.image.load(f"Sprites/Moeda_girando_1.png"), (25, 25))


class Botao:
    """
    Botão com texto que pode ser clicado pelo mouse, pode receber uma imagem onde o texto ficaria por cima, ou uma cor
    para desenhar um rect com, ou nem imagem nem cor para ter só o texto
    """
    def __init__(self, pos, largura, altura, texto, fonte, cor=None, imagem=None):
        self.rect = pygame.Rect(pos.x, pos.y, largura, altura)
        self.fonte = fonte
        self.texto = self.fonte.render(texto, False, (255, 255, 255))
        self.cor = cor
        self.image = imagem

        if imagem:
            self.image = pygame.transform.scale(imagem.convert_alpha(), (largura, altura))

    def desenhar(self, tela):
        if self.image:
            tela.blit(self.image, self.rect)
        elif self.cor:
            pygame.draw.rect(tela, self.cor, self.rect)
        tela.blit(self.texto, self.texto.get_rect(center=self.rect.center))

    def mouse_interacao(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.rect.collidepoint(evento.pos):
                return True
        return False


class Barra(pygame.sprite.Sprite):
    def __init__(self, largura, altura):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.image = pygame.Surface((self.largura, self.altura))
        self.rect = self.image.get_rect()


# Barra que segue o jogador mostrando o HP dele
class BarraVida(Barra):
    def __init__(self, largura, altura, offset):
        self.offset = offset
        super().__init__(largura, altura)

    def atualizar(self, jogador):
        # Atualizar posição com base na posição do jogador
        self.rect.center = (jogador.rect.centerx + self.offset[0], jogador.rect.centery + self.offset[1])

        # Calcular largura da barra de vida
        proporcao_de_vida = jogador.hit_points_atuais / jogador.hit_point_max

        self.image.fill((0, 0, 0))

        # Desenhar a barra de vida
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, self.largura * proporcao_de_vida, self.altura))


# Barra que fica em uma posição fixa
class BarraFixa(Barra):
    def __init__(self, largura, altura, posicao_fixa):
        super().__init__(largura, altura)
        self.rect.topleft = posicao_fixa

    def atualizar(self, stat1, stat2, cor):
        # Calcular proporção
        proporcao = stat1 / stat2

        self.image.fill((0, 0, 0))

        # Desenhar a barra fixa
        pygame.draw.rect(self.image, cor, (0, 0, self.largura * proporcao, self.altura))


class PersonagemFrame(pygame.sprite.Sprite):
    def __init__(self, pos, personagem):
        super().__init__()
        self.image = jogador_frame
        self.rect = self.image.get_rect(topleft=pos)
        self.personagem = personagem

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)
        tela.blit(self.personagem.image, self.personagem.image.get_rect(center=(self.rect.centerx, self.rect.centery)))


# Função para mostrar o menu principal
def menu_principal(TELA, BRANCO, moedas_acumuladas, iniciar_jogo, JOGAR_botao, SAIR_botao, MAIS_botao, MENOS_botao, personagem_tupla):
    pygame.mixer_music.stop()
    volume_barra = BarraFixa(240, 30, (520, 595))
    frames = pygame.sprite.Group()
    for i, coord_x in enumerate((365, 505, 645, 785)):
        frame = PersonagemFrame((coord_x, 124), personagem_tupla[i])
        frames.add(frame)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or SAIR_botao.mouse_interacao(evento):
                pygame.quit()
                sys.exit()
            if JOGAR_botao.mouse_interacao(evento):
                iniciar_jogo(pygame.time.get_ticks(), moedas_acumuladas)
            if MAIS_botao.mouse_interacao(evento):
                pygame.mixer.music.set_volume(min(1, pygame.mixer.music.get_volume() + 0.1))
            if MENOS_botao.mouse_interacao(evento):
                pygame.mixer.music.set_volume(max(0, pygame.mixer.music.get_volume() - 0.1))

        TELA.blit(background.convert_alpha(), background.get_rect(topleft=(0, 0)))

        # Caixa para barra de volume. Possivelmente opções de mudo e fullscreen?
        TELA.blit(box_config.convert_alpha(), box_config.get_rect(topleft=(408, 538)))

        for i in (365, 505, 645, 785):
            TELA.blit(jogador_frame.convert_alpha(), jogador_frame.get_rect(topleft=(i, 124)))

        # Barra de Volume
        volume_texto = FONTE_NONE_MEDIA.render(f"VOLUME", True, BRANCO)
        TELA.blit(volume_texto, volume_texto.get_rect(center=(640, 570)))
        volume_barra.atualizar(pygame.mixer.music.get_volume(), 1, (255, 255, 255))
        TELA.blit(volume_barra.image, volume_barra.rect)

        # Titulo do Jogo
        titulo_texto = FONTE_NONE_GRANDE.render(f"VAMPIRO SOBREVIVENTES", True, BRANCO)
        TELA.blit(titulo_texto, titulo_texto.get_rect(center=(640, 85)))

        # Contagem de moedas
        TELA.blit(moedas_conta.convert_alpha(), moedas_conta.get_rect(topleft=(483, 0)))
        moedas_texto = FONTE_NONE_MEDIA.render(f"{moedas_acumuladas}", True, BRANCO)
        TELA.blit(moedas_texto, moedas_texto.get_rect(center=(640, 20)))
        TELA.blit(moeda.convert_alpha(), moeda.get_rect(topright=(570, 5)))

        # Botões
        JOGAR_botao.desenhar(TELA)
        SAIR_botao.desenhar(TELA)
        MAIS_botao.desenhar(TELA)
        MENOS_botao.desenhar(TELA)

        for frame in frames:
            frame.desenhar(TELA)

        pygame.display.update()


def menu_pausa(largura, altura, tela, fonte, botoes, cor):
    # Função para desenhar todos os elementos da tela de pausa

    # Camada sobre a tela que permite que coisas sejam desenhadas com opacidade reduzida
    camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.rect(camada, (20, 50, 50, 150), (0, 0, largura, altura))
    tela.blit(camada, (0, 0))

    # Texto grande no meio da tela
    texto_pausa = fonte.render(f"JOGO PAUSADO", False, cor)
    tela.blit(texto_pausa, (largura // 2 - texto_pausa.get_width() // 2, altura // 2 - 100))

    # Desenha cada botão
    for botao in botoes:
        botao.desenhar(tela)


def tela_morte(largura, altura, tela, fonte, botoes, cor, num_inimigos, num_cristais, num_moedas):
    # Função para desenhar todos os elementos da tela de morte
    camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.rect(camada, (20, 50, 50, 150), (0, 0, largura, altura))
    tela.blit(camada, (0, 0))

    # Texto grande no meio da tela
    texto_morte = fonte.render(f"MORTO", True, cor)
    tela.blit(texto_morte, (largura // 2 - texto_morte.get_width() // 2, altura // 2 - 300))

    # Moedas ganhas
    inimigos = FONTE_NONE_MEDIA.render(f"Inimigos Mortos: {num_inimigos}", True, cor)
    cristais = FONTE_NONE_MEDIA.render(f"Cristais Coletados: {num_cristais}", True, cor)
    moedas = FONTE_NONE_MEDIA.render(f"Moedas Coletadas: {num_moedas}", True, cor)

    contagem_inimigos = FONTE_NONE_MEDIA.render(f"{num_inimigos // 2}", True, cor)
    contagem_cristais = FONTE_NONE_MEDIA.render(f"{num_cristais // 4}", True, cor)
    contagem_moedas = FONTE_NONE_MEDIA.render(f"{num_moedas}", True, cor)
    total = FONTE_NONE_MEDIA.render(f"{num_moedas + num_cristais // 4 + num_inimigos // 2}", True, cor)

    tela.blit(inimigos, inimigos.get_rect(topleft=(300, 250)))
    tela.blit(cristais, cristais.get_rect(topleft=(300, 300)))
    tela.blit(moedas, moedas.get_rect(topleft=(300, 350)))

    tela.blit(contagem_inimigos, contagem_inimigos.get_rect(topright=(800, 250)))
    tela.blit(contagem_cristais, contagem_cristais.get_rect(topright=(800, 300)))
    tela.blit(contagem_moedas, contagem_moedas.get_rect(topright=(800, 350)))
    tela.blit(total, total.get_rect(topright=(800, 400)))

    for i in (251, 301, 351):
        tela.blit(moeda.convert_alpha(), moeda.get_rect(topright=(840, i)))

    # Desenha cada botão
    for botao in botoes:
        botao.desenhar(tela)

    return num_moedas + num_cristais // 4 + num_inimigos // 2


def ui_jogo(total_moedas, total_cristais, nivel, xp, xp_para_proximo_nivel, pocoes, inimigos_mortos, segundos, fonte, cor, tela, pocoes_velocidade, bombas, dobro_xp):
    LEVEL_ui = fonte.render(f"lvl {nivel}", False, cor)
    XP_ui = fonte.render(f"{xp}/{xp_para_proximo_nivel}", False, cor)

    KILLCOUNT_ui = fonte.render(f"{inimigos_mortos}", False, cor)
    TIMER_ui = FONTE_NONE_MEDIA.render(f"{segundos // 60:02}:{segundos % 60:02}", False, cor)

    MOEDAS_ui = fonte.render(f"{total_moedas}", False, cor)
    CRISTAIS_ui = fonte.render(f"{total_cristais}", False, cor)

    tela.blit(inventario.convert_alpha(), inventario.get_rect(bottomleft=(0, 800)))
    tela.blit(pocao.convert_alpha(), pocao.get_rect(center=(45, 768)))
    tela.blit(velocidade.convert_alpha(), velocidade.get_rect(center=(120, 768)))
    tela.blit(bomba.convert_alpha(), bomba.get_rect(center=(190, 768)))
    tela.blit(dobroxp.convert_alpha(), dobroxp.get_rect(center=(265, 768)))

    POCOES_CURA_ui = fonte.render(f"{pocoes}", False, cor)
    POCOES_VELOCIDADE_ui = fonte.render(f"{pocoes_velocidade}", False, cor)
    BOMBAS_ui = fonte.render(f"{bombas}", False, cor)
    DOBRO_XP_ui = fonte.render(f"{dobro_xp}", False, cor)

    tela.blit(caveira.convert_alpha(), caveira.get_rect(topleft=(1025, 34)))
    tela.blit(cristal.convert_alpha(), cristal.get_rect(topleft=(1100, 29)))
    tela.blit(moeda, moeda.get_rect(topleft=(1181, 33)))

    tela.blit(KILLCOUNT_ui, KILLCOUNT_ui.get_rect(topleft=(1065, 38)))
    tela.blit(CRISTAIS_ui, CRISTAIS_ui.get_rect(topleft=(1140, 38)))
    tela.blit(MOEDAS_ui, MOEDAS_ui.get_rect(topleft=(1221, 38)))

    tela.blit(LEVEL_ui, LEVEL_ui.get_rect(topright=(1270, 8)))
    tela.blit(XP_ui, XP_ui.get_rect(center=(640, 18)))

    tela.blit(TIMER_ui, TIMER_ui.get_rect(center=(640, 55)))

    tela.blit(POCOES_CURA_ui, POCOES_CURA_ui.get_rect(topleft=(51, 770)))
    tela.blit(POCOES_VELOCIDADE_ui, POCOES_VELOCIDADE_ui.get_rect(topleft=(126, 770)))
    tela.blit(BOMBAS_ui, BOMBAS_ui.get_rect(topleft=(201, 770)))
    tela.blit(DOBRO_XP_ui, DOBRO_XP_ui.get_rect(topleft=(276, 770)))
