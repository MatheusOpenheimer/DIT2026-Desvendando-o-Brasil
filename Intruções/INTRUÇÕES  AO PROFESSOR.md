GUIA PARA CADASTRAR PERGUNTAS E GERENCIAR DADOS
Instruções para estruturar, editar e adicionar conteúdos aos arquivos de texto (.txt) do jogo, além do gerenciamento dos registros de jogadores.


Estrutura das Pastas e Arquivos de Texto
O projeto divide os arquivos .txt em duas pastas principais:
Pasta dados: Armazena as questões, alternativas, curiosidades, pontos turísticos e interface.
questoes_regioes.txt: Perguntas sobre as 5 regiões do Brasil.
alternativas_estados.txt: Perguntas específicas por Estado.
curiosidades_estados.txt: Textos informativos de cada estado.
srs_pontos.txt: Pontos turísticos e interface em Português.
srs_pontos_en.txt: Pontos turísticos e interface em Inglês.
srs_pontos_esp.txt: Pontos turísticos e interface em Espanhol.

Pasta jogador: Armazena o histórico, notas, pontuações e registros de quem jogou:
ranking_brasil.txt: Dados de pontuação do modo Brasil nome;idade;acertos;erros.
estatisticas_brasil.txt: Registro detalhado de desempenho por estado/região do modo Brasil.
ranking_srs.txt: Registro de pontuação das fases de Santa Rita do Sapucaí.
feedbacks_srs.txt: Comentários, avaliações e registros deixados pelos jogadores com data e hora.

---
1. Como Criar Perguntas por Região (dados/questoes_regioes.txt)
Cada bloco de questão utiliza 3 tags obrigatórias: pergunta:, regiao: e dicas:.
pergunta: O enunciado da questão.
regiao: A resposta correta. Deve ser exatamente uma das 5: Norte, Nordeste, Centro-Oeste, Sudeste ou Sul. (Mantenha maiúsculas e acentos exatamente iguais).
dicas: As dicas mostradas ao jogador, separadas obrigatoriamente por ponto e vírgula (;).
Deixe uma linha em branco entre cada pergunta.
Exemplo:
pergunta: Qual é a região do estado do Amazonas?
regiao: Norte
dicas: Fica localizado na porção noroeste do mapa do Brasil.; Faz fronteira internacional com o Peru e com a Colômbia.; Faz divisa ao sul com o estado de Mato Grosso.

pergunta: Qual é a região do estado de São Paulo?
regiao: Sudeste
dicas: Fica no litoral sul/sudeste, fazendo divisa ao sul com o estado do Paraná.; Faz divisa ao norte com Minas Gerais e a leste com o Rio de Janeiro.; Faz divisa a oeste com o estado de Mato Grosso do Sul.


---
2. Como Criar Perguntas por Estado (dados/alternativas_estados.txt)
Organiza as perguntas por unidade federativa usando as tags: Estado:, pergunta:, opcoes: e correta:.
Estado: Nome do estado (deve bater com os nomes cadastrados no jogo, ex: Acre, São Paulo, Mato Grosso).
pergunta: O enunciado da questão.
opcoes: As 4 alternativas. Separe obrigatoriamente por ponto e vírgula (;). Não use vírgula comum para separar.
correta: O índice numérico da opção certa (começando em 0 para A, 1 para B, 2 para C e 3 para D).
Exemplo:
Estado: Acre
pergunta: Qual é a capital do Acre?
opcoes: A) Rio Branco; B) Cruzeiro do Sul; C) Xapuri; D) Sena Madureira
correta: 0

pergunta: Quem foi Plácido de Castro?
opcoes: A) Um escritor que criou o Festival do Acre.; B) Um presidente que fundou Rio Branco.; C) Um líder ligado à Revolução Acreana.; D) Um explorador que descobriu a Floresta Amazônica.
correta: 2

Estado: Amazonas
pergunta: Qual é a capital do Amazonas?
opcoes: A) Belém; B) Rio Branco; C) Parintins; D) Manaus
correta: 3


---
3. Como Criar as Curiosidades (dados/curiosidades_estados.txt)
Estado: Nome exato do estado cadastrado.
Texto: Escreva o texto corrido logo abaixo da tag Estado:. Pode quebrar linhas normalmente; o jogo une e formata o parágrafo automaticamente na tela.
Exemplo:
Estado: Amazonas
Você chegou ao Amazonas, um estado localizado na Região Norte do Brasil. Sua capital é Manaus, uma cidade que cresceu muito durante o chamado Ciclo da Borracha...

Estado: Acre
Você chegou ao Acre, um estado localizado no extremo oeste da Região Norte do Brasil. Sua capital é Rio Branco, cidade que recebeu esse nome em homenagem ao Barão do Rio Branco...


---
4. Modo Santa Rita do Sapucaí (srs_pontos.txt, srs_pontos_en.txt, srs_pontos_esp.txt)
Este modo possui arquivos dedicados para cada idioma (pt para Português, en para Inglês e esp para Espanhol). A estrutura utiliza marcações entre colchetes ([...]).
A) Bloco de Configurações de Interface ([INTERFACE])
Define os textos dos botões e avisos na tela:
Escreva [INTERFACE] no início do bloco.
Cada linha deve seguir o padrão chave: valor.
Exemplo:

[INTERFACE]
pular: PULAR
contador: Pontos Visitados:
qr_aviso: Escaneie o QR
instrucao: Pressione [ESPAÇO] ou [ENTER] para fechar


B) Blocos dos Pontos Turísticos ([ID_DO_PONTO]) os id's devem seguir exatamente os que estão no texto dentro de [] sem alterar nada

Cada atração possui sua própria chave entre colchetes em maiúsculas:
Linha 1 (logo abaixo do colchete): Nome da atração que aparecerá no título.
Demais linhas: O texto explicativo sobre o local (pode quebrar linhas livremente).
Exemplo:

[SANTUARIO]
Santuário de Santa Rita de Cássia
O Santuário é um dos principais marcos religiosos e históricos do município, atraindo romeiros e devotos de diversas regiões ao longo de todo o ano.

[INATEL]
Instituto Nacional de Telecomunicações - Inatel
Fundado em 1965, o Inatel tornou a cidade um polo tecnológico nacional conhecido como o Vale da Eletrônica, impulsionando a inovação e o ensino de engenharia.


---
Estatísticas, Rankings e Feedback (Pasta jogador)
O sistema não utiliza banco de dados externo ou arquivos .db; todas as informações de usuários são registradas diretamente em arquivos de texto delimitados por ponto e vírgula (;):
Senha de Acesso: Acesso restrito para professores e administradores visualizarem os dados na interface do jogo:
SENHA: faitec

Estrutura dos Arquivos de Jogadores:
ranking_brasil.txt: Registra o histórico das partidas gerais no formato nome;idade;acertos;erros.
estatisticas_brasil.txt: Registra o percentual e taxa de acertos por regiões/etapas de cada jogador (nome;dado1;dado2;...).
ranking_srs.txt: Armazena as pontuações da etapa de Santa Rita do Sapucaí (nome;acertos;erros ou nome;idade;pontos).
feedbacks_srs.txt: Guarda os depoimentos enviados pelos alunos no formato Nome;Instituição;Mensagem;Data e Hora.

Como Zerar os Registros de Jogadores:
Para reiniciar o ranking ou limpar estatísticas antigas, acesse a pasta jogador e abra o arquivo correspondente (como ranking_brasil.txt ou estatisticas_brasil.txt).
Apague todas as linhas de texto de dentro dele e salve o arquivo em branco, ou exclua o arquivo para que o jogo gere um novo limpo automaticamente na próxima partida.

---
Informações Importantes para o Cadastrador
Tags padronizadas: Escreva as palavras-chave exatamente como indicado (pergunta:, regiao:, dicas:, Estado:, opcoes:, correta:, [INTERFACE]).
Codificação UTF-8: Ao salvar qualquer arquivo em editores de texto (Bloco de Notas, Notepad++, VS Code), selecione a codificação UTF-8 para evitar erros em acentos gráficos.
Separador de ponto e vírgula (;): Utilize exclusivamente ; para separar dicas, opções e colunas de dados dos jogadores.
---
Sobre Ocorrências Inesperadas
Caso necessite de configurações personalizadas, ajustes de layout ou auxílio técnico no cadastro dos dados, contate a equipe de desenvolvimento.