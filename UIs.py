import pygame
pygame.init()

# Images
inventario = pygame.image.load('Sprites/UI/Inventário.png')
pocao = pygame.transform.scale(pygame.image.load('Sprites/pocao grande.png'), (45, 45))
velocidade = pygame.transform.scale(pygame.image.load('Sprites/pocao pequena.png'), (36, 45))
bomba = pygame.transform.scale(pygame.image.load('Sprites/bomba.png'), (45, 45))
dobroxp = pygame.transform.scale(pygame.image.load('Sprites/banana_dobro_xp.png'), (45, 45))
caveira = pygame.transform.scale(pygame.image.load('Sprites/UI/caveira.png'), (24, 26))
cristal = pygame.transform.scale(pygame.image.load(f"Sprites/Cristais/Pink/pink_crystal_0000.png"), (34, 34))
moeda = pygame.transform.scale(pygame.image.load(f"Sprites/Moeda_girando_1.png"), (25, 25))

def ui_jogo(total_moedas, total_cristais, nivel, xp, xp_para_proximo_nivel, pocoes, inimigos_mortos, segundos, fonte, cor, tela,
            pocoes_velocidade, bombas, dobro_xp, barraxp, jogador, barrahp):
    FONTE_NONE_MEDIA = pygame.font.Font(None, 50)

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


def tela_morte(largura, altura, tela, fonte, botoes, cor):
    # Função para desenhar todos os elementos da tela de morte
    camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.rect(camada, (20, 50, 50, 150), (0, 0, largura, altura))
    tela.blit(camada, (0, 0))

    # Texto grande no meio da tela
    texto_morte = fonte.render(f"MORTO", True, cor)
    tela.blit(texto_morte, (largura // 2 - texto_morte.get_width() // 2, altura // 2 - 100))

    # Desenha cada botão
    for botao in botoes:
        botao.desenhar(tela)

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
