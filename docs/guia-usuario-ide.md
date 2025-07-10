# 👨‍💻 Guia do Usuário - Rainbow IDE

## Introdução

A Rainbow IDE é um ambiente de desenvolvimento integrado completo para a linguagem Rainbow. Este guia apresenta todas as funcionalidades disponíveis e como utilizá-las efetivamente.

## 🚀 Iniciando

### Primeira Execução

1. **Abra a IDE:**
   ```bash
   python3 main.py
   ```

2. **Animação de Boas-vindas:**
   - Aguarde a animação do arco-íris (4 segundos)
   - A IDE será carregada automaticamente

3. **Interface Principal:**
   - Editor de código (lado esquerdo)
   - Painel de resultados (lado direito)
   - Toolbar com botões de ação
   - Barra de status na parte inferior

## 🎨 Interface da IDE

### Layout Principal

```
┌─────────────────────────────────────────────────────────────┐
│ 📄 📂 💾 │ ▶️ 🔧 🔤 🌳 ✅            [Toolbar]               │
├─────────────────┬───────────────────────────────────────────┤
│                 │ ┌─ Tokens ─┐ ┌─ AST ─┐ ┌─ Símbolos ─┐     │
│   Editor        │ │           │ │       │ │            │     │
│   de            │ │           │ │       │ │            │     │
│   Código        │ └───────────┘ └───────┘ └────────────┘     │
│                 │ ┌─ Erros ─┐ ┌─ Console ─┐                  │
│  1 │ RAINBOW.   │ │         │ │           │                  │
│  2 │            │ │         │ │           │                  │
│  3 │ #nome...   │ └─────────┘ └───────────┘                  │
└─────────────────┴───────────────────────────────────────────┤
│ 🟢 Pronto              Ln 1, Col 1              🌙           │
└─────────────────────────────────────────────────────────────┘
```

### Componentes Principais

| Componente | Descrição | Localização |
|------------|-----------|-------------|
| **Editor** | Área principal de edição | Lado esquerdo |
| **Números de Linha** | Numeração automática | Coluna esquerda |
| **Painel de Resultados** | Saídas das análises | Lado direito |
| **Toolbar** | Botões de ação rápida | Topo |
| **Status Bar** | Informações do estado | Rodapé |

## 📝 Trabalhando com Arquivos

### Criando um Novo Arquivo

1. **Via Menu:** `Arquivo → Novo` ou `Ctrl+N`
2. **Via Toolbar:** Clique no ícone 📄
3. **Resultado:** Editor limpo pronto para código

### Abrindo Arquivos Existentes

1. **Via Menu:** `Arquivo → Abrir` ou `Ctrl+O`
2. **Via Toolbar:** Clique no ícone 📂
3. **Filtros:** Mostra apenas arquivos `.rainbow`
4. **Resultado:** Arquivo carregado no editor

### Salvando Arquivos

1. **Salvar:** `Arquivo → Salvar` ou `Ctrl+S`
2. **Salvar Como:** `Arquivo → Salvar Como...`
3. **Auto-save:** Antes de executar programas

## 🌈 Exemplos Inclusos

### Acessando Exemplos

Menu `Exemplos` oferece 7 programas prontos:

| Exemplo | Ícone | Finalidade | Conceitos |
|---------|-------|------------|-----------|
| **Olá Mundo** | 👋 | Primeiro programa | Variáveis, saída |
| **Calculadora** | 🧮 | Operações básicas | Aritmética |
| **Tabuada** | 📊 | Laços de repetição | `enquanto` |
| **Condicional** | 🔀 | Estruturas condicionais | `se/senao` |
| **Laço Para** | 🔄 | Diferentes loops | `para` |
| **Tipos de Dados** | 🏷️ | Demonstração de tipos | NUMERO, TEXTO, LOGICO |
| **Entrada do Usuário** | 💬 | Interação | `ler()`, entrada |

### Como Usar os Exemplos

1. **Abrir:** `Exemplos → [Escolher exemplo]`
2. **Estudar:** Leia o código e comentários
3. **Executar:** Pressione `Ctrl+R` ou ▶️
4. **Modificar:** Experimente alterações
5. **Salvar:** Salve suas modificações

## ⚡ Executando Programas

### Opções de Execução

| Ação | Atalho | Botão | Descrição |
|------|--------|-------|-----------|
| **Executar Programa** | `Ctrl+R` | ▶️ | Execução completa |
| **Análise Léxica** | `F5` | 🔤 | Apenas tokens |
| **Análise Sintática** | `F6` | 🌳 | Tokens + AST |
| **Análise Semântica** | `F7` | ✅ | Análise completa |
| **Compilação Completa** | `F8` | 🔧 | Todas as fases |

### Fluxo de Execução

1. **Preparação:**
   - Arquivo é salvo automaticamente
   - Console é limpo
   - Aba Console é selecionada

2. **Compilação:**
   - Verificação de erros léxicos/sintáticos
   - Se houver erros, execução é interrompida

3. **Execução:**
   - Interpretação linha por linha
   - Interação via diálogos para `ler()`
   - Saída mostrada no console

4. **Finalização:**
   - Mensagem de sucesso ou erro
   - Resultados disponíveis nas abas

## 🎯 Análises Disponíveis

### 1. Análise Léxica (F5)

**Objetivo:** Tokenização do código

**Saídas:**
- **Aba Tokens:** Lista completa de tokens
- **Aba Erros:** Erros léxicos encontrados

**Exemplo de Token:**
```
Linha: 01 - Coluna: 01 - Token:<RAINBOW, RAINBOW>
Linha: 04 - Coluna: 01 - Token:<VARIAVEL, #nome>
```

### 2. Análise Sintática (F6)

**Objetivo:** Construção da árvore sintática

**Saídas:**
- **Aba AST:** Árvore sintática abstrata
- **Aba Erros:** Erros sintáticos

**Exemplo de AST:**
```
PROGRAMA: RAINBOW (L:1, C:1)
  ATRIBUICAO: #nome (L:4, C:1)
    CHAMADA_FUNCAO: ler (L:4, C:14)
```

### 3. Análise Semântica (F7)

**Objetivo:** Verificação de tipos e escopo

**Saídas:**
- **Aba Símbolos:** Tabela de símbolos
- **Aba Erros:** Erros semânticos

**Exemplo de Símbolo:**
```
✓ #nome | Tipo: TEXTO | Escopo: GLOBAL | Linha: 04, Coluna: 01
```

## 🎨 Sistema de Temas

### Temas Disponíveis

| Tema | Ícone | Características |
|------|-------|-----------------|
| **Escuro** | 🌙 | Fundo escuro, texto claro |
| **Claro** | ☀️ | Fundo claro, texto escuro |

### Mudando o Tema

1. **Via Menu:** `Visualizar → Tema → [Escolher]`
2. **Resultado:** Interface atualizada instantaneamente
3. **Persistência:** Tema é mantido entre sessões

### Cores por Tema

#### Tema Escuro (Padrão)
- **Background:** Cinza escuro
- **Texto:** Branco
- **Keywords:** Azul claro
- **Strings:** Laranja
- **Comentários:** Verde

#### Tema Claro
- **Background:** Branco/Cinza claro
- **Texto:** Preto
- **Keywords:** Azul escuro
- **Strings:** Vermelho escuro
- **Comentários:** Verde escuro

## 🔍 Syntax Highlighting

### Elementos Coloridos

| Elemento | Cor (Escuro) | Cor (Claro) | Exemplo |
|----------|-------------|-------------|---------|
| **Palavras-chave** | Azul claro | Azul escuro | `RAINBOW`, `se`, `para` |
| **Strings** | Laranja | Vermelho escuro | `"Olá mundo"` |
| **Comentários** | Verde | Verde escuro | `// Comentário` |
| **Números** | Verde claro | Verde | `42`, `3.14` |
| **Variáveis** | Azul claro | Azul | `#nome`, `#idade` |
| **Erros** | Fundo vermelho | Fundo vermelho | Tokens inválidos |

### Atualização Automática

- **Em tempo real:** Cores aplicadas enquanto digita
- **Validação:** Erros destacados automaticamente
- **Performance:** Otimizado para arquivos grandes

## 💬 Entrada Interativa

### Função `ler()`

```rainbow
#nome recebe ler("Digite seu nome: ").
```

**Comportamento:**
1. **Pausa execução** no comando `ler()`
2. **Abre diálogo** com o prompt especificado
3. **Aguarda entrada** do usuário
4. **Continua execução** com valor digitado

### Diálogos de Entrada

- **Aparência:** Janela modal centralizada
- **Validação:** Aceita qualquer texto
- **Cancelamento:** ESC ou botão cancelar retorna string vazia
- **Histórico:** Entrada mostrada no console

## 📊 Visualização de Resultados

### Aba Tokens

**Conteúdo:**
- Lista numerada de todos os tokens
- Posição exata (linha, coluna)
- Tipo e valor do token

**Exemplo:**
```
=== RELATÓRIO DE TOKENS ===
Linha: 01 - Coluna: 01 - Token:<RAINBOW, RAINBOW>
Linha: 01 - Coluna: 08 - Token:<FIM_LINHA, .>
```

### Aba AST

**Conteúdo:**
- Árvore sintática hierárquica
- Estrutura de nós e filhos
- Posições no código fonte

### Aba Símbolos

**Conteúdo:**
- Todas as variáveis declaradas
- Tipos inferidos automaticamente
- Escopo de cada símbolo

### Aba Erros

**Conteúdo:**
- Lista de todos os erros encontrados
- Categoria (léxico, sintático, semântico)
- Posição exata do erro

### Aba Console

**Conteúdo:**
- Saída da execução do programa
- Interações com usuário
- Mensagens de status

## ⌨️ Atalhos de Teclado

### Arquivo
- `Ctrl+N` - Novo arquivo
- `Ctrl+O` - Abrir arquivo
- `Ctrl+S` - Salvar arquivo
- `Ctrl+Q` - Sair da aplicação

### Execução
- `Ctrl+R` - Executar programa
- `F5` - Análise léxica
- `F6` - Análise sintática
- `F7` - Análise semântica
- `F8` - Compilação completa

### Navegação
- `Ctrl+G` - Ir para linha
- `Ctrl+F` - Buscar (futuro)
- `Ctrl+Z` - Desfazer
- `Ctrl+Y` - Refazer

## 🛠️ Dicas de Uso

### Boas Práticas

1. **Comece com exemplos** para entender a sintaxe
2. **Use comentários** para documentar seu código
3. **Teste frequentemente** com `Ctrl+R`
4. **Observe os erros** na aba específica
5. **Experimente temas** para encontrar sua preferência

### Solução de Problemas

#### Programa não executa
- ✅ Verifique se arquivo foi salvo
- ✅ Observe erros na aba Erros
- ✅ Certifique-se que começa com `RAINBOW.`

#### Entrada não funciona
- ✅ Use sintaxe correta: `ler("prompt")`
- ✅ Digite algo na caixa de diálogo
- ✅ Não cancele o diálogo

#### Syntax highlighting não atualiza
- ✅ Digite espaço ou nova linha
- ✅ Reabra o arquivo
- ✅ Reinicie a IDE

### Limitações Conhecidas

- **Recursão:** Não suportada
- **Arquivos:** Sem leitura/escrita de arquivos
- **Rede:** Sem operações de rede
- **Loops:** Máximo 1000 iterações

## 📈 Monitoramento

### Barra de Status

A barra inferior mostra:

| Elemento | Localização | Informação |
|----------|-------------|------------|
| **Status** | Esquerda | Estado atual da IDE |
| **Posição** | Centro | Linha e coluna do cursor |
| **Tema** | Direita | Indicador visual do tema |

### Indicadores de Estado

- `🟢 Pronto` - IDE aguardando comando
- `🟡 Executando...` - Programa em execução
- `🔴 Erro` - Problema detectado
- `✅ Sucesso` - Operação concluída

---

*Este guia cobre todas as funcionalidades principais da Rainbow IDE. Para informações técnicas detalhadas, consulte a documentação de arquitetura.*