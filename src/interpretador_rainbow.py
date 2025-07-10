#!/usr/bin/env python3
import sys
import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
import re

class InterpretadorRainbow:
    def __init__(self, ide_callback=None):
        self.variaveis = {}
        self.ide_callback = ide_callback  # Para comunicação com a IDE
        self.output = []
        self.input_requests = []
        
    def executar_arquivo(self, arquivo_path):
        """Executa um arquivo Rainbow (.rainbow)"""
        try:
            # Primeiro, compilar para verificar erros
            if not self.compilar_arquivo(arquivo_path):
                return False, "Erro na compilação. Verifique os erros."
                
            # Se passou na compilação, executar
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                codigo = f.read()
                
            return self.executar_codigo(codigo)
            
        except Exception as e:
            return False, f"Erro ao executar arquivo: {str(e)}"
    
    def compilar_arquivo(self, arquivo_path):
        """Verifica se o arquivo compila sem erros críticos"""
        try:
            import subprocess
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            compilador_path = os.path.join(base_dir, "src", "compilador_rainbow.py")
            
            result = subprocess.run([sys.executable, compilador_path, arquivo_path], 
                                  capture_output=True, text=True)
            
            # Verificar se o processo retornou com erro crítico
            if result.returncode != 0:
                return False
                
            # Verificar apenas erros léxicos e sintáticos críticos nos arquivos
            base_name = arquivo_path.rsplit('.', 1)[0]
            critical_error_files = [
                base_name + ".errors",
                base_name + ".syntax.errors"
            ]
            
            for error_file in critical_error_files:
                if os.path.exists(error_file):
                    with open(error_file, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        # Verificar se há erros reais (não apenas texto de cabeçalho)
                        lines = content.split('\n')
                        error_found = False
                        for line in lines:
                            if 'Erro' in line and 'Nenhum erro' not in line:
                                error_found = True
                                break
                        if error_found:
                            return False
                            
            # Se chegou aqui, pode prosseguir com a execução
            return True
            
        except Exception as e:
            print(f"Erro na compilação: {e}")
            return False
    
    def executar_codigo(self, codigo):
        """Executa código Rainbow linha por linha"""
        try:
            self.variaveis = {}
            self.output = []
            
            linhas = codigo.strip().split('\n')
            
            # Verificar se começa com RAINBOW
            if not linhas[0].strip().startswith("RAINBOW"):
                return False, "Programa deve começar com RAINBOW."
            
            # Executar linha por linha
            i = 1  # Pular linha RAINBOW
            while i < len(linhas):
                linha = linhas[i].strip()
                
                # Pular comentários e linhas vazias
                if not linha or linha.startswith('//'):
                    i += 1
                    continue
                    
                try:
                    i = self.executar_linha(linha, linhas, i)
                except Exception as e:
                    return False, f"Erro na linha {i+1}: {str(e)}"
                    
            return True, "\n".join(self.output)
            
        except Exception as e:
            return False, f"Erro na execução: {str(e)}"
    
    def executar_linha(self, linha, linhas, indice_atual):
        """Executa uma linha específica"""
        linha = linha.rstrip('.')
        
        # Atribuição de variável
        if 'recebe' in linha:
            self.executar_atribuicao(linha)
            
        # Comando mostrar
        elif linha.startswith('mostrar('):
            self.executar_mostrar(linha)
            
        # Estrutura se
        elif linha.startswith('se ('):
            return self.executar_se(linha, linhas, indice_atual)
            
        # Estrutura enquanto
        elif linha.startswith('enquanto ('):
            return self.executar_enquanto(linha, linhas, indice_atual)
            
        # Estrutura para
        elif linha.startswith('para '):
            return self.executar_para(linha, linhas, indice_atual)
            
        return indice_atual + 1
    
    def executar_atribuicao(self, linha):
        """Executa atribuição de variável"""
        # Exemplo: #nome recebe "João"
        # Exemplo: #idade recebe ler("Digite idade: ")
        
        match = re.match(r'(#\w+)\s+recebe\s+(.+)', linha)
        if not match:
            raise Exception(f"Sintaxe de atribuição inválida: {linha}")
            
        var_nome = match.group(1)
        expressao = match.group(2)
        
        # print(f"DEBUG ASSIGN: {var_nome} = '{expressao}'")
        valor = self.avaliar_expressao(expressao)
        self.variaveis[var_nome] = valor
    
    def executar_mostrar(self, linha):
        """Executa comando mostrar"""
        # Exemplo: mostrar("Olá " + #nome)
        match = re.match(r'mostrar\((.+)\)', linha)
        if not match:
            raise Exception(f"Sintaxe de mostrar inválida: {linha}")
            
        expressao = match.group(1)
        # Debug
        # print(f"DEBUG: Avaliando expressão: '{expressao}'")
        valor = self.avaliar_expressao(expressao)
        
        # Converter para string se necessário
        if isinstance(valor, bool):
            valor = "Verdadeiro" if valor else "Falso"
        elif valor is None:
            valor = ""
            
        self.output.append(str(valor))
    
    def executar_se(self, linha, linhas, indice):
        """Executa estrutura condicional se"""
        # Exemplo: se (#idade >= 18) {
        match = re.match(r'se \((.+)\) \{', linha)
        if not match:
            raise Exception(f"Sintaxe de se inválida: {linha}")
            
        condicao = match.group(1)
        resultado = self.avaliar_expressao(condicao)
        
        # Encontrar o bloco correspondente
        i = indice + 1
        nivel = 1
        bloco_se = []
        bloco_senao = []
        em_senao = False
        
        while i < len(linhas) and nivel > 0:
            linha_atual = linhas[i].strip()
            
            if '{' in linha_atual:
                nivel += linha_atual.count('{')
            if '}' in linha_atual:
                nivel -= linha_atual.count('}')
                
            if nivel == 1 and linha_atual == '} senao {':
                em_senao = True
                i += 1
                continue
                
            if nivel > 0:
                if em_senao:
                    bloco_senao.append(linha_atual)
                else:
                    bloco_se.append(linha_atual)
                    
            i += 1
        
        # Executar bloco apropriado
        if resultado:
            for linha_bloco in bloco_se:
                if linha_bloco.strip() and not linha_bloco.strip() == '}':
                    self.executar_linha(linha_bloco.strip(), linhas, 0)
        else:
            for linha_bloco in bloco_senao:
                if linha_bloco.strip() and not linha_bloco.strip() == '}':
                    self.executar_linha(linha_bloco.strip(), linhas, 0)
        
        return i
    
    def executar_enquanto(self, linha, linhas, indice):
        """Executa laço enquanto"""
        # Exemplo: enquanto (#i <= 10) {
        match = re.match(r'enquanto \((.+)\) \{', linha)
        if not match:
            raise Exception(f"Sintaxe de enquanto inválida: {linha}")
            
        condicao = match.group(1)
        
        # Encontrar o bloco
        i = indice + 1
        nivel = 1
        bloco = []
        
        while i < len(linhas) and nivel > 0:
            linha_atual = linhas[i].strip()
            
            if '{' in linha_atual:
                nivel += linha_atual.count('{')
            if '}' in linha_atual:
                nivel -= linha_atual.count('}')
                
            if nivel > 0:
                bloco.append(linha_atual)
                
            i += 1
        
        # Executar laço
        max_iteracoes = 1000  # Prevenir loop infinito
        iteracoes = 0
        
        while self.avaliar_expressao(condicao) and iteracoes < max_iteracoes:
            for linha_bloco in bloco:
                if linha_bloco.strip() and not linha_bloco.strip() == '}':
                    self.executar_linha(linha_bloco.strip(), linhas, 0)
            iteracoes += 1
            
        if iteracoes >= max_iteracoes:
            raise Exception("Loop infinito detectado!")
        
        return i
    
    def executar_para(self, linha, linhas, indice):
        """Executa laço para"""
        # Exemplo: para #i de 1 ate 10 passo 1 {
        match = re.match(r'para (#\w+) de (.+) ate (.+) passo (.+) \{', linha)
        if not match:
            raise Exception(f"Sintaxe de para inválida: {linha}")
            
        var_nome = match.group(1)
        inicio = self.avaliar_expressao(match.group(2))
        fim = self.avaliar_expressao(match.group(3))
        passo = self.avaliar_expressao(match.group(4))
        
        # Encontrar o bloco
        i = indice + 1
        nivel = 1
        bloco = []
        
        while i < len(linhas) and nivel > 0:
            linha_atual = linhas[i].strip()
            
            if '{' in linha_atual:
                nivel += linha_atual.count('{')
            if '}' in linha_atual:
                nivel -= linha_atual.count('}')
                
            if nivel > 0:
                bloco.append(linha_atual)
                
            i += 1
        
        # Executar laço
        valor_atual = inicio
        while (passo > 0 and valor_atual <= fim) or (passo < 0 and valor_atual >= fim):
            self.variaveis[var_nome] = valor_atual
            
            for linha_bloco in bloco:
                if linha_bloco.strip() and not linha_bloco.strip() == '}':
                    self.executar_linha(linha_bloco.strip(), linhas, 0)
                    
            valor_atual += passo
        
        return i
    
    def avaliar_expressao(self, expressao):
        """Avalia uma expressão"""
        expressao = expressao.strip()
        
        # Remover parênteses externos se existirem
        if expressao.startswith('(') and expressao.endswith(')'):
            # Verificar se os parênteses são balanceados
            nivel = 0
            for i, char in enumerate(expressao):
                if char == '(':
                    nivel += 1
                elif char == ')':
                    nivel -= 1
                    if nivel == 0 and i < len(expressao) - 1:
                        # Parênteses não são externos, quebrar
                        break
            else:
                # Parênteses são externos, remover
                if nivel == 0:
                    expressao = expressao[1:-1].strip()
        
        # String literal (verificar se não tem operadores)
        if expressao.startswith('"') and expressao.endswith('"'):
            # Verificar se há operadores fora das aspas
            if not self._tem_operador_fora_aspas(expressao):
                return expressao[1:-1]
            
        # Número
        try:
            if '.' in expressao:
                return float(expressao)
            return int(expressao)
        except ValueError:
            pass
            
        # Booleano
        if expressao == "Verdadeiro":
            return True
        if expressao == "Falso":
            return False
            
        # Variável (apenas se não contém operadores)
        if expressao.startswith('#') and not self._tem_operador_fora_aspas(expressao):
            if expressao in self.variaveis:
                return self.variaveis[expressao]
            else:
                raise Exception(f"Variável {expressao} não definida")
                
        # Função ler
        if expressao.startswith('ler('):
            match = re.match(r'ler\("(.+)"\)', expressao)
            if match:
                prompt = match.group(1)
                return self.solicitar_entrada(prompt)
                
        # Operações matemáticas e lógicas
        return self.avaliar_operacao(expressao)
    
    def avaliar_operacao(self, expressao):
        """Avalia operações matemáticas e lógicas"""
        # Operações relacionais
        for op in ['>=', '<=', '>', '<', '==', '!=']:
            if op in expressao:
                partes = expressao.split(op, 1)
                esq = self.avaliar_expressao(partes[0].strip())
                dir = self.avaliar_expressao(partes[1].strip())
                
                # Converter para números se possível para comparação
                try:
                    esq_num = float(esq) if isinstance(esq, str) and esq.replace('.', '').replace('-', '').isdigit() else esq
                    dir_num = float(dir) if isinstance(dir, str) and dir.replace('.', '').replace('-', '').isdigit() else dir
                    esq, dir = esq_num, dir_num
                except:
                    pass
                
                if op == '>=': return esq >= dir
                elif op == '<=': return esq <= dir
                elif op == '>': return esq > dir
                elif op == '<': return esq < dir
                elif op == '==': return esq == dir
                elif op == '!=': return esq != dir
                
        # Operações matemáticas
        for op in ['+', '-', '*', '/', '%']:
            if op in expressao:
                partes = self.dividir_expressao(expressao, op)
                if len(partes) >= 2:
                    # Avaliar primeira parte
                    resultado = self.avaliar_expressao(partes[0].strip())
                    
                    # Avaliar e combinar com as partes restantes
                    for i in range(1, len(partes)):
                        dir = self.avaliar_expressao(partes[i].strip())
                        
                        # Para soma, verificar se é concatenação de string
                        if op == '+':
                            # Se algum operando é string ou contém string, fazer concatenação
                            if isinstance(resultado, str) or isinstance(dir, str):
                                resultado = str(resultado) + str(dir)
                            else:
                                resultado = resultado + dir
                        else:
                            # Para outras operações, converter para números
                            try:
                                if isinstance(resultado, str):
                                    resultado = float(resultado) if '.' in resultado else int(resultado)
                                if isinstance(dir, str):
                                    dir = float(dir) if '.' in dir else int(dir)
                            except ValueError:
                                raise Exception(f"Não é possível converter para número: {resultado} ou {dir}")
                            
                            if op == '-': resultado = resultado - dir
                            elif op == '*': resultado = resultado * dir
                            elif op == '/': resultado = resultado / dir if dir != 0 else 0
                            elif op == '%': resultado = resultado % dir if dir != 0 else 0
                    
                    return resultado
                    
        # Operações lógicas
        if ' E ' in expressao:
            partes = expressao.split(' E ', 1)
            return self.avaliar_expressao(partes[0].strip()) and self.avaliar_expressao(partes[1].strip())
            
        if ' OU ' in expressao:
            partes = expressao.split(' OU ', 1)
            return self.avaliar_expressao(partes[0].strip()) or self.avaliar_expressao(partes[1].strip())
            
        if expressao.startswith('NAO '):
            return not self.avaliar_expressao(expressao[4:].strip())
            
        raise Exception(f"Expressão não reconhecida: {expressao}")
    
    def _tem_operador_fora_aspas(self, expressao):
        """Verifica se há operadores fora das aspas"""
        em_string = False
        for i, char in enumerate(expressao):
            if char == '"':
                em_string = not em_string
            elif not em_string and char in ['+', '-', '*', '/', '%']:
                return True
        return False
    
    def dividir_expressao(self, expressao, operador):
        """Divide expressão respeitando strings entre aspas"""
        partes = []
        atual = ""
        em_string = False
        
        i = 0
        while i < len(expressao):
            if expressao[i] == '"':
                em_string = not em_string
                atual += expressao[i]
            elif not em_string and expressao[i:i+len(operador)] == operador:
                partes.append(atual)
                atual = ""
                i += len(operador) - 1
            else:
                atual += expressao[i]
            i += 1
            
        partes.append(atual)
        return partes
    
    def solicitar_entrada(self, prompt):
        """Solicita entrada do usuário"""
        if self.ide_callback:
            return self.ide_callback(prompt)
        else:
            # Para uso em linha de comando, usar valor padrão se não houver entrada
            try:
                return input(prompt + " ")
            except EOFError:
                # Se não há entrada disponível, retornar string vazia
                return ""

def main():
    if len(sys.argv) != 2:
        print("Uso: python interpretador_rainbow.py <arquivo.rainbow>")
        sys.exit(1)
        
    interpretador = InterpretadorRainbow()
    sucesso, resultado = interpretador.executar_arquivo(sys.argv[1])
    
    if sucesso:
        print("=== EXECUÇÃO ===")
        print(resultado)
    else:
        print("=== ERRO ===")
        print(resultado)

if __name__ == "__main__":
    main()