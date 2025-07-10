"""
Analisador Semântico para a Linguagem Rainbow
Implementa verificação de tipos, escopo e tabela de símbolos
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Set
from enum import Enum, auto
from analisador_sintatico import NoAST, TipoNo
import json
import os
from datetime import datetime


class TipoSimbolo(Enum):
    """Tipos de dados da linguagem Rainbow"""
    NUMERO = auto()
    TEXTO = auto()
    LOGICO = auto()
    LISTA = auto()
    INDEFINIDO = auto()


class TipoEscopo(Enum):
    """Tipos de escopo"""
    GLOBAL = auto()
    BLOCO = auto()
    LACO = auto()


@dataclass
class Simbolo:
    """Representa um símbolo na tabela de símbolos"""
    nome: str
    tipo: TipoSimbolo
    escopo: TipoEscopo
    linha: int
    coluna: int
    declarado: bool = False
    usado: bool = False
    valor_inicial: Any = None
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'tipo': self.tipo.name,
            'escopo': self.escopo.name,
            'linha': self.linha,
            'coluna': self.coluna,
            'declarado': self.declarado,
            'usado': self.usado,
            'valor_inicial': self.valor_inicial
        }


class TabelaSimbolos:
    """Tabela de símbolos com suporte a escopo hierárquico"""
    
    def __init__(self):
        self.escopos: List[Dict[str, Simbolo]] = [{}]  # Escopo global
        self.tipos_escopo: List[TipoEscopo] = [TipoEscopo.GLOBAL]
        self.historico_simbolos: List[Simbolo] = []
    
    def entrar_escopo(self, tipo_escopo: TipoEscopo = TipoEscopo.BLOCO):
        """Entra em um novo escopo"""
        self.escopos.append({})
        self.tipos_escopo.append(tipo_escopo)
    
    def sair_escopo(self):
        """Sai do escopo atual"""
        if len(self.escopos) > 1:
            escopo_removido = self.escopos.pop()
            self.tipos_escopo.pop()
            # Adicionar símbolos removidos ao histórico
            for simbolo in escopo_removido.values():
                self.historico_simbolos.append(simbolo)
    
    def declarar_simbolo(self, nome: str, tipo: TipoSimbolo, linha: int, coluna: int) -> bool:
        """Declara um novo símbolo no escopo atual"""
        escopo_atual = self.escopos[-1]
        tipo_escopo_atual = self.tipos_escopo[-1]
        
        if nome in escopo_atual:
            return False  # Já declarado no escopo atual
        
        simbolo = Simbolo(nome, tipo, tipo_escopo_atual, linha, coluna, True)
        escopo_atual[nome] = simbolo
        return True
    
    def buscar_simbolo(self, nome: str) -> Optional[Simbolo]:
        """Busca um símbolo em todos os escopos (do mais interno ao mais externo)"""
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        return None
    
    def marcar_usado(self, nome: str) -> bool:
        """Marca um símbolo como usado"""
        simbolo = self.buscar_simbolo(nome)
        if simbolo:
            simbolo.usado = True
            return True
        return False
    
    def obter_simbolos_nao_usados(self) -> List[Simbolo]:
        """Retorna símbolos declarados mas não usados"""
        simbolos_nao_usados = []
        
        # Verificar escopos atuais
        for escopo in self.escopos:
            for simbolo in escopo.values():
                if simbolo.declarado and not simbolo.usado:
                    simbolos_nao_usados.append(simbolo)
        
        # Verificar histórico
        for simbolo in self.historico_simbolos:
            if simbolo.declarado and not simbolo.usado:
                simbolos_nao_usados.append(simbolo)
        
        return simbolos_nao_usados
    
    def obter_todos_simbolos(self) -> List[Simbolo]:
        """Retorna todos os símbolos (atuais + histórico)"""
        todos_simbolos = []
        
        for escopo in self.escopos:
            todos_simbolos.extend(escopo.values())
        
        todos_simbolos.extend(self.historico_simbolos)
        return todos_simbolos


class AnalisadorSemantico:
    """Analisador semântico da linguagem Rainbow"""
    
    def __init__(self):
        self.tabela_simbolos = TabelaSimbolos()
        self.erros: List[str] = []
        self.avisos: List[str] = []
        
        # Mapeamento de tipos de tokens para tipos semânticos
        self.mapeamento_tipos = {
            'numero': TipoSimbolo.NUMERO,
            'texto': TipoSimbolo.TEXTO,
            'logico': TipoSimbolo.LOGICO,
            'lista': TipoSimbolo.LISTA
        }
    
    def analisar(self, ast: NoAST) -> tuple[List[str], List[str]]:
        """
        Realiza análise semântica da AST
        Retorna (erros, avisos)
        """
        self.erros = []
        self.avisos = []
        
        if not ast:
            self.erros.append("AST não fornecida para análise semântica")
            return self.erros, self.avisos
        
        try:
            self._analisar_no(ast)
            
            # Verificar símbolos não usados
            simbolos_nao_usados = self.tabela_simbolos.obter_simbolos_nao_usados()
            for simbolo in simbolos_nao_usados:
                self.avisos.append(
                    f"Linha: {simbolo.linha:02d} - Coluna: {simbolo.coluna:02d} - "
                    f"Aviso: Variável '{simbolo.nome}' declarada mas não utilizada"
                )
            
        except Exception as e:
            self.erros.append(f"Erro interno na análise semântica: {str(e)}")
        
        return self.erros, self.avisos
    
    def _analisar_no(self, no: NoAST):
        """Analisa um nó da AST recursivamente"""
        if no.tipo == TipoNo.PROGRAMA:
            self._analisar_programa(no)
        elif no.tipo == TipoNo.DECLARACAO_VARIAVEL:
            self._analisar_declaracao_variavel(no)
        elif no.tipo == TipoNo.ATRIBUICAO:
            self._analisar_atribuicao(no)
        elif no.tipo == TipoNo.CONDICIONAL:
            self._analisar_condicional(no)
        elif no.tipo == TipoNo.LACO_PARA:
            self._analisar_laco_para(no)
        elif no.tipo == TipoNo.LACO_ENQUANTO:
            self._analisar_laco_enquanto(no)
        elif no.tipo == TipoNo.CHAMADA_FUNCAO:
            self._analisar_chamada_funcao(no)
        elif no.tipo == TipoNo.BLOCO:
            self._analisar_bloco(no)
        elif no.tipo == TipoNo.EXPRESSAO_BINARIA:
            self._analisar_expressao_binaria(no)
        elif no.tipo == TipoNo.EXPRESSAO_UNARIA:
            self._analisar_expressao_unaria(no)
        elif no.tipo == TipoNo.VARIAVEL:
            self._analisar_variavel(no)
        elif no.tipo == TipoNo.LITERAL:
            self._analisar_literal(no)
    
    def _analisar_programa(self, no: NoAST):
        """Analisa o nó programa"""
        for filho in no.filhos:
            self._analisar_no(filho)
    
    def _analisar_declaracao_variavel(self, no: NoAST):
        """Analisa declaração de variável"""
        if not isinstance(no.valor, dict) or 'tipo' not in no.valor or 'nome' not in no.valor:
            self.erros.append(f"Linha: {no.linha:02d} - Erro: Declaração de variável mal formada")
            return
        
        tipo_str = no.valor['tipo']
        nome_var = no.valor['nome']
        
        if tipo_str not in self.mapeamento_tipos:
            self.erros.append(
                f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                f"Erro: Tipo '{tipo_str}' não reconhecido"
            )
            return
        
        tipo_simbolo = self.mapeamento_tipos[tipo_str]
        
        if not self.tabela_simbolos.declarar_simbolo(nome_var, tipo_simbolo, no.linha, no.coluna):
            self.erros.append(
                f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                f"Erro: Variável '{nome_var}' já foi declarada neste escopo"
            )
    
    def _analisar_atribuicao(self, no: NoAST):
        """Analisa atribuição de variável"""
        nome_var = no.valor
        
        # Verificar se a variável foi declarada
        simbolo = self.tabela_simbolos.buscar_simbolo(nome_var)
        
        # Analisar expressão do lado direito primeiro
        tipo_expressao = TipoSimbolo.INDEFINIDO
        if no.filhos:
            tipo_expressao = self._analisar_expressao(no.filhos[0])
        
        if not simbolo:
            # Declaração implícita: inferir tipo da expressão
            if tipo_expressao != TipoSimbolo.INDEFINIDO:
                self.tabela_simbolos.declarar_simbolo(nome_var, tipo_expressao, no.linha, no.coluna)
                simbolo = self.tabela_simbolos.buscar_simbolo(nome_var)
            else:
                # Se não conseguir inferir, assumir como indefinido por enquanto
                self.tabela_simbolos.declarar_simbolo(nome_var, TipoSimbolo.INDEFINIDO, no.linha, no.coluna)
                simbolo = self.tabela_simbolos.buscar_simbolo(nome_var)
        
        # Marcar como usada
        if simbolo:
            self.tabela_simbolos.marcar_usado(nome_var)
            
            # Verificar compatibilidade de tipos (apenas se ambos estão definidos)
            if (tipo_expressao != TipoSimbolo.INDEFINIDO and 
                simbolo.tipo != TipoSimbolo.INDEFINIDO and 
                simbolo.tipo != tipo_expressao):
                # Permitir algumas conversões implícitas
                if not self._conversao_permitida(simbolo.tipo, tipo_expressao):
                    self.avisos.append(
                        f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                        f"Aviso: Possível incompatibilidade de tipos - esperado '{simbolo.tipo.name}', "
                        f"encontrado '{tipo_expressao.name}'"
                    )
    
    def _analisar_condicional(self, no: NoAST):
        """Analisa estrutura condicional"""
        if no.filhos:
            # Analisar condição
            tipo_condicao = self._analisar_expressao(no.filhos[0])
            
            if tipo_condicao != TipoSimbolo.LOGICO and tipo_condicao != TipoSimbolo.INDEFINIDO:
                self.erros.append(
                    f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                    f"Erro: Condição deve ser do tipo 'logico', encontrado '{tipo_condicao.name}'"
                )
            
            # Analisar blocos
            for i in range(1, len(no.filhos)):
                self._analisar_no(no.filhos[i])
    
    def _analisar_laco_para(self, no: NoAST):
        """Analisa laço para"""
        nome_var_controle = no.valor
        
        # Declarar variável de controle no escopo do laço
        self.tabela_simbolos.entrar_escopo(TipoEscopo.LACO)
        
        if not self.tabela_simbolos.declarar_simbolo(nome_var_controle, TipoSimbolo.NUMERO, no.linha, no.coluna):
            # Se já existe, verificar se é do tipo correto
            simbolo = self.tabela_simbolos.buscar_simbolo(nome_var_controle)
            if simbolo and simbolo.tipo != TipoSimbolo.NUMERO:
                self.erros.append(
                    f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                    f"Erro: Variável de controle '{nome_var_controle}' deve ser do tipo 'numero'"
                )
        
        # Marcar variável de controle como usada
        self.tabela_simbolos.marcar_usado(nome_var_controle)
        
        if len(no.filhos) >= 4:
            # Analisar expressões de início, fim e passo
            for i in range(3):
                tipo_expr = self._analisar_expressao(no.filhos[i])
                if tipo_expr != TipoSimbolo.NUMERO and tipo_expr != TipoSimbolo.INDEFINIDO:
                    self.erros.append(
                        f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                        f"Erro: Expressões do laço 'para' devem ser do tipo 'numero'"
                    )
            
            # Analisar corpo do laço
            self._analisar_no(no.filhos[3])
        
        self.tabela_simbolos.sair_escopo()
    
    def _analisar_laco_enquanto(self, no: NoAST):
        """Analisa laço enquanto"""
        self.tabela_simbolos.entrar_escopo(TipoEscopo.LACO)
        
        if no.filhos:
            # Analisar condição
            tipo_condicao = self._analisar_expressao(no.filhos[0])
            
            if tipo_condicao != TipoSimbolo.LOGICO and tipo_condicao != TipoSimbolo.INDEFINIDO:
                self.erros.append(
                    f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                    f"Erro: Condição do 'enquanto' deve ser do tipo 'logico'"
                )
            
            # Analisar corpo
            if len(no.filhos) > 1:
                self._analisar_no(no.filhos[1])
        
        self.tabela_simbolos.sair_escopo()
    
    def _analisar_chamada_funcao(self, no: NoAST):
        """Analisa chamada de função"""
        nome_funcao = no.valor
        
        # Verificar funções built-in
        if nome_funcao == "mostrar":
            if no.filhos:
                self._analisar_expressao(no.filhos[0])
        elif nome_funcao == "ler":
            if no.filhos:
                tipo_arg = self._analisar_expressao(no.filhos[0])
                if tipo_arg != TipoSimbolo.TEXTO and tipo_arg != TipoSimbolo.INDEFINIDO:
                    self.avisos.append(
                        f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                        f"Aviso: Argumento de 'ler' deve ser do tipo 'texto'"
                    )
        else:
            self.erros.append(
                f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                f"Erro: Função '{nome_funcao}' não reconhecida"
            )
    
    def _analisar_bloco(self, no: NoAST):
        """Analisa bloco de código"""
        self.tabela_simbolos.entrar_escopo(TipoEscopo.BLOCO)
        
        for filho in no.filhos:
            self._analisar_no(filho)
        
        self.tabela_simbolos.sair_escopo()
    
    def _analisar_expressao(self, no: NoAST) -> TipoSimbolo:
        """Analisa expressão e retorna seu tipo"""
        if no.tipo == TipoNo.LITERAL:
            return self._analisar_literal(no)
        elif no.tipo == TipoNo.VARIAVEL:
            return self._analisar_variavel(no)
        elif no.tipo == TipoNo.EXPRESSAO_BINARIA:
            return self._analisar_expressao_binaria(no)
        elif no.tipo == TipoNo.EXPRESSAO_UNARIA:
            return self._analisar_expressao_unaria(no)
        elif no.tipo == TipoNo.CHAMADA_FUNCAO:
            self._analisar_chamada_funcao(no)
            if no.valor == "ler":
                return TipoSimbolo.TEXTO  # ler retorna texto
            return TipoSimbolo.INDEFINIDO
        else:
            return TipoSimbolo.INDEFINIDO
    
    def _analisar_expressao_binaria(self, no: NoAST) -> TipoSimbolo:
        """Analisa expressão binária e retorna seu tipo"""
        if len(no.filhos) < 2:
            return TipoSimbolo.INDEFINIDO
        
        tipo_esq = self._analisar_expressao(no.filhos[0])
        tipo_dir = self._analisar_expressao(no.filhos[1])
        operador = no.valor
        
        # Operadores aritméticos
        if operador in ['+', '-', '*', '/', '%']:
            if operador == '+':
                # + pode ser soma ou concatenação
                if tipo_esq == TipoSimbolo.TEXTO or tipo_dir == TipoSimbolo.TEXTO:
                    return TipoSimbolo.TEXTO
                elif tipo_esq == TipoSimbolo.NUMERO and tipo_dir == TipoSimbolo.NUMERO:
                    return TipoSimbolo.NUMERO
                else:
                    self.erros.append(
                        f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                        f"Erro: Operador '+' requer tipos compatíveis"
                    )
                    return TipoSimbolo.INDEFINIDO
            else:
                if tipo_esq != TipoSimbolo.NUMERO or tipo_dir != TipoSimbolo.NUMERO:
                    self.erros.append(
                        f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                        f"Erro: Operador '{operador}' requer operandos do tipo 'numero'"
                    )
                return TipoSimbolo.NUMERO
        
        # Operadores relacionais
        elif operador in ['>', '<', '>=', '<=', 'igual', 'diferente']:
            # Permitir comparações entre tipos compatíveis
            if (tipo_esq != tipo_dir and 
                tipo_esq != TipoSimbolo.INDEFINIDO and 
                tipo_dir != TipoSimbolo.INDEFINIDO and
                not self._tipos_comparaveis(tipo_esq, tipo_dir)):
                self.avisos.append(
                    f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                    f"Aviso: Comparação entre tipos diferentes ('{tipo_esq.name}' e '{tipo_dir.name}')"
                )
            return TipoSimbolo.LOGICO
        
        # Operadores lógicos
        elif operador in ['E', 'OU']:
            if tipo_esq != TipoSimbolo.LOGICO or tipo_dir != TipoSimbolo.LOGICO:
                self.erros.append(
                    f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                    f"Erro: Operador '{operador}' requer operandos do tipo 'logico'"
                )
            return TipoSimbolo.LOGICO
        
        return TipoSimbolo.INDEFINIDO
    
    def _analisar_expressao_unaria(self, no: NoAST) -> TipoSimbolo:
        """Analisa expressão unária e retorna seu tipo"""
        if not no.filhos:
            return TipoSimbolo.INDEFINIDO
        
        tipo_operando = self._analisar_expressao(no.filhos[0])
        operador = no.valor
        
        if operador == '-':
            if tipo_operando != TipoSimbolo.NUMERO:
                self.erros.append(
                    f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                    f"Erro: Operador '-' unário requer operando do tipo 'numero'"
                )
            return TipoSimbolo.NUMERO
        elif operador == 'NAO':
            if tipo_operando != TipoSimbolo.LOGICO:
                self.erros.append(
                    f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                    f"Erro: Operador 'NAO' requer operando do tipo 'logico'"
                )
            return TipoSimbolo.LOGICO
        
        return TipoSimbolo.INDEFINIDO
    
    def _analisar_variavel(self, no: NoAST) -> TipoSimbolo:
        """Analisa uso de variável e retorna seu tipo"""
        nome_var = no.valor
        
        simbolo = self.tabela_simbolos.buscar_simbolo(nome_var)
        if not simbolo:
            # Em Rainbow, variáveis podem ser usadas sem declaração explícita
            # Vamos criar um símbolo com tipo indefinido e gerar um aviso
            self.avisos.append(
                f"Linha: {no.linha:02d} - Coluna: {no.coluna:02d} - "
                f"Aviso: Variável '{nome_var}' usada sem declaração explícita"
            )
            # Declarar implicitamente com tipo indefinido
            self.tabela_simbolos.declarar_simbolo(nome_var, TipoSimbolo.INDEFINIDO, no.linha, no.coluna)
            simbolo = self.tabela_simbolos.buscar_simbolo(nome_var)
        
        # Marcar como usada
        if simbolo:
            self.tabela_simbolos.marcar_usado(nome_var)
            return simbolo.tipo
        
        return TipoSimbolo.INDEFINIDO
    
    def _analisar_literal(self, no: NoAST) -> TipoSimbolo:
        """Analisa literal e retorna seu tipo"""
        valor = no.valor
        
        if isinstance(valor, str):
            if valor.startswith('"') and valor.endswith('"'):
                return TipoSimbolo.TEXTO
            elif valor in ['Verdadeiro', 'Falso']:
                return TipoSimbolo.LOGICO
            elif valor.replace('.', '').replace('-', '').isdigit():
                return TipoSimbolo.NUMERO
        
        return TipoSimbolo.INDEFINIDO
    
    def _conversao_permitida(self, tipo_destino: TipoSimbolo, tipo_origem: TipoSimbolo) -> bool:
        """Verifica se uma conversão de tipo é permitida"""
        # Conversões implícitas permitidas
        conversoes_permitidas = {
            TipoSimbolo.TEXTO: [TipoSimbolo.NUMERO, TipoSimbolo.LOGICO],  # Para concatenação
            TipoSimbolo.NUMERO: [TipoSimbolo.TEXTO],  # Para conversão string->numero
        }
        
        return tipo_origem in conversoes_permitidas.get(tipo_destino, [])
    
    def _tipos_comparaveis(self, tipo1: TipoSimbolo, tipo2: TipoSimbolo) -> bool:
        """Verifica se dois tipos podem ser comparados"""
        # Tipos idênticos são sempre comparáveis
        if tipo1 == tipo2:
            return True
        
        # Texto e número são comparáveis (conversão implícita)
        if (tipo1 == TipoSimbolo.TEXTO and tipo2 == TipoSimbolo.NUMERO) or \
           (tipo1 == TipoSimbolo.NUMERO and tipo2 == TipoSimbolo.TEXTO):
            return True
        
        return False
    
    def gerar_relatorio_simbolos(self, arquivo_saida: str):
        """Gera relatório da tabela de símbolos"""
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("=== TABELA DE SÍMBOLOS ===\n")
            f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            simbolos = self.tabela_simbolos.obter_todos_simbolos()
            
            if simbolos:
                f.write("=== SÍMBOLOS DECLARADOS ===\n")
                for simbolo in sorted(simbolos, key=lambda s: (s.linha, s.coluna)):
                    status = "✓" if simbolo.usado else "✗"
                    f.write(
                        f"{status} {simbolo.nome} | Tipo: {simbolo.tipo.name} | "
                        f"Escopo: {simbolo.escopo.name} | "
                        f"Linha: {simbolo.linha:02d}, Coluna: {simbolo.coluna:02d}\n"
                    )
                
                simbolos_nao_usados = self.tabela_simbolos.obter_simbolos_nao_usados()
                if simbolos_nao_usados:
                    f.write(f"\n=== SÍMBOLOS NÃO UTILIZADOS ===\n")
                    for simbolo in simbolos_nao_usados:
                        f.write(f"- {simbolo.nome} (Linha: {simbolo.linha:02d})\n")
            else:
                f.write("Nenhum símbolo declarado.\n")
            
            f.write(f"\n=== RESUMO ===\n")
            f.write(f"Total de símbolos: {len(simbolos)}\n")
            f.write(f"Total de erros: {len(self.erros)}\n")
            f.write(f"Total de avisos: {len(self.avisos)}\n")
    
    def gerar_relatorio_erros_semanticos(self, arquivo_saida: str):
        """Gera relatório específico de erros semânticos"""
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("=== RELATÓRIO DE ERROS SEMÂNTICOS ===\n")
            f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if self.erros:
                f.write("=== ERROS ===\n")
                for erro in self.erros:
                    f.write(f"{erro}\n")
            else:
                f.write("Nenhum erro semântico encontrado!\n")
            
            if self.avisos:
                f.write(f"\n=== AVISOS ===\n")
                for aviso in self.avisos:
                    f.write(f"{aviso}\n")
            
            f.write(f"\n=== RESUMO ===\n")
            f.write(f"Total de erros semânticos: {len(self.erros)}\n")
            f.write(f"Total de avisos: {len(self.avisos)}\n")
    
    def exportar_json(self, arquivo_saida: str):
        """Exporta análise semântica em JSON"""
        simbolos = self.tabela_simbolos.obter_todos_simbolos()
        
        resultado = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_simbolos': len(simbolos),
                'total_erros': len(self.erros),
                'total_avisos': len(self.avisos)
            },
            'simbolos': [simbolo.to_dict() for simbolo in simbolos],
            'erros': self.erros,
            'avisos': self.avisos,
            'estatisticas': {
                'simbolos_por_tipo': self._contar_simbolos_por_tipo(simbolos),
                'simbolos_por_escopo': self._contar_simbolos_por_escopo(simbolos),
                'simbolos_nao_usados': len(self.tabela_simbolos.obter_simbolos_nao_usados())
            }
        }
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    def _contar_simbolos_por_tipo(self, simbolos: List[Simbolo]) -> Dict[str, int]:
        """Conta símbolos por tipo"""
        contagem = {}
        for simbolo in simbolos:
            tipo = simbolo.tipo.name
            contagem[tipo] = contagem.get(tipo, 0) + 1
        return contagem
    
    def _contar_simbolos_por_escopo(self, simbolos: List[Simbolo]) -> Dict[str, int]:
        """Conta símbolos por escopo"""
        contagem = {}
        for simbolo in simbolos:
            escopo = simbolo.escopo.name
            contagem[escopo] = contagem.get(escopo, 0) + 1
        return contagem


def main():
    """Função principal para testar o analisador semântico"""
    import sys
    from analisador_lexico import AnalisadorLexico
    from analisador_sintatico import AnalisadorSintatico
    
    if len(sys.argv) < 2:
        print("Uso: python analisador_semantico.py <arquivo.rainbow>")
        return
    
    arquivo = sys.argv[1]
    
    try:
        # Executar todas as fases
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        print("=== ANÁLISE COMPLETA ===")
        
        # Fase 1: Análise Léxica
        print("1. Análise Léxica...")
        analisador_lexico = AnalisadorLexico()
        tokens, erros_lexicos = analisador_lexico.analisar(codigo)
        
        if erros_lexicos:
            print(f"   ❌ {len(erros_lexicos)} erro(s) léxico(s)")
            for erro in erros_lexicos[:3]:  # Mostrar apenas os primeiros 3
                print(f"      {erro}")
            if len(erros_lexicos) > 3:
                print(f"      ... e mais {len(erros_lexicos) - 3} erro(s)")
        else:
            print("   ✅ Sem erros léxicos")
        
        # Fase 2: Análise Sintática
        print("2. Análise Sintática...")
        analisador_sintatico = AnalisadorSintatico()
        ast, erros_sintaticos = analisador_sintatico.analisar(tokens)
        
        if erros_sintaticos:
            print(f"   ❌ {len(erros_sintaticos)} erro(s) sintático(s)")
            for erro in erros_sintaticos[:3]:
                print(f"      {erro}")
            if len(erros_sintaticos) > 3:
                print(f"      ... e mais {len(erros_sintaticos) - 3} erro(s)")
        else:
            print("   ✅ Sem erros sintáticos")
        
        # Fase 3: Análise Semântica
        print("3. Análise Semântica...")
        analisador_semantico = AnalisadorSemantico()
        erros_semanticos, avisos = analisador_semantico.analisar(ast)
        
        if erros_semanticos:
            print(f"   ❌ {len(erros_semanticos)} erro(s) semântico(s)")
            for erro in erros_semanticos[:3]:
                print(f"      {erro}")
            if len(erros_semanticos) > 3:
                print(f"      ... e mais {len(erros_semanticos) - 3} erro(s)")
        else:
            print("   ✅ Sem erros semânticos")
        
        if avisos:
            print(f"   ⚠️  {len(avisos)} aviso(s)")
            for aviso in avisos[:3]:
                print(f"      {aviso}")
            if len(avisos) > 3:
                print(f"      ... e mais {len(avisos) - 3} aviso(s)")
        
        # Gerar arquivos de saída
        base_name = os.path.splitext(arquivo)[0]
        
        # Relatório de símbolos
        simbolos_file = base_name + '.simbolos'
        analisador_semantico.gerar_relatorio_simbolos(simbolos_file)
        print(f"✅ Arquivo de símbolos gerado: {simbolos_file}")
        
        # Relatório de erros semânticos
        semantic_errors_file = base_name + '.semantic.errors'
        analisador_semantico.gerar_relatorio_erros_semanticos(semantic_errors_file)
        print(f"✅ Arquivo de erros semânticos gerado: {semantic_errors_file}")
        
        # JSON da análise semântica
        semantic_json_file = base_name + '.semantic.json'
        analisador_semantico.exportar_json(semantic_json_file)
        print(f"✅ Arquivo JSON semântico gerado: {semantic_json_file}")
        
        # Resumo final
        total_erros = len(erros_lexicos) + len(erros_sintaticos) + len(erros_semanticos)
        print(f"\n=== RESUMO FINAL ===")
        print(f"Total de erros: {total_erros}")
        print(f"Total de avisos: {len(avisos)}")
        
        if total_erros == 0:
            print("🎉 ANÁLISE COMPLETA BEM-SUCEDIDA!")
        else:
            print("💥 ANÁLISE COMPLETA COM ERROS")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()