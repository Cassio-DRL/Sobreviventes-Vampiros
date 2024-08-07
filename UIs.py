import pygame

pygame.init()

# Fontes
FONTE_NONE_GRANDE = pygame.font.Font("fonte/Silkscreen-Regular.ttf", 100)
FONTE_NONE_MEDIA = pygame.font.Font("fonte/Silkscreen-Regular.ttf", 50)
fonte = "fonte/Silkscreen-Regular.ttf"

# Player Frame
jogador_frame = pygame.image.load('Sprites/UI/Character_frame.png')
cadeado = pygame.transform.scale(pygame.image.load('Sprites/cadeado.png'), (90, 90))

# Tela de Upgrade
frame_levelup = pygame.image.load('Sprites/UI/frame levelup.png')

# UI durante jogo
inventario = pygame.image.load('Sprites/UI/Inventário.png')
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
        self.texto = self.fonte.render(texto, True, (255, 255, 255))
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
                som = pygame.mixer.Sound('Audio/ButtonPlate Click (Minecraft Sound) - Sound Effect for editing.mp3')
                pygame.mixer.Sound.set_volume(som, pygame.mixer_music.get_volume())
                pygame.mixer.Sound.play(som)
                pygame.time.wait(100)
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


# Barra que fica em uma posição fixa (Usada para barra de XP no jogo e barra de volume no menu inicial)
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
    """
    Objeto no menu principal com a possibilidade de comprar ou selecionar personagens
    """
    def __init__(self, pos, personagem, preco):
        super().__init__()
        self.image = jogador_frame
        self.rect = self.image.get_rect(topleft=pos)
        self.personagem_classe = personagem
        self.personagem = personagem(pygame.math.Vector2(0, 0), pygame.time.get_ticks())
        self.preco = preco
        self.desbloqueado_variavel = False
        self.botao_comprar = Botao(pygame.math.Vector2(self.rect.centerx - 60, self.rect.centery + 55), 120, 47, f"{preco}", pygame.font.Font(fonte, 45), cor=(130, 192, 86))
        self.botao_selecionar = Botao(pygame.math.Vector2(self.rect.centerx - 60, self.rect.centery + 55), 120, 47, f"SELECIONAR", pygame.font.Font(fonte, 23), cor=(0, 106, 181))

    def desenhar(self, tela):

        tela.blit(self.image, self.rect)
        if self.desbloqueado_variavel:
            tela.blit(pygame.transform.scale(self.personagem.image, (88, 88)), self.personagem.image.get_rect(center=(self.rect.centerx, self.rect.centery-25)))

            NOME = pygame.font.Font(fonte, 17).render(f"{self.personagem.dicionario['Nome']}", False, (255, 255, 255))
            HP = pygame.font.Font(fonte, 17).render(f"HP: {self.personagem.dicionario['HP']}", False, (255, 255, 255))
            ATK = pygame.font.Font(fonte, 17).render(f"ATK: {self.personagem.dicionario['ATK']}", False, (255, 255, 255))
            DEF = pygame.font.Font(fonte, 17).render(f"DEF: {self.personagem.dicionario['DEF']}", False, (255, 255, 255))
            SPD = pygame.font.Font(fonte, 17).render(f"SPEED: {self.personagem.dicionario['SPD']}", False, (255, 255, 255))

            tela.blit(NOME, NOME.get_rect(center=(self.rect.centerx, self.rect.centery-90)))
            tela.blit(HP, HP.get_rect(topleft=(self.rect.centerx-56, self.rect.centery-15)))
            tela.blit(ATK, ATK.get_rect(topleft=(self.rect.centerx - 56, self.rect.centery - 0)))
            tela.blit(DEF, DEF.get_rect(topleft=(self.rect.centerx - 56, self.rect.centery + 15)))
            tela.blit(SPD, SPD.get_rect(topleft=(self.rect.centerx - 56, self.rect.centery + 30)))

            self.botao_selecionar.desenhar(tela)

        else:
            tela.blit(cadeado.convert_alpha(), cadeado.get_rect(center=(self.rect.centerx, self.rect.centery-25)))
            self.botao_comprar.desenhar(tela)

    def comprar(self, dinheiro, selecionado, evento):
        comprado = False
        if self.desbloqueado_variavel:
            if self.botao_selecionar.mouse_interacao(evento):
                selecionado = self.personagem_classe
        else:
            if self.botao_comprar.mouse_interacao(evento) and dinheiro >= self.preco:
                dinheiro -= self.preco
                comprado = True

        return dinheiro, selecionado, comprado

class MolduraAtaqueLevelUP(pygame.sprite.Sprite):
    def __init__(self, pos, ataque):
        super().__init__()
        self.image = frame_levelup
        self.rect = self.image.get_rect(center=pos)
        self.ataque = ataque
        self.botao_selecionar = Botao(pygame.math.Vector2(self.rect.topleft[0] + 131, self.rect.topleft[1] + 104), 383, 25, "SELECIONAR", pygame.font.Font(fonte, 29), cor=(130, 192, 86))

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

        NOME = pygame.font.Font(fonte, 30).render(f"{self.ataque.nome}", False, (255, 255, 255))
        NIVEL = pygame.font.Font(fonte, 20).render(f"LVL {self.ataque.nivel + 1}", False, (255, 255, 255))
        DESCRICAO = pygame.font.Font(fonte, 23).render(f"{self.ataque.level_up_dict[self.ataque.nivel + 1]}", False, (0, 0, 0))

        tela.blit(self.ataque.icone, self.ataque.icone.get_rect(topleft = (self.rect.topleft[0]+4, self.rect.topleft[1]+4)))
        tela.blit(NOME, NOME.get_rect(topleft=(self.rect.topleft[0] + 131, self.rect.topleft[1] + 20)))
        tela.blit(NIVEL, NIVEL.get_rect(topleft=(self.rect.topleft[0] + 424, self.rect.topleft[1] + 20)))
        tela.blit(DESCRICAO, DESCRICAO.get_rect(topleft=(self.rect.topleft[0] + 131, self.rect.topleft[1] + 50)))
        self.botao_selecionar.desenhar(tela)

    def selecionar_upgrade(self, evento):
        if self.botao_selecionar.mouse_interacao(evento):
            return self.ataque
        return None

def hud(total_moedas, total_cristais, nivel, xp, xp_para_proximo_nivel, pocoes, inimigos_mortos, segundos, fonte, cor, tela, pocoes_velocidade, bombas, dobro_xp):
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

    tela.blit(caveira.convert_alpha(), caveira.get_rect(topleft=(980, 34)))
    tela.blit(cristal.convert_alpha(), cristal.get_rect(topleft=(1077, 29)))
    tela.blit(moeda, moeda.get_rect(topleft=(1181, 33)))

    tela.blit(KILLCOUNT_ui, KILLCOUNT_ui.get_rect(topleft=(1020, 28)))
    tela.blit(CRISTAIS_ui, CRISTAIS_ui.get_rect(topleft=(1117, 28)))
    tela.blit(MOEDAS_ui, MOEDAS_ui.get_rect(topleft=(1221, 28)))

    tela.blit(LEVEL_ui, LEVEL_ui.get_rect(topright=(1270, 0)))
    tela.blit(XP_ui, XP_ui.get_rect(center=(640, 18)))

    tela.blit(TIMER_ui, TIMER_ui.get_rect(center=(640, 55)))

    tela.blit(POCOES_CURA_ui, POCOES_CURA_ui.get_rect(topleft=(51, 760)))
    tela.blit(POCOES_VELOCIDADE_ui, POCOES_VELOCIDADE_ui.get_rect(topleft=(126, 760)))
    tela.blit(BOMBAS_ui, BOMBAS_ui.get_rect(topleft=(201, 760)))
    tela.blit(DOBRO_XP_ui, DOBRO_XP_ui.get_rect(topleft=(276, 760)))
