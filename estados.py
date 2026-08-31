import pygame
import funcoes

caminhos_mapas = {
    "Acre": "assets/MAPAS/mapAcre.png",
    "Alagoas": "assets/MAPAS/mapAlagoas.png",
    "Amapá": "assets/MAPAS/mapAmapa.png",
    "Amazonas": "assets/MAPAS/mapAmazonas.png",
    "Bahia": "assets/MAPAS/mapBahia.png",
    "Ceará": "assets/MAPAS/mapCeara.png",
    "Espírito Santo": "assets/MAPAS/mapEspiritoSanto.png",
    "Goiás": "assets/MAPAS/mapGoias.png",
    "Maranhão": "assets/MAPAS/mapMaranhao.png",
    "Mato Grosso": "assets/MAPAS/mapMatoG.png",
    "Mato Grosso do Sul": "assets/MAPAS/mapMatoGSul.png",
    "Minas Gerais": "assets/MAPAS/mapMinas.png",
    "Pará": "assets/MAPAS/mapPara.png",
    "Paraíba": "assets/MAPAS/mapParaiba.png",
    "Paraná": "assets/MAPAS/mapParana.png",
    "Pernambuco": "assets/MAPAS/mapPernambuco.png",
    "Piauí": "assets/MAPAS/mapPiaui.png",
    "Rio Grande do Norte": "assets/MAPAS/mapRioGrandeNorte.png",
    "Rio Grande do Sul": "assets/MAPAS/mapRioGrandeSul.png",
    "Rio de Janeiro": "assets/MAPAS/mapRJ.png",
    "Rondônia": "assets/MAPAS/mapRondonia.png",
    "Roraima": "assets/MAPAS/mapRoraima.png",
    "Santa Catarina": "assets/MAPAS/mapSantaCatarina.png",
    "São Paulo": "assets/MAPAS/mapSaoPaulo.png",
    "Sergipe": "assets/MAPAS/mapSergipe.png",
    "Tocantins": "assets/MAPAS/mapTocantins.png",
    "Distrito Federal": "assets/MAPAS/mapDistrito.png"
}

mapas_carregados = {}

def obter_mapa(nome_estado):
    if nome_estado not in mapas_carregados:
        caminho = caminhos_mapas[nome_estado]
        mapas_carregados[nome_estado] = pygame.image.load(funcoes.resource_path(caminho)).convert_alpha()

    return mapas_carregados[nome_estado]