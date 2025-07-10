# 📚 Exemplos Práticos - Linguagem Rainbow

## Índice
1. [Programas Básicos](#programas-básicos)
2. [Estruturas de Controle](#estruturas-de-controle)
3. [Programas Interativos](#programas-interativos)
4. [Algoritmos Matemáticos](#algoritmos-matemáticos)
5. [Jogos Simples](#jogos-simples)
6. [Validação de Dados](#validação-de-dados)
7. [Programas com Listas](#programas-com-listas)
8. [Exercícios Práticos](#exercícios-práticos)

## Programas Básicos

### 1. Olá Mundo
```rainbow
RAINBOW.

// Primeiro programa em Rainbow
mostrar("🌈 Olá, mundo Rainbow! 🌈").
```

### 2. Entrada e Saída Simples
```rainbow
RAINBOW.

// Programa básico de entrada e saída
#nome recebe ler("Digite seu nome: ").
#idade recebe ler("Digite sua idade: ").

mostrar("Olá, " + #nome + "!").
mostrar("Você tem " + #idade + " anos.").
```

### 3. Operações Matemáticas
```rainbow
RAINBOW.

// Calculadora básica
#a recebe ler("Digite o primeiro número: ").
#b recebe ler("Digite o segundo número: ").

#soma recebe #a + #b.
#subtracao recebe #a - #b.
#multiplicacao recebe #a * #b.
#divisao recebe #a / #b.

mostrar("Soma: " + #soma).
mostrar("Subtração: " + #subtracao).
mostrar("Multiplicação: " + #multiplicacao).
mostrar("Divisão: " + #divisao).
```

## Estruturas de Controle

### 4. Verificação de Idade
```rainbow
RAINBOW.

// Verificador de maioridade
#idade recebe ler("Digite sua idade: ").

se (#idade >= 18) {
    mostrar("Você é maior de idade!").
    mostrar("Pode dirigir e votar.").
} senao {
    mostrar("Você é menor de idade.").
    #anos_faltam recebe 18 - #idade.
    mostrar("Faltam " + #anos_faltam + " anos para a maioridade.").
}
```

### 5. Classificação de Notas
```rainbow
RAINBOW.

// Sistema de notas
#nota recebe ler("Digite sua nota (0-10): ").

se (#nota >= 9) {
    mostrar("Conceito: A - Excelente!").
} senaose (#nota >= 7) {
    mostrar("Conceito: B - Bom!").
} senaose (#nota >= 5) {
    mostrar("Conceito: C - Regular").
} senaose (#nota >= 3) {
    mostrar("Conceito: D - Insuficiente").
} senao {
    mostrar("Conceito: F - Reprovado").
}
```

### 6. Tabuada com Loop
```rainbow
RAINBOW.

// Gerador de tabuada
#numero recebe ler("Digite um número para a tabuada: ").

mostrar("=== TABUADA DO " + #numero + " ===").

para #i de 1 ate 10 passo 1 {
    #resultado recebe #numero * #i.
    mostrar(#numero + " x " + #i + " = " + #resultado).
}
```

### 7. Contador com While
```rainbow
RAINBOW.

// Contador regressivo
#inicio recebe ler("Digite um número para contagem regressiva: ").

mostrar("Iniciando contagem regressiva...").

enquanto (#inicio > 0) {
    mostrar(#inicio).
    #inicio recebe #inicio - 1.
}

mostrar("🚀 Decolagem!").
```

## Programas Interativos

### 8. Menu de Opções
```rainbow
RAINBOW.

// Sistema de menu
#continuar recebe Verdadeiro.

enquanto (#continuar igual Verdadeiro) {
    mostrar("=== MENU PRINCIPAL ===").
    mostrar("1. Calculadora").
    mostrar("2. Tabuada").
    mostrar("3. Contador").
    mostrar("4. Sair").
    
    #opcao recebe ler("Escolha uma opção: ").
    
    se (#opcao igual 1) {
        #a recebe ler("Primeiro número: ").
        #b recebe ler("Segundo número: ").
        mostrar("Soma: " + (#a + #b)).
        
    } senaose (#opcao igual 2) {
        #num recebe ler("Número da tabuada: ").
        para #i de 1 ate 10 passo 1 {
            mostrar(#num + " x " + #i + " = " + (#num * #i)).
        }
        
    } senaose (#opcao igual 3) {
        #n recebe ler("Contar até: ").
        para #i de 1 ate #n passo 1 {
            mostrar("Contagem: " + #i).
        }
        
    } senaose (#opcao igual 4) {
        #continuar recebe Falso.
        mostrar("Até logo!").
        
    } senao {
        mostrar("Opção inválida!").
    }
}
```

### 9. Calculadora Avançada
```rainbow
RAINBOW.

// Calculadora com múltiplas operações
#continuar recebe Verdadeiro.

enquanto (#continuar igual Verdadeiro) {
    mostrar("=== CALCULADORA RAINBOW ===").
    
    #num1 recebe ler("Primeiro número: ").
    #num2 recebe ler("Segundo número: ").
    
    mostrar("Operações disponíveis:").
    mostrar("1. Soma (+)").
    mostrar("2. Subtração (-)").
    mostrar("3. Multiplicação (*)").
    mostrar("4. Divisão (/)").
    mostrar("5. Módulo (%)").
    
    #op recebe ler("Escolha a operação: ").
    
    se (#op igual 1) {
        #resultado recebe #num1 + #num2.
        mostrar("Resultado: " + #num1 + " + " + #num2 + " = " + #resultado).
        
    } senaose (#op igual 2) {
        #resultado recebe #num1 - #num2.
        mostrar("Resultado: " + #num1 + " - " + #num2 + " = " + #resultado).
        
    } senaose (#op igual 3) {
        #resultado recebe #num1 * #num2.
        mostrar("Resultado: " + #num1 + " * " + #num2 + " = " + #resultado).
        
    } senaose (#op igual 4) {
        se (#num2 diferente 0) {
            #resultado recebe #num1 / #num2.
            mostrar("Resultado: " + #num1 + " / " + #num2 + " = " + #resultado).
        } senao {
            mostrar("Erro: Divisão por zero!").
        }
        
    } senaose (#op igual 5) {
        #resultado recebe #num1 % #num2.
        mostrar("Resultado: " + #num1 + " % " + #num2 + " = " + #resultado).
        
    } senao {
        mostrar("Operação inválida!").
    }
    
    #resposta recebe ler("Fazer outro cálculo? (s/n): ").
    se (#resposta diferente "s") {
        #continuar recebe Falso.
    }
}
```

## Algoritmos Matemáticos

### 10. Números Primos
```rainbow
RAINBOW.

// Verificador de números primos
#numero recebe ler("Digite um número: ").

se (#numero <= 1) {
    mostrar(#numero + " não é primo.").
} senao {
    #primo recebe Verdadeiro.
    #divisor recebe 2.
    
    enquanto (#divisor < #numero E #primo igual Verdadeiro) {
        se (#numero % #divisor igual 0) {
            #primo recebe Falso.
        }
        #divisor recebe #divisor + 1.
    }
    
    se (#primo igual Verdadeiro) {
        mostrar(#numero + " é primo!").
    } senao {
        mostrar(#numero + " não é primo.").
    }
}
```

### 11. Sequência de Fibonacci
```rainbow
RAINBOW.

// Gerador de Fibonacci
#n recebe ler("Quantos números de Fibonacci gerar? ").

se (#n <= 0) {
    mostrar("Quantidade deve ser maior que zero!").
} senaose (#n igual 1) {
    mostrar("Fibonacci: 0").
} senaose (#n igual 2) {
    mostrar("Fibonacci: 0, 1").
} senao {
    mostrar("Sequência de Fibonacci:").
    
    #a recebe 0.
    #b recebe 1.
    
    mostrar("1: " + #a).
    mostrar("2: " + #b).
    
    para #i de 3 ate #n passo 1 {
        #proximo recebe #a + #b.
        mostrar(#i + ": " + #proximo).
        
        #a recebe #b.
        #b recebe #proximo.
    }
}
```

### 12. Fatorial
```rainbow
RAINBOW.

// Calculadora de fatorial
#numero recebe ler("Digite um número para calcular o fatorial: ").

se (#numero < 0) {
    mostrar("Fatorial não definido para números negativos!").
} senao {
    #fatorial recebe 1.
    #original recebe #numero.
    
    enquanto (#numero > 1) {
        #fatorial recebe #fatorial * #numero.
        #numero recebe #numero - 1.
    }
    
    mostrar("Fatorial de " + #original + " = " + #fatorial).
}
```

## Jogos Simples

### 13. Jogo da Adivinhação
```rainbow
RAINBOW.

// Jogo de adivinhação
#segredo recebe 42.
#tentativas recebe 0.
#acertou recebe Falso.

mostrar("=== JOGO DA ADIVINHAÇÃO ===").
mostrar("Tente adivinhar o número entre 1 e 100!").

enquanto (#acertou igual Falso) {
    #palpite recebe ler("Seu palpite: ").
    #tentativas recebe #tentativas + 1.
    
    se (#palpite igual #segredo) {
        #acertou recebe Verdadeiro.
        mostrar("🎉 Parabéns! Você acertou!").
        mostrar("Número de tentativas: " + #tentativas).
        
        se (#tentativas <= 3) {
            mostrar("Excelente! Você é um gênio!").
        } senaose (#tentativas <= 6) {
            mostrar("Muito bom! Você tem talento!").
        } senaose (#tentativas <= 10) {
            mostrar("Bom trabalho!").
        } senao {
            mostrar("Foi difícil, mas você conseguiu!").
        }
        
    } senaose (#palpite < #segredo) {
        mostrar("📈 Muito baixo! Tente um número maior.").
    } senao {
        mostrar("📉 Muito alto! Tente um número menor.").
    }
    
    se (#tentativas >= 15 E #acertou igual Falso) {
        mostrar("Você está tendo dificuldades. O número é " + #segredo).
        #acertou recebe Verdadeiro.
    }
}
```

### 14. Pedra, Papel, Tesoura
```rainbow
RAINBOW.

// Jogo Pedra, Papel, Tesoura
#vitorias_jogador recebe 0.
#vitorias_computador recebe 0.
#empates recebe 0.

mostrar("=== PEDRA, PAPEL, TESOURA ===").
mostrar("Melhor de 5 rodadas!").

para #rodada de 1 ate 5 passo 1 {
    mostrar("=== RODADA " + #rodada + " ===").
    mostrar("1. Pedra").
    mostrar("2. Papel").
    mostrar("3. Tesoura").
    
    #jogador recebe ler("Sua escolha: ").
    #computador recebe (#rodada * 7 + 13) % 3 + 1.  // Simulação de escolha aleatória
    
    mostrar("Você escolheu: " + #jogador).
    mostrar("Computador escolheu: " + #computador).
    
    se (#jogador igual #computador) {
        mostrar("🤝 Empate!").
        #empates recebe #empates + 1.
        
    } senaose (
        (#jogador igual 1 E #computador igual 3) OU
        (#jogador igual 2 E #computador igual 1) OU
        (#jogador igual 3 E #computador igual 2)
    ) {
        mostrar("🎉 Você ganhou esta rodada!").
        #vitorias_jogador recebe #vitorias_jogador + 1.
        
    } senao {
        mostrar("🤖 Computador ganhou esta rodada!").
        #vitorias_computador recebe #vitorias_computador + 1.
    }
}

mostrar("=== RESULTADO FINAL ===").
mostrar("Suas vitórias: " + #vitorias_jogador).
mostrar("Vitórias do computador: " + #vitorias_computador).
mostrar("Empates: " + #empates).

se (#vitorias_jogador > #vitorias_computador) {
    mostrar("🏆 Você é o campeão!").
} senaose (#vitorias_computador > #vitorias_jogador) {
    mostrar("🤖 O computador ganhou!").
} senao {
    mostrar("🤝 Empate geral!").
}
```

## Validação de Dados

### 15. Validador de Entrada
```rainbow
RAINBOW.

// Validador de idade
#idade recebe -1.

enquanto (#idade < 0 OU #idade > 120) {
    #idade recebe ler("Digite uma idade válida (0-120): ").
    
    se (#idade < 0) {
        mostrar("❌ Idade não pode ser negativa!").
    } senaose (#idade > 120) {
        mostrar("❌ Idade muito alta! Seja realista!").
    } senao {
        mostrar("✅ Idade válida!").
    }
}

mostrar("Idade registrada: " + #idade + " anos.").
```

### 16. Validador de Senha
```rainbow
RAINBOW.

// Sistema de senha
#senha_correta recebe "rainbow123".
#tentativas recebe 0.
#max_tentativas recebe 3.
#logado recebe Falso.

mostrar("=== SISTEMA DE LOGIN ===").

enquanto (#tentativas < #max_tentativas E #logado igual Falso) {
    #senha recebe ler("Digite a senha: ").
    #tentativas recebe #tentativas + 1.
    
    se (#senha igual #senha_correta) {
        #logado recebe Verdadeiro.
        mostrar("✅ Login realizado com sucesso!").
        mostrar("Bem-vindo ao sistema!").
        
    } senao {
        #restantes recebe #max_tentativas - #tentativas.
        se (#restantes > 0) {
            mostrar("❌ Senha incorreta! Tentativas restantes: " + #restantes).
        } senao {
            mostrar("❌ Muitas tentativas incorretas! Acesso bloqueado!").
        }
    }
}
```

## Programas com Listas

### 17. Lista de Números
```rainbow
RAINBOW.

// Trabalhando com listas
cor_lista #numeros.
#numeros recebe [10, 25, 7, 33, 18, 42, 1, 95].

mostrar("Lista original: " + #numeros).

// Encontrar maior e menor
#maior recebe #numeros[0].
#menor recebe #numeros[0].

para #i de 1 ate 7 passo 1 {
    se (#numeros[#i] > #maior) {
        #maior recebe #numeros[#i].
    }
    se (#numeros[#i] < #menor) {
        #menor recebe #numeros[#i].
    }
}

mostrar("Maior número: " + #maior).
mostrar("Menor número: " + #menor).

// Calcular média
#soma recebe 0.
para #i de 0 ate 7 passo 1 {
    #soma recebe #soma + #numeros[#i].
}
#media recebe #soma / 8.

mostrar("Média: " + #media).
```

### 18. Lista de Nomes
```rainbow
RAINBOW.

// Gerenciador de lista de nomes
cor_lista #nomes.
#nomes recebe ["Ana", "Bruno", "Carlos", "Diana", "Eduardo"].

mostrar("=== LISTA DE NOMES ===").

para #i de 0 ate 4 passo 1 {
    mostrar((#i + 1) + ". " + #nomes[#i]).
}

#buscar recebe ler("Digite um nome para buscar: ").
#encontrado recebe Falso.

para #i de 0 ate 4 passo 1 {
    se (#nomes[#i] igual #buscar) {
        #encontrado recebe Verdadeiro.
        mostrar("✅ " + #buscar + " encontrado na posição " + (#i + 1)).
    }
}

se (#encontrado igual Falso) {
    mostrar("❌ " + #buscar + " não encontrado na lista.").
}
```

## Exercícios Práticos

### 19. Conversor de Temperatura
```rainbow
RAINBOW.

// Conversor de temperatura
mostrar("=== CONVERSOR DE TEMPERATURA ===").
mostrar("1. Celsius para Fahrenheit").
mostrar("2. Fahrenheit para Celsius").
mostrar("3. Celsius para Kelvin").
mostrar("4. Kelvin para Celsius").

#opcao recebe ler("Escolha uma opção: ").
#temperatura recebe ler("Digite a temperatura: ").

se (#opcao igual 1) {
    #fahrenheit recebe (#temperatura * 9 / 5) + 32.
    mostrar(#temperatura + "°C = " + #fahrenheit + "°F").
    
} senaose (#opcao igual 2) {
    #celsius recebe (#temperatura - 32) * 5 / 9.
    mostrar(#temperatura + "°F = " + #celsius + "°C").
    
} senaose (#opcao igual 3) {
    #kelvin recebe #temperatura + 273.15.
    mostrar(#temperatura + "°C = " + #kelvin + "K").
    
} senaose (#opcao igual 4) {
    #celsius recebe #temperatura - 273.15.
    mostrar(#temperatura + "K = " + #celsius + "°C").
    
} senao {
    mostrar("Opção inválida!").
}
```

### 20. Calculadora de IMC
```rainbow
RAINBOW.

// Calculadora de IMC
mostrar("=== CALCULADORA DE IMC ===").

#peso recebe ler("Digite seu peso (kg): ").
#altura recebe ler("Digite sua altura (m): ").

#imc recebe #peso / (#altura * #altura).

mostrar("Seu IMC é: " + #imc).

se (#imc < 18.5) {
    mostrar("Classificação: Abaixo do peso").
    mostrar("Recomendação: Procure orientação nutricional").
    
} senaose (#imc < 25) {
    mostrar("Classificação: Peso normal").
    mostrar("Recomendação: Mantenha hábitos saudáveis");
    
} senaose (#imc < 30) {
    mostrar("Classificação: Sobrepeso").
    mostrar("Recomendação: Considere atividade física regular");
    
} senaose (#imc < 35) {
    mostrar("Classificação: Obesidade grau I").
    mostrar("Recomendação: Procure acompanhamento médico");
    
} senaose (#imc < 40) {
    mostrar("Classificação: Obesidade grau II").
    mostrar("Recomendação: Acompanhamento médico necessário");
    
} senao {
    mostrar("Classificação: Obesidade grau III").
    mostrar("Recomendação: Procure ajuda médica urgente");
}
```

---

## Dicas para Praticar

### 1. Comece Simples
- Experimente os programas básicos primeiro
- Entenda cada linha de código
- Modifique os valores para ver diferentes resultados

### 2. Pratique Estruturas
- Combine diferentes tipos de loops
- Use condições aninhadas
- Experimente diferentes operadores

### 3. Crie Variações
- Modifique os programas existentes
- Adicione novas funcionalidades
- Combine diferentes exemplos

### 4. Desafios
- Crie seus próprios programas
- Implemente algoritmos conhecidos
- Resolva problemas do dia a dia

### 5. Debug e Testes
- Execute os programas passo a passo
- Teste com diferentes entradas
- Procure por erros e corrija-os

---

Estes exemplos cobrem os principais aspectos da linguagem Rainbow e servem como base para criar programas mais complexos. Pratique modificando e expandindo estes códigos!