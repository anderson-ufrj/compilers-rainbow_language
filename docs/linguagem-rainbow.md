# 🌈 Documentação da Linguagem Rainbow

## Índice
1. [Introdução](#introdução)
2. [Estrutura do Programa](#estrutura-do-programa)
3. [Elementos Léxicos](#elementos-léxicos)
4. [Tipos de Dados](#tipos-de-dados)
5. [Variáveis](#variáveis)
6. [Operadores](#operadores)
7. [Estruturas de Controle](#estruturas-de-controle)
8. [Entrada e Saída](#entrada-e-saída)
9. [Comentários](#comentários)
10. [Convenções e Boas Práticas](#convenções-e-boas-práticas)
11. [Exemplos Completos](#exemplos-completos)
12. [Referência Rápida](#referência-rápida)

## Introdução

Rainbow é uma linguagem de programação educacional desenvolvida especialmente para o ensino de programação para falantes nativos de português. A linguagem foi projetada com os seguintes objetivos:

- **Sintaxe em Português**: Todas as palavras-chave e comandos são em português
- **Simplicidade**: Fácil de aprender e entender
- **Didática**: Ideal para ensino de conceitos fundamentais de programação
- **Expressiva**: Suporta os principais paradigmas de programação estruturada

## Estrutura do Programa

Todo programa Rainbow deve obrigatoriamente começar com a palavra-chave `RAINBOW` seguida de um ponto:

```rainbow
RAINBOW.

// Seu código aqui
```

### Regras Gerais:
- **Todas as instruções terminam com ponto (.)**: Isso inclui declarações, atribuições, chamadas de função, etc.
- **Blocos de código usam chaves {}**: Para delimitar escopo em estruturas de controle
- **Indentação é recomendada**: Embora não obrigatória, melhora a legibilidade

## Elementos Léxicos

### Palavras Reservadas

| Palavra | Descrição | Uso |
|---------|-----------|-----|
| `RAINBOW` | Marca o início do programa | `RAINBOW.` |
| `cor_numero` | Tipo numérico | `cor_numero #idade.` |
| `cor_texto` | Tipo texto/string | `cor_texto #nome.` |
| `cor_logico` | Tipo booleano | `cor_logico #ativo.` |
| `cor_lista` | Tipo lista/array | `cor_lista #numeros.` |
| `recebe` | Operador de atribuição | `#x recebe 10.` |
| `se` | Condicional if | `se (#x > 0) { }` |
| `senao` | Condicional else | `senao { }` |
| `senaose` | Condicional else if | `senaose (#x igual 0) { }` |
| `para` | Laço for | `para #i de 1 ate 10 passo 1 { }` |
| `enquanto` | Laço while | `enquanto (#x < 10) { }` |
| `de` | Usado em laços for | `de 1` |
| `ate` | Usado em laços for | `ate 10` |
| `passo` | Incremento em laços for | `passo 1` |
| `mostrar` | Função de saída | `mostrar("Olá").` |
| `ler` | Função de entrada | `ler("Digite: ")` |
| `Verdadeiro` | Valor booleano true | `#ativo recebe Verdadeiro.` |
| `Falso` | Valor booleano false | `#ativo recebe Falso.` |
| `E` | Operador lógico AND | `#a E #b` |
| `OU` | Operador lógico OR | `#a OU #b` |
| `NAO` | Operador lógico NOT | `NAO #a` |
| `igual` | Operador de igualdade | `#a igual #b` |
| `diferente` | Operador de desigualdade | `#a diferente #b` |

### Identificadores (Variáveis)

As variáveis em Rainbow devem:
- Começar com o símbolo `#`
- Seguido por uma letra
- Podem conter letras, números e underscore (_)
- Máximo de 50 caracteres
- São case-sensitive

**Exemplos válidos:**
```rainbow
#nome
#idade
#valor_total
#contador1
#nomeCompleto
```

**Exemplos inválidos:**
```rainbow
#1nome      // Não pode começar com número
#nome-user  // Hífen não é permitido
#@valor     // Caracteres especiais não permitidos
nome        // Falta o #
```

### Números

Rainbow suporta números inteiros e decimais:
- Inteiros: `42`, `-10`, `0`
- Decimais: `3.14`, `-2.5`, `0.001`
- Máximo de 20 dígitos
- Números negativos são suportados

**Exemplos:**
```rainbow
#idade recebe 25.
#pi recebe 3.14159.
#temperatura recebe -5.5.
```

### Strings (Textos)

Strings são delimitadas por aspas duplas:
- Devem estar entre aspas duplas: `"texto"`
- Suportam caracteres de escape: `\"`, `\\`, `\n`, `\t`
- Podem ser concatenadas com o operador `+`

**Exemplos:**
```rainbow
#mensagem recebe "Olá, mundo!".
#frase recebe "Ele disse: \"Oi!\"".
#completo recebe #nome + " tem " + #idade + " anos.".
```

## Tipos de Dados

### cor_numero
Representa valores numéricos (inteiros e decimais):
```rainbow
cor_numero #idade.
#idade recebe 25.

cor_numero #preco.
#preco recebe 19.99.
```

### cor_texto
Representa strings de texto:
```rainbow
cor_texto #nome.
#nome recebe "Maria Silva".

cor_texto #endereco.
#endereco recebe "Rua das Flores, 123".
```

### cor_logico
Representa valores booleanos (Verdadeiro/Falso):
```rainbow
cor_logico #ativo.
#ativo recebe Verdadeiro.

cor_logico #encontrado.
#encontrado recebe Falso.
```

### cor_lista
Representa listas/arrays de elementos:
```rainbow
cor_lista #numeros.
#numeros recebe [1, 2, 3, 4, 5].

cor_lista #nomes.
#nomes recebe ["Ana", "Bruno", "Carlos"].
```

## Variáveis

### Declaração
Variáveis podem ser declaradas com tipo explícito:
```rainbow
cor_numero #idade.
cor_texto #nome.
cor_logico #casado.
```

### Atribuição
Use o operador `recebe` para atribuir valores:
```rainbow
#idade recebe 30.
#nome recebe "João".
#casado recebe Verdadeiro.
```

### Declaração e Atribuição
Você pode declarar e atribuir em momentos diferentes ou usar diretamente:
```rainbow
// Declaração explícita
cor_numero #salario.
#salario recebe 5000.50.

// Uso direto (tipo inferido)
#bonus recebe 500.
```

## Operadores

### Operadores Aritméticos
| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `+` | Adição | `#a + #b` |
| `-` | Subtração | `#a - #b` |
| `*` | Multiplicação | `#a * #b` |
| `/` | Divisão | `#a / #b` |
| `%` | Módulo (resto) | `#a % #b` |

### Operadores Relacionais
| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `>` | Maior que | `#a > #b` |
| `<` | Menor que | `#a < #b` |
| `>=` | Maior ou igual | `#a >= #b` |
| `<=` | Menor ou igual | `#a <= #b` |
| `igual` | Igual a | `#a igual #b` |
| `diferente` | Diferente de | `#a diferente #b` |

### Operadores Lógicos
| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `E` | AND lógico | `#a E #b` |
| `OU` | OR lógico | `#a OU #b` |
| `NAO` | NOT lógico | `NAO #a` |

### Operador de Atribuição
| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `recebe` | Atribui valor | `#x recebe 10.` |

### Precedência de Operadores
1. `NAO`
2. `*`, `/`, `%`
3. `+`, `-`
4. `<`, `>`, `<=`, `>=`
5. `igual`, `diferente`
6. `E`
7. `OU`

Use parênteses para alterar a precedência:
```rainbow
#resultado recebe (#a + #b) * #c.
```

## Estruturas de Controle

### Condicional (se/senao/senaose)

**Estrutura básica:**
```rainbow
se (condição) {
    // código se verdadeiro
}
```

**Com senao:**
```rainbow
se (#idade >= 18) {
    mostrar("Maior de idade").
} senao {
    mostrar("Menor de idade").
}
```

**Com senaose (múltiplas condições):**
```rainbow
se (#nota >= 9) {
    mostrar("Excelente!").
} senaose (#nota >= 7) {
    mostrar("Bom!").
} senaose (#nota >= 5) {
    mostrar("Regular").
} senao {
    mostrar("Insuficiente").
}
```

### Laço Para (for)

Estrutura para repetir um bloco um número determinado de vezes:

```rainbow
para #variavel de inicio ate fim passo incremento {
    // código a repetir
}
```

**Exemplos:**
```rainbow
// Contar de 1 a 10
para #i de 1 ate 10 passo 1 {
    mostrar(#i).
}

// Contar de 10 a 1 (decrescente)
para #i de 10 ate 1 passo -1 {
    mostrar(#i).
}

// Contar de 2 em 2
para #i de 0 ate 20 passo 2 {
    mostrar(#i).
}
```

### Laço Enquanto (while)

Estrutura para repetir enquanto uma condição for verdadeira:

```rainbow
enquanto (condição) {
    // código a repetir
}
```

**Exemplos:**
```rainbow
#contador recebe 0.
enquanto (#contador < 10) {
    mostrar("Contador: " + #contador).
    #contador recebe #contador + 1.
}

// Validação de entrada
#senha recebe "".
enquanto (#senha diferente "1234") {
    #senha recebe ler("Digite a senha: ").
}
mostrar("Senha correta!").
```

## Entrada e Saída

### Função mostrar()
Exibe informações na tela:

```rainbow
// Mostrar texto simples
mostrar("Olá, mundo!").

// Mostrar variáveis
mostrar(#nome).

// Mostrar expressões
mostrar("Resultado: " + #a + #b).

// Mostrar múltiplas linhas
mostrar("Linha 1").
mostrar("Linha 2").
```

### Função ler()
Lê entrada do usuário:

```rainbow
// Ler sem mensagem
#valor recebe ler().

// Ler com mensagem
#nome recebe ler("Digite seu nome: ").

// Ler números (conversão automática)
#idade recebe ler("Sua idade: ").
```

## Comentários

Use `//` para comentários de linha:

```rainbow
// Este é um comentário de linha
#x recebe 10. // Comentário no final da linha

// Comentário de múltiplas linhas
// pode ser feito usando
// várias linhas com //
```

## Convenções e Boas Práticas

### Nomenclatura
- **Variáveis**: use nomes descritivos em português
  - Bom: `#nomeCompleto`, `#idadeUsuario`, `#saldoConta`
  - Ruim: `#n`, `#x`, `#tmp`

### Indentação
- Use 4 espaços ou 1 tab para cada nível
- Seja consistente em todo o código

### Organização
```rainbow
RAINBOW.

// 1. Declarações de variáveis
cor_numero #idade.
cor_texto #nome.

// 2. Inicializações
#idade recebe 0.
#nome recebe "".

// 3. Lógica principal
#nome recebe ler("Nome: ").
#idade recebe ler("Idade: ").

// 4. Processamento
se (#idade >= 18) {
    mostrar("Bem-vindo, " + #nome).
}
```

### Comentários
- Comente o "por quê", não o "o quê"
- Use comentários para explicar lógica complexa
- Mantenha comentários atualizados

## Exemplos Completos

### Exemplo 1: Calculadora Simples
```rainbow
RAINBOW.

// Calculadora básica
mostrar("=== CALCULADORA RAINBOW ===").

#num1 recebe ler("Digite o primeiro número: ").
#num2 recebe ler("Digite o segundo número: ").
#operacao recebe ler("Digite a operação (+, -, *, /): ").

#resultado recebe 0.

se (#operacao igual "+") {
    #resultado recebe #num1 + #num2.
} senaose (#operacao igual "-") {
    #resultado recebe #num1 - #num2.
} senaose (#operacao igual "*") {
    #resultado recebe #num1 * #num2.
} senaose (#operacao igual "/") {
    se (#num2 diferente 0) {
        #resultado recebe #num1 / #num2.
    } senao {
        mostrar("Erro: Divisão por zero!").
    }
} senao {
    mostrar("Operação inválida!").
}

mostrar("Resultado: " + #resultado).
```

### Exemplo 2: Verificador de Números Primos
```rainbow
RAINBOW.

// Verificador de números primos
#numero recebe ler("Digite um número: ").
#primo recebe Verdadeiro.
#divisor recebe 2.

se (#numero <= 1) {
    #primo recebe Falso.
} senao {
    enquanto (#divisor < #numero) {
        se (#numero % #divisor igual 0) {
            #primo recebe Falso.
        }
        #divisor recebe #divisor + 1.
    }
}

se (#primo igual Verdadeiro) {
    mostrar(#numero + " é primo!").
} senao {
    mostrar(#numero + " não é primo.").
}
```

### Exemplo 3: Jogo de Adivinhação
```rainbow
RAINBOW.

// Jogo de adivinhação
#secreto recebe 42.
#tentativas recebe 0.
#acertou recebe Falso.

mostrar("=== JOGO DA ADIVINHAÇÃO ===").
mostrar("Tente adivinhar o número entre 1 e 100!").

enquanto (#acertou igual Falso) {
    #palpite recebe ler("Seu palpite: ").
    #tentativas recebe #tentativas + 1.
    
    se (#palpite igual #secreto) {
        #acertou recebe Verdadeiro.
        mostrar("Parabéns! Você acertou em " + #tentativas + " tentativas!").
    } senaose (#palpite < #secreto) {
        mostrar("Muito baixo! Tente novamente.").
    } senao {
        mostrar("Muito alto! Tente novamente.").
    }
}
```

### Exemplo 4: Tabuada Interativa
```rainbow
RAINBOW.

// Tabuada interativa
#continuar recebe Verdadeiro.

enquanto (#continuar igual Verdadeiro) {
    #numero recebe ler("Digite um número para ver a tabuada (0 para sair): ").
    
    se (#numero igual 0) {
        #continuar recebe Falso.
        mostrar("Até logo!").
    } senao {
        mostrar("=== TABUADA DO " + #numero + " ===").
        
        para #i de 1 ate 10 passo 1 {
            #resultado recebe #numero * #i.
            mostrar(#numero + " x " + #i + " = " + #resultado).
        }
        
        mostrar("").  // Linha em branco
    }
}
```

## Referência Rápida

### Template Básico
```rainbow
RAINBOW.

// Declarações
cor_numero #variavel1.
cor_texto #variavel2.

// Entrada
#variavel1 recebe ler("Prompt: ").

// Processamento
se (condição) {
    // código
}

// Saída
mostrar("Resultado: " + #variavel1).
```

### Estruturas Comuns

**Loop com contador:**
```rainbow
para #i de 1 ate 10 passo 1 {
    mostrar(#i).
}
```

**Loop condicional:**
```rainbow
enquanto (#continuar igual Verdadeiro) {
    // código
}
```

**Menu de opções:**
```rainbow
mostrar("1. Opção 1").
mostrar("2. Opção 2").
mostrar("3. Sair").
#opcao recebe ler("Escolha: ").

se (#opcao igual 1) {
    // código opção 1
} senaose (#opcao igual 2) {
    // código opção 2
} senaose (#opcao igual 3) {
    mostrar("Saindo...").
} senao {
    mostrar("Opção inválida!").
}
```

**Validação de entrada:**
```rainbow
#idade recebe -1.
enquanto (#idade < 0 OU #idade > 150) {
    #idade recebe ler("Digite uma idade válida: ").
}
```

### Dicas Finais

1. **Sempre termine comandos com ponto (.)**
2. **Use chaves {} para delimitar blocos**
3. **Variáveis sempre começam com #**
4. **Strings sempre entre aspas duplas**
5. **Teste incrementalmente seu código**
6. **Use comentários para documentar**
7. **Mantenha código organizado e indentado**

---

Rainbow foi projetada para tornar a programação acessível e intuitiva para falantes de português. Com sua sintaxe clara e recursos didáticos, é a linguagem ideal para dar os primeiros passos no mundo da programação!