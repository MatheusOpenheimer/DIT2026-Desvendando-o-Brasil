# **GUIA PARA CADASTRAR PERGUNTAS**

Para estruturar e adicionar novas perguntas aos arquivos de texto (.txt).



**Estrutura dos Arquivos de Texto**

O jogo utiliza três arquivos .txt principais localizados na raiz do projeto. Todos são de extrema importância para o funcionamento do jogo, eles que guardam os dados a serem apresentados para o jogador



questoes\_regioes.txt (Perguntas sobre as 5 regiões do Brasil)

alternativas\_estados.txt (Perguntas específicas por Estado)



##### **1. Como Criar Perguntas por Região (questoes\_regioes.txt)**

Cada pergunta de região precisa de 3 tags obrigatórias: **pergunta:, regiao: e dicas:.**



Regras de Formatação:



**pergunta:** O enunciado da questão.



**regiao**: A resposta correta (deve ser: Norte, Nordeste, Centro-Oeste, Sudeste ou Sul). *OBS: siga exatamente a mesma formatação de escrita, letras maiúsculas e minúsculas.*



**dicas:** As 3 dicas mostradas ao jogador, obrigatoriamente separadas por ponto e vírgula (;).



Deixe uma linha em branco entre cada bloco de pergunta.



**Exemplo:**

*pergunta: Qual é a região do estado do Amazonas?*

*regiao: Norte*

*dicas: Fica localizado na porção noroeste do mapa do Brasil.; Faz fronteira internacional com o Peru e com a Colômbia.; Faz divisa ao sul com o estado de Mato Grosso.*



pergunta: Qual é a região do estado de São Paulo?

regiao: Sudeste

dicas: Fica no litoral sul/sudeste, fazendo divisa ao sul com o estado do Paraná.; Faz divisa ao norte com Minas Gerais e a leste com o Rio de Janeiro.; Faz divisa a oeste com o estado de Mato Grosso do Sul.



##### **2. Como Criar Perguntas por Estado (alternativas\_estados.txt)**

Este arquivo organiza as perguntas divididas por cada estado do mapa. Usa 4 tags principais: Estado:, pergunta:, opcoes: e correta:.



**Regras de Formatação:**

**Estado:** O nome do estado (exatamente como consta nas chaves do jogo, como Acre, São Paulo, Mato Grosso).



**pergunta:** O enunciado da questão.



**opcoes:** As 4 alternativas da questão. **ATENÇÃO**: Separe obrigatoriamente cada uma das **4** opções com ponto e vírgula **(;)**. Não use vírgula para separar as opções, pois textos longos podem conter vírgulas e quebrar a leitura, adicione sempre somente 4 alternativas



**correta:** O índice numérico da alternativa correta (começando em 0 para a alternativa A, 1 para a B, 2 para a C e 3 para a D). Indique a correta com o número correspondente a alternativa.



**Exemplo:**

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



##### **3.Como criar as Curiosidades**

**Regras de Formatação:**



**Estado:** Nome exato do estado (deve corresponder exatamente às chaves utilizadas no jogo, como Acre, São Paulo, Mato Grosso, etc.).



**Texto do Estado:** Escreva o texto descritivo logo abaixo da tag Estado:. Você pode usar parágrafos normais e quebras de linha à vontade.



**Separação:** Para começar um novo estado, basta inserir uma nova tag Estado: na linha seguinte.



**Exemplo de Preenchimento:**

Estado: Amazonas

Você chegou ao Amazonas, um estado localizado na Região Norte do Brasil. Sua capital é Manaus, uma cidade que cresceu muito durante o chamado Ciclo da Borracha...



Estado: Acre

Você chegou ao Acre, um estado localizado no extremo oeste da Região Norte do Brasil. Sua capital é Rio Branco, cidade que recebeu esse nome em homenagem ao Barão do Rio Branco...



##### **Dicas para as Curiosidades**



**Nomes dos Estados:** Verifique se o nome após a tag Estado: está escrito exatamente igual ao usado no restante do projeto *(exemplo: Mato Grosso, Distrito Federal, Rio Grande do Norte)*.



**Tamanho dos Textos:** Evite blocos de texto excessivamente longos sem quebra de linha para facilitar a formatação dinâmica dentro das caixas de texto do Jogo.



##### **Informações importantes para o Cadastrador**



**TAGS:** Os textos informativos, antes dos dados que você deseja inserir, devem ser configurados exatamente como está nos exemplos deste documento: ***pergunta, regiao, opcoes, correta, Estado***. As letras maiúsculas, minúsculas e a remoção de acentuação são intencionais e obrigatórias.



**Acentos:** O arquivo deve ser salvo na codificação UTF-8 no seu editor para que os acentos funcionem corretamente no jogo.



**Separadores de Alternativas:** Lembre-se sempre de usar o **;** para dividir as opções de resposta no arquivo de estados e as dicas no arquivo de regiões.



**Quantidade de Alternativas:** Mantenha sempre exatamente 4 alternativas por pergunta no arquivo de estados para corresponder aos 4 botões na interface do jogo.



**Perguntas:** Sempre certifique-se de que tenha questões sobre todos os estados.



**ESTATISTICAS e RANKING**
---

A senha de acesso para estatísticas é uma senha padrão, sendo ela sem espaços ou acentos e com todos os caracteres minúsculos:


**SENHA:** faitec



Para limpar os dados dos jogadores, tanto de estatísticas quanto do ranking, basta apagar o arquivo (GameData) na pasta "dados" do jogo, assim iniciará um novo arquivo limpo, que irá cadastrar os próximos jogadores e informações do zero.





##### **SOBRE OCORRÊNCIAS INESPERADAS**



Caso necessite de configurações personalizadas, ajustes de pontos em desconformidade com sua necessidade ou de ajuda para cadastro, contate um de nossos técnicos.

