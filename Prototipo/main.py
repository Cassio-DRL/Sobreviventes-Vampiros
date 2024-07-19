from gameObjects import Jogador, Moeda, Cura, Badger, Missel
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

# Objetos
todos_sprites = pygame.sprite.Group()
moedas = pygame.sprite.Group()
pocoes = pygame.sprite.Group()
misseis = pygame.sprite.Group()

# Gera 10 moedas em posições aleatórias e adiciona elas aos sprite groups
for i in range(10):
    moeda = Moeda(random.randint(100, 1101), random.randint(100, 701))
    todos_sprites.add(moeda)
    moedas.add(moeda)

jogador = Jogador(600, 400)
todos_sprites.add(jogador)
obstagoon = Badger(200, 100)
todos_sprites.add(obstagoon)

cura = Cura(550, 550)
todos_sprites.add(cura)
pocoes.add(cura)

missel = Missel(jogador, obstagoon)
misseis.add(missel)
todos_sprites.add(missel)

clock = pygame.time.Clock()
tempo_inicial_missel = pygame.time.get_ticks()

while True:

    clock.tick(FPS)
    delta_time = clock.tick(FPS) / 10

    # Resetar o fundo
    tela.fill((0, 0, 0))

    # Missel Instanciador
    tempo_agora = pygame.time.get_ticks()
    if tempo_agora - tempo_inicial_missel > 1000:
        tempo_inicial_missel = tempo_agora
        missel = Missel(jogador, obstagoon)
        misseis.add(missel)
        todos_sprites.add(missel)

    # Desenha sprites
    todos_sprites.draw(tela)

    # Moedas
    for coin in moedas:
        coin.animar_sprite()
        total_moedas += coin.checar_colisao(jogador)

    # Jogador
    jogador.movemento(delta_time)
    jogador.animar_sprite()

    # Pocao
    for potion in pocoes:
        jogador.hit_points_atuais += potion.checar_colisao(jogador)
        if jogador.hit_points_atuais > 100: jogador.hit_points_atuais = 100

    # Badger
    obstagoon.movimento(jogador.pos, delta_time)
    obstagoon.animar_sprite()
    jogador.hit_points_atuais -= obstagoon.dar_dano(jogador)
    obstagoon.checar_hp()

    # Missel
    for projectil in misseis:
        projectil.movimento(delta_time)
        projectil.animar_sprite()
        obstagoon.hit_points_atuais -= projectil.dar_dano(obstagoon)

    # UI
    FPS_ui = fonte_none.render(f"FPS: {clock.get_fps():.1f}", False, (255, 255, 255))
    MOEDAS_ui = fonte_none.render(f"Moedas: {total_moedas}", False, (255, 255, 255))
    HP_ui = fonte_none.render(f"Vida do Jogador: {jogador.hit_points_atuais}/{jogador.hit_point_max}", False, (255, 255, 255))

    tela.blit(FPS_ui, FPS_ui.get_rect(center=(800, 20)))
    tela.blit(MOEDAS_ui, MOEDAS_ui.get_rect(center=(1000, 20)))
    tela.blit(HP_ui, HP_ui.get_rect(center=(150, 20)))

    # Fechar o jogo caso aperte X
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Atualiza a tela
    pygame.display.update()
