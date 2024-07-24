import pygame

pygame.init()

# Fontes
FONTE_NONE_GRANDE = pygame.font.Font(None, 50)
FONTE_NONE_MEDIA = pygame.font.Font(None, 50)

# Images
inventario = pygame.image.load('Sprites/UI/Inventário.png')
pocao = pygame.transform.scale(pygame.image.load('Sprites/pocao grande.png'), (45, 45))
velocidade = pygame.transform.scale(pygame.image.load('Sprites/pocao pequena.png'), (36, 45))
bomba = pygame.transform.scale(pygame.image.load('Sprites/bomba.png'), (45, 45))
dobroxp = pygame.transform.scale(pygame.image.load('Sprites/banana_dobro_xp.png'), (45, 45))
caveira = pygame.transform.scale(pygame.image.load('Sprites/UI/caveira.png'), (24, 26))
cristal = pygame.transform.scale(pygame.image.load(f"Sprites/Cristais/Pink/pink_crystal_0000.png"), (34, 34))
moeda = pygame.transform.scale(pygame.image.load(f"Sprites/Moeda_girando_1.png"), (25, 25))


def ui_jogo(total_moedas, total_cristais, nivel, xp, xp_para_proximo_nivel, pocoes, inimigos_mortos, segundos, fonte,
            cor, tela,
            pocoes_velocidade, bombas, dobro_xp, barraxp, jogador, barrahp):
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

    barrahp.atualizar(jogador)
    barraxp.atualizar(jogador)


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
    tela.blit(texto_morte, (largura // 2 - texto_morte.get_width() // 2, altura // 2 - 100))

    # Moedas ganhas
    moedas_ganhas = FONTE_NONE_GRANDE.render(f"MOEDAS GANHAS", True, cor)
    inimigos = FONTE_NONE_MEDIA.render(f"Inimigos Mortos: {num_inimigos}", True, cor)
    cristais = FONTE_NONE_MEDIA.render(f"Cristais Coletados: {num_cristais}", True, cor)
    moedas = FONTE_NONE_MEDIA.render(f"Moedas Coletadas: {num_moedas}", True, cor)

    contagem_inimigos = FONTE_NONE_MEDIA.render(f"{num_inimigos // 2}", True, cor)
    contagem_cristais = FONTE_NONE_MEDIA.render(f"{num_cristais // 4}", True, cor)
    contagem_moedas = FONTE_NONE_MEDIA.render(f"{num_moedas}", True, cor)
    total = FONTE_NONE_MEDIA.render(f"Moedas Totais: {num_moedas + num_cristais // 4 + num_inimigos // 2}", True, cor)

    tela.blit(moedas_ganhas, moedas_ganhas.get_rect(topleft=(300, 400)))
    tela.blit(inimigos, inimigos.get_rect(topleft=(300, 450)))
    tela.blit(cristais, cristais.get_rect(topleft=(300, 500)))
    tela.blit(moedas, moedas.get_rect(topleft=(300, 550)))

    tela.blit(contagem_inimigos, contagem_inimigos.get_rect(topright=(800, 450)))
    tela.blit(contagem_cristais, contagem_cristais.get_rect(topright=(800, 500)))
    tela.blit(contagem_moedas, contagem_moedas.get_rect(topright=(800, 550)))
    tela.blit(total, total.get_rect(topleft=(300, 600)))

    for i in (450, 505, 555):
        tela.blit(moeda.convert_alpha(), moeda.get_rect(topright=(840, i)))

    # Desenha cada botão
    for botao in botoes:
        botao.desenhar(tela)

    return num_moedas + num_cristais // 4 + num_inimigos // 2


class Barra(pygame.sprite.Sprite):
    def __init__(self, largura, altura, offset):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.offset = offset
        self.image = pygame.Surface((self.largura, self.altura))
        self.rect = self.image.get_rect()


class BarraVida(Barra):
    def __init__(self, largura, altura, offset):
        super().__init__(largura, altura, offset)

    def atualizar(self, jogador):
        # Atualizar posição com base na posição do jogador
        self.rect.center = (jogador.rect.centerx + self.offset[0], jogador.rect.centery + self.offset[1])

        # Calcular largura da barra de vida
        proporcao_de_vida = jogador.hit_points_atuais / jogador.hit_point_max

        self.image.fill((0, 0, 0))

        # Desenhar a barra de vida
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, self.largura * proporcao_de_vida, self.altura))


class BarraExp(Barra):
    def __init__(self, largura, altura, posicao_fixa):
        super().__init__(largura, altura, (0, 0))
        self.rect.topleft = posicao_fixa

    def atualizar(self, jogador):
        # Calcular proporção
        proporcao = jogador.xp / jogador.xp_para_proximo_nivel

        self.image.fill((0, 0, 0))

        # Desenhar a barra fixa
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, self.largura * proporcao, self.altura))
