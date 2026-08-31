import os
import pygame
import funcoes


class PontoTuristico:
    def __init__(self, nome, x, y, curiosidade, imagem_path, foto_popup_path, qr_path):
        self.nome = nome
        self.x = x
        self.y = y
        self.curiosidade = curiosidade
        self.imagem_path = imagem_path
        self.foto_popup_path = foto_popup_path
        self.qr_path = qr_path
        self.visitado = False

        caminho_img = funcoes.resource_path(self.imagem_path)
        if os.path.exists(caminho_img):
            img_carregada = pygame.image.load(caminho_img).convert_alpha()
            self.imagem = pygame.transform.scale(img_carregada, (90, 90))
            self.imagem_rect = self.imagem.get_rect(center=(self.x, self.y))
        else:
            self.imagem = pygame.Surface((90, 90), pygame.SRCALPHA)
            pygame.draw.circle(self.imagem, (220, 80, 50), (45, 45), 35)
            self.imagem_rect = self.imagem.get_rect(center=(self.x, self.y))

        # Carrega a foto do pop-up
        caminho_foto = funcoes.resource_path(self.foto_popup_path)
        if os.path.exists(caminho_foto):
            self.foto_popup = pygame.image.load(caminho_foto).convert_alpha()
        else:
            self.foto_popup = None

        # Carrega o QR Code do pop-up
        caminho_qr = funcoes.resource_path(self.qr_path)
        if os.path.exists(caminho_qr):
            self.qr_img = pygame.image.load(caminho_qr).convert_alpha()
        else:
            self.qr_img = None

    def dentro_do_raio(self, px, py, tamanho_jogador=32):
        rect_jogador = pygame.Rect(px - 10, py - 10, 20, 20)
        if self.imagem_rect:
            return self.imagem_rect.colliderect(rect_jogador)
        return False

    def marcar_visitado(self):
        self.visitado = True

    def resetar(self):
        self.visitado = False


ENTRADA_CIDADE = {
    "nome": "Estátua de Santa Rita - Entrada da Cidade",
    "x": 1051,
    "y": 750,
    "imagem_path": "assets/IMAGENS_SRS/santa_estatua.png",
    "foto_popup_path": "assets/IMAGENS_SRS/srs.png",
    "qr_path": "assets/IMAGENS_SRS/img_santa.png",
    "mensagem": (
        "Bem-vindo a Santa Rita do Sapucaí! Você está diante do monumento da nossa "
        "padroeira, o ponto de acolhida de quem chega ao Vale da Eletrônica. Aqui "
        "começa uma jornada pela Rota da Inovação: um roteiro onde o aconchego do "
        "interior mineiro se encontra com a alta tecnologia, a arquitetura centenária, "
        "a fé e os sabores da nossa terra. Explore o mapa, caminhe pelas ruas e "
        "descubra a história por trás de cada patrimônio da cidade!"
    ),
}

EVENTO_RIO_SAPUCAI = {
    "nome": "Travessia do Rio Sapucaí",
    "foto_popup_path": "assets/IMAGENS_SRS/img_rio.png",
    "qr_path": "assets/IMAGENS_SRS/qr_rio.png",
    "mensagem": (
        "Você acabou de cruzar as águas do Rio Sapucaí, o rio que dá nome ao "
        "município e moldou a paisagem do vale onde a cidade nasceu. Ele atravessa "
        "o Centro histórico e passa bem ao lado da Galeria Aberta de Arte Urbana, "
        "na região da Beira Rio — hoje um dos cartões-postais mais criativos de "
        "Santa Rita do Sapucaí."
    ),
}


def criar_pontos_santa_rita():
    return [
        PontoTuristico(
            nome="Santuário Santa Rita de Cássia",
            x=851, y=216,
            curiosidade=(
                "Bem no coração da Praça Santa Rita, este santuário guarda a fé que "
                "batiza a cidade inteira. Todos os anos, entre 17 e 25 de maio, a "
                "praça se enche de devoção durante a Festa de Santa Rita: nove dias "
                "de novenas, a tradicional bênção das rosas e uma procissão luminosa "
                "que atravessa as ruas do Centro. É daqui que nasce a identidade mais "
                "antiga da cidade — muito antes de virar Vale da Eletrônica, Santa "
                "Rita já era terra de fé e tradição."
            ),
            imagem_path="assets/IMAGENS_SRS/igreja.png",
            foto_popup_path="assets/IMAGENS_SRS/img_igreja.png",
            qr_path="assets/IMAGENS_SRS/qr_igreja.png",
        ),
        PontoTuristico(
            nome="Teatro Municipal",
            x=957, y=320,
            curiosidade=(
                "Erguido ainda na década de 1920, o Teatro Municipal Monsenhor José "
                "Carneiro Pinto viu quase um século de histórias serem contadas em "
                "seu palco. Recentemente revitalizado, hoje reúne 242 lugares e "
                "continua vivo: recebe aulas de teatro, coral e espetáculos culturais "
                "o ano inteiro. É prova de que, em Santa Rita, cultura e história "
                "andam de mãos dadas com o presente."
            ),
            imagem_path="assets/IMAGENS_SRS/teatro.png",
            foto_popup_path="assets/IMAGENS_SRS/img_teatro.jpg",
            qr_path="assets/IMAGENS_SRS/qr_teatro.png",
        ),
        PontoTuristico(
            nome="Mercado Municipal",
            x=1075, y=210,
            curiosidade=(
                "O Mercado Municipal Benedito Pereira dos Reis funciona todos os "
                "dias, mas é aos domingos de manhã que ganha vida de verdade: a "
                "tradicional Feira Livre toma conta da praça com queijos artesanais, "
                "café especial da Serra da Mantiqueira, doces caseiros e produtos "
                "direto da roça. Para os moradores, é ritual de fim de semana. Para "
                "quem visita, é a forma mais gostosa de provar o sabor real do "
                "interior de Minas."
            ),
            imagem_path="assets/IMAGENS_SRS/mercadao.png",
            foto_popup_path="assets/IMAGENS_SRS/img_mercadao.png",
            qr_path="assets/IMAGENS_SRS/qr_mercado.png",
        ),
        PontoTuristico(
            nome="Centro de Eventos e Festivais",
            x=196, y=371,
            curiosidade=(
                "É aqui que Santa Rita do Sapucaí mostra ao mundo por que é chamada "
                "de Vale da Eletrônica — e, mais recentemente, comparada em "
                "reportagens nacionais a um 'Vale do Silício brasileiro'. O espaço "
                "recebe feiras de inovação, festivais gastronômicos e eventos "
                "tecnológicos como o HackTown, um dos maiores festivais de tecnologia "
                "e inovação da América Latina, atraindo milhares de visitantes todos "
                "os anos. Tradição e futuro se cruzam bem aqui, no meio da cidade."
            ),
            imagem_path="assets/IMAGENS_SRS/eventos.png",
            foto_popup_path="assets/IMAGENS_SRS/img_eventos.png",
            qr_path="assets/IMAGENS_SRS/qr_eventos.png",
        ),
        PontoTuristico(
            nome="Museu Histórico Dr. Delfim Moreira",
            x=328, y=734,
            curiosidade=(
                "Esta casa já foi lar de Delfim Moreira, um dos filhos mais ilustres "
                "de Santa Rita do Sapucaí, que chegou a ocupar a Presidência da "
                "República. Tombada como Patrimônio Histórico em 2006, a residência "
                "hoje é museu e guarda móveis de época, fotografias e acervos que "
                "contam a memória de uma cidade que, mesmo pequena, sempre teve "
                "grandes histórias para contar."
            ),
            imagem_path="assets/IMAGENS_SRS/museu.png",
            foto_popup_path="assets/IMAGENS_SRS/img_museu.png",
            qr_path="assets/IMAGENS_SRS/qr_museu.png",
        ),
        PontoTuristico(
            nome="ETE FMC",
            x=1152, y=344,
            curiosidade=(
                "Marco zero do Vale da Eletrônica. Em 1959, Dona Sinhá Moreira "
                "negociou pessoalmente com o então governador Juscelino Kubitschek a "
                "autorização para ensinar eletrônica no Brasil — e fundou a primeira "
                "escola técnica de eletrônica da América Latina. Ela dizia sonhar em "
                "transformar Santa Rita em 'uma cidade do futuro', e foi exatamente "
                "o que aconteceu: hoje o Vale da Eletrônica reúne cerca de 239 "
                "indústrias de eletroeletrônicos e mais de 5 mil empregos diretos — "
                "tudo começou nesta escola."
            ),
            imagem_path="assets/IMAGENS_SRS/ete.png",
            foto_popup_path="assets/IMAGENS_SRS/img_ete.png",
            qr_path="assets/IMAGENS_SRS/qr_ete.png",
        ),
        PontoTuristico(
            nome="FAI Centro de Ensino Superior",
            x=1437, y=266,
            curiosidade=(
                "Em 1971, Francisco Ribeiro de Magalhães teve uma ideia ousada: "
                "trazer o primeiro curso de Administração do Sul de Minas para uma "
                "cidade de pouco mais de 12 mil habitantes. Nascia a FAI — hoje "
                "referência em Gestão, Tecnologia e Educação, e casa da FAITEC, a "
                "feira que todos os anos reúne centenas de estudantes apresentando "
                "suas próprias inovações para a cidade e o mundo."
                "Em 1978, a instituição implantou o primeiro curso superior de"
                "Informática em uma faculdade privada de Minas Gerais, figurando também" 
                "entre os doze primeiros do país."
            ),
            imagem_path="assets/IMAGENS_SRS/fai.png",
            foto_popup_path="assets/IMAGENS_SRS/img_fai.png",
            qr_path="assets/IMAGENS_SRS/qr_fai.png",
        ),
        PontoTuristico(
            nome="INATEL",
            x=1157, y=101,
            curiosidade=(
                "Fundado em 1965 por José Nogueira Leite, o INATEL colocou Santa "
                "Rita do Sapucaí no mapa mundial das telecomunicações. Hoje é "
                "referência internacional e centro nacional de pesquisa em "
                "tecnologias 5G e 6G — prova de que uma cidade do interior de Minas "
                "pode ajudar a desenhar o futuro da conexão no Brasil inteiro."
            ),
            imagem_path="assets/IMAGENS_SRS/inatel.png",
            foto_popup_path="assets/IMAGENS_SRS/img_inatel.png",
            qr_path="assets/IMAGENS_SRS/qr_inatel.png",
        ),
        PontoTuristico(
            nome="Morro do Cruzeiro",
            x=705, y=65,
            curiosidade=(
                "O Morro do Cruzeiro é o coração afetivo e um dos maiores cartões-postais "
                "de Santa Rita do Sapucaí. Mais do que um mirante, ele é o símbolo vivo da "
                "nossa comunidade: um patrimônio abraçado pelo povo, que dispensa bilheterias "
                "para oferecer uma vista panorâmica de tirar o fôlego e o pôr do sol mais "
                "inesquecível da Serra da Mantiqueira. Visitar o Cruzeiro é vivenciar a alma "
                "acolhedora da cidade e valorizar o turismo mais genuíno que temos."
            ),
            imagem_path="assets/IMAGENS_SRS/morro.png",
            foto_popup_path="assets/IMAGENS_SRS/img_morro.png",
            qr_path="assets/IMAGENS_SRS/qr_morro.png",
        ),
        PontoTuristico(
            nome="GAAU - Galeria Aberta de Arte Urbana",
            x=960, y=490,
            curiosidade=(
                "Às margens do Rio Sapucaí, na região conhecida como Beira Rio, a "
                "GAAU transforma os muros da cidade em um museu a céu aberto. "
                "Grafites e murais de artistas locais e convidados ocupam o espaço, "
                "misturando arte urbana contemporânea com a paisagem ribeirinha — "
                "um retrato da veia criativa que também faz parte da identidade de "
                "Santa Rita do Sapucaí."
            ),
            imagem_path="assets/IMAGENS_SRS/ponto.png",
            foto_popup_path="assets/IMAGENS_SRS/img_gaau.png",
            qr_path="assets/IMAGENS_SRS/qr_gaau.png",
        ),
        PontoTuristico(
            nome="Rampa de Voo Livre",
            x=80, y=780,
            curiosidade=(
                "Na Serra do Paredão, na divisa com São Sebastião da Bela Vista, "
                "fica uma das rampas de voo livre mais respeitadas do país. Suas "
                "condições aerológicas estão entre as melhores do Brasil, atraindo "
                "praticantes de parapente e asa-delta que colorem o céu e enxergam "
                "o vale inteiro lá de cima — um lado mais radical do turismo de "
                "Santa Rita do Sapucaí."
            ),
            imagem_path="assets/IMAGENS_SRS/ponto.png",
            foto_popup_path="assets/IMAGENS_SRS/img_voo.png",
            qr_path="assets/IMAGENS_SRS/qr_voo.png",
        ),
        PontoTuristico(
            nome="Parque Mun. Natural Dr. Cyro de Luna Dias",
            x=1450, y=700,
            curiosidade=(
                "Vizinho da Reserva Biológica Mítzi Brandão, no bairro Piedade, este "
                "parque preserva remanescentes de Mata Atlântica e conta com um "
                "viveiro de mudas próprio. É um espaço pensado para educação "
                "ambiental, lazer e conservação — a prova de que Santa Rita cuida "
                "tanto da sua história quanto da natureza que a cerca."
            ),
            imagem_path="assets/IMAGENS_SRS/ponto.png",
            foto_popup_path="assets/IMAGENS_SRS/img_parque.png",
            qr_path="assets/IMAGENS_SRS/qr_parque.png",
        ),
        PontoTuristico(
            nome="REBIO - Reserva Biológica Profª. Dra. Mítzi",
            x=1480, y=120,
            curiosidade=(
                "Com mais de 300 hectares de Mata Atlântica preservada, a Reserva "
                "Biológica Mítzi Brandão foi criada em 1980 e protege, há quase 80 "
                "anos, os mananciais que abastecem a cidade. Por ser uma área de "
                "preservação integral, a visitação é restrita a fins educacionais — "
                "um verdadeiro cofre ecológico do Sul de Minas."
            ),
            imagem_path="assets/IMAGENS_SRS/ponto.png",
            foto_popup_path="assets/IMAGENS_SRS/img_rebio.png",
            qr_path="assets/IMAGENS_SRS/qr_rebio.png",
        ),
    ]