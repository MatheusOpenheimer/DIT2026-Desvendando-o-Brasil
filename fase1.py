import copy
import math
import random
import config
import funcoes
import pygame
import os


class Fase1:

  def __init__(self):
    PERGUNTAS_BANCO = funcoes.carregar_questoes_txt(os.path.join("dados", "questoes_regioes.txt"))
    # INICIALIZAÇÃO DO BANCO (Usando copy para não estragar o banco original ao reiniciar) -----
    self.perguntas_disponiveis = copy.deepcopy(PERGUNTAS_BANCO)

    #FUNDO------------------------------------
  # Carrega e ajusta o tamanho da imagem de fundo para a resolução do jogo
    self.fundo_img = pygame.image.load(funcoes.resource_path("assets/IMAGENS/fundo_fase1.png")).convert_alpha()
    self.fundo_img = pygame.transform.scale(self.fundo_img, (config.largura, config.altura))

    # INTRO ----------------------------------------------------------------
    self.intro_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/fase1.png")), (600, 400))
    self.intro_rect = self.intro_img.get_rect(centerx=config.centroX, centery=-300)

    self.intro_estado = "ENTRANDO"
    self.alvo_y = config.altura // 2
    self.tempo_inicio_espera = 0
    self.duracao_espera = 1000
    # ----------------------------------------------------------------------

    # SPAM DE FIM ----------------------------------------------------------
    self.esgotado_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/esgotadoTempo.png")), (500, 500))
    self.esgotado_rect = self.esgotado_img.get_rect(centerx=config.centroX, centery=-300)

    self.esgotado_estado = "ENTRANDO"
    self.alvo_y_esgotado = config.altura // 2
    self.tempo_inicio_espera_esgotado = 0
    self.duracao_espera_esgotado = 650

    self.acabou_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/acabouFase1.png")), (500, 500))
    self.acabou_rect = self.acabou_img.get_rect(centerx=config.centroX, centery=-300)

    self.acabou_estado = "ENTRANDO"
    self.alvo_y_acabou = config.altura // 2
    self.tempo_inicio_espera_acabou = 0
    self.duracao_espera_acabou = 650

    # MAPA -----------------------------------------------------------------
    self.mapa = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/mapaRegião.png")), (800, 800))
    self.mapa_rect = self.mapa.get_rect()
    self.mapa_rect.centerx = 920
    self.mapa_rect.centery = config.altura / 2

    self.mapaTela = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/mapaTelaRegiao.png")), (800, 800))
    self.mapaTela_rect = self.mapa.get_rect()
    self.mapaTela_rect.centerx = 920
    self.mapaTela_rect.centery = config.altura / 2

    # PERGUNTAS ------------------------------------------------------------
        #FASE1
    pos = (30, 200)
    tam = (440, 500)

    self.bloco_perguntas = pygame.Rect(pos, tam)

    # Sortear a primeira pergunta da nova estrutura de dicionários
    if len(self.perguntas_disponiveis) > 0:
      idsorteado = random.randint(0, len(self.perguntas_disponiveis) - 1)
      self.questao_atual = self.perguntas_disponiveis.pop(idsorteado)
      self.perg_sorteada = self.questao_atual["pergunta"]
      self.dica_sorteada = self.questao_atual["dicas"]
    else:
      self.Acabou = True
      self.perg_sorteada = ""
      self.dica_sorteada = ["", "", ""]

    # PERSONAGEM MARCADOR DO MAPA ------------------------------------------
    self.person_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/person1.png")), (30, 50))
    self.person_rect = self.person_img.get_rect()

    # MODO POWER
    self.contador_piscar = 0

    # REINICIAR BOTAO ------------------------------------------------------
    self.botao_reiniciar = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_reiniciar.png")), (50, 50))
    self.botao_reiniciar_rect = self.botao_reiniciar.get_rect(x=114, y=2)

    # SPAM DE ERRO E ACERTO
    self.Errou_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/Errou.png")), (200, 200))
    self.Errou_rect = self.Errou_img.get_rect(centerx=config.centroX, centery=config.altura / 2)
    self.Acerto_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/Acertou.png")), (200, 200))
    self.Acerto_rect = self.Acerto_img.get_rect(centerx=config.centroX, centery=config.altura / 2)

    self.erro_sound = pygame.mixer.Sound(funcoes.resource_path("assets/AUDIOS/error_som.mp3"))
    self.erro_sound.set_volume(1.0)

    self.acerto_sound = pygame.mixer.Sound(funcoes.resource_path("assets/AUDIOS/acerto.mp3"))
    self.acerto_sound.set_volume(1.0)
    # GERENCIADOR DE ESTADOS ------------------------------------------------

    self.acertosSequencia = 0

    self.Errou_status = False
    self.Acerto_status = False

    self.contAcertos = 0
    self.contErros = 0
    self.regioes_erradas = { #começa com zero erros
        "Norte": 0,
        "Nordeste": 0,
        "Centro-Oeste": 0,
        "Sudeste": 0,
        "Sul": 0,
    }

    self.contagem_regioes = {#começa com 0 regioes jogadas
      "Norte": 0,
      "Nordeste": 0,
      "Centro-Oeste": 0,
      "Sudeste": 0,
      "Sul": 0,
    }

    self.Dica1_status = False
    self.Dica2_status = False
    self.Dica3_status = False

    self.SUMIR_STATUS_EVENTO = pygame.USEREVENT + 3

    self.errosQuestao = 0

    self.Acabou = False

    self.acabou_finalizacao = False
    self.tempo_esgotado = False
    self.liberar = False

    self.ler_clique = True

    self.reiniciar = False
    self.modo_power = False

  def verificar_acerto(self, regiao_clicada, modo):
    
    self.contagem_regioes[self.questao_atual["regiao"]] += 1 #soma um a regiao das questões jogadas
    if regiao_clicada == self.questao_atual["regiao"]:
      # se entrou aqui significa que Acertou
      self.acerto_sound.play()
      self.errosQuestao = 0
      self.Dica1_status = False
      self.Dica2_status = False
      self.Dica3_status = False

      self.Acerto_status = True
      pygame.time.set_timer(self.SUMIR_STATUS_EVENTO, 400, loops=1)
      self.contAcertos += 1

      # Sorteia a próxima questão do banco de dicionários
      if len(self.perguntas_disponiveis) > 0:
        idsorteado = random.randint(0, len(self.perguntas_disponiveis) - 1)
        self.questao_atual = self.perguntas_disponiveis.pop(idsorteado)
        self.perg_sorteada = self.questao_atual["pergunta"]
        self.dica_sorteada = self.questao_atual["dicas"]

      else:
        self.Acabou = True
        self.perg_sorteada = "Fim do Jogo! Você respondeu tudo."
        self.dica_sorteada = ["", "", ""]

      if self.acertosSequencia < 2:  # Erros por questão para ativar dica
        self.acertosSequencia += 1
      else:
        self.modo_power = True

    else:
      self.erro_sound.play()
      self.Errou_status = True  # mostra X
      pygame.time.set_timer(self.SUMIR_STATUS_EVENTO, 400, loops=1)
      self.contErros += 1  # conta todos os erros

      self.regioes_erradas[self.questao_atual["regiao"]] += 1  # soma + 1 nos erros por regiao, na regiao jogada
      self.acertosSequencia = 0  # zera a sequencia
      self.modo_power = False
      self.contador_piscar = 0

      if self.errosQuestao < 3 and modo == "facil":  # Erros por questão para ativar dica
        self.errosQuestao += 1
        if self.errosQuestao == 1:
          self.Dica1_status = True
        elif self.errosQuestao == 2:
          self.Dica2_status = True
        elif self.errosQuestao == 3:
          self.Dica3_status = True
      elif modo == "dificil":  # se o modo é dificil mesmo errando muda a questão perde a chance de ganhar um acerto
        if len(self.perguntas_disponiveis) > 0:
          idsorteado = random.randint(0, len(self.perguntas_disponiveis) - 1)
          self.questao_atual = self.perguntas_disponiveis.pop(idsorteado)
          self.perg_sorteada = self.questao_atual["pergunta"]
          self.dica_sorteada = self.questao_atual["dicas"]
        else:
          self.Acabou = True
          self.perg_sorteada = "Fim do Jogo! Você respondeu tudo."
          self.dica_sorteada = ["", "", ""]

  def gerenciar_eventos(self, evento, modo):
    mouse_seta = pygame.mouse.get_pos()

    if self.mapa_rect.collidepoint(mouse_seta) or self.botao_reiniciar_rect.collidepoint(mouse_seta):
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if evento.type == self.SUMIR_STATUS_EVENTO:
      self.Errou_status = False
      self.Acerto_status = False
      self.ler_clique = True #libera o clique somente após mostrar se está correto ou errado

    if evento.type == pygame.MOUSEBUTTONDOWN:
      if evento.button == 1:
        config.click_sound.play()
        mouse_x, mouse_y = evento.pos
        pos_mouse = evento.pos

        if self.mapa_rect.collidepoint(mouse_x, mouse_y):
          pixel_x = mouse_x - self.mapa_rect.x
          pixel_y = mouse_y - self.mapa_rect.y

          cor_pixel = self.mapa.get_at((pixel_x, pixel_y))
          rgb = (cor_pixel.r, cor_pixel.g, cor_pixel.b)

          self.regiao_clicada = funcoes.obter_regiao_por_cor(rgb)

          if self.regiao_clicada != None and self.ler_clique and not self.Acabou:
            self.ler_clique = False #desativa a leitura até parar de mostrar
            self.person_rect.center = pos_mouse
            self.verificar_acerto(self.regiao_clicada, modo)

        if self.botao_reiniciar_rect.collidepoint(pos_mouse):
          self.reiniciar = True

  def atualizar(self, tempo_restante, reiniciar):

    if self.reiniciar:
      reiniciar = True
      return "MENU", reiniciar, self.regioes_erradas, self.contagem_regioes, None, None

    if self.Acabou and tempo_restante > 182:
      self.acabou_finalizacao = True

    if tempo_restante <= 180:
      self.tempo_esgotado = True

    if self.liberar:
      acertos = self.contAcertos
      erros = self.contErros
      return "FASE2", reiniciar, self.regioes_erradas, self.contagem_regioes, acertos, erros #retorna acertos e erros

    else:
      return "FASE1", reiniciar, self.regioes_erradas, self.contagem_regioes, None, None

  def desenhar(self, tela):
    tela.blit(self.fundo_img, (0, 0))
    pygame.draw.rect(tela, config.bege, self.bloco_perguntas)
    tela.blit(self.mapaTela, self.mapaTela_rect)
    tela.blit(self.person_img, self.person_rect)
    tela.blit(self.botao_reiniciar, self.botao_reiniciar_rect)

    largura_maxima = self.bloco_perguntas.width - 40

    linhas_pergunta = funcoes.formatar_texto_largura(
        self.perg_sorteada, config.fonte_fases, largura_maxima
    )
    y_atual = self.bloco_perguntas.y + 30
    for linha in linhas_pergunta:
        pergunta_renderizada = config.fonte_fases.render(linha, False, config.verde)
        pergunta_renderizada_rect = pergunta_renderizada.get_rect()
        pergunta_renderizada_rect.centerx = self.bloco_perguntas.centerx
        pergunta_renderizada_rect.y = y_atual
        tela.blit(pergunta_renderizada, pergunta_renderizada_rect)
        y_atual += pergunta_renderizada.get_height() + 5

        # Animação da Intro
        if self.intro_estado != "FIM":
            self.intro_estado, self.tempo_inicio_espera = funcoes.animacao(
                self.intro_estado,
                self.intro_rect,
                self.alvo_y,
                self.duracao_espera,
                self.tempo_inicio_espera,
            )
            tela.blit(self.intro_img, self.intro_rect)


    if self.Errou_status == True:
      tela.blit(self.Errou_img, self.Errou_rect)
    elif self.Acerto_status == True:
      tela.blit(self.Acerto_img, self.Acerto_rect)

    if self.Dica1_status and len(self.dica_sorteada) > 0:
      linhas_dica1 = funcoes.formatar_texto_largura(self.dica_sorteada[0], config.fonte_dicas, largura_maxima)
      y_dica = self.bloco_perguntas.y + 110
      for linha in linhas_dica1:
        dica_renderizada = config.fonte_dicas.render(linha, False, config.azul)
        dica_rect = dica_renderizada.get_rect()
        dica_rect.centerx = self.bloco_perguntas.centerx
        dica_rect.y = y_dica
        tela.blit(dica_renderizada, dica_rect)
        y_dica += dica_renderizada.get_height() + 4

      if self.Dica2_status and len(self.dica_sorteada) > 1:
        linhas_dica2 = funcoes.formatar_texto_largura(self.dica_sorteada[1], config.fonte_dicas, largura_maxima)
        y_dica = self.bloco_perguntas.y + 210
        for linha in linhas_dica2:
          dica2_renderizada = config.fonte_dicas.render(linha, False, config.azul)
          dica2_rect = dica2_renderizada.get_rect()
          dica2_rect.centerx = self.bloco_perguntas.centerx
          dica2_rect.y = y_dica
          tela.blit(dica2_renderizada, dica2_rect)
          y_dica += dica2_renderizada.get_height() + 4

      if self.Dica3_status and len(self.dica_sorteada) > 2:
        linhas_dica3 = funcoes.formatar_texto_largura(self.dica_sorteada[2], config.fonte_dicas, largura_maxima)
        y_dica = self.bloco_perguntas.y + 310
        for linha in linhas_dica3:
          dica3_renderizada = config.fonte_dicas.render(linha, False, config.azul)
          dica3_rect = dica3_renderizada.get_rect()
          dica3_rect.centerx = self.bloco_perguntas.centerx
          dica3_rect.y = y_dica
          tela.blit(dica3_renderizada, dica3_rect)
          y_dica += dica3_renderizada.get_height() + 4

    if self.tempo_esgotado == True and self.esgotado_estado != "FIM":
        self.esgotado_estado, self.tempo_inicio_espera_esgotado, self.tempo_esgotado, self.liberar = funcoes.animacao2(
            self.esgotado_estado, 
            self.esgotado_rect, 
            self.alvo_y_esgotado, 
            self.duracao_espera_esgotado, 
            self.tempo_inicio_espera_esgotado, 
            self.tempo_esgotado, 
            self.liberar
        )
        tela.blit(self.esgotado_img, self.esgotado_rect)

    if self.acabou_finalizacao and self.acabou_estado != "FIM":
        self.acabou_estado, self.tempo_inicio_espera_acabou, self.acabou_finalizacao, self.liberar = funcoes.animacao2(
            self.acabou_estado, 
            self.acabou_rect, 
            self.alvo_y_acabou, 
            self.duracao_espera_acabou, 
            self.tempo_inicio_espera_acabou, 
            self.acabou_finalizacao, 
            self.liberar
        )
        tela.blit(self.acabou_img, self.acabou_rect)

    if self.modo_power:
      self.contador_piscar += 0.1
      # Transparência do texto variando entre 30 e 255 (visível a bem brilhante)
      transparencia_texto = int(142 + math.sin(self.contador_piscar) * 112)

      # Renderiza as linhas de texto
      linha1 = config.fonte_grossa.render("Parabéns! Você ativou o modo BOOST", True, config.amarelo)
      linha2 = config.fonte_grossa.render("Sequência de acertos, continue assim!", True, config.bege)

      # Aplica a transparência suave diretamente nas imagens dos textos
      linha1.set_alpha(transparencia_texto)
      linha2.set_alpha(transparencia_texto)

      # Define a posição das mensagens (centralizadas)
      linha1_rect = linha1.get_rect(centerx=config.centroX, y=15)
      linha2_rect = linha2.get_rect(centerx=config.centroX, y=linha1_rect.bottom + 5)

      # Desenha os textos piscando na tela
      tela.blit(linha1, linha1_rect)
      tela.blit(linha2, linha2_rect)