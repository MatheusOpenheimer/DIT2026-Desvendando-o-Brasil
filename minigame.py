import os
import pygame
import config
import funcoes
from sprite import Personagem


class Minigame:
    def __init__(self, personagem_selected):
        self.curiosidades_estados = funcoes.carregar_curiosidades_txt(os.path.join("dados", "curiosidades.txt"))

        # Carrega e ajusta o tamanho da imagem de fundo
        self.fundo_img = pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/fundo_game.png")).convert_alpha()
        self.fundo_img = pygame.transform.scale(self.fundo_img, (config.largura, config.altura))

        # INTRO ----------------------------------------------------------------
        self.intro_img = pygame.transform.scale(pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/minigame.png")), (600, 400))
        self.intro_rect = self.intro_img.get_rect(centerx=config.centroX, centery=-300)

        self.intro_estado = "ENTRANDO"
        self.alvo_y = config.altura // 2
        self.tempo_inicio_espera = 0
        self.duracao_espera = 1000

        # MAPA VISÍVEL (TELA) --------------------------------------------------
        self.mapa = pygame.transform.scale(pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/mapaTelaRegiao.png")), (900, 900))
        self.mapa_rect = self.mapa.get_rect(centerx=config.centroX, centery=(config.altura // 2) + 20)

        # MAPA DE COLISÃO INVISÍVEL --------------------------------------------
        caminho_mapa_colisao = funcoes.obter_caminho_arquivo("assets/IMAGENS/mapaEstado.png")
        self.mapa_colisao = pygame.transform.scale(pygame.image.load(caminho_mapa_colisao), (900, 900))

        self.fonte_siglas = pygame.font.SysFont("Franklin Gothic Medium", 13, bold=True)
        self.fonte_oceanos = pygame.font.SysFont("Franklin Gothic Medium", 16, bold=True)

        # Prepara a lista de siglas
        self.marcadores_siglas = []
        self.criar_marcadores_siglas()

        # PERSONAGEM -----------------------------------------------------------
        self.todas_sprites = pygame.sprite.Group()
        self.personagem = Personagem(personagem_selected)
        self.personagem.rect.right = self.mapa_rect.left - 10
        self.personagem.rect.centery = config.altura // 2
        self.todas_sprites.add(self.personagem)

        # BOTÃO PULAR (Canto Superior Direito) ---------------------------------
        self.botao_skip = pygame.transform.scale(pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/skip.png")), (150, 54))
        self.botao_skip_rect = self.botao_skip.get_rect(topright=(config.largura - 15, 10))

        self.janela_skip = pygame.transform.scale(pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/skip_pop.png")), (400, 400))
        self.janela_skip_rect = self.janela_skip.get_rect(centerx=config.centroX, centery=config.altura // 2)
        self.botao_sair = pygame.transform.scale(pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/pular.png")), (155, 80))
        self.botao_sair_rect = self.botao_sair.get_rect(centerx=config.centroX - 85, y=self.janela_skip_rect.y + 250)
        self.botao_continuar = pygame.transform.scale(pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/botao_continuar.png")), (155, 80))
        self.botao_continuar_rect = self.botao_continuar.get_rect(centerx=config.centroX + 85, y=self.botao_sair_rect.y)

        # CONTROLE DE ESTADOS
        self.estado_atual_colisao = None
        self.popup_fechado_espaco = False
        self.confirmacao_fase1 = False
        self.mudar_fase = False
        self.clicou_ficar = False
        self.confirmacao_fase1_por_clique = False

    def criar_marcadores_siglas(self):
        siglas = {
            "Acre": "AC", "Alagoas": "AL", "Amapá": "AP", "Amazonas": "AM",
            "Bahia": "BA", "Ceará": "CE", "Distrito Federal": "DF",
            "Espírito Santo": "ES", "Goiás": "GO", "Maranhão": "MA",
            "Mato Grosso": "MT", "Mato Grosso do Sul": "MS", "Minas Gerais": "MG",
            "Pará": "PA", "Paraíba": "PB", "Paraná": "PR", "Pernambuco": "PE",
            "Piauí": "PI", "Rio de Janeiro": "RJ", "Rio Grande do Norte": "RN",
            "Rio Grande do Sul": "RS", "Rondônia": "RO", "Roraima": "RR",
            "Santa Catarina": "SC", "São Paulo": "SP", "Sergipe": "SE", "Tocantins": "TO"
        }

        posicoes = {
            "Acre": (62, 190), "Alagoas": (465, 200), "Amapá": (281, 52),
            "Amazonas": (137, 137), "Bahia": (395, 235), "Ceará": (435, 138),
            "Distrito Federal": (326, 265), "Espírito Santo": (405, 325),
            "Goiás": (295, 280), "Maranhão": (355, 145), "Mato Grosso": (235, 240),
            "Mato Grosso do Sul": (245, 320), "Minas Gerais": (355, 295),
            "Pará": (270, 125), "Paraíba": (485, 174), "Paraná": (280, 375),
            "Pernambuco": (430, 182), "Piauí": (395, 165), "Rio de Janeiro": (380, 350),
            "Rio Grande do Norte": (465, 150), "Rio Grande do Sul": (260, 430),
            "Rondônia": (155, 200), "Roraima": (175, 58), "Santa Catarina": (295, 415),
            "São Paulo": (310, 340), "Sergipe": (465, 215), "Tocantins": (320, 200)
        }

        deslocamentos_x = {
            "Paraíba": 50,
            "Sergipe": 60
        }

        escala = 900 / 500

        for nome_estado, (x_mapa, y_mapa) in posicoes.items():
            origem_x = self.mapa_rect.x + int(x_mapa * escala)
            origem_y = self.mapa_rect.y + int(y_mapa * escala)
            deslocamento = deslocamentos_x.get(nome_estado, 0)
            
            pos_x = origem_x + deslocamento
            pos_y = origem_y

            ponto_origem = (origem_x - 10, origem_y) if deslocamento != 0 else None

            self.marcadores_siglas.append({
                "nome": nome_estado,
                "sigla": siglas.get(nome_estado, ""),
                "pos": (pos_x, pos_y),
                "ponto_origem": ponto_origem
            })

    def gerenciar_eventos(self, evento):
        # Mostra o pop-up caso o personagem passe por cima do botão pular
        if self.personagem.rect.colliderect(self.botao_skip_rect):
            if not self.clicou_ficar:
                self.confirmacao_fase1 = True
        else:
            self.clicou_ficar = False
            if not self.confirmacao_fase1_por_clique:
                self.confirmacao_fase1 = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_mouse = evento.pos

            # Clique direto no botão pular
            if self.botao_skip_rect.collidepoint(pos_mouse):
                self.confirmacao_fase1 = True
                self.confirmacao_fase1_por_clique = True
            elif self.botao_sair_rect.collidepoint(pos_mouse) and self.confirmacao_fase1:
                self.mudar_fase = True
            elif self.botao_continuar_rect.collidepoint(pos_mouse) and self.confirmacao_fase1:
                self.clicou_ficar = True
                self.confirmacao_fase1 = False
                self.confirmacao_fase1_por_clique = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if self.estado_atual_colisao is not None:
                    self.popup_fechado_espaco = True

    def atualizar(self):
        teclas = pygame.key.get_pressed()
        self.personagem.mover(teclas)
        self.todas_sprites.update()

        # Detecção de colisão via Mapa de Cores Invisível
        pes_x = self.personagem.rect.centerx
        pes_y = self.personagem.rect.bottom - 4

        estado_encontrado = None

        if self.mapa_rect.collidepoint(pes_x, pes_y):
            pixel_x = pes_x - self.mapa_rect.x
            pixel_y = pes_y - self.mapa_rect.y

            cor_pixel = self.mapa_colisao.get_at((pixel_x, pixel_y))
            rgb = (cor_pixel.r, cor_pixel.g, cor_pixel.b)

            estado_encontrado = funcoes.obter_estado_por_cor(rgb)

        if estado_encontrado != self.estado_atual_colisao:
            self.popup_fechado_espaco = False

        self.estado_atual_colisao = estado_encontrado

        if self.mudar_fase:
            return "FASE1"

        return "GAME"

    def desenhar(self, tela):
        tela.blit(self.fundo_img, (0, 0))
        tela.blit(self.mapa, self.mapa_rect)

        # TEXTOS DOS OCEANOS ---------------------------------------------------
        centery_tela = config.altura // 2

        # Oceano Atlântico
        texto_atlantico = self.fonte_oceanos.render("Oceano Atlântico", True, config.preto)
        rect_atlantico = texto_atlantico.get_rect(left=self.mapa_rect.right + 20, centery=centery_tela)
        tela.blit(texto_atlantico, rect_atlantico)

        # Oceano Pacífico
        texto_pacifico = self.fonte_oceanos.render("Oceano Pacífico", True, config.preto)
        rect_pacifico = texto_pacifico.get_rect(right=self.mapa_rect.left - 100, centery=centery_tela)
        tela.blit(texto_pacifico, rect_pacifico)

        # Linhas guia para estados menores
        for marcador in self.marcadores_siglas:
            if marcador["ponto_origem"]:
                pygame.draw.line(tela, (255, 255, 255), marcador["ponto_origem"], marcador["pos"], 2)
                pygame.draw.circle(tela, (255, 255, 255), marcador["ponto_origem"], 3)

        # Desenha as siglas no mapa
        for marcador in self.marcadores_siglas:
            pos_x, pos_y = marcador["pos"]
            
            if self.estado_atual_colisao == marcador["nome"]:
                cor_fundo = config.amarelo
                cor_borda = (50, 30, 15)
                cor_texto = config.preto
            else:
                cor_fundo = (35, 35, 40)
                cor_borda = (240, 240, 240)
                cor_texto = config.branco

            tag_rect = pygame.Rect(0, 0, 26, 18)
            tag_rect.center = (pos_x, pos_y)

            pygame.draw.rect(tela, cor_fundo, tag_rect, border_radius=4)
            pygame.draw.rect(tela, cor_borda, tag_rect, width=1, border_radius=4)

            texto_sigla = self.fonte_siglas.render(marcador["sigla"], True, cor_texto)
            tela.blit(texto_sigla, texto_sigla.get_rect(center=tag_rect.center))

        # Botão Pular Minigame
        tela.blit(self.botao_skip, self.botao_skip_rect)

        # Personagem
        self.todas_sprites.draw(tela)

        # Pop-up de Curiosidade
        if self.estado_atual_colisao and not self.popup_fechado_espaco:
            self.desenhar_popup(tela)

        # Pop-up de confirmação de pulo
        if self.confirmacao_fase1:
            tela.blit(self.janela_skip, self.janela_skip_rect)
            tela.blit(self.botao_sair, self.botao_sair_rect)
            tela.blit(self.botao_continuar, self.botao_continuar_rect)

        # Animação inicial
        if self.intro_estado != "FIM":
            self.intro_estado, self.tempo_inicio_espera = funcoes.animacao(
                self.intro_estado, self.intro_rect, self.alvo_y, self.duracao_espera, self.tempo_inicio_espera
            )
            tela.blit(self.intro_img, self.intro_rect)

    def desenhar_popup(self, tela):
        popup_rect = pygame.Rect(0, 0, 800, 650)
        popup_rect.center = (config.largura // 2, config.altura // 2)

        pygame.draw.rect(tela, config.bege, popup_rect, border_radius=15)
        pygame.draw.rect(tela, config.amarelo, popup_rect, width=4, border_radius=15)

        titulo = config.fonte_dicas.render(f"Estado: {self.estado_atual_colisao}", True, config.preto)
        tela.blit(titulo, (popup_rect.x + 25, popup_rect.y + 20))

        texto_curiosidade = self.curiosidades_estados.get(self.estado_atual_colisao, "Curiosidade não encontrada.")
        largura_maxima = popup_rect.width - 50
        linhas = funcoes.formatar_texto_largura(texto_curiosidade, config.fonte_dicas, largura_maxima)

        pos_y_linha = popup_rect.y + 60
        for linha in linhas:
            linha_renderizada = config.fonte_dicas.render(linha, True, config.preto)
            tela.blit(linha_renderizada, (popup_rect.x + 25, pos_y_linha))
            pos_y_linha += 22

        instrucao = config.fonte_dicas.render("Pressione [ESPAÇO] para fechar", True, (140, 40, 30))
        tela.blit(instrucao, (popup_rect.centerx - (instrucao.get_width() // 2), popup_rect.bottom - 26))