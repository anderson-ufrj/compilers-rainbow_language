📐 Requisitos Técnicos — Compilador Rainbow
🧠 Visão Geral
O projeto Rainbow é um compilador educacional que realiza análise léxica, sintática e semântica de programas escritos em uma linguagem própria. Ele conta com uma interface gráfica amigável e suporta a análise automática de arquivos de exemplo, gerando saídas correspondentes.

📁 Estrutura do Projeto
```
compilers-rainbow_language/
├── src/                            # Código-fonte
│   └── analisador_lexico.py        # Implementação do scanner
├── tests/                          # Arquivos de teste
│   ├── teste1.rainbow              # Programa válido de teste
│   ├── teste2.rainbow              # Teste de detecção de erros
│   └── teste3.rainbow              # Teste abrangente de funcionalidades
├── docs/
│   ├── Requisitos Técnicos.md      # Este documento
│   └── 🌈Rainbow✨ - Compiladores.pdf  # Documentação da linguagem
├── CLAUDE.md                       # Guia para Claude Code
├── README.md                       # Documentação principal
└── .gitignore                      # Arquivos ignorados pelo git
```
🔧 Requisitos Funcionais
🧾 Análise Léxica
 Leitura do arquivo .rainbow

 Ignorar espaços em branco, quebras de linha e tabulações

 Identificar corretamente:

Palavras-chave

Identificadores

Números inteiros e reais

Strings e caracteres

Símbolos e operadores

 Detectar erros léxicos:

Caracteres inválidos (@)

Identificadores inválidos (1var, j@)

Números mal formados (2.a3)

Comentários não fechados { ...

Strings não terminadas ("exemplo)

 Exibir erros com linha, coluna, tipo e lexema

🧮 Análise Sintática
 Validar a sequência de tokens conforme regras gramaticais

 Detectar:

Blocos ou expressões não fechadas ({, (, " etc.)

Comandos fora de ordem

Operadores mal utilizados

 Exibir erros com contexto, linha e coluna

🧠 Análise Semântica
 Verificar:

Declaração prévia de variáveis

Tipos compatíveis em operações e atribuições

Escopo e visibilidade de variáveis

Duplicidade de identificadores

 Manter tabela de símbolos (nome, tipo, escopo, linha/coluna)

 Gerar relatórios de erro semântico

⚙️ Execução dos Arquivos de Exemplo
 O compilador deve processar automaticamente cada arquivo .rainbow da pasta tests/ e gerar:

Um arquivo .tokens com a listagem de tokens encontrados

Um arquivo .errors com os erros léxicos/sintáticos/semânticos, se houver

 Cada saída deve seguir o padrão:

Exemplo: teste1.tokens

ruby
Copiar
Editar
Linha: 1 - Coluna: 1 - Token:<PalavraChave, program>
Linha: 1 - Coluna: 9 - Token:<Identificador, exemplo>
...
Exemplo: teste1.errors

nginx
Copiar
Editar
Erro Léxico - Linha 2, Coluna 4: Símbolo inválido '@'
Erro Sintático - Linha 3, Coluna 10: Esperado 'fim', encontrado 'se'
🖥️ Requisitos da Interface Gráfica
 Deve permitir:

Abrir arquivo .rainbow

Salvar código modificado

Listar tokens

Executar análise sintática

Executar análise semântica

Limpar tela

Sair do programa

 Exibir:

Lista de tokens com tipo, linha, coluna e lexema

Lista de erros destacados em cor (vermelho, amarelo, etc.)

 (Opcional): visualização da árvore sintática em modo textual ou gráfico

🛠️ Requisitos Não Funcionais
Linguagem: Python 3.10+

Interface: Tkinter ou PyQt5 (preferencialmente Tkinter)

IDE utilizada: PyCharm / VSCode / Thonny

Estilo visual limpo, responsivo e acessível

📄 Documentação de Entrega
No .pdf explicativo, incluir:

Qual IDE e linguagem foi utilizada

Como rodar o projeto passo a passo

Regras gramaticais adotadas

Tabela de símbolos (estrutura explicada)

Exemplos dos principais erros tratados

Prints da interface gráfica (opcional, mas recomendado)
