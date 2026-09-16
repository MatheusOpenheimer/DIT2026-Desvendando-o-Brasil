import copy
import banco
import random
import config
import funcoes
import pygame
import os
from srs_ponto_turistico import criar_pontos_santa_rita

def obter_nome_ponto_minusculo(ponto):
    return ponto.nome.lower()

class JogoSantaRita:
    def __init__(self, modo, nome_jogador):
        self.nome_jogador = nome_jogador

        self.fundo_img = pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS_SRS/img_morro.png")).convert_alpha()
        self.fundo_img = pygame.transform.scale(self.fundo_img, (config.largura, config.altura))
        
        self.modo = modo
        self.estado = "QUIZ"

        # PONTOS TURÍSTICOS -----------------------------------------------
        self.pontos, _, _, _ = criar_pontos_santa_rita(self.modo)

        # BANCO DE PERGUNTAS ----------------------------------------------
        if self.modo == "en":
            arquivo_perguntas = "srs_perguntas_en.txt"
        elif self.modo == "esp":
            arquivo_perguntas = "srs_perguntas_esp.txt"
        else:
            arquivo_perguntas = "srs_perguntas.txt"

        caminho_perguntas = os.path.join("dados", arquivo_perguntas)
        banco_carregado = funcoes.carregar_questoes_txt(caminho_perguntas)
        lista_questoes = banco_carregado.get("SRS", [])
        
        self.perguntas_disponiveis = copy.deepcopy(lista_questoes)
        random.shuffle(self.perguntas_disponiveis)
        self.perguntas_disponiveis = self.perguntas_disponiveis[:15]

        self.total_questoes = len(self.perguntas_disponiveis)

        # PRIMEIRA PERGUNTA -----------------------------------------------
        if len(self.perguntas_disponiveis) > 0:
            self.questao_atual = self.perguntas_disponiveis.pop(0)
            self.perg_sorteada = self.questao_atual["pergunta"]
            self.alternativas_sorteadas = self.questao_atual["opcoes"]
        else:
            self.questao_atual = None
            self.perg_sorteada = ""
            self.alternativas_sorteadas = []

        # Armazena os feedbacks dados APENAS na partida atual
        self.feedbacks_sessao = {}

        # BLOCO DE PERGUNTAS ----------------------------------------------
        self.bloco_perguntas = pygame.Rect(config.centroX - 380, 50, 760, 600)

        # BOTÕES DE ALTERNATIVAS
        self.botoes_alternativas = []
        for i in range(4):
            rect_opcao = pygame.Rect(self.bloco_perguntas.x + 30, self.bloco_perguntas.y + 195 + (i * 72), 700, 58)
            self.botoes_alternativas.append(rect_opcao)

        # FEEDBACK VISUAL DE ACERTO / ERRO --------------------------------
        self.Errou_img = pygame.transform.scale(pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/Errou.png")), (200, 200))
        self.Errou_rect = self.Errou_img.get_rect(centerx=config.centroX, centery=config.altura / 2)
        
        self.Acerto_img = pygame.transform.scale(pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/Acertou.png")), (200, 200))
        self.Acerto_rect = self.Acerto_img.get_rect(centerx=config.centroX, centery=config.altura / 2)

        self.erro_sound = pygame.mixer.Sound(funcoes.obter_caminho_arquivo("assets/AUDIOS/error_som.mp3"))
        self.erro_sound.set_volume(1.0)

        self.acerto_sound = pygame.mixer.Sound(funcoes.obter_caminho_arquivo("assets/AUDIOS/acerto.mp3"))
        self.acerto_sound.set_volume(1.0)

        # CONTROLE DE ESTADOS ---------------------------------------------
        self.Errou_status = False
        self.Acerto_status = False
        self.mostrar_feedback_cores = False
        self.opcao_selecionada = None
        self.SUMIR_STATUS_EVENTO = pygame.USEREVENT + 4
        self.ler_clique = True
        self.finalizar = False

        self.contAcertos = 0
        self.contErros = 0
        self.num_questao = 1

        # FEEDBACK / BANCO ------------------------------------------------
        self.ponto_selecionado = None
        self.texto_feedback = ""
        self.scroll_y = 0

        self.botao_finalizar_rect = pygame.Rect(config.largura - 180, config.altura - 55, 150, 45)
        self.botao_salvar_fb_rect = pygame.Rect(config.centroX + 20, config.altura // 2 + 130, 140, 40)
        self.botao_cancelar_fb_rect = pygame.Rect(config.centroX - 160, config.altura // 2 + 130, 140, 40)

    def salvar_feedback_banco(self, ponto_nome, texto):
        self.feedbacks_sessao[ponto_nome] = texto
        # Salva utilizando a variável do jogador local da instância
        banco.salvar_feedback_srs(self.nome_jogador, ponto_nome, texto)

    def verificar_resposta(self, indice_clicado):
        self.opcao_selecionada = indice_clicado
        self.mostrar_feedback_cores = True

        if indice_clicado == self.questao_atual["correta"]:
            self.acerto_sound.play()
            self.Acerto_status = True
            self.contAcertos += 1
        else:
            self.erro_sound.play()
            self.Errou_status = True
            self.contErros += 1

        pygame.time.set_timer(self.SUMIR_STATUS_EVENTO, 800, loops=1)

    def gerenciar_eventos(self, evento):
        pos_mouse = pygame.mouse.get_pos()

        if evento.type == self.SUMIR_STATUS_EVENTO:
            self.Errou_status = False
            self.Acerto_status = False
            self.mostrar_feedback_cores = False
            self.opcao_selecionada = None
            self.ler_clique = True

            if len(self.perguntas_disponiveis) > 0:
                self.questao_atual = self.perguntas_disponiveis.pop(0)
                self.perg_sorteada = self.questao_atual["pergunta"]
                self.alternativas_sorteadas = self.questao_atual["opcoes"]
                self.num_questao += 1
            else:
                self.estado = "SELECAO_PONTO"

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if self.estado == "QUIZ" and self.ler_clique:
                    for i in range(len(self.botoes_alternativas)):
                        if self.botoes_alternativas[i].collidepoint(pos_mouse):
                            self.ler_clique = False
                            self.verificar_resposta(i)
                            break

                elif self.estado == "SELECAO_PONTO":
                    if self.botao_finalizar_rect.collidepoint(pos_mouse):
                        self.finalizar = True

                    y_item = 80 + self.scroll_y
                    for ponto in sorted(self.pontos, key=obter_nome_ponto_minusculo):
                        item_rect = pygame.Rect(40, y_item, config.largura - 80, 56)
                        if item_rect.top >= 75 and item_rect.bottom <= config.altura - 60:
                            if item_rect.collidepoint(pos_mouse):
                                self.ponto_selecionado = ponto
                                self.texto_feedback = self.feedbacks_sessao.get(ponto.nome, "")
                                self.estado = "FEEDBACK_POPUP"
                                break
                        y_item += 66

                elif self.estado == "FEEDBACK_POPUP":
                    if self.botao_salvar_fb_rect.collidepoint(pos_mouse):
                        if self.texto_feedback.strip() != "":
                            self.salvar_feedback_banco(self.ponto_selecionado.nome, self.texto_feedback.strip())
                        self.estado = "SELECAO_PONTO"

                    if self.botao_cancelar_fb_rect.collidepoint(pos_mouse):
                        self.estado = "SELECAO_PONTO"

            # Rolagem da lista de pontos turísticos
            elif evento.button == 4 and self.estado == "SELECAO_PONTO":
                if self.scroll_y < 0:
                    self.scroll_y = min(0, self.scroll_y + 35)
            elif evento.button == 5 and self.estado == "SELECAO_PONTO":
                limite_scroll = -max(0, (len(self.pontos) * 66) - (config.altura - 160))
                if self.scroll_y > limite_scroll:
                    self.scroll_y = max(limite_scroll, self.scroll_y - 35)

        if self.estado == "FEEDBACK_POPUP" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                self.texto_feedback = self.texto_feedback[:-1]
            elif evento.key == pygame.K_ESCAPE:
                self.estado = "SELECAO_PONTO"
            elif evento.key == pygame.K_RETURN:
                self.texto_feedback += " "
            else:
                if len(self.texto_feedback) < 250 and evento.unicode.isprintable():
                    self.texto_feedback += evento.unicode

    def atualizar(self, salvarBD):
        
        if self.finalizar:
            acertos = self.contAcertos
            erros = self.contErros
            salvarBD = "SRS"
            return "FINAL", salvarBD, acertos, erros
        
        return "JOGO_SRS", salvarBD, None, None

    def desenhar(self, tela):
        tela.blit(self.fundo_img, (0, 0))
        pos_mouse = pygame.mouse.get_pos()

        # DICIONÁRIO DE IDIOMA (utiliza self.nome_jogador local)
        textos_interface = {
            "pt": {
                "questao": f"Questão {self.num_questao} de {self.total_questoes}",
                "placar": f"Acertos: {self.contAcertos} | Erros: {self.contErros}",
                "titulo_pontos": "Pontos Turísticos de Santa Rita do Sapucaí",
                "sub_pontos": "Clique em um ponto turístico para registrar seu feedback:",
                "finalizar": "Finalizar",
                "fb_feito": "Feedback registrado",
                "fb_pendente": "Clique para avaliar este local",
                "avaliacao_de": f"Avaliação de {self.nome_jogador}:",
                "salvar": "Salvar",
                "cancelar": "Cancelar"
            },
            "en": {
                "questao": f"Question {self.num_questao} of {self.total_questoes}",
                "placar": f"Correct: {self.contAcertos} | Wrong: {self.contErros}",
                "titulo_pontos": "Tourist Attractions of Santa Rita do Sapucaí",
                "sub_pontos": "Click on a tourist spot to submit your feedback:",
                "finalizar": "Finish",
                "fb_feito": "Feedback registered",
                "fb_pendente": "Click to review this place",
                "avaliacao_de": f"Review by {self.nome_jogador}:",
                "salvar": "Save",
                "cancelar": "Cancel"
            },
            "esp": {
                "questao": f"Pregunta {self.num_questao} de {self.total_questoes}",
                "placar": f"Aciertos: {self.contAcertos} | Errores: {self.contErros}",
                "titulo_pontos": "Puntos Turísticos de Santa Rita do Sapucaí",
                "sub_pontos": "Haga clic en un punto turístico para registrar su opinión:",
                "finalizar": "Finalizar",
                "fb_feito": "Comentario registrado",
                "fb_pendente": "Haga clic para evaluar este lugar",
                "avaliacao_de": f"Evaluación de {self.nome_jogador}:",
                "salvar": "Guardar",
                "cancelar": "Cancelar"
            }
        }
        ui = textos_interface.get(self.modo, textos_interface["pt"])

        # QUIZ -------------------------------------------------------------
        if self.estado == "QUIZ":
            pygame.draw.rect(tela, config.bege, self.bloco_perguntas, border_radius=12)
            pygame.draw.rect(tela, (50, 30, 15), self.bloco_perguntas, 3, border_radius=12)

            txt_progresso = config.fonte_dicas.render(ui["questao"], False, (50, 30, 15))
            tela.blit(txt_progresso, (self.bloco_perguntas.x + 30, self.bloco_perguntas.y + 20))

            txt_placar = config.fonte_dicas.render(ui["placar"], False, (50, 30, 15))
            tela.blit(txt_placar, (self.bloco_perguntas.right - txt_placar.get_width() - 30, self.bloco_perguntas.y + 20))

            linhas_pergunta = funcoes.formatar_texto_largura(self.perg_sorteada, config.fonte_fases, 680)
            y_texto = self.bloco_perguntas.y + 60
            for linha in linhas_pergunta:
                linha_render = config.fonte_fases.render(linha, False, config.verde)
                linha_rect = linha_render.get_rect()
                linha_rect.centerx = self.bloco_perguntas.centerx
                linha_rect.y = y_texto
                tela.blit(linha_render, linha_rect)
                y_texto += linha_render.get_height() + 5

            letras = ["A", "B", "C", "D"]
            for i in range(len(self.alternativas_sorteadas)):
                btn_rect = self.botoes_alternativas[i]
                
                # Feedback de cores ao responder
                if self.mostrar_feedback_cores:
                    if i == self.questao_atual["correta"]:
                        cor_fundo = (46, 204, 113)
                    elif i == self.opcao_selecionada:
                        cor_fundo = (231, 76, 60)
                    else:
                        cor_fundo = config.azul
                else:
                    cor_fundo = (90, 150, 220) if btn_rect.collidepoint(pos_mouse) else config.azul

                pygame.draw.rect(tela, cor_fundo, btn_rect, border_radius=8)
                pygame.draw.rect(tela, (50, 30, 15), btn_rect, 2, border_radius=8)

                texto_alt = f"{letras[i]})  {self.alternativas_sorteadas[i]}"
                largura_maxima_alt = btn_rect.width - 35
                linhas_alt = funcoes.formatar_texto_largura(texto_alt, config.fonte_dicas, largura_maxima_alt)

                altura_linha = config.fonte_dicas.get_height()
                altura_total_alt = len(linhas_alt) * altura_linha + (len(linhas_alt) - 1) * 3
                pos_y_inicial_alt = btn_rect.centery - (altura_total_alt // 2)

                for j in range(len(linhas_alt)):
                    alt_render = config.fonte_dicas.render(linhas_alt[j], False, (255, 255, 255))
                    tela.blit(alt_render, (btn_rect.x + 18, pos_y_inicial_alt + j * (altura_linha + 3)))

            if self.Errou_status:
                tela.blit(self.Errou_img, self.Errou_rect)
            elif self.Acerto_status:
                tela.blit(self.Acerto_img, self.Acerto_rect)

        # LISTA DE PONTOS TURÍSTICOS ---------------------------------------
        elif self.estado in ("SELECAO_PONTO", "FEEDBACK_POPUP"):
            y_item = 80 + self.scroll_y
            for ponto in sorted(self.pontos, key=obter_nome_ponto_minusculo):
                item_rect = pygame.Rect(40, y_item, config.largura - 80, 56)

                if item_rect.top >= 75 and item_rect.bottom <= config.altura - 60:
                    fb_existe = self.feedbacks_sessao.get(ponto.nome, "") != ""
                    
                    cor_fundo_item = config.bege
                    if fb_existe:
                        cor_fundo_item = (220, 245, 220)
                    if item_rect.collidepoint(pos_mouse):
                        cor_fundo_item = (210, 230, 245)

                    pygame.draw.rect(tela, cor_fundo_item, item_rect, border_radius=8)
                    pygame.draw.rect(tela, (50, 30, 15), item_rect, 2, border_radius=8)

                    txt_nome = config.fonte_dicas.render(ponto.nome, False, (50, 30, 15))
                    tela.blit(txt_nome, (item_rect.x + 20, item_rect.y + 6))

                    msg_status = ui["fb_feito"] if fb_existe else ui["fb_pendente"]
                    cor_status = (40, 140, 40) if fb_existe else (110, 110, 110)
                    txt_st = config.fonte_dicas.render(msg_status, False, cor_status)
                    tela.blit(txt_st, (item_rect.x + 20, item_rect.y + 30))

                y_item += 66

            cabecalho_rect = pygame.Rect(0, 0, config.largura, 76)
            pygame.draw.rect(tela, (79, 148, 77), cabecalho_rect)

            txt_titulo = config.fonte_fases.render(ui["titulo_pontos"], False, (50, 30, 15))
            txt_titulo_rect = txt_titulo.get_rect(centerx=config.centroX, y=14)
            tela.blit(txt_titulo, txt_titulo_rect)

            txt_sub = config.fonte_dicas.render(ui["sub_pontos"], False, (240, 240, 240))
            txt_sub_rect = txt_sub.get_rect(centerx=config.centroX, y=44)
            tela.blit(txt_sub, txt_sub_rect)

            rodape_rect = pygame.Rect(0, config.altura - 60, config.largura, 60)
            pygame.draw.rect(tela, (79, 148, 77), rodape_rect)

            pygame.draw.rect(tela, config.azul, self.botao_finalizar_rect, border_radius=8)
            pygame.draw.rect(tela, (50, 30, 15), self.botao_finalizar_rect, 2, border_radius=8)
            txt_finalizar = config.fonte_dicas.render(ui["finalizar"], False, (255, 255, 255))
            tela.blit(txt_finalizar, txt_finalizar.get_rect(center=self.botao_finalizar_rect.center))

        # POP-UP DE FEEDBACK -----------------------------------------------
        if self.estado == "FEEDBACK_POPUP" and self.ponto_selecionado is not None:
            escurecer = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
            escurecer.fill((0, 0, 0, 160))
            tela.blit(escurecer, (0, 0))

            pop_rect = pygame.Rect(config.centroX - 320, config.altura // 2 - 200, 640, 400)
            pygame.draw.rect(tela, config.bege, pop_rect, border_radius=12)
            pygame.draw.rect(tela, (50, 30, 15), pop_rect, 3, border_radius=12)

            tit_ponto = config.fonte_fases.render(self.ponto_selecionado.nome, False, (50, 30, 15))
            tela.blit(tit_ponto, (pop_rect.x + 25, pop_rect.y + 20))

            sub_inst = config.fonte_dicas.render(ui["avaliacao_de"], False, (80, 80, 80))
            tela.blit(sub_inst, (pop_rect.x + 25, pop_rect.y + 55))

            campo_rect = pygame.Rect(pop_rect.x + 25, pop_rect.y + 85, 590, 200)
            pygame.draw.rect(tela, (255, 255, 255), campo_rect, border_radius=8)
            pygame.draw.rect(tela, (140, 140, 140), campo_rect, 2, border_radius=8)

            linhas_fb = funcoes.formatar_texto_largura(self.texto_feedback + "|", config.fonte_dicas, 560)
            y_fb = campo_rect.y + 12
            for l in linhas_fb[:7]:
                txt_render = config.fonte_dicas.render(l, False, (30, 30, 30))
                tela.blit(txt_render, (campo_rect.x + 12, y_fb))
                y_fb += 24

            pygame.draw.rect(tela, config.verde, self.botao_salvar_fb_rect, border_radius=8)
            pygame.draw.rect(tela, (50, 30, 15), self.botao_salvar_fb_rect, 2, border_radius=8)
            txt_salvar = config.fonte_dicas.render(ui["salvar"], False, (255, 255, 255))
            tela.blit(txt_salvar, txt_salvar.get_rect(center=self.botao_salvar_fb_rect.center))

            pygame.draw.rect(tela, (180, 60, 50), self.botao_cancelar_fb_rect, border_radius=8)
            pygame.draw.rect(tela, (50, 30, 15), self.botao_cancelar_fb_rect, 2, border_radius=8)
            txt_canc = config.fonte_dicas.render(ui["cancelar"], False, (255, 255, 255))
            tela.blit(txt_canc, txt_canc.get_rect(center=self.botao_cancelar_fb_rect.center))