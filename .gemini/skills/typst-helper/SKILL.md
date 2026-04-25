---
name: typst-helper
description: Use for creating, compiling, and managing Typst documents. Trigger when working with .typ files, typesetting academic papers, CVs, or reports using Typst.
---

# Typst Helper

## Overview
This skill provides workflows and patterns for efficient Typst development. It enables Gemini CLI to compile PDFs, manage modular Typst components, and apply consistent styling to documents.


## Typst Development Workflows

### 1. Document Compilation
To compile a document and check for errors, use the `typst` CLI:
```bash
typst compile document.typ
```
For watch mode during development:
```bash
typst watch document.typ
```

### 2. Modular Component Usage
When creating complex documents (like CVs or portfolios):
- Break the document into logical `.typ` modules (e.g., `modules_en/`).
- Use `#include` to import modules into the main document.
- Define variables and functions in central files to ensure consistency across modules.

### 3. PDF Export & Artifacts
- Always store source files in the project root or a dedicated `src/` directory.
- Compiled PDFs should be stored in the root or an `exports/` folder.
- Ensure all required assets (logos, images, bibliography files) are available in the project structure before compiling.



