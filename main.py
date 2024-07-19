from personagems import Chicote
from inimigos import Texugo
from coletaveis import Moeda, Cura, CristalXp
import pygame
import random

pygame.init()

# Constantes
LARGURA = 1200
ALTURA = 800
FPS = 120

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Vampiro Sobreviventes')

# Fontes
fonte_none = pygame.font.Font(None, 30)

# Jogo Stats
total_moedas = 0

# Grupos de sprite
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
moedas = pygame.sprite.Group()
pocoes = pygame.sprite.Group()
cristais = pygame.sprite.Group()

# Gera 10 moedas em posições aleatórias e adiciona elas aos sprite groups
for i in range(10):
    moeda = Moeda(random.randint(100, 1101), random.randint(100, 701))
    todos_sprites.add(moeda)
    moedas.add(moeda)

jogador = Chicote(600, 400)
todos_sprites.add(jogador)
obstagoon = Texugo(pygame.math.Vector2(200, 100))
todos_sprites.add(obstagoon)

cura = Cura(550, 550)
todos_sprites.add(cura)
pocoes.add(cura)

for i in range(10):
    cristal = CristalXp(random.randint(100, 1101), random.randint(100, 701), random.choice(['Blue', 'Green', 'Red']))
    todos_sprites.add(cristal)
    cristais.add(cristal)

clock = pygame.time.Clock()

while True:

    clock.tick(FPS)
    delta_time = clock.tick(FPS) / 10

    # Resetar o fundo
    tela.fill((0, 0, 0))

    # Desenha sprites
    todos_sprites.draw(tela)

    # Moedas
    for coin in moedas:
        coin.animar_sprite()
        total_moedas += coin.checar_colisao(jogador)

    # Jogador
    jogador.movimento(delta_time)
    jogador.animar_sprite()
    jogador.nivel_update()

    # Pocao
    for potion in pocoes:
        jogador.hit_points_atuais += potion.checar_colisao(jogador)
        if jogador.hit_points_atuais > 100: jogador.hit_points_atuais = 100

    # Badger
    obstagoon.movimento(jogador.pos, delta_time)
    obstagoon.animar_sprite()
    jogador.hit_points_atuais -= obstagoon.dar_dano(jogador)
    obstagoon.checar_hp()

    # Cristais
    for cristal in cristais:
        cristal.animar_sprite()
        jogador.exp += cristal.checar_colisao(jogador)

    # UI
    FPS_ui = fonte_none.render(f"FPS: {clock.get_fps():.1f}", False, (255, 255, 255))
    MOEDAS_ui = fonte_none.render(f"Moedas: {total_moedas}", False, (255, 255, 255))
    HP_ui = fonte_none.render(f"Vida do Jogador: {jogador.hit_points_atuais}/{jogador.hit_point_max}", False, (255, 255, 255))
    LEVEL_ui = fonte_none.render(f"Nível do Jogador: {jogador.nivel}", False, (255, 255, 255))
    XP_ui = fonte_none.render(f"XP: {jogador.exp}/{jogador.exp_para_proximo_nivel}", False, (255, 255, 255))

    tela.blit(FPS_ui, FPS_ui.get_rect(center=(800, 20)))
    tela.blit(MOEDAS_ui, MOEDAS_ui.get_rect(center=(1000, 20)))
    tela.blit(HP_ui, HP_ui.get_rect(center=(150, 20)))
    tela.blit(LEVEL_ui, LEVEL_ui.get_rect(center=(121, 50)))
    tela.blit(XP_ui,  XP_ui.get_rect(center=(121, 70)))

    # Fechar o jogo caso aperte X
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Atualiza a tela
    pygame.display.update()
