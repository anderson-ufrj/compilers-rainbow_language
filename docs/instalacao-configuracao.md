# 📦 Instalação e Configuração - Rainbow IDE

## Pré-requisitos

### Sistema Operacional
- **Linux** (Ubuntu, Debian, Fedora, etc.)
- **Windows** 10/11
- **macOS** 10.14+

### Python
- **Versão:** Python 3.10 ou superior
- **Recomendado:** Python 3.11 ou 3.12

#### Verificar Versão do Python
```bash
python3 --version
# Deve retornar: Python 3.10.x ou superior
```

### Bibliotecas Necessárias
- **tkinter** - Interface gráfica (geralmente incluído)
- **threading** - Execução assíncrona (padrão)
- **pathlib** - Manipulação de caminhos (padrão)
- **json** - Processamento JSON (padrão)
- **subprocess** - Execução de processos (padrão)

## 🚀 Instalação

### Método 1: Clone do Repositório (Recomendado)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/anderson-ufrj/compilers-rainbow_language
   cd compilers-rainbow_language
   ```

2. **Verificar estrutura:**
   ```bash
   ls -la
   # Deve mostrar: main.py, src/, exemplos/, docs/, etc.
   ```

3. **Testar instalação:**
   ```bash
   python3 main.py
   ```

### Método 2: Download ZIP

1. **Baixar:** [Releases do GitHub](https://github.com/anderson-ufrj/compilers-rainbow_language/releases)
2. **Extrair:** Para pasta desejada
3. **Executar:** `python3 main.py`

## ⚙️ Configuração do Ambiente

### Linux (Ubuntu/Debian)

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade

# Instalar Python 3.10+
sudo apt install python3 python3-pip python3-tk

# Verificar tkinter
python3 -c "import tkinter; print('Tkinter OK')"

# Executar Rainbow IDE
cd compilers-rainbow_language
python3 main.py
```

### Linux (Fedora/CentOS)

```bash
# Instalar Python e tkinter
sudo dnf install python3 python3-pip python3-tkinter

# Ou no CentOS/RHEL:
sudo yum install python3 python3-pip tkinter

# Executar Rainbow IDE
python3 main.py
```

### Windows

1. **Instalar Python:**
   - Baixar de [python.org](https://python.org/downloads/)
   - ✅ Marcar "Add Python to PATH"
   - ✅ Marcar "Install tkinter"

2. **Verificar instalação:**
   ```cmd
   python --version
   python -c "import tkinter; print('Tkinter OK')"
   ```

3. **Executar Rainbow IDE:**
   ```cmd
   cd compilers-rainbow_language
   python main.py
   ```

### macOS

```bash
# Instalar Python via Homebrew
brew install python3
brew install python-tk

# Ou usar Python oficial
# Download de python.org (inclui tkinter)

# Executar Rainbow IDE
cd compilers-rainbow_language
python3 main.py
```

## 🛠️ Scripts de Execução

### Linux/macOS - Script Shell

Criar arquivo `run.sh`:
```bash
#!/bin/bash
cd "$(dirname "$0")"
python3 main.py
```

Tornar executável:
```bash
chmod +x run.sh
./run.sh
```

### Windows - Script Batch

Criar arquivo `run.bat`:
```batch
@echo off
cd /d "%~dp0"
python main.py
pause
```

Executar:
```cmd
run.bat
```

## 🔧 Resolução de Problemas

### Problemas Comuns

#### 1. "Python não encontrado"
**Linux/macOS:**
```bash
# Instalar Python
sudo apt install python3  # Ubuntu/Debian
sudo dnf install python3  # Fedora
brew install python3      # macOS
```

**Windows:**
- Reinstalar Python marcando "Add to PATH"
- Usar `python` em vez de `python3`

#### 2. "ModuleNotFoundError: tkinter"
**Linux:**
```bash
sudo apt install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

**Windows/macOS:**
- Reinstalar Python com todas as opções marcadas

#### 3. "Permission denied"
```bash
# Dar permissão ao script
chmod +x run.sh

# Ou executar diretamente
python3 main.py
```

#### 4. Interface não aparece
- Verificar se está usando ambiente gráfico
- Testar: `python3 -c "import tkinter; tkinter.Tk().mainloop()"`
- No WSL: instalar servidor X (VcXsrv, Xming)

#### 5. Caracteres especiais não aparecem
```bash
# Definir encoding UTF-8
export LANG=pt_BR.UTF-8
export LC_ALL=pt_BR.UTF-8
```

### Verificação de Saúde do Sistema

Script de diagnóstico:
```python
#!/usr/bin/env python3
import sys
import os

def verificar_sistema():
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Diretório: {os.getcwd()}")
    
    # Testar importações
    try:
        import tkinter
        print("✅ tkinter: OK")
    except ImportError:
        print("❌ tkinter: ERRO")
    
    try:
        import threading
        print("✅ threading: OK")
    except ImportError:
        print("❌ threading: ERRO")
    
    # Verificar arquivos
    arquivos = ['main.py', 'src/analisador_lexico.py', 'exemplos/']
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}: OK")
        else:
            print(f"❌ {arquivo}: NÃO ENCONTRADO")

if __name__ == "__main__":
    verificar_sistema()
```

Salvar como `verificar.py` e executar:
```bash
python3 verificar.py
```

## 🌍 Configurações Regionais

### Localização Portuguesa

**Linux:**
```bash
# Instalar locales português
sudo apt install language-pack-pt
sudo locale-gen pt_BR.UTF-8

# Configurar
export LANG=pt_BR.UTF-8
export LC_ALL=pt_BR.UTF-8
```

**Windows:**
- Painel de Controle → Região → Português (Brasil)

**macOS:**
- System Preferences → Language & Region → Português

## 📂 Estrutura de Arquivos

### Organização Recomendada
```
~/Documentos/
└── rainbow-projetos/
    ├── compilers-rainbow_language/  # Código fonte da IDE
    ├── meus-programas/              # Seus programas .rainbow
    │   ├── exercicios/
    │   ├── projetos/
    │   └── testes/
    └── exemplos-personalizados/     # Exemplos criados
```

### Configuração de Workspace
```bash
# Criar estrutura
mkdir -p ~/Documentos/rainbow-projetos/{meus-programas,exemplos-personalizados}
mkdir -p ~/Documentos/rainbow-projetos/meus-programas/{exercicios,projetos,testes}

# Copiar exemplos
cp exemplos/*.rainbow ~/Documentos/rainbow-projetos/exemplos-personalizados/
```

## 🚀 Performance e Otimização

### Configurações Recomendadas

#### Para Desenvolvimento
```bash
# Usar Python otimizado
python3 -O main.py

# Ou modo debug
python3 -d main.py
```

#### Para Produção
```bash
# Compilar bytecode
python3 -m compileall src/

# Executar
python3 main.py
```

### Monitoramento de Recursos
```python
# Adicionar ao início de main.py para debug
import psutil
import time

def monitor_recursos():
    processo = psutil.Process()
    print(f"💾 Memória: {processo.memory_info().rss / 1024 / 1024:.1f} MB")
    print(f"⚡ CPU: {processo.cpu_percent():.1f}%")
```

## 🐳 Execução via Docker (Avançado)

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar código
COPY . .

# Comando padrão
CMD ["python3", "main.py"]
```

### Executar com X11
```bash
# Build
docker build -t rainbow-ide .

# Executar (Linux)
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  rainbow-ide
```

## 📱 Integração com IDEs Externas

### VS Code
1. Instalar extensão Python
2. Abrir pasta do projeto
3. Configurar interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
4. Executar: `F5` ou terminal integrado

### PyCharm
1. New Project → Existing Sources
2. Selecionar pasta do projeto  
3. Configure Python interpreter
4. Run → main.py

## 🔐 Permissões e Segurança

### Permissões de Arquivo
```bash
# Dar permissões adequadas
chmod 755 main.py run.sh
chmod 644 src/*.py exemplos/*.rainbow
chmod 755 docs/
```

### Segurança
- ✅ Código fonte aberto e auditável
- ✅ Não requer privilégios administrativos
- ✅ Não acessa rede ou arquivos do sistema
- ✅ Execução em sandbox (interpretador)

## 📋 Checklist de Instalação

- [ ] Python 3.10+ instalado
- [ ] Tkinter disponível
- [ ] Código baixado/clonado
- [ ] Estrutura de arquivos verificada
- [ ] IDE executa sem erros
- [ ] Exemplos funcionam
- [ ] Temas mudam corretamente
- [ ] Programas executam com entrada
- [ ] Todas as análises funcionam

## 💡 Dicas Avançadas

### Alias para Execução Rápida
```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
alias rainbow="cd ~/Documentos/rainbow-projetos/compilers-rainbow_language && python3 main.py"

# Usar:
rainbow
```

### Backup Automático
```bash
#!/bin/bash
# backup.sh
DATA=$(date +%Y%m%d_%H%M%S)
tar -czf "rainbow_backup_$DATA.tar.gz" ~/Documentos/rainbow-projetos/
```

### Atualização Automática
```bash
#!/bin/bash
# update.sh
cd ~/Documentos/rainbow-projetos/compilers-rainbow_language
git pull origin main
echo "Rainbow IDE atualizado!"
```

---

*Para suporte adicional, consulte as [Issues do GitHub](https://github.com/anderson-ufrj/compilers-rainbow_language/issues) ou entre em contato com os desenvolvedores.*