import pygame
import config
import funcoes

class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        caminhos_sprites = [ #Organizado em ordem para o sistema de mudança na direção
            "assets/SPRITES/reddown.png",  "assets/SPRITES/reddown1.png",  "assets/SPRITES/reddown2.png",
            "assets/SPRITES/redback.png",  "assets/SPRITES/redback1.png",  "assets/SPRITES/redback2.png",
            "assets/SPRITES/redright.png", "assets/SPRITES/redright1.png", "assets/SPRITES/redright2.png",
            "assets/SPRITES/redleft.png",  "assets/SPRITES/redleft1.png",  "assets/SPRITES/redleft2.png"
        ]
        
        self.sprites = []
        for caminho in caminhos_sprites:
            img = pygame.image.load(funcoes.resource_path(caminho)).convert_alpha()
            img_escalada = pygame.transform.scale(img, (19 * 3, 32 * 3))
            self.sprites.append(img_escalada)

        self.atual = 0.0
        self.modo = "baixo"
        self.image = self.sprites[int(self.atual)]

        self.rect = self.image.get_rect()
        self.rect.center = (config.largura // 2, config.altura // 2)
        self.velocidade = 4

    def mover(self, teclas):

        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
            self.modo = "esquerda"
        elif teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
            self.modo = "direita"
        elif teclas[pygame.K_UP]:
            self.rect.y -= self.velocidade
            self.modo = "cima"
        elif teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidade
            self.modo = "baixo"

        #DELIMITAÇÃO DA TELA
        #retângulo com as dimensões da janela
        area_tela = pygame.Rect(0, 0, config.largura, config.altura)
        
        # Prende o personagem dentro da area_tela
        self.rect.clamp_ip(area_tela)

    def update(self):
        teclas = pygame.key.get_pressed()

        andando = (
            teclas[pygame.K_DOWN]
            or teclas[pygame.K_UP]
            or teclas[pygame.K_RIGHT]
            or teclas[pygame.K_LEFT]
        )

        if andando: #sistema de troca de imagens de acordo com a direção
            self.atual += 0.6
            if self.modo == "baixo":
                if self.atual >= 3 or self.atual < 0:
                    self.atual = 0

            elif self.modo == "cima":
                if self.atual >= 6 or self.atual < 3:
                    self.atual = 3

            elif self.modo == "direita":
                if self.atual >= 9 or self.atual < 6:
                    self.atual = 6

            elif self.modo == "esquerda":
                if self.atual >= 12 or self.atual < 9:
                    self.atual = 9

        else:
            # Se NENHUMA tecla estiver pressionada, trava no primeiro frame (parado) da direção atual
            if self.modo == "baixo":
                self.atual = 0
            elif self.modo == "cima":
                self.atual = 3
            elif self.modo == "direita":
                self.atual = 6
            elif self.modo == "esquerda":
                self.atual = 9

        self.image = self.sprites[int(self.atual)]