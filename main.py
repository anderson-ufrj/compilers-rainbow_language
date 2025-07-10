#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkfont
import subprocess
import sys
import os
import json
import threading
import time
from pathlib import Path

class RainbowAnimation:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']
        self.bars = []
        self.animation_done = False
        
    def create_rainbow(self):
        bar_height = self.height / len(self.colors)
        for i, color in enumerate(self.colors):
            y1 = i * bar_height
            y2 = (i + 1) * bar_height
            bar = self.canvas.create_rectangle(0, y1, 0, y2, fill=color, outline=color)
            self.bars.append(bar)
    
    def animate(self, callback=None):
        self.create_rainbow()
        self.expand_bars(0, callback)
    
    def expand_bars(self, step, callback):
        if step <= 100:
            width = (self.width / 100) * step
            for bar in self.bars:
                self.canvas.coords(bar, 0, self.canvas.coords(bar)[1], width, self.canvas.coords(bar)[3])
            self.canvas.after(20, lambda: self.expand_bars(step + 1, callback))
        else:
            self.fade_out(20, callback)
    
    def fade_out(self, alpha, callback):
        if alpha >= 0:
            self.canvas.configure(bg=f'#{alpha:X}{alpha:X}{alpha:X}')
            for bar in self.bars:
                color = self.canvas.itemcget(bar, 'fill')
                if len(color) == 7:
                    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                    r = int(r * (alpha / 20))
                    g = int(g * (alpha / 20))
                    b = int(b * (alpha / 20))
                    new_color = f'#{r:02X}{g:02X}{b:02X}'
                    self.canvas.itemconfig(bar, fill=new_color, outline=new_color)
            self.canvas.after(50, lambda: self.fade_out(alpha - 1, callback))
        else:
            self.animation_done = True
            if callback:
                callback()

class RainbowIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Rainbow IDE 🌈")
        self.root.geometry("1200x800")
        
        # Definir temas
        self.themes = {
            'dark': {
                'bg_color': "#1e1e1e",
                'text_bg': "#2d2d2d",
                'text_fg': "#ffffff",
                'highlight_bg': "#3d3d3d",
                'button_bg': "#4a4a4a",
                'toolbar_bg': "#2b2b2b",
                'menu_bg': "#2b2b2b",
                'border_color': "#555555",
                'line_number_bg': "#252525",
                'line_number_fg': "#858585",
                'success_color': "#4CAF50",
                'error_color': "#f44336",
                'selection_bg': "#264f78",
                'cursor_color': "#ffffff"
            },
            'light': {
                'bg_color': "#f5f5f5",
                'text_bg': "#ffffff",
                'text_fg': "#000000",
                'highlight_bg': "#e0e0e0",
                'button_bg': "#ffffff",
                'toolbar_bg': "#f8f8f8",
                'menu_bg': "#ffffff",
                'border_color': "#cccccc",
                'line_number_bg': "#f5f5f5",
                'line_number_fg': "#999999",
                'success_color': "#4CAF50",
                'error_color': "#f44336",
                'selection_bg': "#0066cc",
                'cursor_color': "#000000"
            }
        }
        
        # Tema inicial (detectar preferência do sistema se possível)
        self.current_theme = 'dark'
        self.apply_theme(self.current_theme)
        
        self.rainbow_colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']
        
        # Variáveis
        self.current_file = None
        self.modified = False
        
        # Configurar estilo macOS/Linux
        self.setup_native_style()
        
        # Mostrar animação de abertura
        self.show_splash_screen()
        
    def apply_theme(self, theme_name):
        theme = self.themes[theme_name]
        self.bg_color = theme['bg_color']
        self.text_bg = theme['text_bg']
        self.text_fg = theme['text_fg']
        self.highlight_bg = theme['highlight_bg']
        self.button_bg = theme['button_bg']
        self.toolbar_bg = theme['toolbar_bg']
        self.menu_bg = theme['menu_bg']
        self.border_color = theme['border_color']
        self.line_number_bg = theme['line_number_bg']
        self.line_number_fg = theme['line_number_fg']
        self.success_color = theme['success_color']
        self.error_color = theme['error_color']
        self.selection_bg = theme['selection_bg']
        self.cursor_color = theme['cursor_color']
        
        self.root.configure(bg=self.bg_color)
        
    def setup_native_style(self):
        # Detectar sistema operacional
        import platform
        system = platform.system()
        
        if system == "Darwin":  # macOS
            # Configurações específicas do macOS
            self.root.tk.call('tk::unsupported::MacWindowStyle', 'style', self.root._w, 'moveableModal', '')
            # Adicionar padding para o traffic light buttons do macOS
            self.macos_padding = 28
        else:
            self.macos_padding = 0
        
    def show_splash_screen(self):
        # Tela de splash com animação
        self.splash = tk.Toplevel(self.root)
        self.splash.overrideredirect(True)
        self.splash.configure(bg='black')
        
        # Centralizar splash
        width, height = 600, 400
        x = (self.splash.winfo_screenwidth() - width) // 2
        y = (self.splash.winfo_screenheight() - height) // 2
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        
        # Canvas para animação
        canvas = tk.Canvas(self.splash, width=width, height=300, bg='black', highlightthickness=0)
        canvas.pack()
        
        # Título
        title_label = tk.Label(self.splash, text="Rainbow IDE", font=("Arial", 36, "bold"),
                              bg='black', fg='white')
        title_label.pack(pady=20)
        
        # Animação
        animation = RainbowAnimation(canvas, width, 300)
        animation.animate(callback=self.close_splash)
        
    def close_splash(self):
        self.splash.destroy()
        self.setup_ui()
        
    def setup_ui(self):
        # Configurar estilo
        self.setup_styles()
        
        # Menu
        self.create_menu()
        
        # Toolbar
        self.create_toolbar()
        
        # Painel principal
        self.create_main_panel()
        
        # Status bar
        self.create_status_bar()
        
        # Atalhos de teclado
        self.setup_keybindings()
        
        # Configurar syntax highlighting
        self.setup_syntax_highlighting()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores do tema escuro
        style.configure("Toolbar.TFrame", background=self.button_bg)
        style.configure("Dark.TButton", background=self.button_bg, foreground=self.text_fg)
        style.map("Dark.TButton",
                  background=[('active', self.highlight_bg)],
                  foreground=[('active', self.text_fg)])
        
        style.configure("Dark.TNotebook", background=self.bg_color)
        style.configure("Dark.TNotebook.Tab", background=self.button_bg, foreground=self.text_fg)
        style.map("Dark.TNotebook.Tab",
                  background=[('selected', self.highlight_bg)],
                  foreground=[('selected', self.text_fg)])
        
    def create_menu(self):
        menubar = tk.Menu(self.root, bg=self.button_bg, fg=self.text_fg)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.button_bg, fg=self.text_fg)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Novo", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Abrir", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Salvar", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Salvar Como...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.quit_app, accelerator="Ctrl+Q")
        
        # Menu Executar
        run_menu = tk.Menu(menubar, tearoff=0, bg=self.button_bg, fg=self.text_fg)
        menubar.add_cascade(label="Executar", menu=run_menu)
        run_menu.add_command(label="▶️ Executar Programa", command=self.run_program, accelerator="Ctrl+R")
        run_menu.add_separator()
        run_menu.add_command(label="Análise Léxica", command=self.run_lexical, accelerator="F5")
        run_menu.add_command(label="Análise Sintática", command=self.run_syntactic, accelerator="F6")
        run_menu.add_command(label="Análise Semântica", command=self.run_semantic, accelerator="F7")
        run_menu.add_command(label="Compilação Completa", command=self.run_full, accelerator="F8")
        
        # Menu Exemplos
        examples_menu = tk.Menu(menubar, tearoff=0, bg=self.button_bg, fg=self.text_fg)
        menubar.add_cascade(label="Exemplos", menu=examples_menu)
        examples_menu.add_command(label="👋 Olá Mundo", command=lambda: self.open_example("ola_mundo.rainbow"))
        examples_menu.add_command(label="🧮 Calculadora", command=lambda: self.open_example("calculadora.rainbow"))
        examples_menu.add_command(label="📊 Tabuada", command=lambda: self.open_example("tabuada.rainbow"))
        examples_menu.add_command(label="🔀 Condicional", command=lambda: self.open_example("condicional.rainbow"))
        examples_menu.add_command(label="🔄 Laço Para", command=lambda: self.open_example("laco_para.rainbow"))
        examples_menu.add_command(label="🏷️ Tipos de Dados", command=lambda: self.open_example("tipos_dados.rainbow"))
        examples_menu.add_separator()
        examples_menu.add_command(label="💬 Entrada do Usuário", command=lambda: self.open_example("entrada_usuario.rainbow"))
        examples_menu.add_command(label="🤖 Programa Interativo", command=lambda: self.open_example("programa_interativo.rainbow"))
        
        # Menu Visualizar
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.button_bg, fg=self.text_fg)
        menubar.add_cascade(label="Visualizar", menu=view_menu)
        
        # Submenu de temas
        theme_menu = tk.Menu(view_menu, tearoff=0, bg=self.button_bg, fg=self.text_fg)
        view_menu.add_cascade(label="Tema", menu=theme_menu)
        theme_menu.add_radiobutton(label="🌙 Escuro", value="dark", 
                                  variable=tk.StringVar(value=self.current_theme),
                                  command=lambda: self.switch_theme('dark'))
        theme_menu.add_radiobutton(label="☀️ Claro", value="light",
                                  variable=tk.StringVar(value=self.current_theme),
                                  command=lambda: self.switch_theme('light'))
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.button_bg, fg=self.text_fg)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        
        # Submenu Tutoriais
        tutorials_menu = tk.Menu(help_menu, tearoff=0, bg=self.button_bg, fg=self.text_fg)
        help_menu.add_cascade(label="📚 Tutoriais", menu=tutorials_menu)
        tutorials_menu.add_command(label="📖 Guia do Usuário", command=lambda: self.show_documentation("guia-usuario-ide.md"))
        tutorials_menu.add_command(label="🏗️ Arquitetura do Sistema", command=lambda: self.show_documentation("arquitetura-sistema.md"))
        tutorials_menu.add_command(label="⚡ Interpretador Rainbow", command=lambda: self.show_documentation("interpretador-rainbow.md"))
        tutorials_menu.add_command(label="📦 Instalação e Configuração", command=lambda: self.show_documentation("instalacao-configuracao.md"))
        tutorials_menu.add_command(label="🌈 Linguagem Rainbow", command=lambda: self.show_documentation("linguagem-rainbow.md"))
        tutorials_menu.add_command(label="📝 Exemplos Rainbow", command=lambda: self.show_documentation("exemplos-rainbow.md"))
        tutorials_menu.add_command(label="📐 Gramática Rainbow", command=lambda: self.show_documentation("gramatica-rainbow.md"))
        
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ Sobre", command=self.show_about)
        
    def switch_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme(theme_name)
        self.update_theme_colors()
        
    def update_theme_colors(self):
        # Atualizar cores de todos os widgets existentes
        if hasattr(self, 'text_editor'):
            self.text_editor.config(bg=self.text_bg, fg=self.text_fg, 
                                  insertbackground=self.cursor_color,
                                  selectbackground=self.selection_bg)
        if hasattr(self, 'line_numbers'):
            self.line_numbers.config(bg=self.line_number_bg, fg=self.line_number_fg)
        if hasattr(self, 'toolbar_frame'):
            self.toolbar_frame.config(bg=self.toolbar_bg)
            # Atualizar botões da toolbar
            for btn in self.toolbar_buttons:
                btn.config(bg=self.toolbar_bg, fg=self.text_fg,
                          activebackground=self.highlight_bg)
        if hasattr(self, 'status_bar'):
            self.status_bar.config(bg=self.toolbar_bg, fg=self.text_fg)
            self.position_label.config(bg=self.toolbar_bg, fg=self.text_fg)
            theme_indicator = "🌙" if self.current_theme == "dark" else "☀️"
            self.theme_label.config(text=theme_indicator, bg=self.toolbar_bg, fg=self.text_fg)
            
        # Atualizar cores das abas de saída
        if hasattr(self, 'tokens_text'):
            for widget in [self.tokens_text, self.ast_text, self.symbols_text, 
                          self.errors_text, self.console_text]:
                widget.config(bg=self.text_bg, fg=self.text_fg)
                
            # Atualizar frames das abas
            for frame in [self.tokens_frame, self.ast_frame, self.symbols_frame,
                         self.errors_frame, self.console_frame]:
                frame.config(bg=self.bg_color)
                
        # Atualizar frames principais
        if hasattr(self, 'text_frame'):
            text_frame = self.text_editor.master
            text_frame.config(bg=self.bg_color)
            left_frame = text_frame.master
            left_frame.config(bg=self.bg_color)
                
        # Re-aplicar syntax highlighting
        if hasattr(self, 'setup_syntax_highlighting'):
            self.setup_syntax_highlighting()
            self.apply_syntax_highlighting()
            
    def create_toolbar(self):
        # Frame da toolbar com estilo moderno
        self.toolbar_frame = tk.Frame(self.root, bg=self.toolbar_bg, height=40)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X, pady=(self.macos_padding, 0))
        self.toolbar_frame.pack_propagate(False)
        
        # Container interno para centralizar botões
        button_container = tk.Frame(self.toolbar_frame, bg=self.toolbar_bg)
        button_container.pack(expand=True)
        
        # Botões modernos com hover effect
        self.toolbar_buttons = []
        buttons = [
            ("📄", self.new_file, "Novo arquivo"),
            ("📂", self.open_file, "Abrir arquivo"),
            ("💾", self.save_file, "Salvar"),
            ("|", None, None),  # Separador
            ("▶️", self.run_program, "Executar Programa"),
            ("🔧", self.run_full, "Compilar"),
            ("🔤", self.run_lexical, "Análise Léxica"),
            ("🌳", self.run_syntactic, "Análise Sintática"),
            ("✅", self.run_semantic, "Análise Semântica"),
        ]
        
        for icon, command, tooltip in buttons:
            if icon == "|":
                sep = tk.Frame(button_container, width=1, bg=self.border_color)
                sep.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
            else:
                btn = tk.Button(button_container, text=icon, command=command,
                               bg=self.toolbar_bg, fg=self.text_fg,
                               bd=0, padx=10, pady=5, font=("Arial", 14),
                               activebackground=self.highlight_bg,
                               highlightthickness=0)
                btn.pack(side=tk.LEFT, padx=2)
                
                # Adicionar hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.highlight_bg))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.toolbar_bg))
                
                if tooltip:
                    self.create_tooltip(btn, tooltip)
                    
                self.toolbar_buttons.append(btn)
                    
    def create_tooltip(self, widget, text):
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", 
                           relief=tk.SOLID, borderwidth=1, font=("Arial", 10))
            label.pack()
            widget.tooltip = tooltip
            
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
                
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
    def create_main_panel(self):
        # Painel principal com divisão
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Painel esquerdo - Editor
        left_frame = tk.Frame(main_paned, bg=self.bg_color)
        main_paned.add(left_frame, weight=2)
        
        # Números de linha e editor de texto
        text_frame = tk.Frame(left_frame, bg=self.bg_color)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Números de linha
        self.line_numbers = tk.Text(text_frame, width=4, padx=3, takefocus=0,
                                   border=0, state='disabled',
                                   background=self.line_number_bg, foreground=self.line_number_fg,
                                   font=("Consolas", 12))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Separador entre números e editor
        separator = tk.Frame(text_frame, width=1, bg=self.border_color)
        separator.pack(side=tk.LEFT, fill=tk.Y)
        
        # Editor de texto
        self.text_editor = tk.Text(text_frame, wrap=tk.NONE, undo=True,
                                  background=self.text_bg, foreground=self.text_fg,
                                  insertbackground=self.cursor_color,
                                  selectbackground=self.selection_bg,
                                  font=("Consolas", 12),
                                  bd=0, highlightthickness=0)
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.sync_scroll)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=self.text_editor.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.text_editor.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.line_numbers.config(yscrollcommand=scrollbar_y.set)
        
        # Vincular eventos
        self.text_editor.bind("<<Modified>>", self.on_text_modified)
        self.text_editor.bind("<KeyRelease>", self.on_key_release)
        self.text_editor.bind("<Button-1>", self.on_click)
        self.text_editor.bind("<ButtonRelease-1>", self.update_cursor_position)
        
        # Painel direito - Resultados
        right_frame = tk.Frame(main_paned, bg=self.bg_color)
        main_paned.add(right_frame, weight=1)
        
        # Notebook para diferentes saídas
        self.notebook = ttk.Notebook(right_frame, style="Dark.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Abas
        self.create_output_tabs()
        
    def create_output_tabs(self):
        # Aba Tokens
        self.tokens_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.tokens_frame, text="Tokens")
        
        self.tokens_text = tk.Text(self.tokens_frame, wrap=tk.WORD,
                                  background=self.text_bg, foreground=self.text_fg,
                                  font=("Consolas", 10), bd=0, highlightthickness=0)
        self.tokens_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Aba AST
        self.ast_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.ast_frame, text="AST")
        
        self.ast_text = tk.Text(self.ast_frame, wrap=tk.WORD,
                               background=self.text_bg, foreground=self.text_fg,
                               font=("Consolas", 10), bd=0, highlightthickness=0)
        self.ast_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Aba Símbolos
        self.symbols_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.symbols_frame, text="Símbolos")
        
        self.symbols_text = tk.Text(self.symbols_frame, wrap=tk.WORD,
                                   background=self.text_bg, foreground=self.text_fg,
                                   font=("Consolas", 10), bd=0, highlightthickness=0)
        self.symbols_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Aba Erros
        self.errors_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.errors_frame, text="Erros")
        
        self.errors_text = tk.Text(self.errors_frame, wrap=tk.WORD,
                                  background=self.text_bg, foreground=self.text_fg,
                                  font=("Consolas", 10), bd=0, highlightthickness=0)
        self.errors_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Aba Console
        self.console_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.console_frame, text="Console")
        
        self.console_text = tk.Text(self.console_frame, wrap=tk.WORD,
                                   background=self.text_bg, foreground=self.text_fg,
                                   font=("Consolas", 10), bd=0, highlightthickness=0)
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
    def create_status_bar(self):
        # Frame do status bar
        status_frame = tk.Frame(self.root, bg=self.toolbar_bg, height=25)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        # Linha separadora
        separator = tk.Frame(self.root, height=1, bg=self.border_color)
        separator.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status text
        self.status_bar = tk.Label(status_frame, text="Pronto", 
                                  bg=self.toolbar_bg, fg=self.text_fg,
                                  anchor=tk.W, padx=10)
        self.status_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Informações adicionais (linha:coluna)
        self.position_label = tk.Label(status_frame, text="Ln 1, Col 1",
                                      bg=self.toolbar_bg, fg=self.text_fg,
                                      padx=10)
        self.position_label.pack(side=tk.RIGHT)
        
        # Indicador de tema
        theme_indicator = "🌙" if self.current_theme == "dark" else "☀️"
        self.theme_label = tk.Label(status_frame, text=theme_indicator,
                                   bg=self.toolbar_bg, fg=self.text_fg,
                                   padx=10)
        self.theme_label.pack(side=tk.RIGHT)
        
    def setup_keybindings(self):
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-q>', lambda e: self.quit_app())
        self.root.bind('<Control-r>', lambda e: self.run_program())
        self.root.bind('<F5>', lambda e: self.run_lexical())
        self.root.bind('<F6>', lambda e: self.run_syntactic())
        self.root.bind('<F7>', lambda e: self.run_semantic())
        self.root.bind('<F8>', lambda e: self.run_full())
        
    def setup_syntax_highlighting(self):
        # Tags para syntax highlighting baseadas no tema
        if self.current_theme == 'dark':
            self.text_editor.tag_configure("keyword", foreground="#569cd6")
            self.text_editor.tag_configure("string", foreground="#ce9178")
            self.text_editor.tag_configure("comment", foreground="#6a9955")
            self.text_editor.tag_configure("number", foreground="#b5cea8")
            self.text_editor.tag_configure("variable", foreground="#9cdcfe")
            self.text_editor.tag_configure("operator", foreground="#d4d4d4")
        else:  # light theme
            self.text_editor.tag_configure("keyword", foreground="#0000ff")
            self.text_editor.tag_configure("string", foreground="#a31515")
            self.text_editor.tag_configure("comment", foreground="#008000")
            self.text_editor.tag_configure("number", foreground="#098658")
            self.text_editor.tag_configure("variable", foreground="#001080")
            self.text_editor.tag_configure("operator", foreground="#000000")
            
        self.text_editor.tag_configure("error", background=self.error_color, foreground="#ffffff")
        
        # Palavras-chave da linguagem Rainbow
        self.keywords = ["RAINBOW", "NUMERO", "TEXTO", "LOGICO", "LISTA", "GLOBAL", "se", "senao", 
                        "senaose", "para", "enquanto", "mostrar", "ler", "recebe", "e", "ou", "nao"]
        
        # Keywords já são coloridas pelo on_key_release
        
    def sync_scroll(self, *args):
        self.line_numbers.yview(*args)
        self.text_editor.yview(*args)
        
    def on_text_modified(self, event=None):
        self.modified = True
        self.update_title()
        self.text_editor.edit_modified(False)
        
    def on_key_release(self, event=None):
        self.update_line_numbers()
        self.apply_syntax_highlighting()
        self.update_cursor_position()
        
    def on_click(self, event=None):
        self.update_line_numbers()
        
    def update_cursor_position(self, event=None):
        position = self.text_editor.index(tk.INSERT)
        line, col = position.split('.')
        self.position_label.config(text=f"Ln {line}, Col {int(col) + 1}")
        
    def update_line_numbers(self, event=None):
        lines = self.text_editor.get("1.0", "end-1c").split("\n")
        line_numbers_text = "\n".join(str(i+1) for i in range(len(lines)))
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state='disabled')
        
    def apply_syntax_highlighting(self, event=None):
        # Remover tags existentes
        for tag in ["keyword", "string", "comment", "number", "variable", "operator"]:
            self.text_editor.tag_remove(tag, "1.0", "end")
            
        content = self.text_editor.get("1.0", "end-1c")
        
        # Comentários
        for i, line in enumerate(content.split("\n")):
            if "//" in line:
                start_index = line.index("//")
                self.text_editor.tag_add("comment", f"{i+1}.{start_index}", f"{i+1}.end")
                
        # Strings
        import re
        for match in re.finditer(r'"[^"]*"', content):
            start = self.text_editor.index(f"1.0+{match.start()}c")
            end = self.text_editor.index(f"1.0+{match.end()}c")
            self.text_editor.tag_add("string", start, end)
            
        # Números
        for match in re.finditer(r'\b\d+(\.\d+)?\b', content):
            start = self.text_editor.index(f"1.0+{match.start()}c")
            end = self.text_editor.index(f"1.0+{match.end()}c")
            self.text_editor.tag_add("number", start, end)
            
        # Variáveis
        for match in re.finditer(r'#\w+', content):
            start = self.text_editor.index(f"1.0+{match.start()}c")
            end = self.text_editor.index(f"1.0+{match.end()}c")
            self.text_editor.tag_add("variable", start, end)
            
        # Palavras-chave
        for keyword in self.keywords:
            start = "1.0"
            while True:
                pos = self.text_editor.search(rf"\b{keyword}\b", start, "end", regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(keyword)}c"
                self.text_editor.tag_add("keyword", pos, end)
                start = end
                
    def update_title(self):
        title = "Rainbow IDE 🌈"
        if self.current_file:
            title += f" - {os.path.basename(self.current_file)}"
        if self.modified:
            title += " *"
        self.root.title(title)
        
    def new_file(self):
        if self.modified:
            if not messagebox.askyesno("Novo Arquivo", "Descartar alterações não salvas?"):
                return
        self.text_editor.delete("1.0", "end")
        self.current_file = None
        self.modified = False
        self.update_title()
        self.update_line_numbers()
        self.clear_outputs()
        
    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Abrir arquivo",
            filetypes=[("Rainbow files", "*.rainbow"), ("All files", "*.*")]
        )
        if filename:
            self.load_file(filename)
            
    def open_example(self, example_name):
        examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exemplos")
        filename = os.path.join(examples_dir, example_name)
        
        if os.path.exists(filename):
            self.load_file(filename)
        else:
            messagebox.showerror("Erro", f"Exemplo '{example_name}' não encontrado!")
            
    def load_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            self.text_editor.delete("1.0", "end")
            self.text_editor.insert("1.0", content)
            self.current_file = filename
            self.modified = False
            self.update_title()
            self.update_line_numbers()
            self.apply_syntax_highlighting()
            self.clear_outputs()
            self.status_bar.config(text=f"Arquivo carregado: {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{str(e)}")
            
    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_file_as()
            
    def save_file_as(self):
        filename = filedialog.asksaveasfilename(
            title="Salvar arquivo",
            defaultextension=".rainbow",
            filetypes=[("Rainbow files", "*.rainbow"), ("All files", "*.*")]
        )
        if filename:
            self.save_to_file(filename)
            
    def save_to_file(self, filename):
        content = self.text_editor.get("1.0", "end-1c")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        self.current_file = filename
        self.modified = False
        self.update_title()
        self.status_bar.config(text=f"Arquivo salvo: {filename}")
        
    def quit_app(self):
        if self.modified:
            if not messagebox.askyesno("Sair", "Descartar alterações não salvas?"):
                return
        self.root.quit()
        
    def clear_outputs(self):
        for text_widget in [self.tokens_text, self.ast_text, self.symbols_text, 
                           self.errors_text, self.console_text]:
            text_widget.delete("1.0", "end")
            
    def run_analysis(self, analyzer_script, analysis_type):
        if not self.current_file:
            messagebox.showwarning("Aviso", "Salve o arquivo antes de executar a análise!")
            return
            
        if self.modified:
            self.save_file()
            
        # Limpar saídas anteriores
        self.clear_outputs()
        
        # Mostrar aba do console
        self.notebook.select(self.console_frame)
        
        # Executar análise em thread separada
        thread = threading.Thread(target=self._run_analysis_thread, 
                                 args=(analyzer_script, analysis_type))
        thread.daemon = True
        thread.start()
        
    def _run_analysis_thread(self, analyzer_script, analysis_type):
        try:
            # Atualizar status
            self.status_bar.config(text=f"Executando {analysis_type}...")
            
            # Executar o analisador
            cmd = [sys.executable, analyzer_script, self.current_file]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
            
            stdout, stderr = process.communicate()
            
            # Mostrar saída no console
            self.console_text.insert("end", f"=== {analysis_type} ===\n")
            if stdout:
                self.console_text.insert("end", stdout + "\n")
            if stderr:
                self.console_text.insert("end", stderr + "\n", "error")
                
            # Carregar arquivos de saída
            self.load_output_files()
            
            # Atualizar status
            if process.returncode == 0:
                self.status_bar.config(text=f"{analysis_type} concluída com sucesso!")
                self.highlight_errors()
            else:
                self.status_bar.config(text=f"{analysis_type} concluída com erros.")
                
        except Exception as e:
            self.console_text.insert("end", f"Erro ao executar análise: {str(e)}\n", "error")
            self.status_bar.config(text="Erro na execução")
            
    def load_output_files(self):
        if not self.current_file:
            return
            
        base_path = self.current_file.rsplit('.', 1)[0]
        
        # Carregar tokens
        tokens_file = base_path + ".tokens"
        if os.path.exists(tokens_file):
            with open(tokens_file, 'r', encoding='utf-8') as f:
                self.tokens_text.insert("1.0", f.read())
                
        # Carregar AST
        ast_file = base_path + ".ast"
        if os.path.exists(ast_file):
            with open(ast_file, 'r', encoding='utf-8') as f:
                self.ast_text.insert("1.0", f.read())
                
        # Carregar símbolos
        symbols_file = base_path + ".simbolos"
        if os.path.exists(symbols_file):
            with open(symbols_file, 'r', encoding='utf-8') as f:
                self.symbols_text.insert("1.0", f.read())
                
        # Carregar erros
        error_files = [
            base_path + ".errors",
            base_path + ".syntax.errors",
            base_path + ".semantic.errors"
        ]
        
        all_errors = []
        for error_file in error_files:
            if os.path.exists(error_file):
                with open(error_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content and content != "Nenhum erro encontrado.":
                        all_errors.append(content)
                        
        if all_errors:
            self.errors_text.insert("1.0", "\n\n".join(all_errors))
            self.notebook.select(self.errors_frame)
        else:
            self.errors_text.insert("1.0", "Nenhum erro encontrado! ✅")
            
    def highlight_errors(self):
        # Remover highlights anteriores
        self.text_editor.tag_remove("error", "1.0", "end")
        
        # Buscar erros no texto de erros
        errors_content = self.errors_text.get("1.0", "end-1c")
        
        # Procurar por padrões de linha:coluna
        import re
        for match in re.finditer(r'Linha (\d+), Coluna (\d+)', errors_content):
            line = int(match.group(1))
            col = int(match.group(2))
            
            # Destacar posição do erro
            start = f"{line}.{col-1}"
            end = f"{line}.{col}"
            self.text_editor.tag_add("error", start, end)
            
    def run_lexical(self):
        self.run_analysis("src/analisador_lexico.py", "Análise Léxica")
        
    def run_syntactic(self):
        self.run_analysis("src/analisador_sintatico.py", "Análise Sintática")
        
    def run_semantic(self):
        self.run_analysis("src/analisador_semantico.py", "Análise Semântica")
        
    def run_full(self):
        self.run_analysis("src/compilador_rainbow.py", "Compilação Completa")
        
    def run_program(self):
        """Executa o programa Rainbow"""
        if not self.current_file:
            messagebox.showwarning("Aviso", "Salve o arquivo antes de executar!")
            return
            
        if self.modified:
            self.save_file()
            
        # Abrir executor visual
        self.open_visual_executor()
    
    def open_visual_executor(self):
        """Abre o executor visual"""
        executor_window = tk.Toplevel(self.root)
        executor_window.title("🚀 Executor Rainbow")
        executor_window.geometry("700x500")
        executor_window.configure(bg=self.bg_color)
        
        # Centralizar janela
        executor_window.transient(self.root)
        
        x = (executor_window.winfo_screenwidth() - 700) // 2
        y = (executor_window.winfo_screenheight() - 500) // 2
        executor_window.geometry(f"700x500+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(executor_window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text="🌈 Executando Programa Rainbow", 
                              font=("Arial", 16, "bold"), 
                              bg=self.bg_color, fg=self.text_fg)
        title_label.pack(pady=(0, 10))
        
        # Frame para saída
        output_frame = tk.Frame(main_frame, bg=self.bg_color)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Console de saída
        output_text = tk.Text(output_frame, 
                             bg=self.text_bg, 
                             fg=self.text_fg,
                             font=("Consolas", 11),
                             wrap=tk.WORD,
                             padx=10,
                             pady=10)
        
        scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=output_text.yview)
        output_text.configure(yscrollcommand=scrollbar.set)
        
        output_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para entrada
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Campo de entrada (inicialmente oculto)
        input_label = tk.Label(input_frame, text="", 
                              bg=self.bg_color, fg=self.text_fg,
                              font=("Arial", 10))
        
        input_entry = tk.Entry(input_frame, 
                              bg=self.text_bg, fg=self.text_fg,
                              font=("Arial", 11),
                              insertbackground=self.text_fg)
        
        input_button = tk.Button(input_frame, text="Enviar",
                                bg=self.button_bg, fg=self.text_fg,
                                font=("Arial", 10))
        
        # Inicialmente ocultos
        input_label.pack_forget()
        input_entry.pack_forget()
        input_button.pack_forget()
        
        # Frame para botões
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botão executar
        execute_btn = tk.Button(button_frame, text="▶️ Executar",
                               command=lambda: self._execute_in_visual(output_text, input_label, input_entry, input_button, execute_btn),
                               bg=self.button_bg, fg=self.text_fg,
                               font=("Arial", 10, "bold"),
                               padx=20, pady=5)
        execute_btn.pack(side=tk.LEFT)
        
        # Botão limpar
        clear_btn = tk.Button(button_frame, text="🗑️ Limpar",
                             command=lambda: output_text.delete("1.0", "end"),
                             bg=self.button_bg, fg=self.text_fg,
                             font=("Arial", 10),
                             padx=20, pady=5)
        clear_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Botão fechar
        close_btn = tk.Button(button_frame, text="❌ Fechar",
                             command=executor_window.destroy,
                             bg=self.button_bg, fg=self.text_fg,
                             font=("Arial", 10),
                             padx=20, pady=5)
        close_btn.pack(side=tk.RIGHT)
        
        # Salvar referências para o callback
        self.executor_widgets = {
            'window': executor_window,
            'output': output_text,
            'input_label': input_label,
            'input_entry': input_entry,
            'input_button': input_button,
            'input_frame': input_frame,
            'pending_input': None,
            'input_event': None
        }
    
    def _execute_in_visual(self, output_text, input_label, input_entry, input_button, execute_btn):
        """Executa programa no executor visual"""
        # Desabilitar botão de executar
        execute_btn.config(state=tk.DISABLED, text="⏳ Executando...")
        
        # Limpar saída
        output_text.delete("1.0", "end")
        output_text.insert("end", "🌈 Iniciando execução...\n\n")
        output_text.update()
        
        # Inicializar sistema de entrada
        self.executor_widgets['pending_input'] = None
        self.executor_widgets['input_event'] = None
        
        # Configurar entrada visual
        def handle_input():
            valor = input_entry.get()
            input_entry.delete(0, tk.END)
            
            # Ocultar campos de entrada
            input_label.pack_forget()
            input_entry.pack_forget()
            input_button.pack_forget()
            
            # Mostrar valor na saída
            output_text.insert("end", f"➤ {valor}\n\n")
            output_text.see("end")
            output_text.update()
            
            # Sinalizar que a entrada foi recebida
            if self.executor_widgets.get('input_event'):
                self.executor_widgets['pending_input'] = valor
                self.executor_widgets['input_event'].set()
        
        def on_enter(event):
            handle_input()
        
        input_button.config(command=handle_input)
        input_entry.bind('<Return>', on_enter)
        
        # DEBUG: Testar primeiro sem threading
        try:
            # Mostrar debug
            output_text.insert("end", "DEBUG: Testando execução...\n")
            output_text.update()
            
            # Importar interpretador
            sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
            from interpretador_rainbow import InterpretadorRainbow
            
            output_text.insert("end", "DEBUG: Interpretador importado...\n")
            output_text.update()
            
            # Criar interpretador - usar dialog temporariamente
            def entrada_simples(prompt):
                valor = tk.simpledialog.askstring("Entrada", prompt, parent=self.root)
                output_text.insert("end", f"🔸 {prompt} {valor}\n")
                output_text.update()
                return valor or ""
            
            interpretador = InterpretadorRainbow(ide_callback=entrada_simples)
            
            output_text.insert("end", "DEBUG: Executando arquivo...\n")
            output_text.update()
            
            # Executar
            sucesso, resultado = interpretador.executar_arquivo(self.current_file)
            
            # Mostrar resultado
            if sucesso:
                output_text.insert("end", f"\n🟢 SAÍDA DO PROGRAMA:\n{resultado}\n")
                output_text.insert("end", "\n✅ Sucesso!\n")
            else:
                output_text.insert("end", f"\n🔴 ERRO:\n{resultado}\n")
                self.highlight_error_line(resultado)
                
        except Exception as e:
            output_text.insert("end", f"\n💥 EXCEÇÃO: {str(e)}\n")
            output_text.insert("end", f"Tipo: {type(e).__name__}\n")
            import traceback
            output_text.insert("end", f"Traceback:\n{traceback.format_exc()}\n")
        
        finally:
            execute_btn.config(state=tk.NORMAL, text="▶️ Executar")
            output_text.see("end")
    
    def _execute_visual_thread(self, output_text, execute_btn):
        """Thread para executar no executor visual"""
        try:
            # Mostrar início da execução
            def show_start():
                output_text.insert("end", "Compilando arquivo...\n")
                output_text.see("end")
                output_text.update()
            
            self.root.after(0, show_start)
            
            # Importar interpretador
            sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
            from interpretador_rainbow import InterpretadorRainbow
            
            # Mostrar status
            def show_interpreting():
                output_text.insert("end", "Iniciando interpretação...\n\n")
                output_text.see("end")
                output_text.update()
            
            self.root.after(0, show_interpreting)
            
            # Criar interpretador com callback visual
            interpretador = InterpretadorRainbow(ide_callback=self.solicitar_entrada_visual)
            
            # Executar
            sucesso, resultado = interpretador.executar_arquivo(self.current_file)
            
            # Atualizar interface na thread principal
            def update_ui():
                if sucesso:
                    # Mostrar saída do programa
                    linhas_saida = resultado.split('\n')
                    for linha in linhas_saida:
                        if linha.strip():
                            output_text.insert("end", f"{linha}\n")
                    
                    output_text.insert("end", "\n✅ Programa executado com sucesso!\n")
                else:
                    output_text.insert("end", f"❌ Erro: {resultado}\n")
                    # Destacar linha com erro no editor principal
                    self.highlight_error_line(resultado)
                
                output_text.see("end")
                execute_btn.config(state=tk.NORMAL, text="▶️ Executar")
            
            self.root.after(0, update_ui)
            
        except Exception as e:
            def show_error():
                output_text.insert("end", f"❌ Erro inesperado: {str(e)}\n")
                output_text.insert("end", f"Detalhes: {type(e).__name__}\n")
                self.highlight_error_line(str(e))
                output_text.see("end")
                execute_btn.config(state=tk.NORMAL, text="▶️ Executar")
            
            self.root.after(0, show_error)
    
    def solicitar_entrada_visual(self, prompt):
        """Solicita entrada no executor visual"""
        if not hasattr(self, 'executor_widgets'):
            # Fallback para dialog se não houver executor visual
            return tk.simpledialog.askstring("Entrada", prompt, parent=self.root) or ""
        
        resultado = [None]
        evento = threading.Event()
        
        def mostrar_entrada():
            try:
                # Mostrar prompt na saída
                self.executor_widgets['output'].insert("end", f"📝 {prompt}\n")
                self.executor_widgets['output'].see("end")
                self.executor_widgets['output'].update()
                
                # Mostrar campos de entrada
                self.executor_widgets['input_label'].config(text=prompt)
                self.executor_widgets['input_label'].pack(pady=(5, 0))
                self.executor_widgets['input_entry'].pack(fill=tk.X, pady=5)
                self.executor_widgets['input_button'].pack()
                
                # Focar no campo de entrada
                self.executor_widgets['input_entry'].focus_set()
                
                # Configurar evento
                self.executor_widgets['input_event'] = evento
                
            except Exception as e:
                print(f"Erro ao mostrar entrada: {e}")
                # Fallback para dialog
                valor = tk.simpledialog.askstring("Entrada", prompt, parent=self.root) or ""
                resultado[0] = valor
                evento.set()
        
        self.root.after(0, mostrar_entrada)
        evento.wait()  # Aguardar entrada
        
        return self.executor_widgets.get('pending_input', "") or resultado[0] or ""
    
    def highlight_error_line(self, error_message):
        """Destaca linha com erro no editor"""
        # Extrair número da linha do erro
        import re
        match = re.search(r'linha (\d+)', error_message, re.IGNORECASE)
        if match:
            linha_erro = int(match.group(1))
            
            # Limpar destacamentos anteriores
            self.text_editor.tag_remove("error_line", "1.0", "end")
            
            # Destacar linha com erro
            self.text_editor.tag_configure("error_line", 
                                          background="#ff4444" if self.current_theme == "dark" else "#ffcccc",
                                          font=("Consolas", 10, "italic"))
            
            start_pos = f"{linha_erro}.0"
            end_pos = f"{linha_erro}.end"
            self.text_editor.tag_add("error_line", start_pos, end_pos)
            
            # Ir para a linha do erro
            self.text_editor.see(start_pos)
            self.text_editor.mark_set("insert", start_pos)
        
    def _run_program_thread(self):
        """Thread para executar o programa"""
        try:
            self.status_bar.config(text="Executando programa...")
            self.console_text.insert("end", "🌈 Executando programa Rainbow...\n\n")
            
            # Importar interpretador
            sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
            from interpretador_rainbow import InterpretadorRainbow
            
            # Criar interpretador com callback para entrada
            interpretador = InterpretadorRainbow(ide_callback=self.solicitar_entrada_usuario)
            
            # Executar
            sucesso, resultado = interpretador.executar_arquivo(self.current_file)
            
            if sucesso:
                self.console_text.insert("end", resultado + "\n\n")
                self.console_text.insert("end", "✅ Programa executado com sucesso!\n")
                self.status_bar.config(text="Programa executado com sucesso!")
            else:
                self.console_text.insert("end", f"❌ Erro: {resultado}\n")
                self.status_bar.config(text="Erro na execução")
                
        except Exception as e:
            self.console_text.insert("end", f"❌ Erro: {str(e)}\n")
            self.status_bar.config(text="Erro na execução")
            
    def solicitar_entrada_usuario(self, prompt):
        """Solicita entrada do usuário via dialog"""
        # Esta função será chamada da thread do interpretador
        # Precisamos usar after() para executar na thread principal
        resultado = [None]
        evento = threading.Event()
        
        def pedir_entrada():
            try:
                valor = tk.simpledialog.askstring("Entrada", prompt, parent=self.root)
                if valor is None:
                    valor = ""
                resultado[0] = valor
            except:
                resultado[0] = ""
            finally:
                evento.set()
                
        self.root.after(0, pedir_entrada)
        evento.wait()  # Aguardar resposta
        
        # Mostrar no console
        self.console_text.insert("end", f"{prompt} {resultado[0]}\n")
        
        return resultado[0]
    def show_documentation(self, filename):
        """Exibe janela com documentação markdown"""
        doc_path = os.path.join("docs", filename)
        
        if not os.path.exists(doc_path):
            messagebox.showerror("Erro", f"Arquivo de documentação não encontrado: {filename}")
            return
            
        # Criar janela de documentação
        doc_window = tk.Toplevel(self.root)
        doc_window.title(f"📚 {filename.replace('.md', '').replace('-', ' ').title()}")
        doc_window.geometry("900x700")
        doc_window.configure(bg=self.bg_color)
        
        # Centralizar janela
        doc_window.transient(self.root)
        doc_window.grab_set()
        
        # Centralizar na tela
        x = (doc_window.winfo_screenwidth() - 900) // 2
        y = (doc_window.winfo_screenheight() - 700) // 2
        doc_window.geometry(f"900x700+{x}+{y}")
        
        # Frame principal com scroll
        main_frame = tk.Frame(doc_window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas e scrollbar
        canvas = tk.Canvas(main_frame, bg=self.text_bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.text_bg)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Text widget para exibir markdown formatado
        text_widget = tk.Text(scrollable_frame, 
                             bg=self.text_bg, 
                             fg=self.text_fg,
                             font=("Segoe UI", 11),
                             wrap=tk.WORD,
                             padx=20,
                             pady=20,
                             height=35,
                             width=100,
                             spacing1=2,
                             spacing2=1,
                             spacing3=2)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para formatação markdown
        self._configure_markdown_tags(text_widget)
        
        # Ler e formatar conteúdo markdown
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self._render_markdown(text_widget, content)
                text_widget.config(state=tk.DISABLED)  # Somente leitura
        except Exception as e:
            text_widget.insert(tk.END, f"Erro ao carregar documentação: {str(e)}")
            text_widget.config(state=tk.DISABLED)
        
        # Empacotar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para botões
        button_frame = tk.Frame(doc_window, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Botão fechar
        close_btn = tk.Button(button_frame, text="Fechar", 
                             command=doc_window.destroy,
                             bg=self.button_bg, fg=self.text_fg,
                             font=("Arial", 10),
                             padx=20, pady=8)
        close_btn.pack(side=tk.RIGHT, padx=10)
        
        # Botão abrir no editor externo
        def open_external():
            try:
                import subprocess
                import platform
                
                if platform.system() == 'Darwin':       # macOS
                    subprocess.call(('open', doc_path))
                elif platform.system() == 'Windows':    # Windows
                    os.startfile(doc_path)
                else:                                    # Linux
                    subprocess.call(('xdg-open', doc_path))
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir arquivo: {str(e)}")
        
        external_btn = tk.Button(button_frame, text="📝 Abrir no Editor", 
                                command=open_external,
                                bg=self.button_bg, fg=self.text_fg,
                                font=("Arial", 10),
                                padx=20, pady=8)
        external_btn.pack(side=tk.RIGHT, padx=5)
        
        # Habilitar scroll com mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux
    
    def _configure_markdown_tags(self, text_widget):
        """Configurar tags para formatação de markdown"""
        # Cores baseadas no tema atual
        heading_color = "#4CAF50" if self.current_theme == "dark" else "#2E7D32"
        code_bg = "#2d2d2d" if self.current_theme == "dark" else "#f5f5f5"
        code_fg = "#ff6b6b" if self.current_theme == "dark" else "#d32f2f"
        bold_color = "#81C784" if self.current_theme == "dark" else "#1B5E20"
        link_color = "#64B5F6" if self.current_theme == "dark" else "#1976D2"
        
        # Títulos (H1-H6)
        text_widget.tag_configure("h1", font=("Segoe UI", 20, "bold"), 
                                 foreground=heading_color, spacing1=10, spacing3=5)
        text_widget.tag_configure("h2", font=("Segoe UI", 18, "bold"), 
                                 foreground=heading_color, spacing1=8, spacing3=4)
        text_widget.tag_configure("h3", font=("Segoe UI", 16, "bold"), 
                                 foreground=heading_color, spacing1=6, spacing3=3)
        text_widget.tag_configure("h4", font=("Segoe UI", 14, "bold"), 
                                 foreground=heading_color, spacing1=4, spacing3=2)
        text_widget.tag_configure("h5", font=("Segoe UI", 12, "bold"), 
                                 foreground=heading_color, spacing1=3, spacing3=2)
        text_widget.tag_configure("h6", font=("Segoe UI", 11, "bold"), 
                                 foreground=heading_color, spacing1=2, spacing3=1)
        
        # Texto em negrito
        text_widget.tag_configure("bold", font=("Segoe UI", 11, "bold"), 
                                 foreground=bold_color)
        
        # Texto em itálico
        text_widget.tag_configure("italic", font=("Segoe UI", 11, "italic"))
        
        # Código inline
        text_widget.tag_configure("code", font=("Consolas", 10), 
                                 background=code_bg, foreground=code_fg)
        
        # Blocos de código
        text_widget.tag_configure("codeblock", font=("Consolas", 10), 
                                 background=code_bg, foreground=code_fg,
                                 lmargin1=20, lmargin2=20, spacing1=5, spacing3=5)
        
        # Links
        text_widget.tag_configure("link", foreground=link_color, underline=True)
        
        # Listas
        text_widget.tag_configure("list", lmargin1=20, lmargin2=30)
        
        # Citações
        text_widget.tag_configure("quote", lmargin1=20, lmargin2=20, 
                                 background=code_bg, spacing1=3, spacing3=3)
        
        # Linha horizontal
        text_widget.tag_configure("hr", font=("Segoe UI", 1), spacing1=10, spacing3=10)
        
        # Tabelas
        text_widget.tag_configure("table", font=("Consolas", 10), 
                                 background=code_bg, spacing1=2)
    
    def _render_markdown(self, text_widget, content):
        """Renderizar markdown com formatação"""
        import re
        
        lines = content.split('\n')
        in_code_block = False
        code_lang = ""
        
        for line in lines:
            original_line = line
            
            # Detectar início/fim de bloco de código
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                if in_code_block:
                    code_lang = line.strip()[3:].strip()
                continue
            
            # Se estamos em um bloco de código
            if in_code_block:
                text_widget.insert(tk.END, line + '\n', 'codeblock')
                continue
            
            # Títulos (H1-H6)
            if line.startswith('#'):
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break
                
                if 1 <= level <= 6:
                    title_text = line[level:].strip()
                    tag = f"h{level}"
                    text_widget.insert(tk.END, title_text + '\n\n', tag)
                    continue
            
            # Linha horizontal
            if line.strip() in ['---', '***', '___']:
                text_widget.insert(tk.END, '─' * 50 + '\n\n', 'hr')
                continue
            
            # Lista com marcadores
            if re.match(r'^[\s]*[-*+]\s', line):
                indent = len(line) - len(line.lstrip())
                bullet = '•' if self.current_theme == 'dark' else '●'
                list_text = f"{' ' * indent}{bullet} {line.strip()[1:].strip()}\n"
                text_widget.insert(tk.END, list_text, 'list')
                continue
            
            # Lista numerada
            if re.match(r'^[\s]*\d+\.\s', line):
                text_widget.insert(tk.END, line + '\n', 'list')
                continue
            
            # Citação
            if line.strip().startswith('>'):
                quote_text = line.strip()[1:].strip()
                text_widget.insert(tk.END, f"│ {quote_text}\n", 'quote')
                continue
            
            # Processar formatação inline na linha
            if line.strip():
                self._process_inline_formatting(text_widget, line)
            else:
                text_widget.insert(tk.END, '\n')
    
    def _process_inline_formatting(self, text_widget, line):
        """Processar formatação inline (negrito, itálico, código, links)"""
        import re
        
        # Padrões regex para formatação
        patterns = [
            (r'`([^`]+)`', 'code'),  # Código inline
            (r'\*\*([^*]+)\*\*', 'bold'),  # Negrito
            (r'\*([^*]+)\*', 'italic'),  # Itálico
            (r'\[([^\]]+)\]\([^)]+\)', 'link'),  # Links
        ]
        
        pos = 0
        
        while pos < len(line):
            # Encontrar a próxima formatação
            next_match = None
            next_tag = None
            
            for pattern, tag in patterns:
                match = re.search(pattern, line[pos:])
                if match and (next_match is None or match.start() < next_match.start()):
                    next_match = match
                    next_tag = tag
            
            if next_match:
                # Inserir texto antes da formatação
                if next_match.start() > 0:
                    text_widget.insert(tk.END, line[pos:pos + next_match.start()])
                
                # Inserir texto formatado
                if next_tag == 'link':
                    # Para links, extrair apenas o texto
                    link_match = re.match(r'\[([^\]]+)\]', next_match.group(0))
                    if link_match:
                        text_widget.insert(tk.END, link_match.group(1), next_tag)
                else:
                    # Para outros, usar o grupo capturado
                    text_widget.insert(tk.END, next_match.group(1), next_tag)
                
                pos += next_match.end()
            else:
                # Não há mais formatação, inserir o resto da linha
                text_widget.insert(tk.END, line[pos:])
                break
        
        text_widget.insert(tk.END, '\n')
        
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("Sobre Rainbow IDE")
        about_window.geometry("550x600")
        about_window.configure(bg=self.bg_color)
        about_window.resizable(False, False)
        
        # Centralizar janela
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Centralizar na tela
        x = (about_window.winfo_screenwidth() - 550) // 2
        y = (about_window.winfo_screenheight() - 600) // 2
        about_window.geometry(f"550x600+{x}+{y}")
        
        # Criar gradiente arco-íris
        gradient_frame = tk.Frame(about_window, height=60)
        gradient_frame.pack(fill=tk.X)
        gradient_frame.pack_propagate(False)
        
        for i, color in enumerate(self.rainbow_colors):
            label = tk.Label(gradient_frame, bg=color, width=10)
            label.place(relx=i/7, rely=0, relwidth=1/7, relheight=1)
            
        # Frame para scroll
        main_frame = tk.Frame(about_window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas e scrollbar para conteúdo
        canvas = tk.Canvas(main_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Informações
        info_sections = [
            ("🌈 Rainbow IDE", "Arial", 18, "bold"),
            ("Versão 1.0", "Arial", 12, "normal"),
            ("", "Arial", 8, "normal"),  # Espaço
            ("Ambiente de Desenvolvimento Integrado (IDE)", "Arial", 11, "normal"),
            ("para a linguagem de programação Rainbow", "Arial", 11, "normal"),
            ("", "Arial", 10, "normal"),  # Espaço
            ("📚 PROJETO ACADÊMICO", "Arial", 12, "bold"),
            ("Disciplina: Compiladores", "Arial", 10, "normal"),
            ("Instituição: IFSULDEMINAS Campus Muzambinho", "Arial", 10, "normal"),
            ("Professor: Hudson", "Arial", 10, "normal"),
            ("", "Arial", 8, "normal"),  # Espaço
            ("👨‍💻 DESENVOLVEDORES", "Arial", 12, "bold"),
            ("• Anderson Henrique da Silva", "Arial", 10, "normal"),
            ("• Lurian Letícia dos Reis", "Arial", 10, "normal"),
            ("", "Arial", 8, "normal"),  # Espaço
            ("⚡ CARACTERÍSTICAS", "Arial", 12, "bold"),
            ("• Editor com syntax highlighting", "Arial", 10, "normal"),
            ("• Análise léxica, sintática e semântica", "Arial", 10, "normal"),
            ("• Interpretador integrado", "Arial", 10, "normal"),
            ("• Visualização de tokens, AST e símbolos", "Arial", 10, "normal"),
            ("• Sistema de temas (claro/escuro)", "Arial", 10, "normal"),
            ("• Execução interativa de programas", "Arial", 10, "normal"),
            ("• Exemplos educacionais inclusos", "Arial", 10, "normal"),
            ("", "Arial", 8, "normal"),  # Espaço
            ("🛠️ TECNOLOGIAS", "Arial", 12, "bold"),
            ("• Python 3.10+", "Arial", 10, "normal"),
            ("• Tkinter (Interface Gráfica)", "Arial", 10, "normal"),
            ("• Compilador Rainbow personalizado", "Arial", 10, "normal"),
        ]
        
        for text, font_family, font_size, font_weight in info_sections:
            if text:  # Se não for espaço vazio
                label = tk.Label(scrollable_frame, text=text, 
                               bg=self.bg_color, fg=self.text_fg,
                               font=(font_family, font_size, font_weight), 
                               justify=tk.LEFT)
                label.pack(anchor="w", pady=2)
            else:  # Espaço vazio
                spacer = tk.Label(scrollable_frame, text="", 
                                bg=self.bg_color, 
                                font=("Arial", font_size))
                spacer.pack()
        
        # Empacotar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para botão
        button_frame = tk.Frame(about_window, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Botão fechar
        close_btn = tk.Button(button_frame, text="Fechar", 
                             command=about_window.destroy,
                             bg=self.button_bg, fg=self.text_fg,
                             font=("Arial", 12), padx=30, pady=8)
        close_btn.pack()
        
        # Bind mouse wheel para scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        about_window.bind("<MouseWheel>", _on_mousewheel)

def main():
    root = tk.Tk()
    app = RainbowIDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()