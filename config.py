import pygame
import funcoes

pygame.init()
pygame.font.init()
pygame.mixer.init()

#JANELA
largura = 1600
altura = 900

#CORES
verde = (34, 139, 34)
branco = (255, 255, 255)
bege = (242, 230, 162)
preto = (0, 0, 0)
azul = (0, 0, 255)
amarelo = (255, 200, 0)
vermelho = (255, 0, 0)
green = (10, 255, 30)

ouro = (255, 215, 0)       # Amarelo Ouro Vibrante
prata = (190, 194, 198)   # Prata Metálico Claro
bronze = (205, 127, 50)   # Bronze Quente
padrao = (240, 223, 168)  # para do 4º lugar em diante
verde_pastel = (157, 242, 157)
amarelo_pastel = (250, 226, 105)

#FONTES (Com suporte ao resource_path)
fonte_input = pygame.font.Font(funcoes.resource_path("assets/FONTES/Afonte.ttf"), 16)

fonte_fases_bold = pygame.font.SysFont("Franklin Gothic Medium", 24, bold=True)
fonte_fases = pygame.font.SysFont("Franklin Gothic Medium", 24)
fonte_dicas = pygame.font.SysFont("Franklin Gothic Medium", 18)

fonte_media = pygame.font.SysFont("Franklin Gothic Medium", 20)

fonte_grossa = pygame.font.SysFont("Franklin Gothic Medium", 40, bold=True)

#AUDIOS (Com suporte ao resource_path)
click_sound = pygame.mixer.Sound(funcoes.resource_path("assets/AUDIOS/click.2.ogg"))
click_sound.set_volume(0.9)

#INFORMAÇÕES DO JOGADOR:---------------------
nome_jogador = ""
idade_jogador = 0
acertos_jogador = 0
erros_jogador = 0
tempo_sobra = 0

#------------------------------------------------------
#config dos objetos
config_botao = [0, 0, 250, 100]
tamanho_botao = (255, 100)
posicoes_botao_y = [320, 450, 580]
centroX = largura / 2