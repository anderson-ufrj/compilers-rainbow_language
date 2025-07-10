# 📐 Requisitos Técnicos — Rainbow IDE & Compilador

## 🧠 Visão Geral

O projeto Rainbow é um **ambiente de desenvolvimento integrado (IDE) completo** com compilador educacional que implementa todas as fases de compilação para a linguagem Rainbow. O sistema realiza análise léxica, sintática, semântica e oferece interpretação direta de programas, proporcionando uma experiência completa de desenvolvimento.

### 🎯 Objetivos do Sistema

- **IDE Moderna**: Interface gráfica intuitiva com recursos profissionais
- **Compilador Completo**: Implementação de todas as fases de compilação
- **Interpretador Integrado**: Execução direta de programas Rainbow
- **Fins Educacionais**: Demonstração prática dos conceitos de compiladores
- **Linguagem Portuguesa**: Sintaxe em português para facilitar aprendizado

## 📁 Estrutura Atual do Projeto

```
compilers-rainbow_language/
├── main.py                         # Rainbow IDE (Interface Principal)
├── run.sh                          # Script de execução
├── src/                            # Código-fonte do compilador
│   ├── analisador_lexico.py        # Análise léxica completa
│   ├── analisador_sintatico.py     # Análise sintática + AST
│   ├── analisador_semantico.py     # Análise semântica + tabela símbolos
│   ├── interpretador_rainbow.py    # Interpretador da linguagem
│   └── compilador_rainbow.py       # Integrador das fases
├── exemplos/                       # Programas demonstrativos
│   ├── ola_mundo.rainbow           # Primeiro programa
│   ├── calculadora.rainbow         # Operações matemáticas
│   ├── tabuada.rainbow             # Laços de repetição
│   ├── condicional.rainbow         # Estruturas condicionais
│   ├── laco_para.rainbow           # Diferentes loops
│   ├── tipos_dados.rainbow         # Tipos de dados
│   └── entrada_usuario.rainbow     # Interação com usuário
├── tests/                          # Arquivos de teste
│   ├── teste1.rainbow              # Programa válido
│   ├── teste2.rainbow              # Detecção de erros
│   └── teste3.rainbow              # Teste abrangente
├── docs/                           # Documentação técnica
│   ├── Requisitos Técnicos.md      # Este documento
│   ├── arquitetura-sistema.md      # Arquitetura do sistema
│   ├── guia-usuario-ide.md         # Manual do usuário
│   ├── interpretador-rainbow.md    # Documentação do interpretador
│   ├── instalacao-configuracao.md  # Guia de instalação
│   ├── linguagem-rainbow.md        # Especificação da linguagem
│   ├── exemplos-rainbow.md         # Guia dos exemplos
│   └── gramatica-rainbow.md        # Gramática formal
├── README.md                       # Documentação principal
└── .gitignore                      # Arquivos ignorados
```
## 🔧 Requisitos Funcionais

### 🌈 Rainbow IDE - Interface Gráfica

#### ✅ **Funcionalidades Implementadas**

**Editor de Código:**
- ✅ Syntax highlighting em tempo real para linguagem Rainbow
- ✅ Numeração de linhas automática
- ✅ Sistema de temas (claro/escuro) com troca dinâmica
- ✅ Abertura e salvamento de arquivos `.rainbow`
- ✅ Detecção de modificações no arquivo

**Painel de Resultados:**
- ✅ Aba **Tokens** - Lista completa com posição
- ✅ Aba **AST** - Árvore sintática estruturada
- ✅ Aba **Símbolos** - Tabela de símbolos com escopo
- ✅ Aba **Erros** - Relatórios detalhados por categoria
- ✅ Aba **Console** - Execução interativa de programas

**Barra de Ferramentas:**
- ✅ Botões de ação rápida com ícones intuitivos
- ✅ Execução de todas as fases de análise
- ✅ Interpretação e execução de programas

**Sistema de Menus:**
- ✅ Menu **Arquivo** - Operações básicas de arquivo
- ✅ Menu **Executar** - Todas as análises e interpretação
- ✅ Menu **Exemplos** - 7 programas demonstrativos
- ✅ Menu **Visualizar** - Sistema de temas
- ✅ Menu **Ajuda** - Tutoriais e documentação integrada

### 🧾 Análise Léxica

#### ✅ **Funcionalidades Implementadas**

**Tokenização Completa:**
- ✅ Leitura de arquivos `.rainbow`
- ✅ Identificação de 30+ tipos de tokens
- ✅ Ignorar espaços, quebras de linha e tabulações
- ✅ Rastreamento preciso de posição (linha/coluna)

**Tokens Reconhecidos:**
- ✅ **Palavras-chave**: `RAINBOW`, `se`, `senao`, `para`, `enquanto`, etc.
- ✅ **Identificadores**: Variáveis com prefixo `#` (ex: `#nome`)
- ✅ **Números**: Inteiros e decimais (`42`, `3.14`)
- ✅ **Strings**: Texto entre aspas (`"Olá mundo"`)
- ✅ **Operadores**: Aritméticos, relacionais, lógicos
- ✅ **Símbolos**: Pontuação e delimitadores

**Detecção de Erros:**
- ✅ Caracteres inválidos (`@`, `$`, etc.)
- ✅ Identificadores malformados (`1var`, `j@`)
- ✅ Números inválidos (`2.a3`, `1.2.3`)
- ✅ Comentários não fechados (`// ...`)
- ✅ Strings não terminadas (`"exemplo`)
- ✅ Recuperação automática de erros

**Saídas Geradas:**
- ✅ Arquivo `.tokens` com lista formatada
- ✅ Arquivo `.errors` com erros léxicos
- ✅ Relatórios com linha, coluna e descrição

### 🧮 Análise Sintática

#### ✅ **Funcionalidades Implementadas**

**Parser Recursivo Descendente:**
- ✅ Validação conforme gramática formal da linguagem Rainbow
- ✅ Construção de Árvore Sintática Abstrata (AST)
- ✅ Recuperação automática de erros sintáticos
- ✅ Análise de estruturas aninhadas

**Estruturas Reconhecidas:**
- ✅ **Programa**: Estrutura `RAINBOW.` obrigatória
- ✅ **Variáveis**: Declaração e atribuição com `recebe`
- ✅ **Condicionais**: `se`, `senao`, `senaose` aninhados
- ✅ **Loops**: `para` e `enquanto` com controle
- ✅ **Expressões**: Matemáticas, lógicas e relacionais
- ✅ **Funções**: `mostrar()`, `ler()` com parâmetros

**Detecção de Erros:**
- ✅ Blocos não fechados (`{`, `}`)
- ✅ Parênteses desbalanceados (`(`, `)`)
- ✅ Comandos fora de ordem
- ✅ Operadores mal utilizados
- ✅ Estruturas incompletas

**Saídas Geradas:**
- ✅ Arquivo `.ast` com árvore estruturada
- ✅ Relatórios de erro com contexto
- ✅ Visualização hierárquica na IDE

### 🧠 Análise Semântica

#### ✅ **Funcionalidades Implementadas**

**Verificação de Tipos:**
- ✅ Compatibilidade em operações matemáticas
- ✅ Verificação de atribuições
- ✅ Conversões automáticas quando possível
- ✅ Validação de operadores lógicos

**Análise de Escopo:**
- ✅ **Escopo GLOBAL**: Variáveis do programa principal
- ✅ **Escopo BLOCO**: Variáveis em condicionais
- ✅ **Escopo LACO**: Variáveis em loops
- ✅ Verificação de visibilidade hierárquica

**Tabela de Símbolos:**
- ✅ Nome, tipo, escopo, linha e coluna
- ✅ Detecção de variáveis não declaradas
- ✅ Prevenção de redeclaração
- ✅ Inferência automática de tipos
- ✅ Saída em formato JSON estruturado

**Validações Realizadas:**
- ✅ Declaração prévia de variáveis
- ✅ Duplicidade de identificadores
- ✅ Uso de variáveis fora de escopo
- ✅ Operações com tipos incompatíveis

### ⚡ Interpretador Rainbow

#### ✅ **Funcionalidades Implementadas**

**Execução Interpretada:**
- ✅ Interpretação linha por linha do código fonte
- ✅ Verificação prévia de compilação
- ✅ Execução assíncrona (não trava a interface)
- ✅ Tratamento robusto de erros em tempo de execução

**Entrada Interativa:**
- ✅ Função `ler()` com diálogos gráficos
- ✅ Prompt personalizado para entrada
- ✅ Validação e tratamento de entrada do usuário
- ✅ Threading para comunicação IDE-interpretador

**Operações Suportadas:**
- ✅ **Variáveis**: Declaração e atribuição automática
- ✅ **Expressões**: Matemáticas, lógicas e concatenação
- ✅ **Condicionais**: `se/senao` com blocos aninhados
- ✅ **Loops**: `para` e `enquanto` com controle de fluxo
- ✅ **I/O**: `mostrar()` para saída, `ler()` para entrada

**Limitações de Segurança:**
- ✅ Prevenção de loops infinitos (máx. 1000 iterações)
- ✅ Sandbox de execução (sem acesso ao sistema)
- ✅ Recuperação graceful de erros
- ✅ Timeout automático em operações longas

### ⚙️ Processamento de Arquivos

#### ✅ **Funcionalidades Implementadas**

**Arquivos de Teste e Exemplos:**
- ✅ Processamento automático de arquivos `.rainbow`
- ✅ Geração de saídas estruturadas
- ✅ Validação completa em todas as fases

**Saídas Geradas:**
- ✅ **`.tokens`** - Lista formatada de tokens
- ✅ **`.errors`** - Relatório de erros por categoria
- ✅ **`.ast`** - Árvore sintática estruturada
- ✅ **`.simbolos`** - Tabela de símbolos
- ✅ **`.semantic.json`** - Análise semântica em JSON

**Formato de Saída (Exemplo):**
```
=== RELATÓRIO DE TOKENS ===
Linha: 01 - Coluna: 01 - Token:<RAINBOW, RAINBOW>
Linha: 01 - Coluna: 08 - Token:<FIM_LINHA, .>
Linha: 04 - Coluna: 01 - Token:<VARIAVEL, #nome>
...

=== RELATÓRIO DE ERROS ===
Erro Léxico - Linha 2, Coluna 4: Caractere inválido '@'
Erro Sintático - Linha 3, Coluna 10: Esperado '}', encontrado 'se'
```

### 🖥️ Interface Gráfica - Requisitos Atendidos

#### ✅ **Funcionalidades Básicas Implementadas**

**Operações de Arquivo:**
- ✅ Abrir arquivos `.rainbow` via diálogo
- ✅ Salvar código modificado
- ✅ Salvar como novo arquivo
- ✅ Detecção automática de modificações

**Análises Disponíveis:**
- ✅ Análise léxica individual (F5)
- ✅ Análise sintática completa (F6)
- ✅ Análise semântica integrada (F7)
- ✅ Compilação completa (F8)
- ✅ Execução de programas (Ctrl+R)

**Visualizações:**
- ✅ Lista de tokens detalhada com posicionamento
- ✅ Árvore sintática hierárquica
- ✅ Tabela de símbolos com escopo
- ✅ Relatórios de erro categorizados e destacados
- ✅ Console de execução interativo

#### ✅ **Funcionalidades Avançadas Implementadas**

**Interface Moderna:**
- ✅ Sistema de temas profissional
- ✅ Syntax highlighting em tempo real
- ✅ Atalhos de teclado intuitivos
- ✅ Barra de status informativa
- ✅ Animação de abertura

**Usabilidade:**
- ✅ Menu de exemplos integrado
- ✅ Documentação acessível via interface
- ✅ Tooltips e ajuda contextual
- ✅ Organização em abas para resultados

## 🛠️ Requisitos Não Funcionais

### ✅ **Tecnologias Utilizadas**

**Linguagem e Versão:**
- ✅ **Python 3.10+** - Linguagem principal do projeto
- ✅ **Compatibilidade**: Python 3.11 e 3.12 testados

**Interface Gráfica:**
- ✅ **Tkinter** - Biblioteca padrão do Python
- ✅ **Threading** - Execução assíncrona
- ✅ **Canvas** - Animações e elementos gráficos

**Ferramentas de Desenvolvimento:**
- ✅ **VSCode** - IDE principal utilizada
- ✅ **Git** - Controle de versão
- ✅ **GitHub** - Repositório remoto

### ✅ **Qualidades de Software**

**Performance:**
- ✅ **Responsividade**: Interface não trava durante execução
- ✅ **Otimização**: Análise single-pass por fase
- ✅ **Memória**: Uso eficiente com limpeza automática

**Usabilidade:**
- ✅ **Interface Intuitiva**: Menus organizados e ícones claros
- ✅ **Feedback Visual**: Destacamento de erros e syntax highlighting
- ✅ **Acessibilidade**: Temas claro/escuro para conforto visual
- ✅ **Atalhos**: Teclas de acesso rápido para funções principais

**Confiabilidade:**
- ✅ **Recuperação de Erros**: Sistema não quebra com código inválido
- ✅ **Validação**: Verificação prévia antes da execução
- ✅ **Sandbox**: Execução segura sem riscos ao sistema

**Manutenibilidade:**
- ✅ **Código Modular**: Separação clara de responsabilidades
- ✅ **Documentação**: Comentários e documentação técnica
- ✅ **Padrões**: Seguimento de convenções Python

### ✅ **Compatibilidade**

**Sistemas Operacionais:**
- ✅ **Linux** (Ubuntu, Fedora, Debian)
- ✅ **Windows** 10/11
- ✅ **macOS** 10.14+

**Dependências:**
- ✅ **Tkinter** (incluído no Python padrão)
- ✅ **Bibliotecas padrão**: threading, os, json, subprocess
- ✅ **Sem dependências externas** - facilita distribuição

## 📄 Documentação Técnica Completa

### ✅ **Documentação Entregue**

**Documentação do Sistema:**
- ✅ **README.md** - Visão geral e guia de início rápido
- ✅ **Requisitos Técnicos.md** - Este documento técnico
- ✅ **Arquitetura do Sistema** - Estrutura detalhada dos componentes
- ✅ **Guia do Usuário** - Manual completo da IDE

**Documentação da Linguagem:**
- ✅ **Especificação da Linguagem Rainbow** - Sintaxe completa
- ✅ **Gramática Formal** - Regras gramaticais implementadas
- ✅ **Exemplos Comentados** - Guia dos programas demonstrativos

**Documentação Técnica:**
- ✅ **Interpretador Rainbow** - Detalhes de implementação
- ✅ **Instalação e Configuração** - Guia completo de setup
- ✅ **Estrutura de Código** - Organização e arquitetura

### ✅ **Conteúdos Técnicos Documentados**

**Informações do Projeto:**
- ✅ **IDE Utilizada**: VSCode com extensões Python
- ✅ **Linguagem**: Python 3.10+ com Tkinter
- ✅ **Execução**: `python3 main.py` ou script `run.sh`

**Implementação Técnica:**
- ✅ **Gramática**: Recursivo descendente baseada na especificação
- ✅ **Tabela de Símbolos**: Estrutura hierárquica com escopo
- ✅ **Tratamento de Erros**: 20+ tipos de erro classificados
- ✅ **Interface**: Screenshots e guia visual completo

**Casos de Teste:**
- ✅ **Programas Válidos**: 7 exemplos funcionais
- ✅ **Detecção de Erros**: Casos de teste para cada tipo de erro
- ✅ **Cenários Complexos**: Estruturas aninhadas e escopo

### 📊 **Estatísticas do Projeto**

**Código Fonte:**
- **Linhas de Código**: ~3.500 linhas
- **Arquivos Python**: 10 arquivos principais
- **Exemplos Rainbow**: 7 programas demonstrativos
- **Documentação**: 8 arquivos markdown detalhados

**Funcionalidades:**
- **Tokens Reconhecidos**: 30+ tipos diferentes
- **Estruturas Sintáticas**: 15+ construções da linguagem
- **Tipos de Erro**: 20+ categorias de erro tratadas
- **Atalhos de Teclado**: 10+ combinações implementadas

---

## 🎯 Status de Conclusão

### ✅ **100% IMPLEMENTADO**

Todos os requisitos técnicos foram **completamente atendidos** e **superados**:

- ✅ **Análise Léxica** - Implementação completa com recuperação de erros
- ✅ **Análise Sintática** - Parser recursivo com construção de AST
- ✅ **Análise Semântica** - Verificação de tipos e escopo
- ✅ **Interface Gráfica** - IDE moderna com recursos avançados
- ✅ **Interpretador** - Execução completa de programas Rainbow
- ✅ **Documentação** - Documentação técnica completa e detalhada

**O projeto Rainbow IDE representa uma implementação educacional completa e profissional de um sistema de compilação, atendendo e superando todos os requisitos técnicos estabelecidos.**
