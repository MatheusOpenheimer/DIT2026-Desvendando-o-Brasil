import pygame
import config
import estados
from sprite import Personagem
import funcoes
import os


class Minigame:

    def __init__(self, personagem_selected):
        self.curiosidades_estados = funcoes.carregar_curiosidades_txt(os.path.join("dados", "curiosidades.txt"))

        # Carrega e ajusta o tamanho da imagem de fundo para a resolução do jogo
        self.fundo_img = pygame.image.load(funcoes.resource_path("assets/IMAGENS/fundo_game.png")).convert_alpha()
        self.fundo_img = pygame.transform.scale(self.fundo_img, (config.largura, config.altura))
        # INTRO ----------------------------------------------------------------
        self.intro_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/minigame.png")), (600, 400))
        self.intro_rect = self.intro_img.get_rect(centerx=config.centroX, centery=-300)

        self.intro_estado = "ENTRANDO"
        self.alvo_y = config.altura // 2
        self.tempo_inicio_espera = 0
        self.duracao_espera = 1000
        # MAPA----------------------------------
        self.mapa = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/brasil_verde.png")), (900, 900))
        self.mapa_rect = self.mapa.get_rect(centerx=config.centroX, centery=(config.altura // 2) + 20)
        # ------------------------------------------------------------------------------------
        self.botao_reiniciar = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_reiniciar.png")),(50, 50))
        self.botao_reiniciar_rect = self.botao_reiniciar.get_rect(x=114, y=2)

        self.fonte_pequena = pygame.font.SysFont("Franklin Gothic Medium", 13)

        self.blocos_estados = []
        self.criar_mapa_estados_quadrado()

        self.todas_sprites = pygame.sprite.Group()
        self.personagem = Personagem(personagem_selected)
        self.personagem.rect.right = self.mapa_rect.left - 10
        self.personagem.rect.centery = config.altura // 2
        self.todas_sprites.add(self.personagem)

        self.botao_skip = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/skip.png")), (150, 54))
        self.botao_skip_rect = self.botao_skip.get_rect(x=config.largura - 290, y=config.altura - 70)

        self.janela_skip = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/skip_pop.png")), (400, 400))
        self.janela_skip_rect = self.janela_skip.get_rect(centerx=config.centroX, centery=config.altura // 2)
        self.botao_sair = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/pular.png")), (155, 80))
        self.botao_sair_rect = self.botao_sair.get_rect(centerx=config.centroX - 85, y=self.janela_skip_rect.y + 250)
        self.botao_continuar = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_continuar.png")), (155, 80))
        self.botao_continuar_rect = self.botao_continuar.get_rect(centerx=config.centroX + 85, y=self.botao_sair_rect.y)

        self.estado_atual_colisao = None
        self.popup_fechado_espaco = False
        self.confirmacao_fase1 = False
        self.mudar_fase = False
        self.clicou_ficar = False
        self.reiniciar = False

    def criar_mapa_estados_quadrado(self):
        largura_img, altura_img = 50, 40

        posicoes = {
            "Acre":                 (62, 190),
            "Alagoas":              (465, 205),
            "Amapá":                (281, 52),
            "Amazonas":             (137, 137),
            "Bahia":                (395, 235),
            "Ceará":                (435, 138),
            "Distrito Federal":     (320, 260),
            "Espírito Santo":       (405, 325),
            "Goiás":                (295, 280),
            "Maranhão":             (355, 145),
            "Mato Grosso":          (235, 240),
            "Mato Grosso do Sul":   (245, 320),
            "Minas Gerais":         (355, 295),
            "Pará":                 (270, 125),
            "Paraíba":              (485, 174),
            "Paraná":               (280, 375),
            "Pernambuco":           (430, 182),
            "Piauí":                (370, 175),
            "Rio de Janeiro":       (380, 350),
            "Rio Grande do Norte":  (465, 150),
            "Rio Grande do Sul":    (260, 430),
            "Rondônia":             (155, 200),
            "Roraima":              (175, 58),
            "Santa Catarina":       (295, 405),
            "São Paulo":            (310, 340),
            "Sergipe":              (465, 215),
            "Tocantins":            (320, 200)
        }

        deslocamentos_x = {
            "Paraíba": 50,
            "Sergipe": 60
        }

        escala = 900 / 500

        for nome_estado, caminho_img in estados.caminhos_mapas.items():

            imagem = pygame.image.load(funcoes.resource_path(caminho_img)).convert_alpha()

            imagem_escalada = pygame.transform.scale(imagem,(largura_img, altura_img))

            # Posição do estado dentro do self.mapa
            x_mapa, y_mapa = posicoes[nome_estado]

            origem_x = self.mapa_rect.x + int(x_mapa * escala)
            origem_y = self.mapa_rect.y + int(y_mapa * escala)

            deslocamento = deslocamentos_x.get(nome_estado, 0)
            x = origem_x - largura_img // 2 + deslocamento
            y = origem_y - altura_img // 2

            rect = imagem_escalada.get_rect(topleft=(x, y))

            # Mantém a posição do estado intocada e recua o ponto inicial da linha em 10px
            ponto_origem = (origem_x - 10, origem_y) if deslocamento != 0 else None

            self.blocos_estados.append({
                "nome": nome_estado,
                "img": imagem_escalada,
                "rect": rect,
                "ponto_origem": ponto_origem
            })

    def gerenciar_eventos(self, evento):

        if self.personagem.rect.colliderect(self.botao_skip_rect):
            if not self.clicou_ficar:
                self.confirmacao_fase1 = True #mostra pop se ele subir no botão e não tiver clicado em ficar
        else:
            self.clicou_ficar = False #deixa o botão ficar como não clicado
            self.confirmacao_fase1 = False #o pop-up não aparece se ele sair de cima do botão
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_mouse = evento.pos
            if self.botao_sair_rect.collidepoint(pos_mouse):
                self.mudar_fase = True
            elif self.botao_continuar_rect.collidepoint(pos_mouse):
                self.clicou_ficar = True #Não mostra o pop-up mesmo o personagem estando em cima do botao
                self.confirmacao_fase1 = False #esconde pop-up
            elif self.botao_reiniciar_rect.collidepoint(pos_mouse):
                self.reiniciar = True

        # Fecha o pop-up ao pressionar ESPAÇO
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if self.estado_atual_colisao is not None:
                    self.popup_fechado_espaco = True

    def atualizar(self, reiniciar):

        if self.reiniciar:
            reiniciar = True
            return "MENU", reiniciar
        
        teclas = pygame.key.get_pressed()
        self.personagem.mover(teclas)
        self.todas_sprites.update()

        # Ponto central do personagem para colisão precisa em cima do estado
        ponto_centro_personagem = self.personagem.rect.center

        estado_encontrado = None
        for estado in self.blocos_estados:
            if estado["rect"].collidepoint(ponto_centro_personagem):
                estado_encontrado = estado["nome"]
                break

        # Se mudou de estado ou saiu de cima de um estado, reseta a trava do ESPAÇO
        if estado_encontrado != self.estado_atual_colisao:
            self.popup_fechado_espaco = False

        self.estado_atual_colisao = estado_encontrado

        if self.mudar_fase:
            return "FASE1", reiniciar

        return "GAME", reiniciar

    def desenhar(self, tela):
        tela.blit(self.fundo_img, (0, 0))
        tela.blit(self.mapa, self.mapa_rect)
        tela.blit(self.botao_reiniciar, self.botao_reiniciar_rect)

        # Linhas brancas começando 10px mais para a esquerda e finalizando no centro atual do estado
        for estado in self.blocos_estados:
            if estado["ponto_origem"]:
                pygame.draw.line(tela, (255, 255, 255), estado["ponto_origem"], estado["rect"].center, 2)
                pygame.draw.circle(tela, (255, 255, 255), estado["ponto_origem"], 3)

        # Desenha o mapa de estados
        for estado in self.blocos_estados:
            if self.estado_atual_colisao == estado["nome"] and not self.popup_fechado_espaco:
                pygame.draw.rect(tela, config.amarelo, estado["rect"].inflate(6, 6), width=3, border_radius=4)

            tela.blit(estado["img"], estado["rect"])
            texto = self.fonte_pequena.render(estado["nome"], True, config.preto)
            texto_rect = texto.get_rect(centerx=estado["rect"].centerx, top=estado["rect"].bottom + 2)
            #tela.blit(texto, texto_rect) #nome do estado

        tela.blit(self.botao_skip, self.botao_skip_rect)

        self.todas_sprites.draw(tela)
        if self.estado_atual_colisao and not self.popup_fechado_espaco:
            self.desenhar_popup(tela)

        if self.confirmacao_fase1:
            tela.blit(self.janela_skip, self.janela_skip_rect)
            tela.blit(self.botao_sair, self.botao_sair_rect)
            tela.blit(self.botao_continuar, self.botao_continuar_rect)

        if self.intro_estado != "FIM":
            self.intro_estado, self.tempo_inicio_espera = funcoes.animacao(
                self.intro_estado, self.intro_rect, self.alvo_y, self.duracao_espera, self.tempo_inicio_espera
            )
            tela.blit(self.intro_img, self.intro_rect)

    def desenhar_popup(self, tela):
        # Pop-up centralizado na tela
        popup_rect = pygame.Rect(0, 0, 920, 800)
        popup_rect.center = (config.largura // 2, config.altura // 2)

        pygame.draw.rect(tela, config.bege, popup_rect, border_radius=15)
        pygame.draw.rect(tela, config.amarelo, popup_rect, width=4, border_radius=15)
        titulo = config.fonte_dicas.render(f"Estado: {self.estado_atual_colisao}", True, config.preto)

        tela.blit(titulo, (popup_rect.x + 20, popup_rect.y + 20))
        
        texto_curiosidade = self.curiosidades_estados.get(self.estado_atual_colisao, "Curiosidade não encontrada.")
        largura_maxima = popup_rect.width - 40
        linhas = funcoes.formatar_texto_largura(texto_curiosidade, config.fonte_dicas, largura_maxima)

        pos_y_linha = popup_rect.y + 55
        for i in range(len(linhas)):
            linha_renderizada = config.fonte_dicas.render(linhas[i], True, config.preto)
            tela.blit(linha_renderizada, (popup_rect.x + 20, pos_y_linha))
            pos_y_linha += 22

        instrucao = config.fonte_dicas.render("Pressione [ESPAÇO] para fechar", True, (140, 40, 30))
        tela.blit(instrucao, (popup_rect.centerx - (instrucao.get_width() // 2), popup_rect.bottom - 22))