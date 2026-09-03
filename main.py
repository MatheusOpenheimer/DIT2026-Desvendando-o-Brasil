import sys
import pygame
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
pygame.init()
pygame.mixer.init()

import banco
import config
import funcoes
from fase1 import Fase1
from fase2 import Fase2
from final import Final
from intro import Intro
from menu import Menu
from minigame import Minigame
from srs_minigame import MinigameSRS
from srs_jogo import JogoSantaRita

banco.criar_banco()
banco.criar_banco_srs()
tela = pygame.display.set_mode((config.largura, config.altura), pygame.FULLSCREEN)
pygame.display.set_caption("Desvendando o Brasil")

# JANELA DE SAÍDA
janela_sair = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/janela_sair.png")), (400, 400))
janela_sair_rect = janela_sair.get_rect(centerx=config.centroX, centery=config.altura // 2)
botao_sair = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_sair.png")), (155, 80))
botao_sair_rect = botao_sair.get_rect(centerx=config.centroX - 85, y=janela_sair_rect.y + 250)
botao_continuar = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_continuar.png")), (155, 80))
botao_continuar_rect = botao_continuar.get_rect(centerx=config.centroX + 85, y=botao_sair_rect.y)

# BOTÃO DE FECHAR (SAIR)
botao_fechar_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/fechar.png")), (50, 50))
botao_fechar_rect = botao_fechar_img.get_rect(x=2, y=2)

# BOTÃO DE ÁUDIO
botao_som = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_som.png")), (50, 50))
botao_som_rect = botao_som.get_rect(x=58, y=2)
botao_mutado = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_mutado.png")), (50, 50))
mutado = False


def trocar_musica(caminho):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(funcoes.resource_path(caminho))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    if mutado:
        pygame.mixer.music.pause()


trocar_musica("assets/AUDIOS/musicaMenu.mp3")
pygame.mixer.music.set_volume(0.2)
musica_play = True

# ESTADOS DO JOGO
FASE = "MENU"
menu = None
intro = None
fase1 = None
fase2 = None
final = None
minigame = None
minigame_srs = None
jogo_srs = None
modo = "facil"
personagem = "boy" #menino por default
dados_jogador = {
    "nome": "Explorador",
    "idade": 0,
    "acertos": 0,
    "erros": 0,
    "tempo_sobra": 0
}

EVENTO_CRONOMETRO = pygame.USEREVENT + 2
tempo_iniciado = False
reiniciar = False
salvarBD = False
show_janela_sair = False
tempo_restante = 250
regioes_erradas = []
regioes_jogadas = []

relogio = pygame.time.Clock()
rodando = True

# LOOP PRINCIPAL
while rodando:

    # EVENTOS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if botao_som_rect.collidepoint(evento.pos):
                mutado = not mutado
                if mutado:
                    pygame.mixer.pause()
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.unpause()
                    pygame.mixer.music.unpause()

            elif botao_fechar_rect.collidepoint(evento.pos):
                show_janela_sair = True

        if show_janela_sair:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_sair_rect.collidepoint(evento.pos):
                    rodando = False
                elif botao_continuar_rect.collidepoint(evento.pos):
                    show_janela_sair = False
            continue

        if FASE == "MENU" and menu is not None:
            PROXIMA_FASE, nome, idade = menu.gerenciar_eventos(evento)
            if PROXIMA_FASE and PROXIMA_FASE != "MENU":
                if nome and idade:
                    dados_jogador["nome"] = nome
                    dados_jogador["idade"] = idade
                menu = None
                FASE = PROXIMA_FASE

        elif FASE == "INTRO" and intro is not None:
            intro.gerenciar_eventos(evento)
        elif FASE == "GAME" and minigame is not None:
            minigame.gerenciar_eventos(evento)

        elif FASE == "GAME_SRS" and minigame_srs is not None:
            minigame_srs.gerenciar_eventos(evento)
        elif FASE == "JOGO_SRS" and jogo_srs is not None:
            jogo_srs.gerenciar_eventos(evento)
        elif FASE == "FASE1" and fase1 is not None:
            fase1.gerenciar_eventos(evento, modo)
        elif FASE == "FASE2" and fase2 is not None:
            fase2.gerenciar_eventos(evento, modo)
        elif FASE == "FINAL" and final is not None:
            final.gerenciar_eventos(evento)

        if evento.type == EVENTO_CRONOMETRO:
            if tempo_restante > 0:
                tempo_restante -= 1

    pos_mouse = pygame.mouse.get_pos()
    if botao_som_rect.collidepoint(pos_mouse) or botao_fechar_rect.collidepoint(pos_mouse) and not show_janela_sair:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    if FASE == "MENU":
        if menu is None:
            menu = Menu()
        if not musica_play:
            trocar_musica("assets/AUDIOS/musicaMenu.mp3")
            musica_play = True
        if reiniciar:
            tempo_iniciado = False
            dados_jogador = {
                "nome": "Explorador",
                "idade": 0,
                "acertos": 0,
                "erros": 0,
            }
            regioes_erradas = []
            regioes_jogadas = []
            reiniciar = False

    elif FASE == "INTRO":
        if intro is None:
            intro = Intro()
        PROXIMA_FASE, reiniciar, modo, personagem = intro.atualizar(reiniciar)
        if PROXIMA_FASE != "INTRO":
            intro = None
            FASE = PROXIMA_FASE

    elif FASE == "GAME":
        if minigame is None:
            minigame = Minigame(personagem)
        PROXIMA_FASE, reiniciar = minigame.atualizar(reiniciar)
        if PROXIMA_FASE != "GAME":
            minigame = None
            FASE = PROXIMA_FASE

    elif FASE == "GAME_SRS":
        if minigame_srs is None:
            minigame_srs = MinigameSRS(personagem)
        PROXIMA_FASE, reiniciar, idioma = minigame_srs.atualizar(reiniciar)
        if PROXIMA_FASE != "GAME_SRS":
            minigame_srs = None
            FASE = PROXIMA_FASE

    elif FASE == "JOGO_SRS":
        if jogo_srs is None:
            jogo_srs = JogoSantaRita(idioma, dados_jogador["nome"])
        PROXIMA_FASE, reiniciar, salvarBD, acertos, erros = jogo_srs.atualizar(reiniciar, salvarBD)
        if PROXIMA_FASE != "JOGO_SRS":
            if acertos and erros: #se não retornou None grava os acertos e erros
                dados_jogador["acertos"] = acertos
                dados_jogador["erros"] = erros
            jogo_srs = None
            FASE = PROXIMA_FASE

    elif FASE == "FASE1":
        if fase1 is None:
            fase1 = Fase1()
        if not tempo_iniciado:
            tempo_restante = 250
            pygame.time.set_timer(EVENTO_CRONOMETRO, 1000)
            tempo_iniciado = True
        PROXIMA_FASE, reiniciar, regioes_erradas, regioes_jogadas, acertos, erros = fase1.atualizar(tempo_restante, reiniciar)
        if musica_play:
            trocar_musica("assets/AUDIOS/musicaGame.mp3")
            musica_play = False

        if PROXIMA_FASE != "FASE1":
            if acertos and erros: #se não retornou None grava os acertos e erros
                dados_jogador["acertos"] = acertos 
                dados_jogador["erros"] = erros
            fase1 = None
            FASE = PROXIMA_FASE

    elif FASE == "FASE2":
        if fase2 is None:
            fase2 = Fase2(regioes_erradas, regioes_jogadas)
        PROXIMA_FASE, salvarBD, reiniciar, acertos, erros = fase2.atualizar(tempo_restante, salvarBD, reiniciar, dados_jogador["nome"])
        if PROXIMA_FASE != "FASE2": #se não retornou None implementa os acertos e erros
            if acertos and erros:
                dados_jogador["acertos"] += acertos
                dados_jogador["erros"] += erros
            fase2 = None
            FASE = PROXIMA_FASE

    elif FASE == "FINAL":
        if final is None:
            final = Final(dados_jogador)
        tempo_iniciado = False
        PROXIMA_FASE, reiniciar = final.atualizar(salvarBD, reiniciar)
        if PROXIMA_FASE != "FINAL":
            final = None
            FASE = PROXIMA_FASE

    #DESENHAR NA TELA
    if FASE == "MENU" and menu is not None:
        menu.desenhar(tela)
    elif FASE == "INTRO" and intro is not None:
        intro.desenhar(tela)
    elif FASE == "GAME" and minigame is not None:
        minigame.desenhar(tela)
    elif FASE == "GAME_SRS" and minigame_srs is not None:
        minigame_srs.desenhar(tela)
    elif FASE == "JOGO_SRS" and jogo_srs is not None:
        jogo_srs.desenhar(tela)
    elif FASE == "FASE1" and fase1 is not None:
        fase1.desenhar(tela)
    elif FASE == "FASE2" and fase2 is not None:
        fase2.desenhar(tela)
    elif FASE == "FINAL" and final is not None:
        final.desenhar(tela)

    tela.blit(botao_fechar_img, botao_fechar_rect)
    if mutado:
        tela.blit(botao_mutado, botao_som_rect)
    else:
        tela.blit(botao_som, botao_som_rect)

    # POP-UP DE CONFIRMAÇÃO DE SAÍDA
    if show_janela_sair:
        tela.blit(janela_sair, janela_sair_rect)
        tela.blit(botao_sair, botao_sair_rect)
        tela.blit(botao_continuar, botao_continuar_rect)

    # RELÓGIO DA PARTIDA
    if tempo_iniciado:
        minutos = tempo_restante // 60
        segundos = tempo_restante % 60
        texto_relogio = f"{minutos:02d}:{segundos:02d}"
        texto_relogio_renderizado = config.fonte_input.render(texto_relogio, True, config.bege)
        tela.blit(texto_relogio_renderizado, (config.largura - 90, 10))

    relogio.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()