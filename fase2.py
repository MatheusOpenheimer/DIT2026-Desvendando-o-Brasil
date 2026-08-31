import copy
import random
import config
import estados
import funcoes
import pygame
import os


class Fase2:

  def __init__(self, regioes_erradas_fase1, regioes_jogadas_fase1):
    alternativas = funcoes.carregar_questoes_txt(os.path.join("dados", "alternativas_estados.txt"))
    # INICIANDO BANCO DE QUESTÔES E MAPAS------------------------
    self.alternativas_disponiveis = copy.deepcopy(alternativas)
    self.mapas_disponiveis = estados.caminhos_mapas.copy()
    #fundo-------------------------
  # Carrega e ajusta o tamanho da imagem de fundo para a resolução do jogo
    self.fundo_img = pygame.image.load(funcoes.resource_path("assets/IMAGENS/fundo_fase2.png")).convert_alpha()
    self.fundo_img = pygame.transform.scale(self.fundo_img, (config.largura, config.altura))
    # Cache para armazenar mapas de estados redimensionados
    self.mapas_estados_cache = {}

    # PAGINA INICIAL--------------------------------------------------
    self.texto_inicial = "Selecione um Estado:"

    self.mapa = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/mapaEstado.png")),(800, 800),)
    self.mapa_rect = self.mapa.get_rect(centerx=config.centroX, centery=(config.altura // 2) + 20)

    # INTRO----------------------------------------------------------------
    self.intro_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/fase2.png")),(600, 400),)
    self.intro_rect = self.intro_img.get_rect(centerx=config.centroX, centery=-300)

    self.intro_estado = "ENTRANDO"
    self.alvo_y = config.altura // 2
    self.tempo_inicio_espera = 0
    self.duracao_espera = 1000
    # -------------------------------------------------
    # BLOCO DE ALTERNATIVAS------------------------------------
    self.alt_A = pygame.Rect(70, 350,
                           (config.largura / 2) - 120, (config.altura / 4) - 30) # Cima / Esquerda
    self.alt_B = pygame.Rect(config.largura // 2, 350,
                           (config.largura / 2) - 120, (config.altura / 4) - 30) # Cima / Direita
    self.alt_C = pygame.Rect(70, config.altura - 300,
                           (config.largura / 2) - 120, (config.altura / 4) - 30)  # Baixo / Esquerda
    self.alt_D = pygame.Rect(config.largura // 2, config.altura - 300,
                           (config.largura / 2) - 120, (config.altura / 4) - 30)  # Baixo / Direita

    self.corA = config.bege
    self.corB = config.bege
    self.corC = config.bege
    self.corD = config.bege

    # SPAM DE ERRO E ACERTO
    self.visitado = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/visitado.png")),(500, 250),)
    self.visitado_rect = self.visitado.get_rect(centerx=config.centroX, centery=config.altura / 2)

    self.Errou_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/Errou.png")),(200, 200),)
    self.Errou_rect = self.Errou_img.get_rect(centerx=config.centroX, centery=config.altura / 2)
    self.Acerto_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/Acertou.png")),(200, 200),)
    self.Acerto_rect = self.Acerto_img.get_rect( centerx=config.centroX, centery=config.altura / 2)

    self.erro_sound = pygame.mixer.Sound(funcoes.resource_path("assets/AUDIOS/error_som.mp3"))
    self.erro_sound.set_volume(2.0)

    self.acerto_sound = pygame.mixer.Sound(funcoes.resource_path("assets/AUDIOS/acerto.mp3"))
    self.acerto_sound.set_volume(2.0)
    # PERSONAGEM MARCADOR DO MAPA---------------------------
    self.person_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/person1.png")),(30, 50))
    self.person_rect = self.person_img.get_rect()

    # reiniciar botao----------------------------------------------------
    self.botao_reiniciar = pygame.transform.scale(
        pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_reiniciar.png")),(50, 50))
    self.botao_reiniciar_rect = self.botao_reiniciar.get_rect(x=114, y=2)

    # SPAM DE FIM-----------------------------------------------------
    self.esgotado_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/gameover.png")),(500, 500),)
    self.esgotado_rect = self.esgotado_img.get_rect(centerx=config.centroX, centery=-300)

    self.esgotado_estado = "ENTRANDO"
    self.alvo_y_esgotado = config.altura // 2
    self.tempo_inicio_espera_esgotado = 0
    self.duracao_espera_esgotado = 1000

    self.acabou_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/final.png")),(500, 500),)
    self.acabou_rect = self.acabou_img.get_rect(centerx=config.centroX, centery=-300)

    self.acabou_estado = "ENTRANDO"
    self.alvo_y_acabou = config.altura // 2
    self.tempo_inicio_espera_acabou = 0
    self.duracao_espera_acabou = 1000

    # ------------------VARIAVEIS INICIALIZADAS--------------------------
    self.questao_sorteada = None
    self.estado_clicado = None  # começa vazio
    self.contAcertos = 0
    self.contErros = 0
    self.Jogados = []  # para não repetir os personagens
    self.estados_marcados = []  # onde terá os personagens

    # GERENCIAMENTO DE ESTADOS--------------------------------
    self.escolha = True
    self.acabou_finalizacao = False
    self.tempo_esgotado = False
    self.liberar = False
    self.reiniciar = False

    self.SUMIR_STATUS_EVENTO = pygame.USEREVENT + 3
    self.Errou_status = False
    self.Acerto_status = False

    self.TEMPO_RESPOSTA_EVENTO = pygame.USEREVENT + 4

    self.SUMIR_VISITADO_EVENTO = pygame.USEREVENT + 5
    self.status_visitado = False

    self.regioes_erradas2 = regioes_erradas_fase1.copy()
    self.contagem_jogadas_regiao = regioes_jogadas_fase1.copy()

    self.brasil = {
        "Norte": [
            "Acre",
            "Amapá",
            "Amazonas",
            "Pará",
            "Rondônia",
            "Roraima",
            "Tocantins",
        ],
        "Nordeste": [
            "Alagoas",
            "Bahia",
            "Ceará",
            "Maranhão",
            "Paraíba",
            "Pernambuco",
            "Piauí",
            "Rio Grande do Norte",
            "Sergipe",
        ],
        "Centro-Oeste": [
            "Distrito Federal",
            "Goiás",
            "Mato Grosso",
            "Mato Grosso do Sul",
        ],
        "Sudeste": ["Espírito Santo", "Minas Gerais", "Rio de Janeiro", "São Paulo"],
        "Sul": ["Paraná", "Rio Grande do Sul", "Santa Catarina"],
    }

    self.ler_clique_por_questao = True #começa lendo o clique

  def perguntas(self):
    if self.estado_clicado in self.alternativas_disponiveis and len(self.alternativas_disponiveis[self.estado_clicado]) > 0:
      self.escolha = False
      # CACHE DE MAPAS DO ESTADO (Para não recalcular transform.scale em todo clique)
      if self.estado_clicado not in self.mapas_estados_cache:
        mapa = estados.obter_mapa(self.estado_clicado)
        self.mapas_estados_cache[self.estado_clicado] = pygame.transform.scale(mapa, (250, 250))

      self.estado_img = self.mapas_estados_cache[self.estado_clicado]
      self.estado_rect = self.estado_img.get_rect(centerx=config.centroX, centery=150)
      self.estado_atual = self.estado_clicado # o estado atual será o estado clicado no momento da pergunta e não em qualquer clique

      idsorteado = random.randint(0, len(self.alternativas_disponiveis[self.estado_clicado]) - 1)
      self.questao_sorteada = self.alternativas_disponiveis[self.estado_clicado].pop(idsorteado)
    else:
      self.questao_sorteada = None
      self.escolha = True

  def gerenciar_eventos(self, evento, modo):
    if evento.type == self.SUMIR_VISITADO_EVENTO:
      self.status_visitado = False
      pygame.time.set_timer(self.SUMIR_VISITADO_EVENTO, 0)
    mouse_seta = pygame.mouse.get_pos()

    if self.escolha and self.mapa_rect.collidepoint(mouse_seta):
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif self.botao_reiniciar_rect.collidepoint(mouse_seta):
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    # Se estiver no modo de pergunta e o mouse estiver sobre algum botão
    elif not self.escolha and self.alt_A.collidepoint(mouse_seta) or self.alt_B.collidepoint(mouse_seta) or self.alt_C.collidepoint(mouse_seta) or self.alt_D.collidepoint(mouse_seta):
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    else:
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if modo == "facil":
      if evento.type == self.TEMPO_RESPOSTA_EVENTO:
        # MODO UMA QUESTÃO POR ESTADO
        # Volta para a tela de escolha (mapa)
        self.alternativas_disponiveis[self.estado_atual] = []  # faz isso pra não continuar na pergunta
        self.ler_clique_por_questao = True #mudou de questão libera o clique pra ler erro ou acerto
        self.escolha = True
        self.questao_sorteada = None
        # deixa vazio pra não entrar novamente, permitindo ter um sorteio no banco de questões e depois de feito deixando a questão do estado sem nada, para não repetir o estado
        # redefine cor do bloco de alternativas
        self.corA = config.bege
        self.corB = config.bege
        self.corC = config.bege
        self.corD = config.bege

    elif modo == "dificil":
      if evento.type == self.TEMPO_RESPOSTA_EVENTO:
        if len(self.alternativas_disponiveis[self.estado_atual]) > 0:
          idsorteado = random.randint(0, len(self.alternativas_disponiveis[self.estado_atual]) - 1)  # pega a posição da questão aleatoria
          self.questao_sorteada = self.alternativas_disponiveis[self.estado_atual].pop(idsorteado)  # guarda a questão aleatóra e exclui a ela do banco
        else:
          self.escolha = True
        self.ler_clique_por_questao = True
        # redefine cor do bloco de alternativas
        self.corA = config.bege
        self.corB = config.bege
        self.corC = config.bege
        self.corD = config.bege

    if evento.type == self.SUMIR_STATUS_EVENTO:  # se tiver ativo na tela, desativa para quando rodar não aparecer de novo
      self.Errou_status = False
      self.Acerto_status = False

    if evento.type == pygame.MOUSEBUTTONDOWN:
      if evento.button == 1:
        config.click_sound.play()

        pos_mouse = evento.pos
        mouse_x, mouse_y = evento.pos

        if self.botao_reiniciar_rect.collidepoint(pos_mouse):
          self.reiniciar = True

        if self.escolha:
          if self.mapa_rect.collidepoint(mouse_x, mouse_y):
            # a posição do pixel dentro da imagem MAPA é calculada subtraindo o x e y do próprio Rect
            pixel_x = mouse_x - self.mapa_rect.x
            pixel_y = mouse_y - self.mapa_rect.y

            cor_pixel = self.mapa.get_at((pixel_x, pixel_y))  # olha somente para o mapa, ignora as medidas da tela etc
            rgb = (cor_pixel.r,cor_pixel.g,cor_pixel.b,)  # pega as cores RGB do pixel clicado

            self.estado_clicado = funcoes.obter_estado_por_cor(rgb)
            print(self.estado_clicado)
            if self.estado_clicado is not None and self.escolha == True:

              if self.estado_clicado not in self.Jogados:  # se o estado clicado não está na lista dos ja jogados, define o local
                # do personagem para não desenhar em todos cliques
                rect_personagem = self.person_img.get_rect(midbottom=pos_mouse)  # center=pos deixaria o personagem no centro do clique
                self.estados_marcados.append(rect_personagem)
              if self.estado_clicado in self.Jogados:
                self.status_visitado = True
                pygame.time.set_timer(self.SUMIR_VISITADO_EVENTO, 1200, loops=1)
              self.perguntas()  # chama perguntas que só é criada se não foi jogada ainda

        # VERIFICANDO ACERTOS NO JOGO---------------------------------------------------
        # só entra no elif se não tiver entrado no if (acima) ou seja
        # espera o código rodar inteiro, confirmando o self.escolha como False
        # se não rodasse o código inteiro, iria alterar para False, entrar no elif (abaixo)
        # sem nem ter mostrado a pergunta
        elif self.escolha == False and self.questao_sorteada is not None:  # significa que está em algum estado jogando
          # SE ENTROU AQUI O ESTADO ESTÁ SENDO JOGADO
          if self.estado_atual not in self.Jogados:
            self.Jogados.append(self.estado_atual)  # bota na lista de estados jogados sem repetir

          acertou = None
          errou = None

          resposta_certa = self.questao_sorteada["correta"]
          
          if self.alt_A.collidepoint(pos_mouse):
            if resposta_certa == 0:
              self.corA = config.green  # mostra a clicada como verde
              acertou = True
            else:
              self.corA = config.vermelho  # Mostra a clicada como vermelho
              errou = True

          elif self.alt_B.collidepoint(pos_mouse):
            if resposta_certa == 1:
              self.corB = config.green
              acertou = True
            else:
              self.corB = config.vermelho
              errou = True

          elif self.alt_C.collidepoint(pos_mouse):
            if resposta_certa == 2:
              self.corC = config.green
              acertou = True
            else:
              self.corC = config.vermelho
              errou = True

          elif self.alt_D.collidepoint(pos_mouse):
            if resposta_certa == 3:
              self.corD = config.green
              acertou = True
            else:
              self.corD = config.vermelho
              errou = True

          if (acertou or errou) and self.ler_clique_por_questao:
            self.ler_clique_por_questao = False #Trava imediatamente pra não ter vários acertos pela mesma alternativa
            
            #Incrementa total da região jogada
            for regiao, estados_regiao in self.brasil.items():
                if self.estado_atual in estados_regiao:
                    self.contagem_jogadas_regiao[regiao] += 1
                    break

            if acertou:
                self.acerto_sound.play()
                self.Acerto_status = True
                self.contAcertos += 1

            elif errou:
                self.erro_sound.play()
                self.Errou_status = True
                self.contErros += 1
                # Mostra o correto para o usuário saber qual era a correta
                if resposta_certa == 0: self.corA = config.green
                elif resposta_certa == 1: self.corB = config.green
                elif resposta_certa == 2: self.corC = config.green
                elif resposta_certa == 3: self.corD = config.green

                #dentro do errou pq pega o erro
                for regiao, estados_regiao in self.brasil.items():
                    if self.estado_atual in estados_regiao:
                        self.regioes_erradas2[regiao] += 1
                        break
                    
            #dentro do acertou ou errou pq serve pros dois
            pygame.time.set_timer(self.SUMIR_STATUS_EVENTO, 400, loops=1)
            pygame.time.set_timer(self.TEMPO_RESPOSTA_EVENTO, 900, loops=1)


  def calcular_porcentagem(self, regiao):
    jogadas = self.contagem_jogadas_regiao.get(regiao, 0) #pega o valor que ficou na região, se não tiver atribui 0
    erros = self.regioes_erradas2.get(regiao, 0)
    if jogadas > 0:
      return round((erros / jogadas) * 100, 1)
    else:
      return 0.0
  
  def atualizar(self, tempo_restante, salvarBD, reiniciar):  # gerencia eventos a todo momento, sem esperar cliques etc
    # Roda a CADA FRAME no loop principal para checar tempo e troca de fase.

    if self.reiniciar:
      reiniciar = True
      return "MENU", salvarBD, reiniciar

    if len(self.Jogados) == len(self.mapas_disponiveis):
      self.acabou_finalizacao = True

    if tempo_restante <= 0.9:
      self.tempo_esgotado = True

    if self.liberar:
      import banco
      #porcentagem de erros
      norte_erros = self.calcular_porcentagem("Norte")
      nordeste_erros = self.calcular_porcentagem("Nordeste")
      centroOeste_erros = self.calcular_porcentagem("Centro-Oeste")
      sudeste_erros = self.calcular_porcentagem("Sudeste")
      sul_erros = self.calcular_porcentagem("Sul")
      banco.salvar_estatisticas(
          config.nome_jogador,
          norte_erros,
          nordeste_erros,
          centroOeste_erros,
          sudeste_erros,
          sul_erros,
      )
      config.acertos_jogador += self.contAcertos# soma erros e acertos aos da fase 1
      config.erros_jogador += self.contErros
      config.tempo_sobra = tempo_restante
      salvarBD = True
      return "FINAL", salvarBD, reiniciar

    else:
      return "FASE2", salvarBD, reiniciar

  def desenhar(self, tela):
    tela.blit(self.fundo_img, (0, 0))
    tela.blit(self.botao_reiniciar, self.botao_reiniciar_rect)

    if self.escolha:
      tela.blit(self.mapa, self.mapa_rect)

      texto_renderizado = config.fonte_fases.render(self.texto_inicial, False, config.amarelo)
      texto_renderizado_rect = texto_renderizado.get_rect(centerx=config.centroX, y=10)
      tela.blit(texto_renderizado, texto_renderizado_rect)

      if self.intro_estado != "FIM":  # VAI DESENHANDO ATÉ DEFINIR FIM
        self.intro_estado, self.tempo_inicio_espera = funcoes.animacao(
            self.intro_estado,
            self.intro_rect,
            self.alvo_y,
            self.duracao_espera,
            self.tempo_inicio_espera,
        )  # inicia o desenho ja animado
        tela.blit(self.intro_img, self.intro_rect)

      for pos in self.estados_marcados: # desenha todos personagens, nas posições guardadas
        tela.blit(self.person_img, pos)

    else:
      if self.questao_sorteada is not None:
        tela.blit(self.estado_img, self.estado_rect)
        nome_estado = config.fonte_fases.render(self.estado_atual, True, config.amarelo)
        nome_estado_rect = nome_estado.get_rect(centerx=config.centroX, y=10)
        tela.blit(nome_estado, nome_estado_rect)

        largura_maxima = 600

        linhas = funcoes.formatar_texto_largura(self.questao_sorteada["pergunta"],config.fonte_fases,largura_maxima,)
        y_pergunta = 290

        for linha in linhas:
          texto_render = config.fonte_fases.render(linha, True, config.preto)
          rect_linha = texto_render.get_rect(centerx=config.centroX, centery=y_pergunta)
          tela.blit(texto_render, rect_linha)
          y_pergunta += 25

        pygame.draw.rect(tela, self.corA, self.alt_A, border_radius=8)
        pygame.draw.rect(tela, self.corB, self.alt_B, border_radius=8)
        pygame.draw.rect(tela, self.corC, self.alt_C, border_radius=8)
        pygame.draw.rect(tela, self.corD, self.alt_D, border_radius=8)
        caixas_alt = [self.alt_A, self.alt_B, self.alt_C, self.alt_D]
        opcoes = self.questao_sorteada["opcoes"]

        limite_loop = min(len(opcoes), len(caixas_alt))

        for i in range(limite_loop):
          opcao_texto = opcoes[i]
          caixa = caixas_alt[i]
          largura_maxima = caixa.width - 20
          linhas = funcoes.formatar_texto_largura( opcao_texto, config.fonte_fases, largura_maxima)

          # CÁLCULO E DESENHO DEVEM FICAR DENTRO DO LOOP 'for i'!
          altura_linha = config.fonte_fases.get_height()
          altura_total = len(linhas) * altura_linha + (len(linhas) - 1) * 4
          pos_y_inicial = caixa.centery - (altura_total // 2)

          for j in range(len(linhas)):
            texto_render = config.fonte_fases.render(linhas[j], True, config.preto)
            rect_linha = texto_render.get_rect()
            rect_linha.centerx = caixa.centerx
            rect_linha.top = pos_y_inicial + j * (altura_linha + 4)
            tela.blit(texto_render, rect_linha)

    if self.Errou_status == True:
      tela.blit(self.Errou_img, self.Errou_rect)
    elif self.Acerto_status == True:
      tela.blit(self.Acerto_img, self.Acerto_rect)

    if self.status_visitado:
      tela.blit(self.visitado, self.visitado_rect)

    if self.tempo_esgotado == True and self.esgotado_estado != "FIM":
        self.esgotado_estado,self.tempo_inicio_espera_esgotado,self.tempo_esgotado,self.liberar = funcoes.animacao2(
          self.esgotado_estado,
          self.esgotado_rect,
          self.alvo_y_esgotado,
          self.duracao_espera_esgotado,
          self.tempo_inicio_espera_esgotado,
          self.tempo_esgotado,
          self.liberar,
        )
        tela.blit(self.esgotado_img, self.esgotado_rect)

    if self.acabou_finalizacao and self.acabou_estado != "FIM":
        self.acabou_estado,self.tempo_inicio_espera_acabou,self.acabou_finalizacao,self.liberar = funcoes.animacao2(
          self.acabou_estado,
          self.acabou_rect,
          self.alvo_y_acabou,
          self.duracao_espera_acabou,
          self.tempo_inicio_espera_acabou,
          self.acabou_finalizacao,
          self.liberar,
        )
        tela.blit(self.acabou_img, self.acabou_rect)