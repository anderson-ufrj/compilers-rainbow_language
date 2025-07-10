# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **complete Rainbow language compiler and IDE** - a Portuguese-based programming language with full implementation including lexical, syntactic, semantic analysis, interpretation, and a professional IDE.

## Commands

```bash
# Run the complete Rainbow IDE
python3 main.py

# Or use the convenient script
./run.sh

# Run individual analysis components
python3 src/analisador_lexico.py <filename.rainbow>
python3 src/analisador_sintatico.py <filename.rainbow>
python3 src/analisador_semantico.py <filename.rainbow>
python3 src/compilador_rainbow.py <filename.rainbow>

# Run Rainbow programs with interpreter
python3 src/interpretador_rainbow.py <filename.rainbow>

# Test with example files
python3 src/compilador_rainbow.py exemplos/ola_mundo.rainbow
python3 src/interpretador_rainbow.py exemplos/programa_interativo.rainbow
```

## Architecture

The compiler follows traditional compilation phases:
1. **Lexical Analysis** (✅ Implemented in `src/analisador_lexico.py`)
   - Tokenizes source code into a stream of tokens
   - Handles error detection and recovery
   - Tracks line/column positions for error reporting
   - Detects: invalid characters (@), malformed identifiers (1var, j@), malformed numbers (2.a3), unclosed comments, unterminated strings

2. **Syntactic Analysis** (✅ Implemented in `src/analisador_sintatico.py`)
   - Validates token sequences according to grammar rules
   - Detects unclosed blocks/expressions ({, (, ")
   - Reports out-of-order commands and misused operators
   - Generates Abstract Syntax Tree (AST)

3. **Semantic Analysis** (✅ Implemented in `src/analisador_semantico.py`)
   - Verifies variable declarations before use
   - Type checking for operations and assignments
   - Scope and visibility checking (GLOBAL, BLOCO, LACO)
   - Duplicate identifier detection
   - Symbol table management with hierarchical scopes
   - Supports implicit variable declaration with type inference

4. **Interpretation** (✅ Implemented in `src/interpretador_rainbow.py`)
   - Complete Rainbow language interpreter
   - Supports all language features including I/O operations
   - Interactive user input via `ler()` function
   - Expression evaluation with operator precedence
   - Control flow execution (if/else, loops)
   - Type conversion and error handling

5. **Professional IDE** (✅ Implemented in `main.py`)
   - Modern GUI with dark/light themes
   - Syntax highlighting and error highlighting
   - Integrated console with program execution
   - Complete compilation workflow showing all analysis phases
   - Interactive program execution with user input support
   - Built-in documentation viewer with markdown support
   - Splash screen with animations

## Rainbow Language Key Features

- **Program Structure**: All programs must start with `RAINBOW`
- **Variables**: Prefixed with `#` (e.g., `#nome`)
- **Statements**: End with `.` (period)
- **Comments**: Use `//`
- **Assignment**: Uses `recebe` operator
- **Data Types**: `NUMERO`, `TEXTO`, `LOGICO`, `LISTA`
- **Control Flow**: `se`/`senao`/`senaose`, `para`, `enquanto`
- **I/O**: `mostrar` (output), `ler` (input)

## Development Guidelines

When extending the lexical analyzer:
- Add new tokens to the `TokenType` enum
- Update `reserved_words` dictionary for new keywords
- Maintain error recovery - don't stop on first error
- Include position tracking (line/column) for all tokens

When implementing next phases:
- Parser should build an AST from the token stream
- Use the existing `Token` class structure
- Maintain the Portuguese language keywords and syntax
- Symbol table should track: name, type, scope, line/column

## Next Steps and Future Improvements

### Potential Enhancements
1. **Code Generation Phase**
   - Implement code generation to assembly or bytecode
   - Add target platform support (x86, ARM, etc.)
   - Create virtual machine for Rainbow bytecode

2. **Language Extensions**
   - Add support for functions/procedures (`funcao`/`procedimento`)
   - Implement arrays and advanced data structures
   - Add object-oriented features (classes, objects)
   - Support for modules and imports

3. **IDE Improvements**
   - Add code completion and IntelliSense
   - Implement debugging support with breakpoints
   - Add project management features
   - Include version control integration
   - Add performance profiling tools

4. **Advanced Features**
   - Optimize interpreter performance
   - Add JIT compilation support
   - Implement garbage collection
   - Add multithreading/concurrency support

5. **Testing and Quality**
   - Expand automated test suite
   - Add performance benchmarks
   - Implement fuzzing for robustness
   - Add static analysis tools

6. **Distribution**
   - Create standalone executable
   - Package for different operating systems
   - Add web-based IDE version
   - Create Rainbow package manager

## Git Commit Guidelines

- NEVER mention "Claude Code" in commit messages
- Focus on technical implementation details
- Use Portuguese when appropriate for feature descriptions
- Keep commit messages concise and professional

## Current Project Status (✅ COMPLETE)

### Implemented Features
- **Complete Rainbow Language Compiler**: All phases implemented
- **Professional IDE**: Modern interface with all required features
- **Interactive Interpreter**: Full program execution with user input
- **Comprehensive Documentation**: Built-in help system and external docs
- **Test Suite**: Multiple example programs demonstrating language features

### IDE Features Implemented
- ✅ Open/save .rainbow files with syntax highlighting
- ✅ Complete compilation showing tokens, AST, symbols, and errors
- ✅ Real-time error highlighting in editor
- ✅ Integrated console with program execution
- ✅ Interactive user input support during program execution
- ✅ Dark/light theme support
- ✅ Built-in documentation viewer
- ✅ Professional splash screen with animations
- ✅ Execute button performs full compilation before execution

## Technical Requirements

- **Language**: Python 3.10+
- **GUI Framework**: Tkinter with PIL for image support
- **Dependencies**: PIL (Pillow) for splash screen images
- **Output Files**: 
  - `.tokens` file with token listings
  - `.ast` file with abstract syntax tree
  - `.simbolos` file with symbol table
  - `.errors`, `.syntax.errors`, `.semantic.errors` for different error types