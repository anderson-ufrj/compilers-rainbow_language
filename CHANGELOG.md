# 📝 Changelog - Rainbow IDE

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Planejado
- [ ] Suporte a funções definidas pelo usuário
- [ ] Arrays/Listas com indexação
- [ ] Estruturas de dados (registros)
- [ ] Sistema de módulos e imports
- [ ] Debugger passo a passo
- [ ] Otimizações de performance (JIT)

## [1.0.0] - 2024-12-10

### ✨ Adicionado - Versão Completa
- **Rainbow IDE** completa com interface gráfica moderna
- **Sistema de Temas** (claro e escuro) com troca dinâmica
- **Interpretador Rainbow** com execução interativa
- **Análise Semântica** completa com verificação de tipos
- **Entrada Interativa** via diálogos gráficos
- **7 Exemplos** demonstrativos da linguagem
- **Syntax Highlighting** em tempo real
- **Console Integrado** para execução de programas
- **Documentação Completa** do sistema

### 🛠️ Técnico
- Interpretador com suporte a todas as estruturas Rainbow
- Verificação prévia de compilação antes da execução
- Threading para execução assíncrona
- Tratamento robusto de erros
- Sistema de callbacks para entrada do usuário

### 📚 Exemplos Inclusos
1. **ola_mundo.rainbow** - Primeiro programa
2. **calculadora.rainbow** - Operações matemáticas
3. **tabuada.rainbow** - Laços de repetição
4. **condicional.rainbow** - Estruturas condicionais
5. **laco_para.rainbow** - Diferentes tipos de loops
6. **tipos_dados.rainbow** - Demonstração de tipos
7. **entrada_usuario.rainbow** - Interação com usuário

## [0.3.0] - 2024-11-25

### ✨ Adicionado - Análise Semântica
- **Analisador Semântico** completo (`src/analisador_semantico.py`)
- **Tabela de Símbolos** hierárquica com escopo
- **Verificação de Tipos** (NUMERO, TEXTO, LOGICO)
- **Análise de Escopo** (GLOBAL, BLOCO, LACO)
- **Detecção de Variáveis** não declaradas
- **Saída JSON** estruturada (`.semantic.json`)

### 🔧 Melhorado
- Integração completa na Rainbow IDE
- Aba "Símbolos" no painel de resultados
- Relatórios de erro semântico detalhados
- Atalho F7 para análise semântica

### 🐛 Corrigido
- Escopo de variáveis em estruturas aninhadas
- Validação de tipos em operações matemáticas
- Detecção de redeclaração de variáveis

## [0.2.0] - 2024-11-20

### ✨ Adicionado - Análise Sintática
- **Analisador Sintático** completo (`src/analisador_sintatico.py`)
- **Parser Recursivo Descendente** baseado na gramática
- **Construção de AST** (Árvore Sintática Abstrata)
- **Detecção de Erros Sintáticos** com recuperação
- **Aba AST** na Rainbow IDE
- **Saída estruturada** da árvore sintática

### 🔧 Melhorado
- Interface da IDE com aba dedicada para AST
- Relatórios de erro mais detalhados
- Atalhos F6 para análise sintática
- Integração com análise léxica

### 📝 Documentação
- Gramática formal da linguagem Rainbow
- Exemplos de estruturas sintáticas
- Documentação do parser

## [0.1.0] - 2024-11-15

### ✨ Adicionado - Fundação do Projeto
- **Rainbow IDE** inicial com interface Tkinter
- **Analisador Léxico** completo (`src/analisador_lexico.py`)
- **30+ Tipos de Tokens** definidos
- **Sistema de Temas** claro e escuro
- **Syntax Highlighting** básico
- **Detecção de Erros Léxicos** com recuperação
- **Exemplos Iniciais** da linguagem Rainbow

### 🎨 Interface
- Editor de código com números de linha
- Painel de resultados com abas
- Barra de ferramentas com ícones
- Sistema de status na parte inferior

### 📊 Funcionalidades
- Abertura e salvamento de arquivos `.rainbow`
- Análise léxica com geração de tokens
- Relatórios de erro detalhados
- Atalhos de teclado intuitivos

### 🔧 Técnico
- Tokenização caractere por caractere
- Rastreamento preciso de posição (linha/coluna)
- Recuperação automática de erros
- Geração de arquivos `.tokens` e `.errors`

## [0.0.1] - 2024-11-10

### ✨ Primeira Release - Prova de Conceito
- **Estrutura Inicial** do projeto
- **Análise Léxica** básica
- **Tokens Fundamentais** da linguagem Rainbow
- **Interface Mínima** para desenvolvimento

### 📋 Definições Base
- Palavras-chave da linguagem Rainbow
- Operadores básicos
- Tipos de dados primitivos
- Estrutura de programa

---

## 📈 Estatísticas de Desenvolvimento

### Evolução do Código
| Versão | Linhas de Código | Arquivos | Funcionalidades |
|--------|-----------------|----------|-----------------|
| 0.0.1  | ~500 linhas     | 3 arquivos | Léxica básica |
| 0.1.0  | ~1.200 linhas   | 5 arquivos | IDE + Léxica completa |
| 0.2.0  | ~2.000 linhas   | 7 arquivos | + Sintática |
| 0.3.0  | ~2.800 linhas   | 8 arquivos | + Semântica |
| 1.0.0  | ~3.500 linhas   | 10 arquivos | + Interpretador |

### Marcos Importantes
- **Nov 2024**: Início do desenvolvimento
- **Nov 15**: Primeira interface gráfica
- **Nov 20**: Parser recursivo funcionando
- **Nov 25**: Análise semântica completa
- **Dez 10**: Interpretador e versão final

## 🏆 Funcionalidades por Versão

### v0.1.0 - Fundação
- ✅ Análise léxica completa
- ✅ Interface gráfica básica
- ✅ Sistema de temas
- ✅ Syntax highlighting

### v0.2.0 - Estrutura
- ✅ Análise sintática
- ✅ Construção de AST
- ✅ Detecção de erros sintáticos
- ✅ Visualização de árvore

### v0.3.0 - Semântica
- ✅ Verificação de tipos
- ✅ Análise de escopo
- ✅ Tabela de símbolos
- ✅ Validação semântica

### v1.0.0 - Execução
- ✅ Interpretador completo
- ✅ Entrada interativa
- ✅ Execução de programas
- ✅ Exemplos funcionais

## 🔮 Roadmap Futuro

### v1.1.0 - Melhorias (Planejado)
- [ ] Sistema de breakpoints
- [ ] Debugger visual
- [ ] Otimização de loops
- [ ] Exportação para outras linguagens

### v1.2.0 - Expansão (Planejado)
- [ ] Suporte a arquivos
- [ ] Bibliotecas padrão
- [ ] Sistema de packages
- [ ] IDE plugins

### v2.0.0 - Profissional (Futuro)
- [ ] Compilação nativa
- [ ] Geração de código de máquina
- [ ] Otimizações avançadas
- [ ] Deploy de aplicações

## 🤝 Contribuições

### Desenvolvedores Principais
- **Anderson Henrique da Silva** - Arquitetura e implementação
- **Lurian Letícia dos Reis** - Interface e documentação

### Orientação Acadêmica
- **Professor Hudson** - IFSULDEMINAS Campus Muzambinho
- **Disciplina:** Compiladores

### Agradecimentos Especiais
- [Claude Code](https://claude.ai/code) - Assistência no desenvolvimento
- Comunidade Python - Ferramentas e bibliotecas
- IFSULDEMINAS - Infraestrutura e apoio

---

## 📋 Notas de Versão

### Convenções de Versionamento
- **Major** (X.0.0): Mudanças incompatíveis
- **Minor** (0.X.0): Funcionalidades novas compatíveis
- **Patch** (0.0.X): Correções de bugs

### Tags Git
- `v1.0.0` - Release completa
- `v0.3.0` - Análise semântica
- `v0.2.0` - Análise sintática
- `v0.1.0` - Análise léxica + IDE

### Branches
- `main` - Código estável
- `develop` - Desenvolvimento ativo
- `feature/*` - Funcionalidades específicas

### Processo de Release
1. Desenvolvimento em `feature/nome`
2. Merge para `develop`
3. Testes e validação
4. Merge para `main`
5. Tag da versão
6. Atualização do CHANGELOG

---

*Este changelog é mantido pelos desenvolvedores do projeto Rainbow IDE e reflete o progresso educacional da disciplina de Compiladores.*