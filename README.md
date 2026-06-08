# AI-DEEPSEEK-V4-pro client web interface

## Project Overview
This project provides a lightweight, **Zero-Dependency** local web terminal integrated with DEEEPSEEK V4 pro. It acts as a secure, fast, and local graphical interface for interacting with DEEPSEEK generative models without relying on heavy frontend frameworks or external backend dependencies.

## Core Philosophy: Zero-Dependency Architecture
Designed for ultimate cross-platform compatibility and minimal technical debt:
- **No external libraries:** No `pip install`, No `npm install`, No Flask, No Node.js. 
- **Native Python Standard Library:** Uses built-in `http.server`, `urllib`, and `json`.
- **OS-Agnostic Portability:** Runs seamlessly across Windows 11, macOS, and modern Linux distributions (like Ubuntu 24.04) without triggering OS-level package manager conflicts (e.g., PEP 668).

## Key Features
- **Lean Context Strategy:** Built-in token optimization for efficient I/O.
- **Local Session Storage:** Conversations are persistently stored as JSON files on your local machine, ensuring absolute data privacy.
- **Environment-Based Security:** Adheres to OWASP security standards by managing API keys strictly through environment variables rather than hardcoded configuration files.
- **Multi-Modal Support:** Easily attach and parse files natively within the browser before sending data to the API.
- **Context optimisation:** Only send new question with AI output history. Saving context tokens of user input .  

## COST for 50 request of 20K tokens per following table for a last request of 1M token . 
Table_Comparaison_Corrigée:
    | Step | Net New Input | Cached History | Generated Output | Total Context End | Step Cost (USD) | Cumulative Cost (USD) | System Status |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    | 1 | 20,000 | 0 | 3,970 | 23,970 | $0.01739 | $0.01739 | Stable |
    | 2 | 20,000 | 23,970 | 3,970 | 47,940 | $0.01840 | $0.03579 | Stable |
    | 3 | 20,000 | 47,940 | 3,970 | 71,910 | $0.01940 | $0.05519 | Stable |
    | 10 | 20,000 | 215,730 | 3,970 | 239,700 | $0.02645 | $0.21921 | Stable |
    | 20 | 20,000 | 455,430 | 3,970 | 479,400 | $0.03652 | $0.53406 | Stable |
    | 30 | 20,000 | 695,130 | 3,970 | 719,100 | $0.04659 | $0.94959 | Stable |
    | 40 | 20,000 | 934,830 | 3,970 | 958,800 | $0.05665 | $1.46580 | ⚠️ Critical Warning: Approaching VRAM Limit |
    | 41 | 20,000 | 958,800 | 3,970 | 982,770 | $0.05766 | $1.52346 | ⚠️ Critical Warning: Edge of Capacity |
    | 42 | 20,000 | 982,770 | 3,970 | 1,006,740 | $0.05867 | $1.58212 | ❌ **FATAL ERROR:** 1M Context Limit Exceeded |
    | 50 | 20,000 | 1,174,530 | 3,970 | 1,198,500 | $0.06672 | $2.10276 | 🚫 **INVALID:** Mathematically Impossible Architecture |
