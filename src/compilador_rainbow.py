#!/usr/bin/env python3
"""
Compilador Rainbow - Integração Léxica e Sintática
Arquivo principal que combina análise léxica e sintática
"""

import sys
import os
from datetime import datetime
from analisador_lexico import AnalisadorLexico, TokenType
from analisador_sintatico import AnalisadorSintatico


class CompiladorRainbow:
    """Compilador principal da linguagem Rainbow"""
    
    def __init__(self):
        self.analisador_lexico = AnalisadorLexico()
        self.analisador_sintatico = AnalisadorSintatico()
        self.tokens = []
        self.erros_lexicos = []
        self.ast = None
        self.erros_sintaticos = []
    
    def compilar_arquivo(self, caminho_arquivo: str) -> bool:
        """
        Compila um arquivo .rainbow completo
        Retorna True se não houver erros, False caso contrário
        """
        print(f"🌈 Compilando arquivo: {caminho_arquivo}")
        print("=" * 80)
        
        # Ler código fonte
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                codigo_fonte = f.read()
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo '{caminho_arquivo}' não encontrado")
            return False
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
            return False
        
        # Fase 1: Análise Léxica
        print("📋 Fase 1: Análise Léxica")
        print("-" * 40)
        
        self.tokens, self.erros_lexicos = self.analisador_lexico.analisar(codigo_fonte)
        
        if self.erros_lexicos:
            print(f"❌ {len(self.erros_lexicos)} erro(s) léxico(s) encontrado(s):")
            for erro in self.erros_lexicos:
                print(f"   {erro}")
        else:
            print("✅ Análise léxica concluída sem erros")
        
        print(f"📊 Total de tokens gerados: {len(self.tokens) - 1}")  # -1 para excluir EOF
        
        # Fase 2: Análise Sintática
        print("\n🌳 Fase 2: Análise Sintática")
        print("-" * 40)
        
        self.ast, self.erros_sintaticos = self.analisador_sintatico.analisar(self.tokens)
        
        if self.erros_sintaticos:
            print(f"❌ {len(self.erros_sintaticos)} erro(s) sintático(s) encontrado(s):")
            for erro in self.erros_sintaticos:
                print(f"   {erro}")
        else:
            print("✅ Análise sintática concluída sem erros")
        
        # Gerar arquivos de saída
        self._gerar_arquivos_saida(caminho_arquivo)
        
        # Resumo final
        total_erros = len(self.erros_lexicos) + len(self.erros_sintaticos)
        
        print("\n" + "=" * 80)
        print("📋 RESUMO DA COMPILAÇÃO")
        print("=" * 80)
        print(f"Arquivo: {caminho_arquivo}")
        print(f"Tokens gerados: {len(self.tokens) - 1}")
        print(f"Erros léxicos: {len(self.erros_lexicos)}")
        print(f"Erros sintáticos: {len(self.erros_sintaticos)}")
        print(f"Total de erros: {total_erros}")
        
        if total_erros == 0:
            print("🎉 COMPILAÇÃO BEM-SUCEDIDA!")
            return True
        else:
            print("💥 COMPILAÇÃO COM ERROS")
            return False
    
    def _gerar_arquivos_saida(self, caminho_arquivo: str):
        """Gera todos os arquivos de saída da compilação"""
        base_name = os.path.splitext(caminho_arquivo)[0]
        
        print("\n📁 Gerando arquivos de saída...")
        
        # Arquivo .tokens (análise léxica)
        tokens_file = base_name + '.tokens'
        self.analisador_lexico.gerar_relatorio_tokens(self.tokens, tokens_file)
        print(f"   ✅ {tokens_file}")
        
        # Arquivo .errors (erros léxicos)
        errors_file = base_name + '.errors'
        self.analisador_lexico.gerar_relatorio_erros(self.erros_lexicos, errors_file)
        print(f"   ✅ {errors_file}")
        
        # Arquivo .stats (estatísticas léxicas)
        stats_file = base_name + '.stats'
        self.analisador_lexico.gerar_relatorio_estatisticas(self.tokens, self.erros_lexicos, stats_file)
        print(f"   ✅ {stats_file}")
        
        # Arquivo .ast (árvore sintática)
        ast_file = base_name + '.ast'
        self.analisador_sintatico.gerar_relatorio_ast(self.ast, ast_file)
        print(f"   ✅ {ast_file}")
        
        # Arquivo .json (análise completa)
        json_file = base_name + '.analysis.json'
        self._gerar_analise_completa_json(json_file)
        print(f"   ✅ {json_file}")
        
        # Arquivo .syntax.errors (erros sintáticos)
        syntax_errors_file = base_name + '.syntax.errors'
        self._gerar_relatorio_erros_sintaticos(syntax_errors_file)
        print(f"   ✅ {syntax_errors_file}")
    
    def _gerar_analise_completa_json(self, arquivo_saida: str):
        """Gera arquivo JSON com análise completa"""
        import json
        
        resultado = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'versao_compilador': '1.0.0',
                'linguagem': 'Rainbow'
            },
            'analise_lexica': {
                'total_tokens': len(self.tokens) - 1,
                'tokens': [token.to_dict() for token in self.tokens if token.tipo != TokenType.EOF],
                'erros': self.erros_lexicos,
                'estatisticas': {
                    'total_linhas': self.analisador_lexico.stats['total_linhas'],
                    'total_caracteres': self.analisador_lexico.stats['total_caracteres'],
                    'tokens_por_tipo': self.analisador_lexico.stats['tokens_por_tipo'],
                    'palavras_reservadas_usadas': list(self.analisador_lexico.stats['palavras_reservadas_usadas']),
                    'variaveis_declaradas': list(self.analisador_lexico.stats['variaveis_declaradas'])
                }
            },
            'analise_sintatica': {
                'ast': self.ast.to_dict() if self.ast else None,
                'erros': self.erros_sintaticos,
                'sucesso': len(self.erros_sintaticos) == 0
            },
            'resumo': {
                'total_erros_lexicos': len(self.erros_lexicos),
                'total_erros_sintaticos': len(self.erros_sintaticos),
                'compilacao_bem_sucedida': len(self.erros_lexicos) + len(self.erros_sintaticos) == 0
            }
        }
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    def _gerar_relatorio_erros_sintaticos(self, arquivo_saida: str):
        """Gera relatório específico de erros sintáticos"""
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("=== RELATÓRIO DE ERROS SINTÁTICOS ===\n")
            f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if self.erros_sintaticos:
                for erro in self.erros_sintaticos:
                    f.write(f"{erro}\n")
            else:
                f.write("Nenhum erro sintático encontrado!\n")
            
            f.write(f"\n=== RESUMO ===\n")
            f.write(f"Total de erros sintáticos: {len(self.erros_sintaticos)}\n")
    
    def compilar_multiplos_arquivos(self, caminhos_arquivos: list) -> bool:
        """Compila múltiplos arquivos"""
        todos_bem_sucedidos = True
        
        print(f"🌈 Compilando {len(caminhos_arquivos)} arquivo(s)...")
        print("=" * 80)
        
        for i, caminho in enumerate(caminhos_arquivos, 1):
            print(f"\\n[{i}/{len(caminhos_arquivos)}] {caminho}")
            print("-" * 60)
            
            sucesso = self.compilar_arquivo(caminho)
            if not sucesso:
                todos_bem_sucedidos = False
        
        print("\n" + "=" * 80)
        print("📋 RESUMO GERAL")
        print("=" * 80)
        
        if todos_bem_sucedidos:
            print("🎉 TODOS OS ARQUIVOS COMPILADOS COM SUCESSO!")
        else:
            print("💥 ALGUNS ARQUIVOS TIVERAM ERROS")
        
        return todos_bem_sucedidos
    
    def modo_interativo(self):
        """Modo interativo para testar código Rainbow"""
        print("🌈 MODO INTERATIVO DO COMPILADOR RAINBOW")
        print("=" * 80)
        print("Digite código Rainbow linha por linha.")
        print("Digite 'COMPILAR' para processar o código.")
        print("Digite 'LIMPAR' para limpar o código.")
        print("Digite 'SAIR' para encerrar.")
        print("-" * 80)
        
        codigo_linhas = []
        numero_linha = 1
        
        while True:
            try:
                if not codigo_linhas:
                    linha = input(f"{numero_linha:02d}> ")
                else:
                    linha = input(f"{numero_linha:02d}> ")
                
                comando = linha.strip().upper()
                
                if comando == 'SAIR':
                    print("👋 Até logo!")
                    break
                elif comando == 'LIMPAR':
                    codigo_linhas = []
                    numero_linha = 1
                    print("🧹 Código limpo!")
                    continue
                elif comando == 'COMPILAR':
                    if not codigo_linhas:
                        print("❌ Nenhum código para compilar!")
                        continue
                    
                    # Processar código
                    codigo_completo = '\\n'.join(codigo_linhas)
                    print("\\n" + "=" * 60)
                    print("🔍 COMPILANDO CÓDIGO...")
                    print("=" * 60)
                    
                    # Análise léxica
                    tokens, erros_lexicos = self.analisador_lexico.analisar(codigo_completo)
                    
                    print("📋 Análise Léxica:")
                    if erros_lexicos:
                        print(f"   ❌ {len(erros_lexicos)} erro(s):")
                        for erro in erros_lexicos:
                            print(f"      {erro}")
                    else:
                        print("   ✅ Sem erros")
                    
                    # Análise sintática
                    ast, erros_sintaticos = self.analisador_sintatico.analisar(tokens)
                    
                    print("🌳 Análise Sintática:")
                    if erros_sintaticos:
                        print(f"   ❌ {len(erros_sintaticos)} erro(s):")
                        for erro in erros_sintaticos:
                            print(f"      {erro}")
                    else:
                        print("   ✅ Sem erros")
                    
                    total_erros = len(erros_lexicos) + len(erros_sintaticos)
                    print(f"\\n📊 Total de tokens: {len(tokens) - 1}")
                    print(f"📊 Total de erros: {total_erros}")
                    
                    if total_erros == 0:
                        print("🎉 CÓDIGO VÁLIDO!")
                    else:
                        print("💥 CÓDIGO COM ERROS")
                    
                    print("=" * 60)
                    continue
                else:
                    codigo_linhas.append(linha)
                    numero_linha += 1
                    
            except KeyboardInterrupt:
                print("\\n\\n⚠️  Interrompido pelo usuário")
                break
            except EOFError:
                print("\\n\\n👋 Até logo!")
                break


def main():
    """Função principal"""
    compilador = CompiladorRainbow()
    
    if len(sys.argv) == 1:
        # Modo interativo se não foram fornecidos arquivos
        compilador.modo_interativo()
    elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
        # Ajuda
        print("🌈 COMPILADOR RAINBOW")
        print("=" * 50)
        print("Uso:")
        print("  python compilador_rainbow.py                    # Modo interativo")
        print("  python compilador_rainbow.py arquivo.rainbow    # Compilar arquivo")
        print("  python compilador_rainbow.py *.rainbow          # Compilar múltiplos")
        print("  python compilador_rainbow.py --help             # Esta ajuda")
        print()
        print("Arquivos gerados:")
        print("  arquivo.tokens          # Lista de tokens")
        print("  arquivo.errors          # Erros léxicos")
        print("  arquivo.syntax.errors   # Erros sintáticos") 
        print("  arquivo.stats           # Estatísticas")
        print("  arquivo.ast             # Árvore sintática")
        print("  arquivo.analysis.json   # Análise completa")
    else:
        # Compilar arquivo(s) fornecido(s)
        arquivos = sys.argv[1:]
        
        # Verificar se todos os arquivos existem
        arquivos_validos = []
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                arquivos_validos.append(arquivo)
            else:
                print(f"❌ Arquivo não encontrado: {arquivo}")
        
        if not arquivos_validos:
            print("❌ Nenhum arquivo válido encontrado!")
            sys.exit(1)
        
        if len(arquivos_validos) == 1:
            sucesso = compilador.compilar_arquivo(arquivos_validos[0])
        else:
            sucesso = compilador.compilar_multiplos_arquivos(arquivos_validos)
        
        # Código de saída
        sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()