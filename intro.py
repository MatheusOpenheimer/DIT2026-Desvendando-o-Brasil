import pygame
import config
import funcoes

class Intro:
    def __init__(self):
        # BLOCO DE INSTRUÇÃO----------------------------------------------------------
        self.pergaminho_img = pygame.image.load(funcoes.resource_path("assets/IMAGENS/pergaminho.png"))
        self.pergaminho_img = pygame.transform.scale(self.pergaminho_img, (1000, 550))
        self.pergaminho_rect = self.pergaminho_img.get_rect(centerx=config.centroX, centery=config.altura // 2 - 100)

        self.fonte_titulo = pygame.font.Font(funcoes.resource_path("assets/FONTES/Afonte.ttf"), 22)

        self.btn_back_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_back.png")), (120, 45))
        self.btn_back_rect = self.btn_back_img.get_rect(centery=self.pergaminho_rect.bottom + 30)
        self.btn_next_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_next.png")), (120, 45))
        self.btn_next_rect = self.btn_next_img.get_rect(centery=self.pergaminho_rect.bottom + 30)
        self.btn_next_rect.centerx = config.centroX
        # -------------------------------------------------------------------------------------
        # Botao iniciar-------------------------------------------------------------------------
        self.placa_iniciar = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/placa_iniciar.png")), (170, 270))
        self.placa_iniciar_rect = self.placa_iniciar.get_rect(x=config.largura - 170, y=config.altura - 270)
        self.placa_iniciar_rect.centery = config.altura + 300  # Onde começa a img

        self.placa_estado = "SUBINDO"
        self.alvo_y = config.altura - 140  # Até onde sobe

        # BOTÕES DE MODO-------------------------------------------------
        self.botao_facil_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/facil.png")), (230, 80))
        self.botao_facil_rect = self.botao_facil_img.get_rect(centerx=config.centroX, centery=self.pergaminho_rect.centery - 80)
        self.facil_clicado_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/facil_clicado.png")), (230, 80))

        self.botao_dificil_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/dificil.png")), (230, 80))
        self.botao_dificil_rect = self.botao_dificil_img.get_rect(centerx=config.centroX, centery=self.pergaminho_rect.centery + 10)
        self.dificil_clicado_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/dificil_clicado.png")), (230, 80))

        # BOTÃO ESPECIAL (Provisório com input_name)----------------------
        self.botao_especial_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/especial.png")), (230, 80))
        self.botao_especial_rect = self.botao_especial_img.get_rect(centerx=config.centroX, centery=self.botao_dificil_rect.centery + 90)
        self.botao_especial_clicado_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/especial_clicado.png")), (230, 80))

        # Reiniciar botao----------------------------------------------------
        self.botao_reiniciar = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_reiniciar.png")), (50, 50))
        self.botao_reiniciar_rect = self.botao_reiniciar.get_rect(x=114, y=2)

        self.mudar = False
        self.questao = 0

        self.tela_final = False
        self.iniciarJogo = False
        self.reiniciar = False

        self.segurando_mouse_dificil = False
        self.segurando_mouse_facil = False
        self.segurando_mouse_especial = False

        self.modo = None

        self.instrucoes = [
            [
                "GUIA GERAL DO JOGO",
                "",
                "ATENÇÃO AOS CLIQUES NO MAPA:",
                "Clique exatamente DENTRO dos territórios.",
                "Cliques nas linhas pretas (divisórias dos estados)",
                "ou fora do mapa NÃO contam,",
                "pois são áreas neutras!",
                "",
                "BOTÃO DE REINICIAR (Canto superior esquerdo):",
                "Cuidado! Ao clicar no ícone de reiniciar,",
                "a partida é resetada instantaneamente, sem confirmação",
                "voltando ao Menu e zerando seu progresso!",
                ""
            ],
            [
                "GUIA DA FASE 1",
                "",
                "Leia a pergunta sobre Geografia/Cultura.",
                "",
                "Para responder, clique na",
                "região correta no mapa do Brasil.",
                "",
                "Seus acertos e erros são contabilizados!",
                "'Chutar' não é uma boa ideia: erros afetam",
                "sua nota final e seu ranking.",
                "",
                "O personagem indicará qual região você clicou.",
                "",
                "Você tem 1 minuto para responder o máximo de questões",
                "que conseguir, na Fase 1."
            ],
            [
                "GUIA DA FASE 2",
                "",
                "Clique em um estado no mapa",
                "para abrir suas perguntas de múltipla escolha.",
                "",
                "O personagem marcará os estados já visitados.",
                "DICA DE OURO (Cuidado com os Estados Pequenos!):",
                "Não se esqueça do DISTRITO FEDERAL e",
                "dos estados menores (principalmente na Região Nordeste)!",
                "O personagem pode parecer estar em cima",
                "de um estado pequeno, mas o clique real",
                "pode ter atingido o estado vizinho!",
                "",
                "A fase só termina quando todos os estados",
                "forem respondidos ou se o tempo esgotar (Game Over)!"
            ],
            [
                "GUIA DO MINIGAME DO APRENDIZADO",
                "",
                "Ande com as setas do teclado para visitar os estados,",
                "ao passar por um estado, você verá curiosidades",
                "sobre ele",
                "",
                "Se não quiser ver as curiosidades ou tiver finalizado",
                "seu aprendizado, basta andar até o botão",
                "'Pular Minigame', no canto inferior direito da tela",
                "e confirmar sua saída, clicando em 'PULAR'"
            ],
            [
                "GUIA DE MODO DE JOGO",
                "Modo Fácil",
                "Fase 1: Ao errar um estado, o jogo libera até 3 dicas",
                "consecutivas para orientar o aluno, permitindo novas",
                "tentativas até a resposta correta.",
                "",
                "Fase 2: Apresenta apenas 1 questão por estado, proporcionando",
                "uma rodada mais rápida e focada nos conceitos principais.",
                "Modo Difícil:",
                "Fase 1: Sem nenhuma dica. O jogador possui apenas",
                "uma única chance: acertando ou errando, o sistema registra",
                "a resposta e avança imediatamente para a próxima questão.",
                "",
                "Fase 2: Apresenta 5 questões por estado, exigindo",
                "conhecimento aprofundado sobre história, geografia e aspectos",
                "culturais de cada unidade federativa.",
                "",
                "VAMOS INICIAR!?"
            ],
            ["SELECIONE UM MODO:"]
        ]

        self.instrucoes_tela = self.instrucoes[0]

    def gerenciar_eventos(self, evento):
        pos_mouse = pygame.mouse.get_pos()
        
        # Gerenciamento de cursor
        if (self.btn_back_rect.collidepoint(pos_mouse) or 
            self.btn_next_rect.collidepoint(pos_mouse) or 
            self.botao_facil_rect.collidepoint(pos_mouse) or 
            self.botao_dificil_rect.collidepoint(pos_mouse) or 
            self.botao_especial_rect.collidepoint(pos_mouse) or 
            self.placa_iniciar_rect.collidepoint(pos_mouse) or 
            self.botao_reiniciar_rect.collidepoint(pos_mouse)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                pos_mouse = evento.pos

                if self.botao_facil_rect.collidepoint(pos_mouse) and self.tela_final:
                    self.segurando_mouse_facil = True
                    self.segurando_mouse_dificil = False
                    self.segurando_mouse_especial = False
                    self.modo = "facil"

                elif self.botao_dificil_rect.collidepoint(pos_mouse) and self.tela_final:
                    self.segurando_mouse_dificil = True
                    self.segurando_mouse_facil = False
                    self.segurando_mouse_especial = False
                    self.modo = "dificil"

                elif self.botao_especial_rect.collidepoint(pos_mouse) and self.tela_final:
                    self.segurando_mouse_especial = True
                    self.segurando_mouse_facil = False
                    self.segurando_mouse_dificil = False
                    self.modo = "especial"

                elif self.botao_reiniciar_rect.collidepoint(pos_mouse):
                    self.reiniciar = True

                elif self.btn_back_rect.collidepoint(pos_mouse):
                    self.questao -= 1
                    self.mudar = True

                elif self.btn_next_rect.collidepoint(pos_mouse):
                    self.questao += 1
                    self.mudar = True

                elif self.placa_iniciar_rect.collidepoint(pos_mouse):
                    if self.modo is not None:
                        self.iniciarJogo = True

        if self.mudar:
            if self.questao < 0:
                self.questao = 0
            elif self.questao > 5:
                self.questao = 5

            self.instrucoes_tela = self.instrucoes[self.questao]

            self.btn_back_rect.centery = self.pergaminho_rect.bottom + 30
            self.btn_next_rect.centery = self.pergaminho_rect.bottom + 30
            if self.questao == 0:
                self.btn_next_rect.centerx = config.centroX
                self.btn_back_rect.centerx = 1000
            elif self.questao == 5:
                self.btn_back_rect.centerx = config.centroX
                self.btn_next_rect.centerx = 1000
                self.tela_final = True
            else:
                self.btn_back_rect.centerx = config.centroX - 70
                self.btn_next_rect.centerx = config.centroX + 70
                self.tela_final = False

            self.mudar = False

    def atualizar(self, reiniciar):
        if self.reiniciar:
            reiniciar = True
            return "MENU", reiniciar, self.modo
        elif self.iniciarJogo:
            if self.modo == "especial":
                return "GAME_SRS", reiniciar, self.modo
            else:
                return "GAME", reiniciar, self.modo
        else:
            return "INTRO", reiniciar, self.modo

    def desenhar(self, tela):
        tela.fill(config.verde)
        tela.blit(self.pergaminho_img, self.pergaminho_rect)
        tela.blit(self.botao_reiniciar, self.botao_reiniciar_rect)

        if self.questao == 3:
            pos_y = self.pergaminho_rect.y + 85
        else:
            pos_y = self.pergaminho_rect.y + 20

        for i, linha in enumerate(self.instrucoes_tela):
            if i == 0:
                superficie_texto = self.fonte_titulo.render(linha, True, (80, 40, 10))
            else:
                superficie_texto = config.fonte_fases.render(linha, True, (40, 20, 5))
            rect_texto = superficie_texto.get_rect(centerx=self.pergaminho_rect.centerx, y=pos_y)
            tela.blit(superficie_texto, rect_texto)
            pos_y += 28

        if self.questao != 0:
            tela.blit(self.btn_back_img, self.btn_back_rect)
        if self.questao != 5:
            tela.blit(self.btn_next_img, self.btn_next_rect)

        if self.tela_final:
            if self.segurando_mouse_facil:
                tela.blit(self.facil_clicado_img, self.botao_facil_rect)
            else:
                tela.blit(self.botao_facil_img, self.botao_facil_rect)

            if self.segurando_mouse_dificil:
                tela.blit(self.dificil_clicado_img, self.botao_dificil_rect)
            else:
                tela.blit(self.botao_dificil_img, self.botao_dificil_rect)

            if self.segurando_mouse_especial:
                tela.blit(self.botao_especial_clicado_img, self.botao_especial_rect)
            else:
                tela.blit(self.botao_especial_img, self.botao_especial_rect)

            if self.modo is not None:
                self.placa_estado = funcoes.animacao_entrar(self.placa_estado, self.placa_iniciar_rect, self.alvo_y)
                tela.blit(self.placa_iniciar, self.placa_iniciar_rect)
                texto_selecionado = f"MODO SELECIONADO: {self.modo.upper()}"
                fase_selecionada = config.fonte_fases.render(texto_selecionado, True, config.preto)
                fase_selecionada_renderizada = fase_selecionada.get_rect(centerx=config.centroX, y=self.botao_especial_rect.bottom + 10)
                tela.blit(fase_selecionada, fase_selecionada_renderizada)