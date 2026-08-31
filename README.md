# Desvendando o Brasil – Um Jogo Educativo 100% Seguro

**Desvendando o Brasil** é um jogo de perguntas e respostas desenvolvido em Python/Pygame, com foco no aprendizado de história, cultura e geografia brasileira. Criado com arquitetura modular, o projeto alia engajamento gamificado para os alunos a ferramentas analíticas para a prática pedagógica nas escolas.

---

## 💡 Inovação e Proposta Pedagógica

Alinhado com a extensão comunitária e com os quesitos de avaliação da FAITEC (como *Aplicabilidade*, *Criatividade*, *Inovação* e *Relevância Social*), o projeto se destaca por:

* **Estatísticas para Educadores:** Armazena dados de desempenho por regiões geográficas (Norte, Nordeste, Centro-Oeste, Sudeste e Sul), permitindo aos professores diagnosticar facilidades e pontos de melhoria de cada aluno ou turma.
* **Personalização de Questões:** Sistema estruturado via arquivos de dados locais que permite aos docentes editar e cadastrar novos conjuntos de perguntas e respostas.
* **Integração de Minigames 2D:** Utilização de minigames interativos com movimentação top-down em pixel art para dinamicidade no aprendizado das unidades federativas.

---

## 🛡️ Segurança e Proteção de Dados

O projeto prioriza a privacidade e o bem-estar dos alunos, atendendo a critérios de segurança no ambiente digital:

* **Totalmente Offline:** Não requer conexão com a internet para rodar, eliminando exposição a interações externas.
* **Zero Anúncios e Rastreamento:** Nenhuma exibição de publicidades comerciais ou coleta de dados de navegação.
* **Privacidade Local (SQLite):** Os dados de pontuação e ranking são gravados localmente em um banco de dados SQLite (`GameData.db`), solicitando apenas nome e idade para personalização.
* **Controle de Tempo Nativo:** Possui um temporizador integrado nas fases para estimular o foco e limitar a duração das sessões de jogo.
