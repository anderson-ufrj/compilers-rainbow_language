"""
Analisador Sintático para a Linguagem Rainbow
Implementa um parser recursivo descendente que constrói uma AST
"""

from dataclasses import dataclass
from typing import List, Optional, Union, Any
from enum import Enum, auto
from analisador_lexico import TokenType, Token, AnalisadorLexico
import json
import os
from datetime import datetime


class TipoNo(Enum):
    """Tipos de nós da AST"""
    PROGRAMA = auto()
    DECLARACAO_VARIAVEL = auto()
    ATRIBUICAO = auto()
    CONDICIONAL = auto()
    LACO_PARA = auto()
    LACO_ENQUANTO = auto()
    CHAMADA_FUNCAO = auto()
    EXPRESSAO_BINARIA = auto()
    EXPRESSAO_UNARIA = auto()
    LITERAL = auto()
    VARIAVEL = auto()
    BLOCO = auto()


@dataclass
class NoAST:
    """Nó da Árvore Sintática Abstrata"""
    tipo: TipoNo
    valor: Any = None
    filhos: List['NoAST'] = None
    linha: int = 0
    coluna: int = 0
    
    def __post_init__(self):
        if self.filhos is None:
            self.filhos = []
    
    def to_dict(self):
        """Converte o nó para dicionário para serialização"""
        return {
            'tipo': self.tipo.name,
            'valor': self.valor,
            'filhos': [filho.to_dict() for filho in self.filhos],
            'linha': self.linha,
            'coluna': self.coluna
        }


class AnalisadorSintatico:
    """Parser recursivo descendente para Rainbow"""
    
    def __init__(self):
        self.tokens: List[Token] = []
        self.posicao = 0
        self.erros: List[str] = []
        self.token_atual: Optional[Token] = None
        
    def analisar(self, tokens: List[Token]) -> tuple[Optional[NoAST], List[str]]:
        """
        Analisa a lista de tokens e retorna a AST e lista de erros
        """
        self.tokens = tokens
        self.posicao = 0
        self.erros = []
        
        if not tokens:
            self.erros.append("Lista de tokens vazia")
            return None, self.erros
        
        self.token_atual = self.tokens[0] if self.tokens else None
        
        try:
            ast = self.programa()
            
            # Verificar se chegamos ao final dos tokens
            if self.token_atual and self.token_atual.tipo != TokenType.EOF:
                self.erro(f"Tokens inesperados após o fim do programa")
            
            return ast, self.erros
            
        except Exception as e:
            self.erro(f"Erro interno do parser: {str(e)}")
            return None, self.erros
    
    def avancar(self):
        """Avança para o próximo token"""
        if self.posicao < len(self.tokens) - 1:
            self.posicao += 1
            self.token_atual = self.tokens[self.posicao]
        else:
            self.token_atual = None
    
    def verificar_token(self, tipo_esperado: TokenType) -> bool:
        """Verifica se o token atual é do tipo esperado"""
        return self.token_atual and self.token_atual.tipo == tipo_esperado
    
    def consumir_token(self, tipo_esperado: TokenType) -> bool:
        """Consome um token do tipo esperado"""
        if self.verificar_token(tipo_esperado):
            self.avancar()
            return True
        else:
            tipo_atual = self.token_atual.tipo.name if self.token_atual else "EOF"
            self.erro(f"Esperado {tipo_esperado.name}, encontrado {tipo_atual}")
            return False
    
    def pular_ate_token(self, tipos_alvo: List[TokenType]):
        """Pula tokens até encontrar um dos tipos especificados"""
        while (self.token_atual and 
               self.token_atual.tipo != TokenType.EOF and 
               self.token_atual.tipo not in tipos_alvo):
            self.avancar()
    
    def erro(self, mensagem: str):
        """Adiciona um erro à lista"""
        linha = self.token_atual.linha if self.token_atual else 0
        coluna = self.token_atual.coluna if self.token_atual else 0
        self.erros.append(f"Linha: {linha:02d} - Coluna: {coluna:02d} - Erro Sintático: {mensagem}")
    
    def sincronizar(self):
        """Sincroniza o parser após um erro"""
        sincronizado = False
        while self.token_atual and self.token_atual.tipo != TokenType.EOF and not sincronizado:
            if self.token_atual.tipo in [
                TokenType.FIM_LINHA, TokenType.SE, TokenType.PARA, 
                TokenType.ENQUANTO, TokenType.FECHA_CHAVES
            ]:
                sincronizado = True
            else:
                self.avancar()
    
    # Métodos de análise sintática
    
    def programa(self) -> Optional[NoAST]:
        """
        programa ::= 'RAINBOW' '.' declaracoes
        """
        if not self.verificar_token(TokenType.RAINBOW):
            self.erro("Programa deve começar com 'RAINBOW'")
            return None
        
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        
        self.avancar()  # Consumir RAINBOW
        
        if not self.consumir_token(TokenType.FIM_LINHA):
            self.sincronizar()
        
        # Criar nó do programa
        no_programa = NoAST(TipoNo.PROGRAMA, "RAINBOW", [], linha, coluna)
        
        # Processar declarações
        while self.token_atual and self.token_atual.tipo != TokenType.EOF:
            posicao_anterior = self.posicao
            declaracao = self.declaracao()
            if declaracao:
                no_programa.filhos.append(declaracao)
            
            # Verificar se avançou para evitar loop infinito
            if self.posicao == posicao_anterior:
                self.erro(f"Token não processado: {self.token_atual.tipo.name}")
                self.avancar()  # Forçar avanço para evitar loop infinito
        
        return no_programa
    
    def declaracao(self) -> Optional[NoAST]:
        """
        declaracao ::= declaracao_variavel | atribuicao | condicional | laco | chamada_funcao
        """
        if not self.token_atual or self.token_atual.tipo == TokenType.EOF:
            return None
        
        try:
            # Declaração de variável (cor_*)
            if self.token_atual.tipo in [TokenType.TIPO_NUMERO, TokenType.TIPO_TEXTO, 
                                        TokenType.TIPO_LOGICO, TokenType.TIPO_LISTA]:
                return self.declaracao_variavel()
            
            # Atribuição de variável
            elif self.token_atual.tipo == TokenType.VARIAVEL:
                return self.atribuicao()
            
            # Estruturas de controle
            elif self.token_atual.tipo == TokenType.SE:
                return self.condicional()
            
            elif self.token_atual.tipo == TokenType.PARA:
                return self.laco_para()
            
            elif self.token_atual.tipo == TokenType.ENQUANTO:
                return self.laco_enquanto()
            
            # Chamadas de função
            elif self.token_atual.tipo in [TokenType.MOSTRAR, TokenType.LER]:
                return self.chamada_funcao()
            
            else:
                self.erro(f"Declaração inválida: {self.token_atual.tipo.name}")
                self.sincronizar()
                if self.token_atual and self.token_atual.tipo == TokenType.FIM_LINHA:
                    self.avancar()
                return None
                
        except Exception as e:
            self.erro(f"Erro na declaração: {str(e)}")
            self.sincronizar()
            if self.token_atual and self.token_atual.tipo == TokenType.FIM_LINHA:
                self.avancar()
            return None
    
    def declaracao_variavel(self) -> Optional[NoAST]:
        """
        declaracao_variavel ::= tipo_dado variavel '.'
        """
        if not self.token_atual:
            return None
        
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        tipo = self.token_atual.lexema
        
        self.avancar()  # Consumir tipo
        
        if not self.verificar_token(TokenType.VARIAVEL):
            self.erro("Esperado nome de variável após tipo")
            return None
        
        nome_var = self.token_atual.lexema
        self.avancar()  # Consumir variável
        
        if not self.consumir_token(TokenType.FIM_LINHA):
            return None
        
        # Criar nó de declaração
        no_declaracao = NoAST(TipoNo.DECLARACAO_VARIAVEL, 
                             {'tipo': tipo, 'nome': nome_var}, 
                             [], linha, coluna)
        
        return no_declaracao
    
    def atribuicao(self) -> Optional[NoAST]:
        """
        atribuicao ::= variavel 'recebe' expressao '.'
        """
        if not self.verificar_token(TokenType.VARIAVEL):
            return None
        
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        nome_var = self.token_atual.lexema
        
        self.avancar()  # Consumir variável
        
        if not self.consumir_token(TokenType.OPER_ATRIBUICAO):
            return None
        
        expressao = self.expressao()
        if not expressao:
            return None
        
        if not self.consumir_token(TokenType.FIM_LINHA):
            return None
        
        # Criar nó de atribuição
        no_atribuicao = NoAST(TipoNo.ATRIBUICAO, nome_var, [expressao], linha, coluna)
        
        return no_atribuicao
    
    def condicional(self) -> Optional[NoAST]:
        """
        condicional ::= 'se' '(' expressao ')' bloco ('senaose' '(' expressao ')' bloco)* ('senao' bloco)?
        """
        if not self.verificar_token(TokenType.SE):
            return None
        
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        
        self.avancar()  # Consumir 'se'
        
        # Verificar se há parênteses ou pular direto para expressão
        tem_parenteses = self.verificar_token(TokenType.ABRE_PARENTESES)
        if tem_parenteses:
            self.avancar()  # Consumir '('
        
        condicao = self.expressao()
        if not condicao:
            self.pular_ate_token([TokenType.ABRE_CHAVES, TokenType.FIM_LINHA])
            return None
        
        if tem_parenteses:
            if not self.consumir_token(TokenType.FECHA_PARENTESES):
                self.pular_ate_token([TokenType.ABRE_CHAVES, TokenType.FIM_LINHA])
        
        bloco_se = self.bloco()
        if not bloco_se:
            return None
        
        # Criar nó condicional
        no_condicional = NoAST(TipoNo.CONDICIONAL, "se", [condicao, bloco_se], linha, coluna)
        
        # Processar senaose
        while self.verificar_token(TokenType.SENAOSE):
            self.avancar()  # Consumir 'senaose'
            
            if not self.consumir_token(TokenType.ABRE_PARENTESES):
                break
            
            condicao_senaose = self.expressao()
            if not condicao_senaose:
                break
            
            if not self.consumir_token(TokenType.FECHA_PARENTESES):
                break
            
            bloco_senaose = self.bloco()
            if not bloco_senaose:
                break
            
            # Adicionar senaose como filho
            no_condicional.filhos.extend([condicao_senaose, bloco_senaose])
        
        # Processar senao
        if self.verificar_token(TokenType.SENAO):
            self.avancar()  # Consumir 'senao'
            
            bloco_senao = self.bloco()
            if bloco_senao:
                no_condicional.filhos.append(bloco_senao)
        
        return no_condicional
    
    def laco_para(self) -> Optional[NoAST]:
        """
        laco_para ::= 'para' variavel 'de' expressao 'ate' expressao 'passo' expressao bloco
        """
        if not self.verificar_token(TokenType.PARA):
            return None
        
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        
        self.avancar()  # Consumir 'para'
        
        if not self.verificar_token(TokenType.VARIAVEL):
            self.erro("Esperado variável após 'para'")
            return None
        
        var_controle = self.token_atual.lexema
        self.avancar()  # Consumir variável
        
        if not self.consumir_token(TokenType.DE):
            return None
        
        inicio = self.expressao()
        if not inicio:
            return None
        
        if not self.consumir_token(TokenType.ATE):
            return None
        
        fim = self.expressao()
        if not fim:
            return None
        
        if not self.consumir_token(TokenType.PASSO):
            return None
        
        passo = self.expressao()
        if not passo:
            return None
        
        corpo = self.bloco()
        if not corpo:
            return None
        
        # Criar nó do laço para
        no_para = NoAST(TipoNo.LACO_PARA, var_controle, 
                       [inicio, fim, passo, corpo], linha, coluna)
        
        return no_para
    
    def laco_enquanto(self) -> Optional[NoAST]:
        """
        laco_enquanto ::= 'enquanto' '(' expressao ')' bloco
        """
        if not self.verificar_token(TokenType.ENQUANTO):
            return None
        
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        
        self.avancar()  # Consumir 'enquanto'
        
        if not self.consumir_token(TokenType.ABRE_PARENTESES):
            return None
        
        condicao = self.expressao()
        if not condicao:
            return None
        
        if not self.consumir_token(TokenType.FECHA_PARENTESES):
            return None
        
        corpo = self.bloco()
        if not corpo:
            return None
        
        # Criar nó do laço enquanto
        no_enquanto = NoAST(TipoNo.LACO_ENQUANTO, "enquanto", 
                           [condicao, corpo], linha, coluna)
        
        return no_enquanto
    
    def chamada_funcao(self) -> Optional[NoAST]:
        """
        chamada_funcao ::= ('mostrar' | 'ler') '(' expressao? ')' '.'
        """
        if not self.token_atual or self.token_atual.tipo not in [TokenType.MOSTRAR, TokenType.LER]:
            return None
        
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        nome_funcao = self.token_atual.lexema
        
        self.avancar()  # Consumir nome da função
        
        if not self.consumir_token(TokenType.ABRE_PARENTESES):
            return None
        
        argumentos = []
        
        # Verificar se há argumentos
        if not self.verificar_token(TokenType.FECHA_PARENTESES):
            arg = self.expressao()
            if arg:
                argumentos.append(arg)
        
        if not self.consumir_token(TokenType.FECHA_PARENTESES):
            return None
        
        if not self.consumir_token(TokenType.FIM_LINHA):
            return None
        
        # Criar nó da chamada de função
        no_chamada = NoAST(TipoNo.CHAMADA_FUNCAO, nome_funcao, argumentos, linha, coluna)
        
        return no_chamada
    
    def bloco(self) -> Optional[NoAST]:
        """
        bloco ::= '{' declaracoes* '}'
        """
        if not self.verificar_token(TokenType.ABRE_CHAVES):
            self.erro("Esperado '{' para início do bloco")
            return None
        
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        
        self.avancar()  # Consumir '{'
        
        declaracoes = []
        max_iteracoes = 1000  # Limite para evitar loops infinitos
        iteracoes = 0
        
        while (self.token_atual and 
               not self.verificar_token(TokenType.FECHA_CHAVES) and 
               self.token_atual.tipo != TokenType.EOF and
               iteracoes < max_iteracoes):
            
            posicao_antes = self.posicao
            declaracao = self.declaracao()
            
            if declaracao:
                declaracoes.append(declaracao)
            
            # Verificar se avançou para evitar loop infinito
            if self.posicao == posicao_antes:
                self.erro(f"Token não processado no bloco: {self.token_atual.tipo.name}")
                self.avancar()
            
            iteracoes += 1
        
        if iteracoes >= max_iteracoes:
            self.erro("Limite de iterações atingido no bloco - possível loop infinito")
        
        if self.token_atual and not self.verificar_token(TokenType.FECHA_CHAVES):
            if self.token_atual.tipo != TokenType.EOF:
                self.erro("Esperado '}' para fechar o bloco")
        else:
            if self.verificar_token(TokenType.FECHA_CHAVES):
                self.avancar()  # Consumir '}'
        
        # Criar nó do bloco
        no_bloco = NoAST(TipoNo.BLOCO, "bloco", declaracoes, linha, coluna)
        
        return no_bloco
    
    def expressao(self) -> Optional[NoAST]:
        """
        expressao ::= expressao_ou
        """
        return self.expressao_ou()
    
    def expressao_ou(self) -> Optional[NoAST]:
        """
        expressao_ou ::= expressao_e ('OU' expressao_e)*
        """
        esquerda = self.expressao_e()
        if not esquerda:
            return None
        
        while self.verificar_token(TokenType.OPER_OU):
            operador = self.token_atual.lexema
            linha = self.token_atual.linha
            coluna = self.token_atual.coluna
            
            self.avancar()  # Consumir operador
            
            direita = self.expressao_e()
            if not direita:
                return None
            
            esquerda = NoAST(TipoNo.EXPRESSAO_BINARIA, operador, 
                           [esquerda, direita], linha, coluna)
        
        return esquerda
    
    def expressao_e(self) -> Optional[NoAST]:
        """
        expressao_e ::= expressao_igualdade ('E' expressao_igualdade)*
        """
        esquerda = self.expressao_igualdade()
        if not esquerda:
            return None
        
        while self.verificar_token(TokenType.OPER_E):
            operador = self.token_atual.lexema
            linha = self.token_atual.linha
            coluna = self.token_atual.coluna
            
            self.avancar()  # Consumir operador
            
            direita = self.expressao_igualdade()
            if not direita:
                return None
            
            esquerda = NoAST(TipoNo.EXPRESSAO_BINARIA, operador, 
                           [esquerda, direita], linha, coluna)
        
        return esquerda
    
    def expressao_igualdade(self) -> Optional[NoAST]:
        """
        expressao_igualdade ::= expressao_comparacao (('igual' | 'diferente') expressao_comparacao)*
        """
        esquerda = self.expressao_comparacao()
        if not esquerda:
            return None
        
        while self.verificar_token(TokenType.OPER_IGUAL) or self.verificar_token(TokenType.OPER_DIFERENTE):
            operador = self.token_atual.lexema
            linha = self.token_atual.linha
            coluna = self.token_atual.coluna
            
            self.avancar()  # Consumir operador
            
            direita = self.expressao_comparacao()
            if not direita:
                return None
            
            esquerda = NoAST(TipoNo.EXPRESSAO_BINARIA, operador, 
                           [esquerda, direita], linha, coluna)
        
        return esquerda
    
    def expressao_comparacao(self) -> Optional[NoAST]:
        """
        expressao_comparacao ::= expressao_adicao (('>' | '<' | '>=' | '<=') expressao_adicao)*
        """
        esquerda = self.expressao_adicao()
        if not esquerda:
            return None
        
        while self.token_atual and self.token_atual.tipo in [
            TokenType.OPER_MAIOR, TokenType.OPER_MENOR, 
            TokenType.OPER_MAIOR_IGUAL, TokenType.OPER_MENOR_IGUAL
        ]:
            operador = self.token_atual.lexema
            linha = self.token_atual.linha
            coluna = self.token_atual.coluna
            
            self.avancar()  # Consumir operador
            
            direita = self.expressao_adicao()
            if not direita:
                return None
            
            esquerda = NoAST(TipoNo.EXPRESSAO_BINARIA, operador, 
                           [esquerda, direita], linha, coluna)
        
        return esquerda
    
    def expressao_adicao(self) -> Optional[NoAST]:
        """
        expressao_adicao ::= expressao_multiplicacao (('+' | '-') expressao_multiplicacao)*
        """
        esquerda = self.expressao_multiplicacao()
        if not esquerda:
            return None
        
        while self.verificar_token(TokenType.OPER_SOMA) or self.verificar_token(TokenType.OPER_SUBTRACAO):
            operador = self.token_atual.lexema
            linha = self.token_atual.linha
            coluna = self.token_atual.coluna
            
            self.avancar()  # Consumir operador
            
            direita = self.expressao_multiplicacao()
            if not direita:
                return None
            
            esquerda = NoAST(TipoNo.EXPRESSAO_BINARIA, operador, 
                           [esquerda, direita], linha, coluna)
        
        return esquerda
    
    def expressao_multiplicacao(self) -> Optional[NoAST]:
        """
        expressao_multiplicacao ::= expressao_unaria (('*' | '/' | '%') expressao_unaria)*
        """
        esquerda = self.expressao_unaria()
        if not esquerda:
            return None
        
        while self.token_atual and self.token_atual.tipo in [
            TokenType.OPER_MULTIPLICACAO, TokenType.OPER_DIVISAO, TokenType.OPER_MODULO
        ]:
            operador = self.token_atual.lexema
            linha = self.token_atual.linha
            coluna = self.token_atual.coluna
            
            self.avancar()  # Consumir operador
            
            direita = self.expressao_unaria()
            if not direita:
                return None
            
            esquerda = NoAST(TipoNo.EXPRESSAO_BINARIA, operador, 
                           [esquerda, direita], linha, coluna)
        
        return esquerda
    
    def expressao_unaria(self) -> Optional[NoAST]:
        """
        expressao_unaria ::= ('NAO' | '-') expressao_unaria | expressao_primaria
        """
        if self.verificar_token(TokenType.OPER_NAO) or self.verificar_token(TokenType.OPER_SUBTRACAO):
            operador = self.token_atual.lexema
            linha = self.token_atual.linha
            coluna = self.token_atual.coluna
            
            self.avancar()  # Consumir operador
            
            expressao = self.expressao_unaria()
            if not expressao:
                return None
            
            return NoAST(TipoNo.EXPRESSAO_UNARIA, operador, [expressao], linha, coluna)
        
        return self.expressao_primaria()
    
    def expressao_primaria(self) -> Optional[NoAST]:
        """
        expressao_primaria ::= numero | texto | 'Verdadeiro' | 'Falso' | variavel | 
                              '(' expressao ')' | chamada_funcao_expr
        """
        if not self.token_atual:
            return None
        
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        
        # Números
        if self.verificar_token(TokenType.NUMERO):
            valor = self.token_atual.lexema
            self.avancar()
            return NoAST(TipoNo.LITERAL, valor, [], linha, coluna)
        
        # Strings
        if self.verificar_token(TokenType.TEXTO):
            valor = self.token_atual.lexema
            self.avancar()
            return NoAST(TipoNo.LITERAL, valor, [], linha, coluna)
        
        # Booleanos
        if self.verificar_token(TokenType.VERDADEIRO) or self.verificar_token(TokenType.FALSO):
            valor = self.token_atual.lexema
            self.avancar()
            return NoAST(TipoNo.LITERAL, valor, [], linha, coluna)
        
        # Variáveis
        if self.verificar_token(TokenType.VARIAVEL):
            nome = self.token_atual.lexema
            self.avancar()
            return NoAST(TipoNo.VARIAVEL, nome, [], linha, coluna)
        
        # Expressões parentizadas
        if self.verificar_token(TokenType.ABRE_PARENTESES):
            self.avancar()  # Consumir '('
            
            expr = self.expressao()
            if not expr:
                return None
            
            if not self.consumir_token(TokenType.FECHA_PARENTESES):
                return None
            
            return expr
        
        # Chamadas de função em expressões (principalmente 'ler')
        if self.verificar_token(TokenType.LER):
            nome_funcao = self.token_atual.lexema
            self.avancar()  # Consumir nome da função
            
            if not self.consumir_token(TokenType.ABRE_PARENTESES):
                return None
            
            argumentos = []
            
            # Verificar se há argumentos
            if not self.verificar_token(TokenType.FECHA_PARENTESES):
                arg = self.expressao()
                if arg:
                    argumentos.append(arg)
            
            if not self.consumir_token(TokenType.FECHA_PARENTESES):
                return None
            
            return NoAST(TipoNo.CHAMADA_FUNCAO, nome_funcao, argumentos, linha, coluna)
        
        # Se chegou aqui, não reconheceu o token
        self.erro(f"Expressão inválida: {self.token_atual.tipo.name}")
        return None
    
    def gerar_relatorio_ast(self, ast: Optional[NoAST], arquivo_saida: str):
        """Gera arquivo com representação da AST"""
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("=== ÁRVORE SINTÁTICA ABSTRATA ===\n")
            f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if ast:
                self._escrever_ast(f, ast, 0)
            else:
                f.write("AST não foi gerada devido a erros.\n")
    
    def _escrever_ast(self, arquivo, no: NoAST, indentacao: int):
        """Escreve um nó da AST no arquivo com indentação"""
        indent = "  " * indentacao
        arquivo.write(f"{indent}{no.tipo.name}")
        
        if no.valor:
            arquivo.write(f": {no.valor}")
        
        arquivo.write(f" (L:{no.linha}, C:{no.coluna})\n")
        
        for filho in no.filhos:
            self._escrever_ast(arquivo, filho, indentacao + 1)
    
    def exportar_ast_json(self, ast: Optional[NoAST], arquivo_saida: str):
        """Exporta AST em formato JSON"""
        resultado = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_erros': len(self.erros)
            },
            'ast': ast.to_dict() if ast else None,
            'erros': self.erros
        }
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)


def main():
    """Função principal para testar o parser"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python analisador_sintatico.py <arquivo.rainbow>")
        return
    
    arquivo = sys.argv[1]
    
    try:
        # Executar análise léxica primeiro
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        print("=== ANÁLISE LÉXICA ===")
        analisador_lexico = AnalisadorLexico()
        tokens, erros_lexicos = analisador_lexico.analisar(codigo)
        
        if erros_lexicos:
            print("Erros léxicos encontrados:")
            for erro in erros_lexicos:
                print(f"  {erro}")
            print()
        
        # Executar análise sintática
        print("=== ANÁLISE SINTÁTICA ===")
        analisador_sintatico = AnalisadorSintatico()
        ast, erros_sintaticos = analisador_sintatico.analisar(tokens)
        
        if erros_sintaticos:
            print("Erros sintáticos encontrados:")
            for erro in erros_sintaticos:
                print(f"  {erro}")
        else:
            print("✅ Análise sintática concluída sem erros!")
        
        # Gerar arquivos de saída
        base_name = os.path.splitext(arquivo)[0]
        
        # Gerar arquivo .ast
        ast_file = base_name + '.ast'
        analisador_sintatico.gerar_relatorio_ast(ast, ast_file)
        print(f"✅ Arquivo AST gerado: {ast_file}")
        
        # Gerar JSON da AST
        ast_json_file = base_name + '.ast.json'
        analisador_sintatico.exportar_ast_json(ast, ast_json_file)
        print(f"✅ Arquivo JSON da AST gerado: {ast_json_file}")
        
        print(f"\nTotal de erros léxicos: {len(erros_lexicos)}")
        print(f"Total de erros sintáticos: {len(erros_sintaticos)}")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()