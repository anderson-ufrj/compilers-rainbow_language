import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Tuple

# Enum para os tipos de tokens
class TokenType(Enum):
    # Identificador da linguagem
    RAINBOW = auto()
    
    # Tipos de dados
    TIPO_NUMERO = auto()
    TIPO_TEXTO = auto()
    TIPO_LOGICO = auto()
    TIPO_LISTA = auto()
    
    # Variáveis
    VARIAVEL = auto()
    
    # Operadores
    OPER_MENOR = auto()
    OPER_MAIOR = auto()
    OPER_MENOR_IGUAL = auto()
    OPER_MAIOR_IGUAL = auto()
    OPER_IGUAL = auto()
    OPER_DIFERENTE = auto()
    OPER_SOMA = auto()
    OPER_SUBTRACAO = auto()
    OPER_MULTIPLICACAO = auto()
    OPER_DIVISAO = auto()
    OPER_MODULO = auto()
    OPER_ATRIBUICAO = auto()
    OPER_E = auto()
    OPER_OU = auto()
    OPER_NAO = auto()
    
    # Estruturas de controle
    SE = auto()
    SENAO = auto()
    SENAOSE = auto()
    PARA = auto()
    ENQUANTO = auto()
    
    # Funções
    MOSTRAR = auto()
    LER = auto()
    
    # Valores
    VERDADEIRO = auto()
    FALSO = auto()
    TEXTO = auto()
    NUMERO = auto()
    
    # Delimitadores
    ABRE_PARENTESES = auto()
    FECHA_PARENTESES = auto()
    ABRE_CHAVES = auto()
    FECHA_CHAVES = auto()
    FIM_LINHA = auto()
    VIRGULA = auto()
    
    # Palavras auxiliares
    DE = auto()
    ATE = auto()
    PASSO = auto()
    RECEBE = auto()
    
    # Comentário
    COMENTARIO = auto()
    
    # Fim de arquivo
    EOF = auto()

@dataclass
class Token:
    tipo: TokenType
    lexema: str
    linha: int
    coluna: int
    
    def __str__(self):
        return f"Linha: {self.linha:02d} - Coluna: {self.coluna:02d} - Token:<{self.tipo.name}, {self.lexema}>"

class AnalisadorLexico:
    def __init__(self):
        # Palavras reservadas da linguagem
        self.palavras_reservadas = {
            'RAINBOW': TokenType.RAINBOW,
            'cor_numero': TokenType.TIPO_NUMERO,
            'cor_texto': TokenType.TIPO_TEXTO,
            'cor_logico': TokenType.TIPO_LOGICO,
            'cor_lista': TokenType.TIPO_LISTA,
            'igual': TokenType.OPER_IGUAL,
            'diferente': TokenType.OPER_DIFERENTE,
            'recebe': TokenType.OPER_ATRIBUICAO,
            'E': TokenType.OPER_E,
            'OU': TokenType.OPER_OU,
            'NAO': TokenType.OPER_NAO,
            'se': TokenType.SE,
            'senao': TokenType.SENAO,
            'senaose': TokenType.SENAOSE,
            'para': TokenType.PARA,
            'enquanto': TokenType.ENQUANTO,
            'mostrar': TokenType.MOSTRAR,
            'ler': TokenType.LER,
            'Verdadeiro': TokenType.VERDADEIRO,
            'Falso': TokenType.FALSO,
            'de': TokenType.DE,
            'ate': TokenType.ATE,
            'passo': TokenType.PASSO
        }
        
        # Limites
        self.MAX_IDENTIFIER_LENGTH = 50
        self.MAX_NUMBER_LENGTH = 20
        
    def analisar(self, codigo: str) -> Tuple[List[Token], List[str]]:
        tokens = []
        erros = []
        linhas = codigo.split('\n')
        
        # Contadores para verificar balanceamento
        chaves_abertas = []
        
        for num_linha, linha in enumerate(linhas, 1):
            coluna = 1
            i = 0
            
            while i < len(linha):
                # Ignorar espaços em branco
                if linha[i].isspace():
                    coluna += 1
                    i += 1
                    continue
                
                # Comentários
                if i < len(linha) - 1 and linha[i:i+2] == '//':
                    # Ignorar o resto da linha
                    break
                
                # Strings
                if linha[i] == '"':
                    inicio = i
                    i += 1
                    coluna_inicio = coluna
                    coluna += 1
                    
                    while i < len(linha) and linha[i] != '"':
                        if linha[i] == '\\' and i + 1 < len(linha):
                            i += 2
                            coluna += 2
                        else:
                            i += 1
                            coluna += 1
                    
                    if i >= len(linha):
                        erros.append(f"Linha: {num_linha:02d} - Coluna: {coluna_inicio:02d} - Erro: String não fechada")
                        continue
                    
                    i += 1  # Pular a aspa de fechamento
                    coluna += 1
                    lexema = linha[inicio:i]
                    tokens.append(Token(TokenType.TEXTO, lexema, num_linha, coluna_inicio))
                    continue
                
                # Números
                if linha[i].isdigit() or (linha[i] == '-' and i + 1 < len(linha) and linha[i + 1].isdigit()):
                    inicio = i
                    coluna_inicio = coluna
                    
                    if linha[i] == '-':
                        i += 1
                        coluna += 1
                    
                    while i < len(linha) and linha[i].isdigit():
                        i += 1
                        coluna += 1
                    
                    # Verificar decimal (mas só se não for seguido por outro ponto - fim de linha)
                    if i < len(linha) and linha[i] == '.' and i + 1 < len(linha) and linha[i + 1] != ' ' and linha[i + 1] != '\t' and linha[i + 1] != '\n':
                        # Verificar se próximo caractere é dígito
                        if i + 1 < len(linha) and linha[i + 1].isdigit():
                            i += 1
                            coluna += 1
                            
                            while i < len(linha) and linha[i].isdigit():
                                i += 1
                                coluna += 1
                        else:
                            # É um ponto mas não seguido de dígito - provavelmente erro
                            erros.append(f"Linha: {num_linha:02d} - Coluna: {coluna_inicio:02d} - Erro: Número mal formado")
                            i += 1
                            coluna += 1
                            continue
                    
                    lexema = linha[inicio:i]
                    
                    if len(lexema) > self.MAX_NUMBER_LENGTH:
                        erros.append(f"Linha: {num_linha:02d} - Coluna: {coluna_inicio:02d} - Erro: Número muito grande: {lexema}")
                    
                    tokens.append(Token(TokenType.NUMERO, lexema, num_linha, coluna_inicio))
                    continue
                
                # Variáveis
                if linha[i] == '#':
                    inicio = i
                    coluna_inicio = coluna
                    i += 1
                    coluna += 1
                    
                    if i >= len(linha) or not linha[i].isalpha():
                        erros.append(f"Linha: {num_linha:02d} - Coluna: {coluna_inicio:02d} - Erro: Variável mal formada")
                        continue
                    
                    while i < len(linha) and (linha[i].isalnum() or linha[i] == '_'):
                        i += 1
                        coluna += 1
                    
                    lexema = linha[inicio:i]
                    
                    if len(lexema) > self.MAX_IDENTIFIER_LENGTH:
                        erros.append(f"Linha: {num_linha:02d} - Coluna: {coluna_inicio:02d} - Erro: Nome de variável muito longo: {lexema[:20]}...")
                    
                    tokens.append(Token(TokenType.VARIAVEL, lexema, num_linha, coluna_inicio))
                    continue
                
                # Operadores de dois caracteres
                if i < len(linha) - 1:
                    dois_chars = linha[i:i+2]
                    if dois_chars == '<=':
                        tokens.append(Token(TokenType.OPER_MENOR_IGUAL, '<=', num_linha, coluna))
                        i += 2
                        coluna += 2
                        continue
                    elif dois_chars == '>=':
                        tokens.append(Token(TokenType.OPER_MAIOR_IGUAL, '>=', num_linha, coluna))
                        i += 2
                        coluna += 2
                        continue
                
                # Operadores e delimitadores de um caractere
                char = linha[i]
                token_map = {
                    '<': TokenType.OPER_MENOR,
                    '>': TokenType.OPER_MAIOR,
                    '+': TokenType.OPER_SOMA,
                    '-': TokenType.OPER_SUBTRACAO,
                    '*': TokenType.OPER_MULTIPLICACAO,
                    '/': TokenType.OPER_DIVISAO,
                    '%': TokenType.OPER_MODULO,
                    '(': TokenType.ABRE_PARENTESES,
                    ')': TokenType.FECHA_PARENTESES,
                    '{': TokenType.ABRE_CHAVES,
                    '}': TokenType.FECHA_CHAVES,
                    '.': TokenType.FIM_LINHA,
                    ',': TokenType.VIRGULA
                }
                
                if char in token_map:
                    tokens.append(Token(token_map[char], char, num_linha, coluna))
                    
                    # Rastrear chaves
                    if char == '{':
                        chaves_abertas.append((num_linha, coluna))
                    elif char == '}':
                        if not chaves_abertas:
                            erros.append(f"Linha: {num_linha:02d} - Coluna: {coluna:02d} - Erro: Chave de fechamento sem correspondente")
                        else:
                            chaves_abertas.pop()
                    
                    i += 1
                    coluna += 1
                    continue
                
                # Identificadores e palavras reservadas
                if linha[i].isalpha():
                    inicio = i
                    coluna_inicio = coluna
                    
                    while i < len(linha) and (linha[i].isalnum() or linha[i] == '_'):
                        i += 1
                        coluna += 1
                    
                    lexema = linha[inicio:i]
                    
                    if lexema in self.palavras_reservadas:
                        tokens.append(Token(self.palavras_reservadas[lexema], lexema, num_linha, coluna_inicio))
                    else:
                        erros.append(f"Linha: {num_linha:02d} - Coluna: {coluna_inicio:02d} - Erro: Identificador inválido: {lexema}")
                    continue
                
                # Caractere não reconhecido
                erros.append(f"Linha: {num_linha:02d} - Coluna: {coluna:02d} - Erro: Símbolo não reconhecido: '{linha[i]}'")
                i += 1
                coluna += 1
        
        # Verificar chaves não fechadas
        for linha, coluna in chaves_abertas:
            erros.append(f"Linha: {linha:02d} - Coluna: {coluna:02d} - Erro: Chave aberta não foi fechada")
        
        # Adicionar token EOF
        tokens.append(Token(TokenType.EOF, '', len(linhas), len(linhas[-1]) + 1 if linhas else 1))
        
        return tokens, erros

# Função principal para testar
def main():
    import sys
    import os
    
    # Criar arquivos de teste se não existirem
    criar_arquivos_teste()
    
    if len(sys.argv) < 2:
        print("\n" + "="*80)
        print("ANALISADOR LÉXICO RAINBOW 🌈")
        print("="*80)
        print("\nOpções:")
        print("1. Digite o código Rainbow diretamente")
        print("2. Use um arquivo: python analisador_lexico.py <arquivo.rainbow>")
        print("\nArquivos de teste disponíveis:")
        print("  - teste1.rainbow (programa válido)")
        print("  - teste2.rainbow (programa com erros)")
        print("  - teste3.rainbow (teste completo)")
        print("\nExemplo: python analisador_lexico.py teste1.rainbow")
        print("-"*80)
        
        # Modo interativo
        print("\n📝 MODO ENTRADA MANUAL")
        print("Digite seu código Rainbow linha por linha.")
        print("Quando terminar, digite 'FIM' em uma linha vazia.\n")
        
        codigo_linhas = []
        linha_num = 1
        
        while True:
            try:
                linha = input(f"{linha_num:02d}> ")
                if linha.strip().upper() == 'FIM':
                    break
                codigo_linhas.append(linha)
                linha_num += 1
            except KeyboardInterrupt:
                print("\n\nEntrada cancelada.")
                return
            except EOFError:
                break
        
        if not codigo_linhas:
            print("\nNenhum código foi digitado!")
            return
            
        codigo = '\n'.join(codigo_linhas)
        
    else:
        arquivo = sys.argv[1]
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo}' não encontrado")
            return
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            return
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado")
        return
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return
    
    analisador = AnalisadorLexico()
    tokens, erros = analisador.analisar(codigo)
    
    print("\n" + "="*80)
    print("ANÁLISE LÉXICA - LINGUAGEM RAINBOW 🌈")
    print("="*80)
    
    if tokens:
        print("\n📋 TOKENS ENCONTRADOS:")
        print("-"*80)
        for token in tokens:
            if token.tipo != TokenType.EOF:  # Não mostrar EOF na saída
                print(token)
    
    if erros:
        print("\n❌ ERROS ENCONTRADOS:")
        print("-"*80)
        for erro in erros:
            print(erro)
    else:
        print("\n✅ Análise concluída sem erros!")
    
    print("\n" + "="*80)
    print(f"Total de tokens: {len(tokens) - 1}")  # -1 para excluir EOF
    print(f"Total de erros: {len(erros)}")
    print("="*80)
    
    # Perguntar se quer analisar outro código
    if len(sys.argv) < 2:  # Só no modo interativo
        print("\nDeseja analisar outro código? (S/N): ", end='')
        resposta = input().strip().upper()
        if resposta == 'S':
            main()  # Recursão para continuar

def criar_arquivos_teste():
    """Cria arquivos de teste se não existirem"""
    import os
    
    # Teste 1 - Programa válido
    teste1 = '''RAINBOW.

// Programa de saudação simples
#nome recebe ler("Digite seu nome: ").
mostrar("Olá, " + #nome + "!").

#idade recebe ler("Sua idade: ").
se (#idade >= 18) {
    mostrar("Você é maior de idade!").
} senao {
    mostrar("Você é menor de idade!").
}

// Tabuada
para #i de 1 ate 5 passo 1 {
    #resultado recebe 2 * #i.
    mostrar("2 x " + #i + " = " + #resultado).
}
'''
    
    # Teste 2 - Programa com erros
    teste2 = '''RAINBOW.

// Erro 1: Variável mal formada
#1nome recebe "erro".
j@ recebe 10.

// Erro 2: String não fechada
mostrar("Olá mundo).

// Erro 3: Número mal formado
#valor recebe 2.a3.
#grande recebe 123456789012345678901234567890.

// Erro 4: Símbolo não reconhecido
#teste @ recebe 5.

// Erro 5: Chave não fechada
se (#teste > 0) {
    mostrar("positivo").

// Erro 6: Identificador inválido
minha_funcao().
'''
    
    # Teste 3 - Teste completo
    teste3 = '''RAINBOW.

// Teste de todos os operadores
#a recebe 10.
#b recebe 5.

// Operadores matemáticos
#soma recebe #a + #b.
#sub recebe #a - #b.
#mult recebe #a * #b.
#div recebe #a / #b.
#mod recebe #a % #b.

// Operadores relacionais
se (#a > #b) {
    mostrar("a maior que b").
}

se (#a igual #b) {
    mostrar("a igual a b").
}

// Operadores lógicos
#x recebe Verdadeiro.
#y recebe Falso.

se (#x E #y) {
    mostrar("ambos verdadeiros").
}

// Laço while
#contador recebe 0.
enquanto (#contador < 3) {
    mostrar("Contando: " + #contador).
    #contador recebe #contador + 1.
}
'''
    
    # Criar arquivos se não existirem
    arquivos = [
        ('teste1.rainbow', teste1),
        ('teste2.rainbow', teste2),
        ('teste3.rainbow', teste3)
    ]
    
    for nome_arquivo, conteudo in arquivos:
        if not os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            print(f"✅ Arquivo '{nome_arquivo}' criado!")

if __name__ == "__main__":
    main()