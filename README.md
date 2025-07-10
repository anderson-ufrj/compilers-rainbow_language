# 🌈 Rainbow IDE & Compilador

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Completo-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-Academic-green?style=for-the-badge)

Uma IDE completa e compilador para a linguagem de programação Rainbow, desenvolvido para fins educacionais.

**🎓 Projeto Acadêmico - Disciplina de Compiladores**
*IFSULDEMINAS Campus Muzambinho | Professor: Hudson*

</div>

## 📋 Sobre o Projeto

O Rainbow IDE é um ambiente de desenvolvimento integrado completo para a linguagem Rainbow, uma linguagem de programação com sintaxe em português projetada para fins didáticos e educacionais.

### 🎯 Objetivos

- Implementar todas as fases de um compilador educacional
- Criar uma IDE moderna e intuitiva para desenvolvimento
- Demonstrar conceitos de compilação de forma prática
- Fornecer interpretador integrado para execução de programas
- Facilitar o aprendizado de programação em português

### 📊 Status do Desenvolvimento

| Componente | Status | Descrição |
|------------|--------|-----------|
| **Rainbow IDE** | ✅ **Completo** | Interface gráfica moderna com temas |
| **Análise Léxica** | ✅ **Completo** | Tokenização com detecção de erros |
| **Análise Sintática** | ✅ **Completo** | Parser com construção de AST |
| **Análise Semântica** | ✅ **Completo** | Verificação de tipos e escopo |
| **Interpretador** | ✅ **Completo** | Execução interativa de programas |
| **Exemplos** | ✅ **Completo** | 8 programas demonstrativos |

## 🚀 Começando

### Pré-requisitos

- Python 3.10 ou superior
- Tkinter (geralmente incluído com Python)
- PIL/Pillow (para imagens na splash screen)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/anderson-ufrj/compilers-rainbow_language
cd compilers-rainbow_language
```

2. Execute a Rainbow IDE:
```bash
python3 main.py
```

## 💻 Usando a Rainbow IDE

### 🖥️ Interface Principal

A Rainbow IDE oferece uma experiência moderna de desenvolvimento:

- **Editor com Syntax Highlighting** - Cores automáticas para código Rainbow
- **Sistema de Temas** - Modo claro e escuro com paleta GitHub
- **Toolbar Moderna** - Botões organizados por funcionalidade
- **Análise em Tempo Real** - Validação léxica, sintática e semântica
- **Interpretador Integrado** - Execute programas diretamente na IDE
- **Console Interativo** - Entrada e saída em tempo real com suporte ao Enter
- **Splash Screen Animada** - Introdução visual com animações
- **Exemplos Inclusos** - 8 programas prontos para aprender

### ⚡ Funcionalidades Principais

| Funcionalidade | Atalho | Descrição |
|----------------|--------|-----------|
| **Executar Programa** | `F5` ou ▶ | Executa o código atual |
| **Novo Arquivo** | `Ctrl+N` | Cria novo arquivo Rainbow |
| **Abrir Arquivo** | `Ctrl+O` | Abre arquivo .rainbow |
| **Salvar** | `Ctrl+S` | Salva arquivo atual |
| **Análise Léxica** | `F7` | Apenas análise léxica |
| **Análise Sintática** | `F8` | Análise léxica + sintática |
| **Análise Semântica** | `F9` | Análise completa |
| **Compilação Completa** | `F6` | Todas as análises |
| **Alternar Tema** | `Ctrl+T` | Alterna entre claro/escuro |

### 📚 Exemplos Inclusos

Acesse via menu **Exemplos**:

1. **👋 Olá Mundo** - Primeiro programa Rainbow
2. **🧮 Calculadora** - Operações matemáticas básicas
3. **📊 Tabuada** - Laços de repetição
4. **🔀 Condicional** - Estruturas se/senao aninhadas
5. **🔄 Laço Para** - Diferentes tipos de loops
6. **🏷️ Tipos de Dados** - Demonstração de tipos
7. **💬 Entrada do Usuário** - Interação com usuário
8. **🤖 Programa Interativo** - Exemplo completo com validações

## 🌟 Linguagem Rainbow

### Estrutura Básica

Todo programa Rainbow deve começar com:
```rainbow
RAINBOW.
```

### Variáveis

As variáveis são prefixadas com `#`:
```rainbow
#nome recebe "João".
#idade recebe 25.
#ativo recebe Verdadeiro.
```

### Tipos de Dados

- **NUMERO** - Inteiros e decimais (42, 3.14)
- **TEXTO** - Strings ("Olá mundo")
- **LOGICO** - Booleanos (Verdadeiro, Falso)
- **LISTA** - Arrays de elementos

### Entrada/Saída

```rainbow
#nome recebe ler("Digite seu nome: ").
mostrar("Olá, " + #nome + "!").
```

### Estruturas de Controle

**Condicionais:**
```rainbow
se (#idade >= 18) {
    mostrar("Maior de idade").
} senao {
    mostrar("Menor de idade").
}
```

**Loops:**
```rainbow
// Laço para com contador
para #i de 1 ate 10 passo 1 {
    mostrar(#i).
}

// Laço enquanto
enquanto (#contador < 10) {
    #contador recebe #contador + 1.
}
```

### Operadores

- **Aritméticos**: `+`, `-`, `*`, `/`, `%`
- **Relacionais**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Lógicos**: `E`, `OU`, `NAO`
- **Atribuição**: `recebe`

## 🏗️ Arquitetura

### Estrutura de Arquivos

```
compilers-rainbow_language/
├── main.py                    # Rainbow IDE (interface principal)
├── src/                       # Código fonte do compilador
│   ├── analisador_lexico.py      # Análise léxica
│   ├── analisador_sintatico.py   # Análise sintática
│   ├── analisador_semantico.py   # Análise semântica
│   ├── interpretador_rainbow.py  # Interpretador
│   └── compilador_rainbow.py     # Integrador principal
├── exemplos/                  # Programas Rainbow de exemplo
│   ├── ola_mundo.rainbow         # Exemplo básico
│   ├── calculadora.rainbow       # Operações matemáticas
│   ├── tabuada.rainbow           # Laços de repetição
│   ├── condicional.rainbow       # Estruturas condicionais
│   ├── laco_para.rainbow         # Laços para
│   ├── tipos_dados.rainbow       # Tipos de dados
│   ├── entrada_usuario.rainbow   # Entrada interativa
│   └── programa_interativo.rainbow # Exemplo completo
├── tests/                     # Casos de teste
│   ├── teste1.rainbow            # Programa válido
│   ├── teste2.rainbow            # Detecção de erros
│   └── teste3.rainbow            # Teste completo
├── docs/                      # Documentação técnica
├── assets/                    # Recursos (imagens, etc.)
└── generated/                 # Arquivos gerados (ignorados no git)
```

## 👨‍💻 Desenvolvedores

**Projeto desenvolvido para a disciplina de Compiladores**

- **👤 Anderson Henrique da Silva**
- **👤 Lurian Letícia dos Reis**

**📚 Orientação**
- **Professor:** Hudson
- **Instituição:** IFSULDEMINAS Campus Muzambinho

## 🛠️ Desenvolvimento

### Tecnologias Utilizadas

- **Python 3.10+** - Linguagem principal
- **Tkinter** - Interface gráfica
- **PIL/Pillow** - Processamento de imagens
- **Threading** - Execução assíncrona
- **JSON** - Saída estruturada
- **RegEx** - Análise de padrões

### Características Técnicas

#### Analisador Léxico
- Tokenização caractere por caractere
- Recuperação automática de erros
- Rastreamento preciso de posição
- 30+ tipos de tokens

#### Analisador Sintático
- Parser recursivo descendente
- Construção de AST completa
- Detecção de erros sintáticos
- Recuperação de erros

#### Analisador Semântico
- Tabela de símbolos hierárquica
- Verificação de tipos
- Análise de escopo (GLOBAL, BLOCO, LACO)
- Detecção de variáveis não declaradas

#### Interpretador
- Execução linha por linha
- Suporte a entrada interativa
- Conversão automática de tipos
- Estruturas de controle completas

#### Interface (IDE)
- Tema escuro/claro moderno
- Syntax highlighting em tempo real
- Console integrado
- Splash screen animada
- Toolbar profissional

## 📖 Exemplos de Uso

### Programa Interativo Completo

```rainbow
RAINBOW.

// Programa de cadastro simples
#nome recebe ler("Digite seu nome: ").
#idade recebe ler("Digite sua idade: ").

mostrar("").
mostrar("=== DADOS CADASTRAIS ===").
mostrar("Nome: " + #nome).
mostrar("Idade: " + #idade).

se (#idade >= 18) {
    mostrar(#nome + " é maior de idade!").
} senao {
    mostrar(#nome + " é menor de idade.").
}

#ano_atual recebe 2025.
#ano_nascimento recebe #ano_atual - #idade.
mostrar("Você nasceu aproximadamente em: " + #ano_nascimento).

mostrar("Cadastro finalizado! 🌈").
```

### Calculadora de Tabuada

```rainbow
RAINBOW.

#numero recebe 5.
#i recebe 1.

mostrar("Tabuada do " + #numero + ":").

enquanto (#i <= 10) {
    #resultado recebe #numero * #i.
    mostrar(#numero + " x " + #i + " = " + #resultado).
    #i recebe #i + 1.
}
```

## 🚀 Como Usar

1. **Abra a Rainbow IDE:**
   ```bash
   python3 main.py
   ```

2. **Assista à splash screen** com animações do arco-íris

3. **Escolha um exemplo** no menu "Exemplos" ou crie um novo arquivo

4. **Execute o programa** com `F5` ou clique em ▶

5. **Digite valores** quando solicitado (suporte ao Enter!)

6. **Veja a saída** no console integrado

7. **Alterne temas** com `Ctrl+T` para personalizar

## 🎨 Recursos Visuais

- **Splash Screen Animada** - Logo Rainbow com cores e animações
- **Temas Modernos** - Paleta inspirada no GitHub Dark/Light
- **Toolbar Profissional** - Botões organizados por categoria
- **Syntax Highlighting** - Cores para palavras-chave, strings, variáveis
- **Tooltips Elegantes** - Dicas contextuais com estilo do tema

## 📞 Contato

Para dúvidas sobre o projeto educacional, entre em contato através das issues do GitHub ou com os desenvolvedores.

---

<div align="center">

**Desenvolvido com 💜 para aprendizado de compiladores**

*Rainbow IDE - Onde o código ganha cores! 🌈*

</div>
