# 📝 Gramática Formal da Linguagem Rainbow

## Notação

Esta gramática está escrita em uma notação simplificada e intuitiva:

- `=` - Definição de regra (substitui ::=)
- `|` - Alternativa (ou)
- `[ ]` - Opcional
- `{ }` - Repetição zero ou mais vezes
- `( )` - Agrupamento
- `"texto"` - Terminal literal
- `MAIUSCULA` - Token terminal
- `minuscula` - Regra não-terminal

## Gramática Completa

### Programa Principal

```bnf
programa = "RAINBOW" "." { declaracao }

declaracao = declaracao_variavel
           | atribuicao
           | condicional
           | laco_para
           | laco_enquanto
           | chamada_funcao
```

### Declarações de Variáveis

```bnf
declaracao_variavel = tipo_dado VARIAVEL "."

tipo_dado = "numero"
          | "texto"
          | "logico"
          | "lista"
```

### Atribuição

```bnf
atribuicao = VARIAVEL "recebe" expressao "."
```

### Estruturas de Controle

#### Condicional

```bnf
condicional = "se" "(" expressao ")" bloco
              { "senaose" "(" expressao ")" bloco }
              [ "senao" bloco ]
```

#### Laço Para

```bnf
laco_para = "para" VARIAVEL "de" expressao "ate" expressao "passo" expressao bloco
```

#### Laço Enquanto

```bnf
laco_enquanto = "enquanto" "(" expressao ")" bloco
```

#### Bloco

```bnf
bloco = "{" { declaracao } "}"
```

### Expressões

```bnf
expressao = expressao_ou

expressao_ou = expressao_e { "OU" expressao_e }

expressao_e = expressao_igualdade { "E" expressao_igualdade }

expressao_igualdade = expressao_comparacao { ( "igual" | "diferente" ) expressao_comparacao }

expressao_comparacao = expressao_adicao { ( ">" | "<" | ">=" | "<=" ) expressao_adicao }

expressao_adicao = expressao_multiplicacao { ( "+" | "-" ) expressao_multiplicacao }

expressao_multiplicacao = expressao_unaria { ( "*" | "/" | "%" ) expressao_unaria }

expressao_unaria = ( "NAO" | "-" ) expressao_unaria
                 | expressao_primaria

expressao_primaria = NUMERO
                   | TEXTO
                   | "Verdadeiro"
                   | "Falso"
                   | VARIAVEL
                   | chamada_funcao_expressao
                   | "(" expressao ")"
```

### Funções

```bnf
chamada_funcao = ( "mostrar" | "ler" ) "(" [ expressao ] ")" "."

chamada_funcao_expressao = "ler" "(" [ expressao ] ")"
```

### Tokens Terminais

```bnf
VARIAVEL = "#" LETRA { LETRA | DIGITO | "_" }

NUMERO = [ "-" ] DIGITO { DIGITO } [ "." DIGITO { DIGITO } ]

TEXTO = "\"" { CARACTERE | ESCAPE } "\""

ESCAPE = "\\" ( "n" | "t" | "r" | "\\" | "\"" | "'" )

LETRA = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"

DIGITO = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

CARACTERE = qualquer_caractere_unicode_exceto_aspas_e_barra
```

## Precedência de Operadores

| Precedência | Operadores | Associatividade |
|-------------|------------|-----------------|
| 1 (maior)   | `NAO`, `-` (unário) | Direita |
| 2           | `*`, `/`, `%` | Esquerda |
| 3           | `+`, `-` | Esquerda |
| 4           | `<`, `>`, `<=`, `>=` | Esquerda |
| 5           | `igual`, `diferente` | Esquerda |
| 6           | `E` | Esquerda |
| 7 (menor)   | `OU` | Esquerda |

## Regras Semânticas

### Escopo de Variáveis

1. **Escopo Global**: Variáveis declaradas no nível do programa
2. **Escopo Local**: Variáveis declaradas dentro de blocos
3. **Escopo de Laço**: Variável de controle do laço `para`

### Regras de Tipos

1. **Operações Aritméticas**: `+`, `-`, `*`, `/`, `%`
   - Operandos: `cor_numero`
   - Resultado: `cor_numero`
   - Exceção: `+` também concatena strings

2. **Operações de Comparação**: `>`, `<`, `>=`, `<=`, `igual`, `diferente`
   - Operandos: `cor_numero` ou `cor_texto`
   - Resultado: `cor_logico`

3. **Operações Lógicas**: `E`, `OU`, `NAO`
   - Operandos: `cor_logico`
   - Resultado: `cor_logico`

4. **Concatenação de Strings**: `+`
   - Operandos: `cor_texto`
   - Resultado: `cor_texto`

### Regras de Declaração

1. **Variáveis devem ser declaradas antes do uso**
2. **Não é permitida redeclaração no mesmo escopo**
3. **Tipo da variável deve ser compatível com o valor atribuído**

### Regras de Estruturas de Controle

1. **Condição em `se` e `enquanto`**: deve ser `cor_logico`
2. **Limites e passo em `para`**: devem ser `cor_numero`
3. **Blocos devem estar balanceados**: `{` e `}`

## Exemplos da Gramática

### Programa Mínimo

```rainbow
programa:
    RAINBOW.
```

### Declaração de Variável

```rainbow
declaracao_variavel:
    cor_numero #idade.
```

### Atribuição

```rainbow
atribuicao:
    #nome recebe "João".
```

### Estrutura Condicional

```rainbow
condicional:
    se (#idade >= 18) {
        mostrar("Maior de idade").
    } senao {
        mostrar("Menor de idade").
    }
```

### Laço Para

```rainbow
laco_para:
    para #i de 1 ate 10 passo 1 {
        mostrar(#i).
    }
```

### Laço Enquanto

```rainbow
laco_enquanto:
    enquanto (#contador < 10) {
        #contador recebe #contador + 1.
    }
```

### Expressão Complexa

```rainbow
expressao:
    #resultado recebe (#a + #b) * (#c - #d) / 2.
```

### Chamada de Função

```rainbow
chamada_funcao:
    mostrar("Olá, " + #nome + "!").
    #entrada recebe ler("Digite algo: ").
```

## Análise Sintática

### Método de Análise

A linguagem Rainbow utiliza **análise sintática recursiva descendente** com as seguintes características:

1. **Sem Ambiguidade**: A gramática é LL(1)
2. **Recuperação de Erros**: Continua análise após encontrar erros
3. **Construção de AST**: Gera árvore sintática abstrata
4. **Validação Estrutural**: Verifica balanceamento de blocos

### Tipos de Erros Sintáticos

1. **Estrutura Inválida**: Sequência de tokens não reconhecida
2. **Tokens Ausentes**: Falta de terminadores ou delimitadores
3. **Blocos Não Balanceados**: Chaves não fechadas
4. **Expressões Mal Formadas**: Operadores sem operandos

### Recuperação de Erros

O parser implementa recuperação de erros através de:

1. **Sincronização**: Busca por tokens de sincronização
2. **Pular Tokens**: Ignora tokens problemáticos
3. **Inserção de Tokens**: Assume tokens ausentes
4. **Limite de Iterações**: Evita loops infinitos

## Extensões Futuras

### Possíveis Melhorias na Gramática

1. **Funções Definidas pelo Usuário**:
   ```bnf
   definicao_funcao = "funcao" IDENTIFICADOR "(" [ parametros ] ")" bloco
   ```

2. **Estruturas de Dados**:
   ```bnf
   acesso_lista = VARIAVEL "[" expressao "]"
   ```

3. **Comentários de Bloco**:
   ```bnf
   comentario_bloco = "/*" { qualquer_caractere } "*/"
   ```

4. **Tratamento de Exceções**:
   ```bnf
   try_catch = "tente" bloco "capture" "(" VARIAVEL ")" bloco
   ```

---

Esta gramática formal serve como base para a implementação do parser e como documentação de referência para desenvolvedores da linguagem Rainbow.