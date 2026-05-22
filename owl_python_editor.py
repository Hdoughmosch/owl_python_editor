#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hide console window on Windows (must be before any GUI imports)
import sys
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
"""
Owl Python Editor 🦉 - Lightweight Python Code Editor
by Husam Doughmosch
Built with tkinter
Fast | Beautiful | Multiple themes | Advanced search | Live execution

═══════════════════════════════════════════════════════════════
  LICENSE & TERMS OF USE
═══════════════════════════════════════════════════════════════

© 2026 Husam Doughmosch. All rights reserved.

FREE FOR PERSONAL USE ONLY
You may use this software for personal, educational, and 
non-commercial purposes at no cost.

STRICTLY PROHIBITED:
  × Commercial use without written permission
  × Redistribution on any website, platform, or repository
  × Modification or creation of derivative works
  × Removal or alteration of author credits
  × Use of the author's name without permission
  × Selling, sublicensing, or monetizing this software

NO WARRANTY:
This software is provided "AS IS" without warranty of any kind,
express or implied. The author is not liable for any damages
arising from the use of this software.

═══════════════════════════════════════════════════════════════
  SUPPORT THE PROJECT
═══════════════════════════════════════════════════════════════

This editor is free because of supporters like you.
Your donation keeps updates coming forever.

Developer: Husam Doughmosch
X (Twitter): https://x.com/HDoughmosch
LinkedIn: https://www.linkedin.com/in/husam-doughmosch-085568407

To donate or sponsor: Contact via X or LinkedIn
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import keyword as kw
import builtins
import io
import sys
import os
import json

# ============================================================
#  THEMES - 10 Beautiful Color Schemes
# ============================================================

THEMES = {
    "taqua": {
        "name": "Taqua (Gold)",
        "bg": "#1a1a1a", "bg_sidebar": "#141414", "bg_status": "#0f0f0f",
        "fg": "#e8e8e8", "fg_dim": "#666666",
        "accent": "#f0c040", "accent2": "#d4a017",
        "keyword": "#ff9f43", "string": "#2ecc71", "comment": "#95a5a6",
        "builtin": "#f1c40f", "number": "#e74c3c", "function": "#3498db",
        "decorator": "#9b59b6", "sel_fg": "#ffffff",
        "line_bg": "#1e1e1e", "line_fg": "#555555", "cursor": "#f0c040",
        "output_bg": "#0a0a0a", "output_fg": "#cccccc",
        "error": "#e74c3c", "success": "#2ecc71",
    },
    "sail": {
        "name": "Sail (Ocean)",
        "bg": "#0f172a", "bg_sidebar": "#0b1120", "bg_status": "#080c18",
        "fg": "#e2e8f0", "fg_dim": "#64748b",
        "accent": "#38bdf8", "accent2": "#0284c7",
        "keyword": "#c084fc", "string": "#4ade80", "comment": "#64748b",
        "builtin": "#38bdf8", "number": "#f472b6", "function": "#60a5fa",
        "decorator": "#a78bfa", "sel_fg": "#ffffff",
        "line_bg": "#162032", "line_fg": "#475569", "cursor": "#38bdf8",
        "output_bg": "#020617", "output_fg": "#cbd5e1",
        "error": "#f87171", "success": "#4ade80",
    },
    "sun": {
        "name": "Sun (Warm)",
        "bg": "#1c1917", "bg_sidebar": "#161311", "bg_status": "#0f0d0b",
        "fg": "#fafaf9", "fg_dim": "#78716c",
        "accent": "#facc15", "accent2": "#ca8a04",
        "keyword": "#fb923c", "string": "#a3e635", "comment": "#78716c",
        "builtin": "#facc15", "number": "#f87171", "function": "#60a5fa",
        "decorator": "#c084fc", "sel_fg": "#ffffff",
        "line_bg": "#231f1d", "line_fg": "#57534e", "cursor": "#facc15",
        "output_bg": "#0c0a09", "output_fg": "#d6d3d1",
        "error": "#ef4444", "success": "#84cc16",
    },
    "monokai": {
        "name": "Monokai",
        "bg": "#272822", "bg_sidebar": "#1e1f1c", "bg_status": "#161712",
        "fg": "#f8f8f2", "fg_dim": "#75715e",
        "accent": "#a6e22e", "accent2": "#7cb518",
        "keyword": "#f92672", "string": "#e6db74", "comment": "#75715e",
        "builtin": "#66d9ef", "number": "#ae81ff", "function": "#a6e22e",
        "decorator": "#fd971f", "sel_fg": "#ffffff",
        "line_bg": "#2d2e29", "line_fg": "#59584f", "cursor": "#f8f8f2",
        "output_bg": "#1a1b16", "output_fg": "#cfcfc2",
        "error": "#f92672", "success": "#a6e22e",
    },
    "dracula": {
        "name": "Dracula",
        "bg": "#282a36", "bg_sidebar": "#21222c", "bg_status": "#191a21",
        "fg": "#f8f8f2", "fg_dim": "#6272a4",
        "accent": "#ff79c6", "accent2": "#bd93f9",
        "keyword": "#ff79c6", "string": "#f1fa8c", "comment": "#6272a4",
        "builtin": "#8be9fd", "number": "#bd93f9", "function": "#50fa7b",
        "decorator": "#ffb86c", "sel_fg": "#ffffff",
        "line_bg": "#2d2f3b", "line_fg": "#5a5e72", "cursor": "#f8f8f2",
        "output_bg": "#1e1f29", "output_fg": "#bfbfbf",
        "error": "#ff5555", "success": "#50fa7b",
    },
    "nord": {
        "name": "Nord (Ice)",
        "bg": "#2e3440", "bg_sidebar": "#272c36", "bg_status": "#1e2229",
        "fg": "#d8dee9", "fg_dim": "#4c566a",
        "accent": "#88c0d0", "accent2": "#5e81ac",
        "keyword": "#81a1c1", "string": "#a3be8c", "comment": "#4c566a",
        "builtin": "#88c0d0", "number": "#b48ead", "function": "#8fbcbb",
        "decorator": "#d08770", "sel_fg": "#eceff4",
        "line_bg": "#353d4b", "line_fg": "#4c566a", "cursor": "#d8dee9",
        "output_bg": "#242933", "output_fg": "#abb9cf",
        "error": "#bf616a", "success": "#a3be8c",
    },
    "gruvbox": {
        "name": "Gruvbox",
        "bg": "#282828", "bg_sidebar": "#1d2021", "bg_status": "#161818",
        "fg": "#ebdbb2", "fg_dim": "#928374",
        "accent": "#fabd2f", "accent2": "#d79921",
        "keyword": "#fb4934", "string": "#b8bb26", "comment": "#928374",
        "builtin": "#fe8019", "number": "#d3869b", "function": "#8ec07c",
        "decorator": "#b16286", "sel_fg": "#fbf1c7",
        "line_bg": "#32302f", "line_fg": "#665c54", "cursor": "#ebdbb2",
        "output_bg": "#1d2021", "output_fg": "#d5c4a1",
        "error": "#cc241d", "success": "#98971a",
    },
    "one_dark": {
        "name": "One Dark",
        "bg": "#282c34", "bg_sidebar": "#21252b", "bg_status": "#181a1f",
        "fg": "#abb2bf", "fg_dim": "#5c6370",
        "accent": "#61afef", "accent2": "#528bcc",
        "keyword": "#c678dd", "string": "#98c379", "comment": "#5c6370",
        "builtin": "#61afef", "number": "#d19a66", "function": "#61afef",
        "decorator": "#e5c07b", "sel_fg": "#ffffff",
        "line_bg": "#2c313a", "line_fg": "#4b5263", "cursor": "#528bff",
        "output_bg": "#1e2127", "output_fg": "#9ca3b0",
        "error": "#e06c75", "success": "#98c379",
    },
    "solarized": {
        "name": "Solarized",
        "bg": "#002b36", "bg_sidebar": "#00222b", "bg_status": "#001e26",
        "fg": "#839496", "fg_dim": "#586e75",
        "accent": "#b58900", "accent2": "#cb4b16",
        "keyword": "#859900", "string": "#2aa198", "comment": "#586e75",
        "builtin": "#268bd2", "number": "#d33682", "function": "#b58900",
        "decorator": "#cb4b16", "sel_fg": "#eee8d5",
        "line_bg": "#003340", "line_fg": "#405c66", "cursor": "#839496",
        "output_bg": "#001e26", "output_fg": "#93a1a1",
        "error": "#dc322f", "success": "#859900",
    },
    "rose_pine": {
        "name": "Rose Pine",
        "bg": "#191724", "bg_sidebar": "#13111f", "bg_status": "#0d0b17",
        "fg": "#e0def4", "fg_dim": "#6e6a86",
        "accent": "#ebbcba", "accent2": "#c4a7e7",
        "keyword": "#31748f", "string": "#f6c177", "comment": "#6e6a86",
        "builtin": "#9ccfd8", "number": "#eb6f92", "function": "#c4a7e7",
        "decorator": "#f6c177", "sel_fg": "#e0def4",
        "line_bg": "#1f1d2e", "line_fg": "#524f67", "cursor": "#e0def4",
        "output_bg": "#16141f", "output_fg": "#cdcbe0",
        "error": "#eb6f92", "success": "#9ccfd8",
    },
    "midnight": {
        "name": "Midnight (Deep Blue)",
        "bg": "#0d1117", "bg_sidebar": "#161b22", "bg_status": "#010409",
        "fg": "#c9d1d9", "fg_dim": "#8b949e",
        "accent": "#58a6ff", "accent2": "#1f6feb",
        "keyword": "#ff7b72", "string": "#a5d6ff", "comment": "#8b949e",
        "builtin": "#79c0ff", "number": "#d2a8ff", "function": "#d2a8ff",
        "decorator": "#f0883e", "sel_fg": "#ffffff",
        "line_bg": "#161b22", "line_fg": "#484f58", "cursor": "#58a6ff",
        "output_bg": "#0d1117", "output_fg": "#b1bac4",
        "error": "#f85149", "success": "#3fb950",
    },
    "tokyo_night": {
        "name": "Tokyo Night",
        "bg": "#1a1b26", "bg_sidebar": "#16161e", "bg_status": "#0f0f14",
        "fg": "#a9b1d6", "fg_dim": "#565f89",
        "accent": "#7aa2f7", "accent2": "#bb9af7",
        "keyword": "#bb9af7", "string": "#9ece6a", "comment": "#565f89",
        "builtin": "#7aa2f7", "number": "#ff9e64", "function": "#7aa2f7",
        "decorator": "#e0af68", "sel_fg": "#c0caf5",
        "line_bg": "#24283b", "line_fg": "#414868", "cursor": "#c0caf5",
        "output_bg": "#16161e", "output_fg": "#a9b1d6",
        "error": "#f7768e", "success": "#9ece6a",
    },
    "catppuccin": {
        "name": "Catppuccin (Mocha)",
        "bg": "#1e1e2e", "bg_sidebar": "#181825", "bg_status": "#11111b",
        "fg": "#cdd6f4", "fg_dim": "#6c7086",
        "accent": "#f5c2e7", "accent2": "#cba6f7",
        "keyword": "#cba6f7", "string": "#a6e3a1", "comment": "#6c7086",
        "builtin": "#89b4fa", "number": "#fab387", "function": "#89b4fa",
        "decorator": "#f9e2af", "sel_fg": "#1e1e2e",
        "line_bg": "#313244", "line_fg": "#45475a", "cursor": "#f5c2e7",
        "output_bg": "#181825", "output_fg": "#bac2de",
        "error": "#f38ba8", "success": "#a6e3a1",
    },
    "everforest": {
        "name": "Everforest",
        "bg": "#2b3339", "bg_sidebar": "#232a2e", "bg_status": "#1e2326",
        "fg": "#d3c6aa", "fg_dim": "#859289",
        "accent": "#a7c080", "accent2": "#7fbbb3",
        "keyword": "#e67e80", "string": "#a7c080", "comment": "#859289",
        "builtin": "#7fbbb3", "number": "#d699b6", "function": "#a7c080",
        "decorator": "#dbbc7f", "sel_fg": "#2b3339",
        "line_bg": "#343f44", "line_fg": "#5c6a72", "cursor": "#d3c6aa",
        "output_bg": "#232a2e", "output_fg": "#d3c6aa",
        "error": "#e67e80", "success": "#a7c080",
    },
    "oceanic": {
        "name": "Oceanic (Deep Sea)",
        "bg": "#1b2b34", "bg_sidebar": "#162228", "bg_status": "#0f1a20",
        "fg": "#d8dee9", "fg_dim": "#65737e",
        "accent": "#6699cc", "accent2": "#5fb3b3",
        "keyword": "#c594c5", "string": "#99c794", "comment": "#65737e",
        "builtin": "#6699cc", "number": "#f99157", "function": "#6699cc",
        "decorator": "#fac863", "sel_fg": "#ffffff",
        "line_bg": "#243340", "line_fg": "#4f5b66", "cursor": "#d8dee9",
        "output_bg": "#162228", "output_fg": "#a7adba",
        "error": "#ec5f67", "success": "#99c794",
    },
    "paper": {
        "name": "Paper (Light)",
        "bg": "#faf8f5", "bg_sidebar": "#f0ede8", "bg_status": "#e8e4de",
        "fg": "#2c2c2c", "fg_dim": "#8a8580",
        "accent": "#d4a017", "accent2": "#b8860b",
        "keyword": "#b45309", "string": "#15803d", "comment": "#a8a29e",
        "builtin": "#0369a1", "number": "#be123c", "function": "#0369a1",
        "decorator": "#7c3aed", "sel_fg": "#ffffff",
        "line_bg": "#f5f0eb", "line_fg": "#c4bfb8", "cursor": "#d4a017",
        "output_bg": "#f0ede8", "output_fg": "#57534e",
        "error": "#dc2626", "success": "#16a34a",
    },
    "sakura": {
        "name": "Sakura (Light Pink)",
        "bg": "#fff5f7", "bg_sidebar": "#fce7ec", "bg_status": "#f9d5e5",
        "fg": "#4a2c3a", "fg_dim": "#b5838d",
        "accent": "#e91e63", "accent2": "#c2185b",
        "keyword": "#c2185b", "string": "#2e7d32", "comment": "#b5838d",
        "builtin": "#1565c0", "number": "#d32f2f", "function": "#1565c0",
        "decorator": "#7b1fa2", "sel_fg": "#ffffff",
        "line_bg": "#fce7ec", "line_fg": "#d4a5b0", "cursor": "#e91e63",
        "output_bg": "#fce7ec", "output_fg": "#6d4c5a",
        "error": "#c62828", "success": "#2e7d32",
    },
    "cream": {
        "name": "Cream (Warm Light)",
        "bg": "#fdf6e3", "bg_sidebar": "#eee8d5", "bg_status": "#e5dcc8",
        "fg": "#2c3e50", "fg_dim": "#93a1a1",
        "accent": "#b58900", "accent2": "#cb4b16",
        "keyword": "#268bd2", "string": "#2aa198", "comment": "#93a1a1",
        "builtin": "#268bd2", "number": "#d33682", "function": "#b58900",
        "decorator": "#cb4b16", "sel_fg": "#ffffff",
        "line_bg": "#f5ecd8", "line_fg": "#c4b9a5", "cursor": "#b58900",
        "output_bg": "#eee8d5", "output_fg": "#586e75",
        "error": "#dc322f", "success": "#859900",
    },
    "mint": {
        "name": "Mint (Fresh Light)",
        "bg": "#f0fdf4", "bg_sidebar": "#dcfce7", "bg_status": "#bbf7d0",
        "fg": "#1a2e22", "fg_dim": "#6b8f71",
        "accent": "#16a34a", "accent2": "#15803d",
        "keyword": "#166534", "string": "#15803d", "comment": "#6b8f71",
        "builtin": "#0d9488", "number": "#c2410c", "function": "#0d9488",
        "decorator": "#7c3aed", "sel_fg": "#ffffff",
        "line_bg": "#dcfce7", "line_fg": "#a7c4ad", "cursor": "#16a34a",
        "output_bg": "#dcfce7", "output_fg": "#3f5c47",
        "error": "#dc2626", "success": "#16a34a",
    },
    "sky": {
        "name": "Sky (Blue Light)",
        "bg": "#f0f9ff", "bg_sidebar": "#e0f2fe", "bg_status": "#bae6fd",
        "fg": "#0f172a", "fg_dim": "#64748b",
        "accent": "#0284c7", "accent2": "#0369a1",
        "keyword": "#7c3aed", "string": "#059669", "comment": "#94a3b8",
        "builtin": "#0284c7", "number": "#dc2626", "function": "#0284c7",
        "decorator": "#c2410c", "sel_fg": "#ffffff",
        "line_bg": "#e0f2fe", "line_fg": "#cbd5e1", "cursor": "#0284c7",
        "output_bg": "#e0f2fe", "output_fg": "#334155",
        "error": "#ef4444", "success": "#059669",
    },
    "lavender": {
        "name": "Lavender (Purple Light)",
        "bg": "#faf5ff", "bg_sidebar": "#f3e8ff", "bg_status": "#e9d5ff",
        "fg": "#2e1065", "fg_dim": "#8b5cf6",
        "accent": "#7c3aed", "accent2": "#6d28d9",
        "keyword": "#7c3aed", "string": "#059669", "comment": "#a78bfa",
        "builtin": "#4f46e5", "number": "#dc2626", "function": "#4f46e5",
        "decorator": "#c2410c", "sel_fg": "#ffffff",
        "line_bg": "#f3e8ff", "line_fg": "#c4b5fd", "cursor": "#7c3aed",
        "output_bg": "#f3e8ff", "output_fg": "#4c1d95",
        "error": "#ef4444", "success": "#059669",
    },
    "peach": {
        "name": "Peach (Soft Light)",
        "bg": "#fff7ed", "bg_sidebar": "#ffedd5", "bg_status": "#fed7aa",
        "fg": "#431407", "fg_dim": "#c2410c",
        "accent": "#ea580c", "accent2": "#c2410c",
        "keyword": "#be123c", "string": "#15803d", "comment": "#fdba74",
        "builtin": "#0369a1", "number": "#dc2626", "function": "#0369a1",
        "decorator": "#7c3aed", "sel_fg": "#ffffff",
        "line_bg": "#ffedd5", "line_fg": "#fdba74", "cursor": "#ea580c",
        "output_bg": "#ffedd5", "output_fg": "#7c2d12",
        "error": "#dc2626", "success": "#15803d",
    },
    "slate_light": {
        "name": "Slate Light",
        "bg": "#f8fafc", "bg_sidebar": "#f1f5f9", "bg_status": "#e2e8f0",
        "fg": "#0f172a", "fg_dim": "#64748b",
        "accent": "#475569", "accent2": "#334155",
        "keyword": "#7c3aed", "string": "#059669", "comment": "#94a3b8",
        "builtin": "#2563eb", "number": "#dc2626", "function": "#2563eb",
        "decorator": "#c2410c", "sel_fg": "#ffffff",
        "line_bg": "#f1f5f9", "line_fg": "#cbd5e1", "cursor": "#475569",
        "output_bg": "#f1f5f9", "output_fg": "#334155",
        "error": "#ef4444", "success": "#059669",
    },
}

# ============================================================
#  SETTINGS - Persistent user preferences
# ============================================================

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "owl_settings.json")

# ============================================================
#  CODE SNIPPETS
# ============================================================

SNIPPETS = {
    "for": "for ${item} in ${iterable}:\n    ${pass}",
    "if": "if ${condition}:\n    ${pass}",
    "ife": "if ${condition}:\n    ${pass}\nelse:\n    ${pass2}",
    "def": "def ${name}(${args}):\n    ${pass}",
    "class": "class ${Name}(${object}):\n    def __init__(self${args}):\n        ${pass}",
    "main": "if __name__ == \"__main__\":\n    ${pass}",
    "try": "try:\n    ${pass}\nexcept ${Exception} as e:\n    ${pass2}",
    "with": "with open(${file}, '${mode}') as ${f}:\n    ${pass}",
    "imp": "import ${module}",
    "from": "from ${module} import ${name}",
    "list": "[${x} for ${x} in ${iterable} if ${condition}]",
    "dict": "{${key}: ${value} for ${key}, ${value} in ${iterable}.items()}",
    "print": "print(f\"${message}\")",
    "log": "import logging\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)",
    "tk": "import tkinter as tk\nfrom tkinter import ttk\n\nroot = tk.Tk()\nroot.title(\"${title}\")\nroot.geometry(\"400x300\")\n\nroot.mainloop()",
}

# ============================================================
#  SYNTAX HIGHLIGHTING PATTERNS
# ============================================================

PYTHON_KEYWORDS = set(kw.kwlist)
PYTHON_BUILTINS = set(dir(builtins))

RE_PATTERNS = [
    (r'\b(def|class)\s+([a-zA-Z_][a-zA-Z0-9_]*)', ['keyword', 'function']),
    (r'@[a-zA-Z_][a-zA-Z0-9_]*', 'decorator'),
    (r'\b(' + '|'.join(re.escape(k) for k in PYTHON_KEYWORDS) + r')\b', 'keyword'),
    (r'\b(' + '|'.join(re.escape(b) for b in PYTHON_BUILTINS if not b.startswith('_')) + r')\b', 'builtin'),
    (r'[ruf]*"""[\s\S]*?"""', 'string'),
    (r"[ruf]*'''[\s\S]*?'''", 'string'),
    (r'[ruf]*"(?:[^"\\\\]|\\\\.)*"', 'string'),
    (r"[ruf]*'(?:[^'\\\\]|\\\\.)*'", 'string'),
    (r'#.*$', 'comment'),
    (r'\b\d+\.?\d*\b', 'number'),
    (r'\b[A-Z_][A-Z0-9_]*\b', 'builtin'),
]

# ============================================================
#  MAIN EDITOR CLASS
# ============================================================

class OwlEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Owl Python Editor 🦉")
        self.root.geometry("1200x750")
        self.root.configure(bg="#1a1a1a")

        # State
        self.current_theme = "taqua"
        self.font_family = "Consolas"
        self.font_size = 13
        self.modified = False
        self.file_path = None
        self.output_visible = False
        self.sidebar_visible = False
        self.multi_cursors = []  # List of (line, col) positions
        self.autocomplete_box = None
        self.folded_regions = {}  # line_start: line_end
        self.recent_files = []  # List of recent file paths
        self.bookmarks = set()  # Set of bookmarked line numbers
        self.word_wrap = False
        self.zen_mode = False

        # Build UI
        self.setup_styles()
        self.create_menu()
        self.create_toolbar()
        self.create_main_area()
        self.create_statusbar()
        self.create_output_panel()
        self.bind_events()

        # Load saved settings
        saved = self._load_settings()
        if saved.get("theme") in THEMES:
            self.current_theme = saved["theme"]
        if saved.get("font_size"):
            self.font_size = saved["font_size"]
        if saved.get("word_wrap"):
            self.word_wrap = saved["word_wrap"]
            self.editor.config(wrap=tk.WORD)
        if saved.get("sidebar_visible"):
            self.sidebar_visible = True
            self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, before=self.paned)
            self._refresh_sidebar()
        if saved.get("output_visible"):
            self.output_visible = True
            self.paned.add(self.output_frame, minsize=80)
            self.root.after(50, self._set_sash_position)

        # Initialize
        self.apply_theme()
        self.update_font()
        self.new_file()
        self.root.after(100, self.update_line_numbers)

        # Ensure window is focused and on top at startup
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(500, lambda: self.root.attributes("-topmost", False))
        self.root.focus_force()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def _load_settings(self):
        """Load saved settings from JSON file"""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_settings(self):
        """Save current settings to JSON file"""
        settings = {
            "theme": self.current_theme,
            "font_size": self.font_size,
            "word_wrap": self.word_wrap,
            "sidebar_visible": self.sidebar_visible,
            "output_visible": self.output_visible,
        }
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
        except:
            pass

    def create_menu(self):
        menubar = tk.Menu(self.root, bg="#1a1a1a", fg="#e8e8e8", 
                         activebackground="#f0c040", activeforeground="#1a1a1a",
                         borderwidth=0)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, bg="#1a1a1a", fg="#e8e8e8",
                           activebackground="#f0c040", activeforeground="#1a1a1a")
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New          Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open         Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save         Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As      Ctrl+Shift+S", command=self.save_as)
        # Recent files submenu
        self.recent_menu = tk.Menu(file_menu, tearoff=0, bg="#1a1a1a", fg="#e8e8e8",
                                  activebackground="#f0c040", activeforeground="#1a1a1a")
        file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Auto Save (30s)", command=self.toggle_auto_save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0, bg="#1a1a1a", fg="#e8e8e8",
                           activebackground="#f0c040", activeforeground="#1a1a1a")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo         Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="Redo         Ctrl+Y", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut          Ctrl+X", command=self.cut)
        edit_menu.add_command(label="Copy         Ctrl+C", command=self.copy)
        edit_menu.add_command(label="Paste        Ctrl+V", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All   Ctrl+A", command=self.select_all)
        edit_menu.add_command(label="Find         Ctrl+F", command=self.show_find)
        edit_menu.add_command(label="Replace      Ctrl+H", command=self.show_replace)

        view_menu = tk.Menu(menubar, tearoff=0, bg="#1a1a1a", fg="#e8e8e8",
                           activebackground="#f0c040", activeforeground="#1a1a1a")
        menubar.add_cascade(label="View", menu=view_menu)

        themes_menu = tk.Menu(view_menu, tearoff=0, bg="#1a1a1a", fg="#e8e8e8",
                             activebackground="#f0c040", activeforeground="#1a1a1a")
        view_menu.add_cascade(label="Themes", menu=themes_menu)

        for theme_id, theme_data in THEMES.items():
            themes_menu.add_command(
                label=f"  {theme_data['name']}",
                command=lambda t=theme_id: self.switch_theme(t)
            )

        view_menu.add_separator()
        view_menu.add_command(label="Toggle Sidebar  F3", command=self.toggle_sidebar)
        view_menu.add_command(label="Toggle Fold  Ctrl+Shift+L", command=self.toggle_fold)
        view_menu.add_separator()
        view_menu.add_command(label="Word Wrap    Alt+Z", command=self.toggle_word_wrap)
        view_menu.add_command(label="Zen Mode     F11", command=self.toggle_zen_mode)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Bookmark  Ctrl+B", command=self.toggle_bookmark)
        view_menu.add_command(label="Next Bookmark    F2", command=self.next_bookmark)
        view_menu.add_command(label="Prev Bookmark    Shift+F2", command=self.prev_bookmark)
        view_menu.add_separator()
        view_menu.add_command(label="Zoom In      Ctrl++", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out     Ctrl+-", command=self.zoom_out)
        view_menu.add_command(label="Reset Zoom   Ctrl+0", command=self.reset_zoom)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Output  F4", command=self.toggle_output)

        run_menu = tk.Menu(menubar, tearoff=0, bg="#1a1a1a", fg="#e8e8e8",
                          activebackground="#f0c040", activeforeground="#1a1a1a")
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run          F5", command=self.run_code)
        run_menu.add_command(label="Run Selection  F6", command=self.run_selection)

        help_menu = tk.Menu(menubar, tearoff=0, bg="#1a1a1a", fg="#e8e8e8",
                           activebackground="#f0c040", activeforeground="#1a1a1a")
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About Owl Editor", command=self.show_about)

        tools_menu = tk.Menu(menubar, tearoff=0, bg="#1a1a1a", fg="#e8e8e8",
                            activebackground="#f0c040", activeforeground="#1a1a1a")
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Scan Installed Modules", command=self.scan_installed_modules)
        tools_menu.add_separator()
        tools_menu.add_command(label="Format JSON    Ctrl+Shift+J", command=self.format_json)
        tools_menu.add_separator()
        tools_menu.add_command(label="Clear Module Cache", command=self._clear_module_cache)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.root, height=38, bg="#141414")
        self.toolbar.pack(fill=tk.X, side=tk.TOP)
        self.toolbar.pack_propagate(False)

        buttons = [
            ("New", self.new_file),
            ("Open", self.open_file),
            ("Save", self.save_file),
            ("|", None),
            ("Cut", self.cut),
            ("Copy", self.copy),
            ("Paste", self.paste),
            ("|", None),
            ("Find", self.show_find),
            ("Replace", self.show_replace),
            ("|", None),
            ("Run (F5)", self.run_code),
        ]

        for text, cmd in buttons:
            if text == "|":
                tk.Label(self.toolbar, text="|", bg="#141414", fg="#333333",
                        font=("Consolas", 14)).pack(side=tk.LEFT, padx=2)
            else:
                btn = tk.Button(self.toolbar, text=text, bg="#141414", fg="#888888",
                               font=("Consolas", 9), relief=tk.FLAT, cursor="hand2",
                               command=cmd)
                btn.pack(side=tk.LEFT, padx=1)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1e1e1e", fg="#f0c040"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#141414", fg="#888888"))
                # Store reference for debugging
                if "Run" in text:
                    self.run_btn = btn

        # Sidebar toggle button
        self.sidebar_btn = tk.Button(self.toolbar, text="Files", bg="#141414", fg="#888888",
                                      font=("Consolas", 9), relief=tk.FLAT, cursor="hand2",
                                      command=self.toggle_sidebar)
        self.sidebar_btn.pack(side=tk.LEFT, padx=1)
        self.sidebar_btn.bind("<Enter>", lambda e: self.sidebar_btn.config(bg="#1e1e1e", fg="#f0c040"))
        self.sidebar_btn.bind("<Leave>", lambda e: self.sidebar_btn.config(bg="#141414", fg="#888888"))

        # TEST: Go to Error button
        self.test_goto_btn = tk.Button(self.toolbar, text="GO TO ERROR", bg="#e74c3c", fg="#ffffff",
                                        font=("Consolas", 9, "bold"), relief=tk.FLAT, cursor="hand2",
                                        command=self._test_goto)
        self.test_goto_btn.pack(side=tk.LEFT, padx=10)
        self.test_goto_btn.bind("<Enter>", lambda e: self.test_goto_btn.config(bg="#c0392b"))
        self.test_goto_btn.bind("<Leave>", lambda e: self.test_goto_btn.config(bg="#e74c3c"))

        tk.Label(self.toolbar, text="Theme:", bg="#141414", fg="#888888",
                font=("Consolas", 9)).pack(side=tk.RIGHT, padx=5)

        self.theme_var = tk.StringVar(value="taqua")
        theme_combo = ttk.Combobox(self.toolbar, textvariable=self.theme_var,
                                  values=list(THEMES.keys()), width=12, state="readonly")
        theme_combo.pack(side=tk.RIGHT, padx=5)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.switch_theme(self.theme_var.get()))

        tk.Label(self.toolbar, text="Zoom:", bg="#141414", fg="#888888",
                font=("Consolas", 9)).pack(side=tk.RIGHT, padx=5)

        zoom_out_btn = tk.Button(self.toolbar, text="-", bg="#141414", fg="#888888",
                                font=("Consolas", 12, "bold"), relief=tk.FLAT,
                                command=self.zoom_out, width=2, cursor="hand2")
        zoom_out_btn.pack(side=tk.RIGHT, padx=1)
        zoom_out_btn.bind("<Enter>", lambda e: zoom_out_btn.config(bg="#1e1e1e", fg="#f0c040"))
        zoom_out_btn.bind("<Leave>", lambda e: zoom_out_btn.config(bg="#141414", fg="#888888"))

        self.zoom_label = tk.Label(self.toolbar, text="13pt", bg="#141414", fg="#666666",
                                  font=("Consolas", 10))
        self.zoom_label.pack(side=tk.RIGHT, padx=5)

        zoom_in_btn = tk.Button(self.toolbar, text="+", bg="#141414", fg="#888888",
                               font=("Consolas", 12, "bold"), relief=tk.FLAT,
                               command=self.zoom_in, width=2, cursor="hand2")
        zoom_in_btn.pack(side=tk.RIGHT, padx=1)
        zoom_in_btn.bind("<Enter>", lambda e: zoom_in_btn.config(bg="#1e1e1e", fg="#f0c040"))
        zoom_in_btn.bind("<Leave>", lambda e: zoom_in_btn.config(bg="#141414", fg="#888888"))

    def create_main_area(self):
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.tab_frame = tk.Frame(self.main_frame, height=32, bg="#0f0f0f")
        self.tab_frame.pack(fill=tk.X, side=tk.TOP)
        self.tab_frame.pack_propagate(False)

        # Content area: sidebar + editor/output
        self.content_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar (file explorer) - created but NOT packed yet
        self.sidebar_frame = tk.Frame(self.content_frame, width=220, bg="#141414")
        self.sidebar_frame.pack_propagate(False)
        self._build_sidebar_content()

        # Right side: Vertical PanedWindow for editor + output
        self.paned = tk.PanedWindow(self.content_frame, orient=tk.VERTICAL, 
                                    bg="#1a1a1a", sashwidth=4, sashrelief=tk.FLAT)
        self.paned.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Editor container (top pane)
        self.editor_container = tk.Frame(self.paned, bg="#1a1a1a")
        self.paned.add(self.editor_container, minsize=200)

        self.line_canvas = tk.Canvas(self.editor_container, width=50, bg="#1e1e1e",
                                     highlightthickness=0)
        self.line_canvas.pack(side=tk.LEFT, fill=tk.Y)

        self.editor_frame = tk.Frame(self.editor_container, bg="#1a1a1a")
        self.editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.editor = tk.Text(
            self.editor_frame,
            wrap=tk.NONE,
            undo=True,
            maxundo=100,
            font=(self.font_family, self.font_size),
            padx=12,
            pady=8,
            borderwidth=0,
            highlightthickness=0,
            spacing1=2,
            spacing3=2,
            tabs="    ",
            blockcursor=False,
            insertwidth=2,
            insertofftime=500,
            insertontime=500,
        )
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scroll = tk.Scrollbar(self.editor_frame, orient=tk.VERTICAL,
                                     command=self.on_scroll)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.h_scroll = tk.Scrollbar(self.editor_container, orient=tk.HORIZONTAL,
                                     command=self.editor.xview)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.editor.config(yscrollcommand=self.sync_scroll,
                          xscrollcommand=self.h_scroll.set)

        self.search_frame = tk.Frame(self.main_frame, height=40, bg="#141414")

    def _build_sidebar_content(self):
        theme = THEMES[self.current_theme]

        # Header
        header = tk.Frame(self.sidebar_frame, height=32, bg=theme["bg_sidebar"])
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        tk.Label(header, text="  FILES", bg=theme["bg_sidebar"], fg=theme["accent"],
                font=("Consolas", 9, "bold")).pack(side=tk.LEFT, padx=5)

        tk.Button(header, text="[X]", bg=theme["bg_sidebar"], fg=theme["fg_dim"],
                 font=("Consolas", 10), relief=tk.FLAT, command=self.toggle_sidebar,
                 cursor="hand2").pack(side=tk.RIGHT, padx=5)

        # Path label
        self.sidebar_path_label = tk.Label(self.sidebar_frame, text="", 
                                           bg=theme["bg_sidebar"], fg=theme["fg_dim"],
                                           font=("Consolas", 8), wraplength=200)
        self.sidebar_path_label.pack(fill=tk.X, padx=8, pady=(4, 0))

        # File list
        self.file_listbox = tk.Listbox(self.sidebar_frame, bg=theme["bg_sidebar"],
                                       fg=theme["fg"], font=("Consolas", 10),
                                       borderwidth=0, highlightthickness=0,
                                       selectbackground=theme["accent"],
                                       selectforeground=theme["sel_fg"],
                                       activestyle="none")
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.file_listbox.bind("<Double-Button-1>", self._on_file_select)
        self.file_listbox.bind("<Return>", self._on_file_select)

        # Refresh button at bottom
        refresh_btn = tk.Button(self.sidebar_frame, text="Refresh", bg=theme["bg_sidebar"],
                               fg=theme["fg_dim"], font=("Consolas", 9),
                               relief=tk.FLAT, command=self._refresh_sidebar,
                               cursor="hand2")
        refresh_btn.pack(fill=tk.X, padx=8, pady=4)

    def _refresh_sidebar(self):
        self.file_listbox.delete(0, tk.END)

        # Use file's folder if available, otherwise current working directory
        if self.file_path:
            folder = os.path.dirname(self.file_path)
        else:
            folder = os.getcwd()

        self.sidebar_path_label.config(text=folder)

        try:
            files = sorted(os.listdir(folder))
            py_files = [f for f in files if f.endswith('.py')]
            other_files = [f for f in files if not f.endswith('.py') and os.path.isfile(os.path.join(folder, f))]

            if not py_files and not other_files:
                self.file_listbox.insert(tk.END, "  (empty folder)")
                return

            for f in py_files:
                self.file_listbox.insert(tk.END, f"  {f}")
                # Highlight current file
                if os.path.join(folder, f) == self.file_path:
                    idx = self.file_listbox.size() - 1
                    self.file_listbox.itemconfig(idx, fg=THEMES[self.current_theme]["accent"])
                    self.file_listbox.selection_set(idx)

            if other_files:
                self.file_listbox.insert(tk.END, "")
                self.file_listbox.insert(tk.END, "  --- Other Files ---")
                for f in other_files:
                    self.file_listbox.insert(tk.END, f"  {f}")

        except Exception as e:
            self.file_listbox.insert(tk.END, f"  Error: {e}")

    def _on_file_select(self, event=None):
        selection = self.file_listbox.curselection()
        if not selection:
            return

        filename = self.file_listbox.get(selection[0]).strip()
        if filename.startswith("---") or filename.startswith("(") or filename.startswith("Error"):
            return

        # Use file's folder if available, otherwise current working directory
        if self.file_path:
            folder = os.path.dirname(self.file_path)
        else:
            folder = os.getcwd()

        filepath = os.path.join(folder, filename)

        if os.path.isfile(filepath):
            self._load_file(filepath)

    def _load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", content)
            self.file_path = path
            self.modified = False
            self.update_tab_title()
            self.status_left.config(text=f"  Opened: {os.path.basename(path)}")
            self.highlight_visible()
            self.update_line_numbers()
            self._refresh_sidebar()  # Refresh to update selection highlight
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def create_statusbar(self):
        self.status_frame = tk.Frame(self.root, height=26, bg="#0f0f0f")
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)

        self.status_left = tk.Label(self.status_frame, text="  Ready",
                                    bg="#0f0f0f", fg="#666666",
                                    font=("Consolas", 9))
        self.status_left.pack(side=tk.LEFT)

        self.status_right = tk.Label(self.status_frame,
                                     text="Ln 1, Col 1  |  UTF-8  |  Python  |  Taqua",
                                     bg="#0f0f0f", fg="#666666",
                                     font=("Consolas", 9))
        self.status_right.pack(side=tk.RIGHT, padx=10)

    def create_output_panel(self):
        # Create output frame but DON'T pack it - managed by PanedWindow
        self.output_frame = tk.Frame(self.paned, height=200, bg="#0a0a0a")
        self.output_frame.pack_propagate(False)

        # Setup read-only behavior without DISABLED state
        self.root.after(100, self._setup_output_readonly)

        output_header = tk.Frame(self.output_frame, height=28, bg="#141414")
        output_header.pack(fill=tk.X, side=tk.TOP)
        output_header.pack_propagate(False)

        tk.Label(output_header, text=">>> OUTPUT", bg="#141414", fg="#f0c040",
                font=("Consolas", 9, "bold")).pack(side=tk.LEFT, padx=10)

        tk.Button(output_header, text="[X]", bg="#141414", fg="#666666",
                 font=("Consolas", 10), relief=tk.FLAT, command=self.toggle_output,
                 cursor="hand2").pack(side=tk.RIGHT, padx=5)

        tk.Button(output_header, text="[Copy]", bg="#141414", fg="#666666",
                 font=("Consolas", 9), relief=tk.FLAT, command=self.copy_output,
                 cursor="hand2").pack(side=tk.RIGHT, padx=5)

        tk.Button(output_header, text="[Clear]", bg="#141414", fg="#666666",
                 font=("Consolas", 9), relief=tk.FLAT, command=self.clear_output,
                 cursor="hand2").pack(side=tk.RIGHT, padx=5)

        self.goto_error_btn = tk.Button(output_header, text="[Go to Error]", bg="#141414", fg="#f0c040",
                                       font=("Consolas", 9), relief=tk.FLAT, command=self._goto_last_error,
                                       cursor="hand2")
        self.goto_error_btn.pack(side=tk.RIGHT, padx=5)
        self.goto_error_btn.pack_forget()  # Hidden by default

        self.output_text = tk.Text(
            self.output_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            padx=10,
            pady=5,
            borderwidth=0,
            highlightthickness=0,
            state=tk.DISABLED,
            spacing1=1,
            spacing3=1,
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def _auto_pair(self, open_char, close_char):
        """Insert opening char + closing char and place cursor between them"""
        self.editor.insert(tk.INSERT, open_char + close_char)
        pos = self.editor.index(tk.INSERT)
        # Move cursor back one character (between the pair)
        line, col = pos.split(".")
        self.editor.mark_set(tk.INSERT, f"{line}.{int(col) - 1}")
        self.on_key_release()
        return "break"

    def _skip_closing(self, char):
        """If next char is the closing bracket/quote, just move cursor past it"""
        pos = self.editor.index(tk.INSERT)
        next_char = self.editor.get(pos, f"{pos} + 1c")
        if next_char == char:
            line, col = pos.split(".")
            self.editor.mark_set(tk.INSERT, f"{line}.{int(col) + 1}")
            self.on_key_release()
            return "break"
        return None  # Let normal character insertion happen

    def highlight_matching_bracket(self):
        """Highlight the matching bracket when cursor is on one"""
        theme = THEMES[self.current_theme]

        # Remove old bracket highlights
        self.editor.tag_remove("matching_bracket", "1.0", tk.END)
        self.editor.tag_config("matching_bracket", 
                               background=theme["accent"], 
                               foreground=theme["sel_fg"])

        pos = self.editor.index(tk.INSERT)
        char = self.editor.get(pos, f"{pos} + 1c")

        brackets = {"(": ")", "[": "]", "{": "}", ")": "(", "]": "[", "}": "{"}

        if char in brackets:
            # Find matching bracket
            open_char = char if char in "([{" else brackets[char]
            close_char = brackets[char] if char in "([{" else char

            if char in "([{":  # Opening bracket - search forward
                match_pos = self._find_matching_bracket(pos, open_char, close_char, 1)
            else:  # Closing bracket - search backward
                match_pos = self._find_matching_bracket(pos, close_char, open_char, -1)

            if match_pos:
                self.editor.tag_add("matching_bracket", pos, f"{pos} + 1c")
                self.editor.tag_add("matching_bracket", match_pos, f"{match_pos} + 1c")

    def _find_matching_bracket(self, start_pos, open_char, close_char, direction):
        """Find matching bracket with proper nesting"""
        content = self.editor.get("1.0", tk.END)
        start_idx = self.editor.count("1.0", start_pos, "chars")[0]

        if direction == 1:
            search_text = content[start_idx + 1:]
        else:
            search_text = content[:start_idx][::-1]
            # Swap open/close for reversed search
            open_char, close_char = close_char, open_char

        depth = 1
        for i, c in enumerate(search_text):
            if c == open_char:
                depth += 1
            elif c == close_char:
                depth -= 1
                if depth == 0:
                    if direction == 1:
                        match_idx = start_idx + 1 + i
                    else:
                        match_idx = start_idx - 1 - i
                    # Convert char index back to text index
                    line = 1
                    col = 0
                    for j, ch in enumerate(content):
                        if j == match_idx:
                            return f"{line}.{col}"
                        if ch == '\n':
                            line += 1
                            col = 0
                        else:
                            col += 1
        return None

    def _on_drop(self, event):
        """Handle drag and drop of files"""
        files = self.root.tk.splitlist(event.data)
        for f in files:
            if f.endswith('.py'):
                self._load_file_and_track(f)
                break  # Open first .py file only

    def duplicate_line(self, event=None):
        """Duplicate current line or selected lines"""
        try:
            sel_start = self.editor.index(tk.SEL_FIRST)
            sel_end = self.editor.index(tk.SEL_LAST)
            text = self.editor.get(sel_start, sel_end)
            self.editor.insert(sel_end, "\n" + text)
        except tk.TclError:
            # No selection - duplicate current line
            pos = self.editor.index(tk.INSERT)
            line = int(pos.split(".")[0])
            line_text = self.editor.get(f"{line}.0", f"{line}.end")
            self.editor.insert(f"{line}.end", "\n" + line_text)

        self.modified = True
        self.update_tab_title()
        self.on_key_release()
        return "break"
    def toggle_fold(self, event=None):
        """Toggle fold/unfold at current line"""
        pos = self.editor.index(tk.INSERT)
        line = int(pos.split(".")[0])

        # Check if already folded
        if line in self.folded_regions:
            self._unfold(line)
            return "break"

        # Find foldable region
        line_text = self.editor.get(f"{line}.0", f"{line}.end")
        stripped = line_text.strip()

        # Check if line starts a block
        if not (stripped.endswith(":") or stripped.startswith(("def ", "class ", "if ", "for ", "while ", "with ", "try"))):
            return None

        # Find end of block (next line at same or less indentation)
        indent = len(line_text) - len(line_text.lstrip())
        total_lines = int(self.editor.index("end-1c").split(".")[0])

        end_line = line + 1
        for i in range(line + 1, total_lines + 1):
            next_text = self.editor.get(f"{i}.0", f"{i}.end")
            if next_text.strip():
                next_indent = len(next_text) - len(next_text.lstrip())
                if next_indent <= indent and not next_text.strip().startswith("#"):
                    end_line = i
                    break
        else:
            end_line = total_lines

        self._fold(line, end_line)
        return "break"

    def _fold(self, start, end):
        """Fold (hide) lines from start to end"""
        self.editor.tag_add(f"fold_{start}", f"{start + 1}.0", f"{end}.0")
        self.editor.tag_config(f"fold_{start}", elide=True)
        self.folded_regions[start] = end

        # Add fold indicator
        self.editor.tag_add("fold_marker", f"{start}.0", f"{start}.end")
        self.editor.tag_config("fold_marker", foreground=THEMES[self.current_theme]["accent"])

        self.update_line_numbers()

    def _unfold(self, start):
        """Unfold (show) lines from start"""
        if start in self.folded_regions:
            self.editor.tag_remove(f"fold_{start}", "1.0", tk.END)
            del self.folded_regions[start]
            self.editor.tag_remove("fold_marker", f"{start}.0", f"{start}.end")
            self.update_line_numbers()

    def _get_completions(self, prefix):
        """Get completion suggestions for a prefix - fast, cached, no module imports"""
        import keyword as kw
        import builtins

        builtins_list = [b for b in dir(builtins) if not b.startswith('_')]
        keywords_list = kw.kwlist

        # Get words from current file content
        content = self.editor.get("1.0", tk.END)
        import re
        file_words = set(re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*', content))

        # Get installed modules from cache (no slow importing!)
        installed = self._load_module_cache()

        all_words = set(builtins_list + keywords_list + list(file_words) + list(installed))
        matches = [w for w in all_words if w.lower().startswith(prefix.lower()) and w != prefix]
        return sorted(matches)[:20]  # Limit to 20 suggestions

    def _load_module_cache(self):
        """Load cached module list from file - instant, no imports"""
        if hasattr(self, '_module_cache'):
            return self._module_cache

        cache_file = os.path.join(os.path.expanduser("~"), ".taqua_modules_cache.txt")

        # Try to load from cache file
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self._module_cache = set(line.strip() for line in f if line.strip())
                return self._module_cache
            except:
                pass

        # Default common libraries (no scanning, no importing)
        self._module_cache = {
            'numpy', 'pandas', 'matplotlib', 'seaborn', 'scipy', 'sklearn',
            'requests', 'flask', 'django', 'fastapi', 'sqlalchemy', 'pillow',
            'opencv', 'cv2', 'tensorflow', 'torch', 'keras', 'pygame', 'kivy',
            'ttkbootstrap', 'customtkinter', 'openpyxl', 'xlsxwriter',
            'beautifulsoup4', 'bs4', 'selenium', 'pytest', 'unittest', 'mock',
            'json', 'csv', 'sqlite3', 'hashlib', 'datetime', 'collections',
            'itertools', 'functools', 'math', 'random', 'statistics', 'string',
            're', 'os', 'sys', 'pathlib', 'shutil', 'glob', 'tempfile',
            'urllib', 'http', 'ftplib', 'smtplib', 'email', 'xml', 'html',
            'socket', 'ssl', 'threading', 'multiprocessing', 'subprocess',
            'argparse', 'configparser', 'logging', 'pickle', 'copy', 'typing',
            'enum', 'dataclasses', 'abc', 'inspect', 'types', 'weakref',
            'contextlib', 'operator', 'numbers', 'fractions',
            'decimal', 'zoneinfo', 'calendar', 'time', 'uuid', 'secrets',
            'hmac', 'base64', 'binascii', 'struct', 'codecs', 'io', 'warnings',
            'traceback', 'linecache', 'pprint', 'reprlib', 'textwrap',
            'stringprep', 'rlcompleter', 'site', 'sysconfig', 'platform',
            'tkinter', 'ttk', 'messagebox', 'filedialog'
        }
        return self._module_cache

    def _clear_module_cache(self):
        """Clear the module cache file"""
        cache_file = os.path.join(os.path.expanduser("~"), ".taqua_modules_cache.txt")
        try:
            if os.path.exists(cache_file):
                os.remove(cache_file)
            if hasattr(self, '_module_cache'):
                delattr(self, '_module_cache')
            self.status_left.config(text="  Module cache cleared")
        except Exception as e:
            self.status_left.config(text=f"  Clear error: {e}")

    def scan_installed_modules(self):
        """Scan all installed modules and save to cache - call from menu when desired"""
        import pkgutil

        self.status_left.config(text="  Scanning installed modules...")
        self.root.update_idletasks()

        modules = set()
        try:
            # Fast scan - just list module names, NO importing
            for importer, modname, ispkg in pkgutil.iter_modules():
                modules.add(modname)
                # Add common subpackage patterns without importing
                if ispkg:
                    common_subs = ['core', 'utils', 'api', 'data', 'io', 'types', 'models']
                    for sub in common_subs:
                        modules.add(f"{modname}.{sub}")
        except Exception as e:
            self.status_left.config(text=f"  Scan error: {e}")
            return

        # Save to cache file
        cache_file = os.path.join(os.path.expanduser("~"), ".taqua_modules_cache.txt")
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                for mod in sorted(modules):
                    f.write(mod + '\n')
        except Exception as e:
            self.status_left.config(text=f"  Cache save error: {e}")
            return

        # Clear memory cache so next autocomplete uses new data
        if hasattr(self, '_module_cache'):
            delattr(self, '_module_cache')

        self.status_left.config(text=f"  Scanned {len(modules)} modules - cached!")
        messagebox.showinfo("Module Scan", f"Found and cached {len(modules)} installed modules.\nAutocompletes will now include all your libraries!")

    def show_autocomplete(self, event=None):
        """Show autocomplete dropdown"""
        if self.autocomplete_box:
            self.hide_autocomplete()

        pos = self.editor.index(tk.INSERT)
        line, col = pos.split(".")

        # Get word prefix before cursor
        line_text = self.editor.get(f"{line}.0", pos)
        import re
        match = re.search(r'([a-zA-Z_][a-zA-Z_0-9]*)$', line_text)
        if not match:
            return

        prefix = match.group(1)
        if len(prefix) < 2:
            return

        completions = self._get_completions(prefix)
        if not completions:
            return

        theme = THEMES[self.current_theme]

        # Create popup
        self.autocomplete_box = tk.Listbox(
            self.root, 
            bg=theme["bg_sidebar"], 
            fg=theme["fg"],
            font=(self.font_family, self.font_size),
            borderwidth=1, 
            highlightthickness=1,
            highlightcolor=theme["accent"],
            selectbackground=theme["accent"],
            selectforeground=theme["sel_fg"],
            activestyle="none",
            height=min(len(completions), 8)
        )

        for c in completions:
            self.autocomplete_box.insert(tk.END, c)

        # Position popup below cursor
        bbox = self.editor.bbox(pos)
        if bbox:
            x = bbox[0] + self.editor.winfo_rootx()
            y = bbox[1] + bbox[3] + self.editor.winfo_rooty()
            self.autocomplete_box.place(x=x, y=y)

        self.autocomplete_box.bind("<Return>", self._accept_completion)
        self.autocomplete_box.bind("<Tab>", self._accept_completion)
        self.autocomplete_box.bind("<Escape>", lambda e: self.hide_autocomplete())
        self.autocomplete_box.bind("<Double-Button-1>", self._accept_completion)
        self.autocomplete_box.bind("<Up>", lambda e: self._navigate_autocomplete(-1))
        self.autocomplete_box.bind("<Down>", lambda e: self._navigate_autocomplete(1))
        # Don't steal focus - let user keep typing normally
        # self.autocomplete_box.focus()

    def _accept_completion(self, event=None):
        """Insert selected completion"""
        if not self.autocomplete_box:
            return "break" if event else None

        selection = self.autocomplete_box.curselection()
        if not selection:
            # If nothing selected but user pressed Tab/Enter, just close popup and continue
            self.hide_autocomplete()
            return "break" if event else None

        completion = self.autocomplete_box.get(selection[0])
        pos = self.editor.index(tk.INSERT)
        line, col = pos.split(".")

        # Get prefix length to replace
        line_text = self.editor.get(f"{line}.0", pos)
        import re
        match = re.search(r'([a-zA-Z_][a-zA-Z_0-9]*)$', line_text)
        if match:
            prefix_len = len(match.group(1))
            start = f"{line}.{int(col) - prefix_len}"
            self.editor.delete(start, pos)
            self.editor.insert(start, completion)

        self.hide_autocomplete()
        self.editor.focus()
        self.on_key_release()
        return "break"

    def hide_autocomplete(self):
        """Hide autocomplete dropdown"""
        if self.autocomplete_box:
            self.autocomplete_box.destroy()
            self.autocomplete_box = None

    def _navigate_autocomplete(self, direction):
        """Navigate autocomplete list with arrow keys"""
        if not self.autocomplete_box:
            return
        selection = self.autocomplete_box.curselection()
        if not selection:
            idx = 0 if direction > 0 else self.autocomplete_box.size() - 1
        else:
            idx = selection[0] + direction
        if 0 <= idx < self.autocomplete_box.size():
            self.autocomplete_box.selection_clear(0, tk.END)
            self.autocomplete_box.selection_set(idx)
            self.autocomplete_box.see(idx)
        return "break"

    def add_multi_cursor(self, event):
        """Add a multi-cursor position with Ctrl+Click"""
        pos = self.editor.index(f"@{event.x},{event.y}")
        line, col = pos.split(".")
        self.multi_cursors.append((int(line), int(col)))
        self._draw_multi_cursors()
        return "break"

    def clear_multi_cursors(self):
        """Clear all multi-cursors"""
        self.multi_cursors = []
        self.editor.tag_remove("multi_cursor", "1.0", tk.END)

    def _draw_multi_cursors(self):
        """Draw visual indicators for multi-cursors"""
        self.editor.tag_remove("multi_cursor", "1.0", tk.END)
        theme = THEMES[self.current_theme]
        self.editor.tag_config("multi_cursor", background=theme["accent2"])
        for line, col in self.multi_cursors:
            self.editor.tag_add("multi_cursor", f"{line}.{col}", f"{line}.{col + 1}")

    def multi_type(self, event):
        """Type at all multi-cursor positions simultaneously"""
        if not self.multi_cursors or event.keysym in ['Shift', 'Control', 'Alt', 'Caps_Lock',
                                                        'Left', 'Right', 'Up', 'Down', 'Return',
                                                        'Tab', 'BackSpace', 'Delete', 'Escape']:
            return None

        char = event.char
        if not char:
            return None

        # Sort cursors bottom-to-top so insertions don't shift positions
        sorted_cursors = sorted(self.multi_cursors, key=lambda x: (x[0], x[1]), reverse=True)

        for line, col in sorted_cursors:
            self.editor.insert(f"{line}.{col}", char)

        # Update all cursor positions
        new_cursors = []
        for line, col in self.multi_cursors:
            new_cursors.append((line, col + 1))
        self.multi_cursors = new_cursors
        self._draw_multi_cursors()

        self.modified = True
        self.update_tab_title()
        self.on_key_release()
        return "break"

    def toggle_bookmark(self, event=None):
        """Toggle bookmark on current line"""
        pos = self.editor.index(tk.INSERT)
        line = int(pos.split(".")[0])

        if line in self.bookmarks:
            self.bookmarks.remove(line)
        else:
            self.bookmarks.add(line)

        self.update_line_numbers()
        self.status_left.config(text=f"  Bookmark: line {line} ({len(self.bookmarks)} total)")
        return "break"

    def next_bookmark(self, event=None):
        """Jump to next bookmark"""
        if not self.bookmarks:
            return
        pos = self.editor.index(tk.INSERT)
        current = int(pos.split(".")[0])

        next_lines = [b for b in self.bookmarks if b > current]
        if next_lines:
            target = min(next_lines)
        else:
            target = min(self.bookmarks)

        self.editor.see(f"{target}.0")
        self.editor.mark_set(tk.INSERT, f"{target}.0")
        self.update_line_numbers()
        self.update_status()
        self.highlight_visible()
        return "break"

    def prev_bookmark(self, event=None):
        """Jump to previous bookmark"""
        if not self.bookmarks:
            return
        pos = self.editor.index(tk.INSERT)
        current = int(pos.split(".")[0])

        prev_lines = [b for b in self.bookmarks if b < current]
        if prev_lines:
            target = max(prev_lines)
        else:
            target = max(self.bookmarks)

        self.editor.see(f"{target}.0")
        self.editor.mark_set(tk.INSERT, f"{target}.0")
        self.update_line_numbers()
        self.update_status()
        self.highlight_visible()
        return "break"

    def show_context_menu(self, event):
        """Show right-click context menu"""
        theme = THEMES[self.current_theme]
        menu = tk.Menu(self.root, tearoff=0, bg=theme["bg_sidebar"], fg=theme["fg"],
                      activebackground=theme["accent"], activeforeground=theme["sel_fg"],
                      font=("Consolas", 10))

        # Check if text is selected
        try:
            self.editor.index(tk.SEL_FIRST)
            has_selection = True
        except tk.TclError:
            has_selection = False

        menu.add_command(label="Cut          Ctrl+X", command=self.cut)
        menu.add_command(label="Copy         Ctrl+C", command=self.copy)
        menu.add_command(label="Paste        Ctrl+V", command=self.paste)
        menu.add_command(label="Select All   Ctrl+A", command=self.select_all)
        menu.add_separator()
        menu.add_command(label="Duplicate    Ctrl+D", command=self.duplicate_line)
        menu.add_command(label="Toggle Comment  Ctrl+Slash", command=self.toggle_comment)
        menu.add_separator()
        menu.add_command(label="Find         Ctrl+F", command=self.show_find)
        menu.add_command(label="Go to Line   Ctrl+G", command=self.show_goto_line)
        menu.add_separator()
        menu.add_command(label="Run          F5", command=self.run_code)
        menu.add_command(label="Run Selection  F6", command=self.run_selection)

        menu.tk_popup(event.x_root, event.y_root)

    def bind_events(self):
        self.editor.bind("<KeyRelease>", self.on_key_release)
        self.editor.bind("<ButtonRelease-1>", self.on_click)
        self.editor.bind("<Control-Button-1>", self.add_multi_cursor)
        self.editor.bind("<Button-3>", self.show_context_menu)
        self.root.bind_all("<Control-MouseWheel>", self.zoom_scroll)
        self.root.bind_all("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind_all("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind_all("<Control-0>", lambda e: self.reset_zoom())
        self.root.bind_all("<Control-n>", lambda e: self.new_file())
        self.root.bind_all("<Control-o>", lambda e: self.open_file())
        self.root.bind_all("<Control-s>", lambda e: self.save_file())
        self.root.bind_all("<Control-S>", lambda e: self.save_as())
        self.root.bind_all("<Control-f>", lambda e: self.show_find())
        self.root.bind_all("<Control-Shift-F>", lambda e: self.search_in_files())
        self.root.bind_all("<Control-b>", lambda e: self.toggle_bookmark())
        self.root.bind_all("<F2>", lambda e: self.next_bookmark())
        self.root.bind_all("<Control-Shift-j>", lambda e: self.format_json())
        self.root.bind_all("<Control-Shift-e>", lambda e: self._goto_last_error())

        # Also bind to output panel specifically (in case focus is there)
        self.output_text.bind("<Control-Shift-e>", lambda e: self._goto_last_error())
        self.output_text.bind("<Double-Button-1>", lambda e: self._goto_last_error())
        self.root.bind_all("<Shift-F2>", lambda e: self.prev_bookmark())
        self.root.bind_all("<Control-h>", lambda e: self.show_replace())
        self.root.bind_all("<Control-g>", lambda e: self.show_goto_line())
        self.root.bind_all("<Control-Shift-l>", lambda e: self.toggle_fold())
        self.root.bind_all("<Alt-z>", lambda e: self.toggle_word_wrap())
        self.root.bind_all("<F11>", lambda e: self.toggle_zen_mode())
        self.root.bind_all("<Control-d>", lambda e: self.duplicate_line())

        # Drag and drop support (Windows)
        try:
            self.root.drop_target_register(tk.DND_FILES)
            self.root.dnd_bind('<<Drop>>', self._on_drop)
        except:
            pass
        self.root.bind_all("<F5>", lambda e: self.run_code())
        self.root.bind_all("<F6>", lambda e: self.run_selection())
        self.root.bind_all("<F3>", lambda e: self.toggle_sidebar())
        self.root.bind_all("<F4>", lambda e: self.toggle_output())
        self.root.bind_all("<Control-z>", lambda e: self.undo())
        self.root.bind_all("<Control-y>", lambda e: self.redo())
        self.root.bind_all("<Control-x>", lambda e: self.cut())
        self.root.bind_all("<Control-c>", lambda e: self.copy())
        self.root.bind_all("<Control-v>", lambda e: self.paste())
        self.editor.bind("<Tab>", self.on_tab)
        self.editor.bind("<Return>", self.on_return)
        self.editor.bind("<BackSpace>", self.on_backspace)
        self.root.bind_all("<Control-a>", lambda e: self.select_all())
        self.root.bind_all("<Control-slash>", lambda e: self.toggle_comment())

        # Auto-pair brackets and quotes
        self.editor.bind("(", lambda e: self._auto_pair("(", ")"))
        self.editor.bind(")", lambda e: self._skip_closing(")"))
        self.editor.bind("[", lambda e: self._auto_pair("[", "]"))
        self.editor.bind("]", lambda e: self._skip_closing("]"))
        self.editor.bind("{", lambda e: self._auto_pair("{", "}"))
        self.editor.bind("}", lambda e: self._skip_closing("}"))
        self.editor.bind('"', lambda e: self._auto_pair('"', '"'))
        self.editor.bind("'", lambda e: self._auto_pair("'", "'"))

    def on_scroll(self, *args):
        self.editor.yview(*args)
        self.update_line_numbers()

    def sync_scroll(self, first, last):
        self.v_scroll.set(first, last)
        self.update_line_numbers()

    def update_line_numbers(self):
        self.line_canvas.delete("all")
        theme = THEMES[self.current_theme]

        first = self.editor.index("@0,0")
        last = self.editor.index("@0,%d" % self.editor.winfo_height())

        first_line = int(first.split(".")[0])
        last_line = int(last.split(".")[0]) + 1
        cursor_line = int(self.editor.index(tk.INSERT).split(".")[0])
        total_lines = int(self.editor.index("end-1c").split(".")[0])
        last_line = min(last_line, total_lines)

        for i in range(first_line, last_line + 1):
            y = self.editor.dlineinfo("%d.0" % i)
            if y:
                y_pos = y[1] + 2
                color = theme["accent"] if i == cursor_line else theme["line_fg"]
                weight = "bold" if i == cursor_line else "normal"

                # Draw bookmark indicator
                if i in self.bookmarks:
                    self.line_canvas.create_text(
                        8, y_pos, text="●", anchor=tk.NW,
                        fill=theme["error"], font=("Consolas", self.font_size - 2, "bold")
                    )

                self.line_canvas.create_text(
                    45, y_pos, text=str(i), anchor=tk.NE,
                    fill=color, font=(self.font_family, self.font_size - 1, weight)
                )

                # Draw indentation guides
                line_text = self.editor.get(f"{i}.0", f"{i}.end")
                indent = len(line_text) - len(line_text.lstrip())
                tab_width = 4 * 7  # Approximate width of 4 spaces in Consolas
                for level in range(1, indent // 4 + 1):
                    x_pos = 50 + (level * tab_width)
                    self.line_canvas.create_line(
                        x_pos, y[1], x_pos, y[1] + y[3],
                        fill=theme["fg_dim"], width=1
                    )

    def on_key_release(self, event=None):
        self.update_line_numbers()
        self.update_status()
        self.highlight_visible()
        self.highlight_matching_bracket()

        # Handle multi-cursor typing
        if event and self.multi_cursors:
            result = self.multi_type(event)
            if result == "break":
                return

        # Show autocomplete after typing letters
        if event and event.char and event.char.isalpha():
            self.show_autocomplete()
        elif event and event.keysym in ['Escape', 'Return', 'Tab', 'space', 'BackSpace', 'Delete']:
            self.hide_autocomplete()
        elif event and event.char and not event.char.isalpha():
            # Any non-letter character (numbers, symbols, etc.) closes autocomplete
            self.hide_autocomplete()

        if event and event.keysym not in ['Shift', 'Control', 'Alt', 'Caps_Lock',
                                            'Left', 'Right', 'Up', 'Down']:
            self.modified = True
            self.update_tab_title()

    def on_click(self, event=None):
        self.clear_multi_cursors()
        self.update_line_numbers()
        self.update_status()
        self.highlight_matching_bracket()

    def update_status(self):
        pos = self.editor.index(tk.INSERT)
        line, col = pos.split(".")
        content = self.editor.get("1.0", "end-1c")
        lines = content.count('\n') + 1 if content else 1
        chars = len(content)
        self.status_right.config(
            text=f"Ln {line}, Col {int(col)+1}  |  {chars} chars  |  {lines} lines  |  {self.font_size}pt  |  {self.current_theme.upper()}"
        )

    def highlight_visible(self):
        theme = THEMES[self.current_theme]
        for tag in ["keyword", "string", "comment", "builtin", "number", 
                    "function", "decorator", "current_line"]:
            self.editor.tag_remove(tag, "1.0", tk.END)

        self.editor.tag_config("keyword", foreground=theme["keyword"])
        self.editor.tag_config("string", foreground=theme["string"])
        self.editor.tag_config("comment", foreground=theme["comment"])
        self.editor.tag_config("builtin", foreground=theme["builtin"])
        self.editor.tag_config("number", foreground=theme["number"])
        self.editor.tag_config("function", foreground=theme["function"])
        self.editor.tag_config("decorator", foreground=theme["decorator"])

        # Current line highlight
        self.editor.tag_config("current_line", background=theme["line_bg"])
        cursor_line = int(self.editor.index(tk.INSERT).split(".")[0])
        self.editor.tag_add("current_line", f"{cursor_line}.0", f"{cursor_line + 1}.0")

        # Rainbow brackets
        rainbow_colors = [theme["error"], theme["accent"], theme["success"], theme["builtin"], theme["number"]]
        bracket_pairs = {"(": ")", "[": "]", "{": "}"}

        for tag_name in [f"rb_{i}" for i in range(5)]:
            self.editor.tag_remove(tag_name, "1.0", tk.END)

        first = self.editor.index("@0,0")
        last = self.editor.index("@0,%d" % self.editor.winfo_height())
        first_line = int(first.split(".")[0])
        last_line = int(last.split(".")[0]) + 2
        start_idx = "%d.0" % first_line
        end_idx = "%d.0" % last_line
        text = self.editor.get(start_idx, end_idx)

        stack = []
        for i, char in enumerate(text):
            if char in bracket_pairs:
                depth = len(stack)
                color = rainbow_colors[depth % len(rainbow_colors)]
                tag = f"rb_{depth % len(rainbow_colors)}"
                self.editor.tag_config(tag, foreground=color, font=(self.font_family, self.font_size, "bold"))
                pos = f"{start_idx} + {i}c"
                self.editor.tag_add(tag, pos, f"{pos} + 1c")
                stack.append((char, depth))
            elif char in ")]}" and stack:
                for j, (open_char, depth) in enumerate(reversed(stack)):
                    if bracket_pairs.get(open_char) == char:
                        color = rainbow_colors[depth % len(rainbow_colors)]
                        tag = f"rb_{depth % len(rainbow_colors)}"
                        self.editor.tag_config(tag, foreground=color, font=(self.font_family, self.font_size, "bold"))
                        pos = f"{start_idx} + {i}c"
                        self.editor.tag_add(tag, pos, f"{pos} + 1c")
                        stack.pop(-(j+1))
                        break

        first = self.editor.index("@0,0")
        last = self.editor.index("@0,%d" % self.editor.winfo_height())
        first_line = int(first.split(".")[0])
        last_line = int(last.split(".")[0]) + 2
        start_idx = "%d.0" % first_line
        end_idx = "%d.0" % last_line
        text = self.editor.get(start_idx, end_idx)

        for pattern, tag_or_tags in RE_PATTERNS:
            if isinstance(tag_or_tags, list):
                for match in re.finditer(pattern, text, re.MULTILINE):
                    for i, tag in enumerate(tag_or_tags):
                        if i < len(match.groups()):
                            group_start = match.start(i + 1)
                            group_end = match.end(i + 1)
                            start = "%s + %dc" % (start_idx, group_start)
                            end = "%s + %dc" % (start_idx, group_end)
                            self.editor.tag_add(tag, start, end)
            else:
                tag = tag_or_tags
                for match in re.finditer(pattern, text, re.MULTILINE):
                    start = "%s + %dc" % (start_idx, match.start())
                    end = "%s + %dc" % (start_idx, match.end())
                    self.editor.tag_add(tag, start, end)

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        self.editor.config(
            bg=theme["bg"],
            fg=theme["fg"],
            selectbackground=theme["accent"],
            selectforeground=theme["sel_fg"],
            insertbackground=theme["cursor"],
        )
        self.line_canvas.config(bg=theme["line_bg"])
        self.output_text.config(bg=theme["output_bg"], fg=theme["output_fg"])
        self._apply_sidebar_theme()
        self.update_line_numbers()
        self.highlight_visible()

    def switch_theme(self, theme_name):
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.theme_var.set(theme_name)
            self.apply_theme()
            self.status_left.config(text=f"  Theme: {THEMES[theme_name]['name']}")
            self._save_settings()

    def zoom_in(self):
        if self.font_size < 72:
            self.font_size += 1
            self.update_font()
            self._save_settings()

    def zoom_out(self):
        if self.font_size > 6:
            self.font_size -= 1
            self.update_font()
            self._save_settings()

    def reset_zoom(self):
        self.font_size = 13
        self.update_font()
        self._save_settings()

    def zoom_scroll(self, event):
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def update_font(self):
        self.editor.config(font=(self.font_family, self.font_size))
        self.zoom_label.config(text=f"{self.font_size}pt")
        self.update_line_numbers()

    def show_goto_line(self):
        """Show dialog to jump to a specific line number"""
        # Create a simple popup
        popup = tk.Toplevel(self.root)
        popup.title("Go to Line")
        popup.geometry("250x100")
        popup.configure(bg="#1a1a1a")
        popup.transient(self.root)
        popup.grab_set()

        theme = THEMES[self.current_theme]
        popup.configure(bg=theme["bg"])

        tk.Label(popup, text="Line number:", bg=theme["bg"], fg=theme["fg"],
                font=("Consolas", 10)).pack(pady=(10, 5))

        entry = tk.Entry(popup, bg=theme["bg_sidebar"], fg=theme["fg"],
                        font=("Consolas", 12), relief=tk.FLAT, 
                        highlightthickness=1, highlightcolor=theme["accent"],
                        insertbackground=theme["cursor"], justify="center")
        entry.pack(padx=20, fill=tk.X)
        entry.focus()

        def do_goto(event=None):
            try:
                line_num = int(entry.get())
                total_lines = int(self.editor.index("end-1c").split(".")[0])
                if 1 <= line_num <= total_lines:
                    self.editor.see(f"{line_num}.0")
                    self.editor.mark_set(tk.INSERT, f"{line_num}.0")
                    self.update_line_numbers()
                    self.update_status()
                    self.highlight_visible()
                    self.highlight_matching_bracket()
                    popup.destroy()
                    self.editor.focus()
                else:
                    entry.configure(highlightcolor=theme["error"])
            except ValueError:
                entry.configure(highlightcolor=theme["error"])

        entry.bind("<Return>", do_goto)
        entry.bind("<Escape>", lambda e: popup.destroy())

        tk.Button(popup, text="Go", bg=theme["bg_sidebar"], fg=theme["accent"],
                 font=("Consolas", 10, "bold"), relief=tk.FLAT, 
                 command=do_goto, cursor="hand2").pack(pady=8)

    def format_json(self):
        """Format/Prettify JSON in editor"""
        try:
            import json
            text = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            is_selection = True
        except tk.TclError:
            text = self.editor.get("1.0", tk.END)
            is_selection = False

        try:
            data = json.loads(text)
            formatted = json.dumps(data, indent=4, ensure_ascii=False)

            if is_selection:
                self.editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
                self.editor.insert(tk.SEL_FIRST, formatted)
            else:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", formatted)

            self.modified = True
            self.update_tab_title()
            self.on_key_release()
            self.status_left.config(text="  JSON formatted")
        except Exception as e:
            self.status_left.config(text=f"  JSON error: {e}")

    def search_in_files(self):
        """Search across all .py files in current folder"""
        theme = THEMES[self.current_theme]

        popup = tk.Toplevel(self.root)
        popup.title("Search in Files")
        popup.geometry("500x400")
        popup.configure(bg=theme["bg"])
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(popup, text="Search:", bg=theme["bg"], fg=theme["fg"],
                font=("Consolas", 10)).pack(pady=(10, 5))

        entry = tk.Entry(popup, bg=theme["bg_sidebar"], fg=theme["fg"],
                        font=("Consolas", 11), relief=tk.FLAT,
                        highlightthickness=1, highlightcolor=theme["accent"],
                        insertbackground=theme["cursor"])
        entry.pack(padx=20, fill=tk.X)
        entry.focus()

        results_frame = tk.Frame(popup, bg=theme["bg"])
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        results_list = tk.Listbox(results_frame, bg=theme["bg_sidebar"], fg=theme["fg"],
                                  font=("Consolas", 9), borderwidth=0,
                                  highlightthickness=1, highlightcolor=theme["accent"],
                                  selectbackground=theme["accent"],
                                  selectforeground=theme["sel_fg"])
        results_list.pack(fill=tk.BOTH, expand=True)

        def do_search(event=None):
            query = entry.get()
            if not query:
                return

            results_list.delete(0, tk.END)

            folder = os.path.dirname(self.file_path) if self.file_path else os.getcwd()
            count = 0

            try:
                for filename in os.listdir(folder):
                    if filename.endswith('.py'):
                        filepath = os.path.join(folder, filename)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                            for i, line in enumerate(lines, 1):
                                if query.lower() in line.lower():
                                    display = f"{filename}:{i}: {line.strip()[:60]}"
                                    results_list.insert(tk.END, display)
                                    count += 1
                        except:
                            pass
            except Exception as e:
                results_list.insert(tk.END, f"Error: {e}")

            if count == 0:
                results_list.insert(tk.END, "No results found")
            else:
                results_list.insert(tk.END, f"--- {count} results ---")

        def open_result(event=None):
            selection = results_list.curselection()
            if not selection:
                return
            text = results_list.get(selection[0])
            if text.startswith("---") or text.startswith("Error") or text.startswith("No results"):
                return

            parts = text.split(":", 2)
            if len(parts) >= 2:
                filename = parts[0]
                line_num = parts[1]
                folder = os.path.dirname(self.file_path) if self.file_path else os.getcwd()
                filepath = os.path.join(folder, filename)
                if os.path.exists(filepath):
                    self._load_file_and_track(filepath)
                    self.editor.see(f"{line_num}.0")
                    self.editor.mark_set(tk.INSERT, f"{line_num}.0")
                    popup.destroy()
                    self.editor.focus()

        entry.bind("<Return>", do_search)
        results_list.bind("<Double-Button-1>", open_result)
        results_list.bind("<Return>", open_result)

        tk.Button(popup, text="Search", bg=theme["bg_sidebar"], fg=theme["accent"],
                 font=("Consolas", 10, "bold"), relief=tk.FLAT,
                 command=do_search, cursor="hand2").pack(pady=5)

    def show_find(self):
        self.search_frame.pack(fill=tk.X, side=tk.TOP, after=self.tab_frame)
        self.search_frame.pack_propagate(False)
        for widget in self.search_frame.winfo_children():
            widget.destroy()

        tk.Label(self.search_frame, text="Find:", bg="#141414", fg="#888888",
                font=("Consolas", 10)).pack(side=tk.LEFT, padx=10)

        self.find_entry = tk.Entry(self.search_frame, bg="#1a1a1a", fg="#e8e8e8",
                                  font=("Consolas", 11), relief=tk.FLAT,
                                  highlightthickness=1, highlightcolor="#f0c040",
                                  insertbackground="#f0c040")
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.find_entry.focus()

        tk.Button(self.search_frame, text="Find Next", bg="#1a1a1a", fg="#888888",
                 font=("Consolas", 9), relief=tk.FLAT, command=self.find_next,
                 cursor="hand2").pack(side=tk.LEFT, padx=2)

        tk.Button(self.search_frame, text="Find Prev", bg="#1a1a1a", fg="#888888",
                 font=("Consolas", 9), relief=tk.FLAT, command=self.find_prev,
                 cursor="hand2").pack(side=tk.LEFT, padx=2)

        tk.Button(self.search_frame, text="X", bg="#141414", fg="#666666",
                 font=("Consolas", 12), relief=tk.FLAT, command=self.hide_search,
                 cursor="hand2").pack(side=tk.RIGHT, padx=10)

        self.find_entry.bind("<Return>", lambda e: self.find_next())
        self.find_entry.bind("<Escape>", lambda e: self.hide_search())

    def show_replace(self):
        self.search_frame.pack(fill=tk.X, side=tk.TOP, after=self.tab_frame)
        self.search_frame.pack_propagate(False)
        self.search_frame.config(height=70)
        for widget in self.search_frame.winfo_children():
            widget.destroy()

        row1 = tk.Frame(self.search_frame, bg="#141414")
        row1.pack(fill=tk.X, pady=2)

        tk.Label(row1, text="Find:", bg="#141414", fg="#888888",
                font=("Consolas", 10), width=10).pack(side=tk.LEFT, padx=10)

        self.find_entry = tk.Entry(row1, bg="#1a1a1a", fg="#e8e8e8",
                                  font=("Consolas", 11), relief=tk.FLAT,
                                  highlightthickness=1, highlightcolor="#f0c040",
                                  insertbackground="#f0c040")
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.find_entry.focus()

        row2 = tk.Frame(self.search_frame, bg="#141414")
        row2.pack(fill=tk.X, pady=2)

        tk.Label(row2, text="Replace:", bg="#141414", fg="#888888",
                font=("Consolas", 10), width=10).pack(side=tk.LEFT, padx=10)

        self.replace_entry = tk.Entry(row2, bg="#1a1a1a", fg="#e8e8e8",
                                     font=("Consolas", 11), relief=tk.FLAT,
                                     highlightthickness=1, highlightcolor="#f0c040",
                                     insertbackground="#f0c040")
        self.replace_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        btn_frame = tk.Frame(self.search_frame, bg="#141414")
        btn_frame.pack(fill=tk.X, pady=2)

        tk.Button(btn_frame, text="Find Next", bg="#1a1a1a", fg="#888888",
                 font=("Consolas", 9), relief=tk.FLAT, command=self.find_next,
                 cursor="hand2").pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Replace", bg="#1a1a1a", fg="#888888",
                 font=("Consolas", 9), relief=tk.FLAT, command=self.replace_one,
                 cursor="hand2").pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Replace All", bg="#1a1a1a", fg="#f0c040",
                 font=("Consolas", 9, "bold"), relief=tk.FLAT, command=self.replace_all,
                 cursor="hand2").pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="X", bg="#141414", fg="#666666",
                 font=("Consolas", 12), relief=tk.FLAT, command=self.hide_search,
                 cursor="hand2").pack(side=tk.RIGHT, padx=10)

        self.find_entry.bind("<Return>", lambda e: self.find_next())
        self.replace_entry.bind("<Return>", lambda e: self.replace_one())
        self.find_entry.bind("<Escape>", lambda e: self.hide_search())

    def hide_search(self):
        self.search_frame.pack_forget()
        self.search_frame.config(height=40)
        self.editor.focus()

    def find_next(self):
        query = self.find_entry.get()
        if not query:
            return
        pos = self.editor.search(query, tk.INSERT, stopindex=tk.END, nocase=True)
        if pos:
            end_pos = f"{pos}+{len(query)}c"
            self.editor.see(pos)
            self.editor.tag_remove(tk.SEL, "1.0", tk.END)
            self.editor.tag_add(tk.SEL, pos, end_pos)
            self.editor.mark_set(tk.INSERT, end_pos)
        else:
            pos = self.editor.search(query, "1.0", stopindex=tk.INSERT, nocase=True)
            if pos:
                end_pos = f"{pos}+{len(query)}c"
                self.editor.see(pos)
                self.editor.tag_remove(tk.SEL, "1.0", tk.END)
                self.editor.tag_add(tk.SEL, pos, end_pos)
                self.editor.mark_set(tk.INSERT, end_pos)

    def find_prev(self):
        query = self.find_entry.get()
        if not query:
            return
        content = self.editor.get("1.0", tk.INSERT)
        idx = content.rfind(query, 0, len(content) - 1)
        if idx >= 0:
            pos = self.editor.index(f"1.0 + {idx}c")
            end_pos = f"{pos}+{len(query)}c"
            self.editor.see(pos)
            self.editor.tag_remove(tk.SEL, "1.0", tk.END)
            self.editor.tag_add(tk.SEL, pos, end_pos)
            self.editor.mark_set(tk.INSERT, pos)

    def replace_one(self):
        query = self.find_entry.get()
        replacement = self.replace_entry.get()
        try:
            sel_start = self.editor.index(tk.SEL_FIRST)
            sel_end = self.editor.index(tk.SEL_LAST)
            self.editor.delete(sel_start, sel_end)
            self.editor.insert(sel_start, replacement)
            self.find_next()
        except tk.TclError:
            self.find_next()

    def replace_all(self):
        query = self.find_entry.get()
        replacement = self.replace_entry.get()
        if not query:
            return
        content = self.editor.get("1.0", tk.END)
        new_content = content.replace(query, replacement)
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", new_content)
        count = content.count(query)
        self.status_left.config(text=f"  Replaced {count} occurrences")

    def run_code(self):
        # Always show output panel when running code
        if not self.output_visible:
            self.show_output()
        self.clear_output()
        self.status_left.config(text="  Running...")
        self.root.update_idletasks()

        code_str = self.editor.get("1.0", tk.END)

        # Check if code uses Kivy - run in separate process to avoid window conflicts
        if "kivy" in code_str.lower() or "from kivy" in code_str.lower() or "import kivy" in code_str.lower():
            self._run_in_subprocess(code_str)
            return

        self._execute_code(code_str)

    def _execute_code(self, code_str):
        """Execute code in editor's process (safe for non-GUI code)"""
        from contextlib import redirect_stdout, redirect_stderr

        out_buffer = io.StringIO()
        err_buffer = io.StringIO()

        with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
            try:
                exec(code_str, {"__name__": "__main__"})
            except Exception as e:
                import traceback
                traceback.print_exc()

        output = out_buffer.getvalue()
        errors = err_buffer.getvalue()

        if errors:
            self.append_output(errors, "error")
            self.status_left.config(text="  Execution failed")
        elif output:
            self.append_output(output, "success")
            self.status_left.config(text="  Execution successful")
        else:
            self.append_output("[Program finished - no output]", "success")
            self.status_left.config(text="  Done (no output)")

    def _run_in_subprocess(self, code_str):
        """Run code in a separate Python process - NON-BLOCKING with real-time output"""
        import subprocess
        import sys
        import threading
        import queue

        # Save to actual file so error line numbers match the editor
        if self.file_path:
            run_path = self.file_path
            try:
                with open(run_path, 'w', encoding='utf-8') as f:
                    f.write(code_str)
                self.modified = False
                self.update_tab_title()
            except Exception as e:
                self.append_output("[Error saving file: " + str(e) + "]\n", "error")
                return
        else:
            folder = os.getcwd()
            run_path = os.path.join(folder, "owl_temp_run.py")
            try:
                with open(run_path, 'w', encoding='utf-8') as f:
                    f.write(code_str)
            except Exception as e:
                self.append_output("[Error creating temp file: " + str(e) + "]\n", "error")
                return

        self.status_left.config(text="  Running in separate process...")
        self.append_output("[Running in separate process - real-time logs below]\n", "success")
        self.append_output("=" * 50 + "\n", "success")

        # Use a queue to safely pass output from thread to main thread
        output_queue = queue.Queue()

        def stream_output(pipe, tag_type):
            """Read output and put in queue"""
            try:
                for line in iter(pipe.readline, ''):
                    if line:
                        output_queue.put((line, tag_type))
                pipe.close()
            except:
                pass

        def process_queue():
            """Process queued output in main thread"""
            try:
                while True:
                    line, tag_type = output_queue.get_nowait()
                    self.append_output(line, tag_type)
            except queue.Empty:
                pass
            # Schedule next check
            self.root.after(100, process_queue)

        def run_process():
            process = None
            try:
                process = subprocess.Popen(
                    [sys.executable, run_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )

                stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, "success"))
                stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, "error"))
                stdout_thread.daemon = True
                stderr_thread.daemon = True
                stdout_thread.start()
                stderr_thread.start()

                # Poll process status instead of blocking wait
                import time
                start_time = time.time()
                while process.poll() is None:
                    if time.time() - start_time > 60:
                        process.kill()
                        self.root.after(0, lambda: self.append_output("[Process timed out - killed]\n", "error"))
                        self.root.after(0, lambda: self.status_left.config(text="  Timeout"))
                        break
                    time.sleep(0.1)

                # Wait for threads to finish reading remaining output
                stdout_thread.join(timeout=3)
                stderr_thread.join(timeout=3)

                # Process any remaining queued output
                self.root.after(0, process_queue)

                def on_done():
                    self.append_output("=" * 50 + "\n", "success")
                    if process.poll() == 0:
                        self.status_left.config(text="  Execution successful")
                        self.append_output("[Process finished successfully]\n", "success")
                    else:
                        self.status_left.config(text="  Execution failed")
                        code = process.poll() if process.poll() is not None else "unknown"
                        self.append_output(f"[Process exited with code {code}]\n", "error")

                self.root.after(200, on_done)

            except Exception as e:
                def on_error():
                    self.append_output(f"[Error running process: {e}]\n", "error")
                    self.status_left.config(text="  Execution error")
                self.root.after(0, on_error)
            finally:
                if not self.file_path:
                    try:
                        if os.path.exists(run_path):
                            os.remove(run_path)
                    except:
                        pass

        # Start queue processor
        self.root.after(100, process_queue)

        # Start process in background thread
        thread = threading.Thread(target=run_process, daemon=True)
        thread.start()

    def run_selection(self):
        try:
            code_str = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)

            # Check if selection uses Kivy
            if "kivy" in code_str.lower() or "from kivy" in code_str.lower() or "import kivy" in code_str.lower():
                self.show_output()
                self.clear_output()
                self._run_in_subprocess(code_str)
                return

            self.show_output()
            self.clear_output()
            self.status_left.config(text="  Running selection...")
            self.root.update_idletasks()

            self._execute_code(code_str)
            self.status_left.config(text="  Selection done")
        except tk.TclError:
            self.status_left.config(text="  No selection")

    def toggle_sidebar(self):
        """Toggle file explorer sidebar"""
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.sidebar_visible = False
            self.sidebar_btn.config(fg="#888888")
        else:
            self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, before=self.paned)
            self.sidebar_visible = True
            self.sidebar_btn.config(fg="#f0c040")
            self._refresh_sidebar()
            self._apply_sidebar_theme()
        self._save_settings()
        self.root.update_idletasks()

    def toggle_word_wrap(self):
        """Toggle word wrap on/off"""
        self.word_wrap = not self.word_wrap
        wrap_mode = tk.WORD if self.word_wrap else tk.NONE
        self.editor.config(wrap=wrap_mode)
        status = "ON" if self.word_wrap else "OFF"
        self.status_left.config(text=f"  Word wrap: {status}")
        self._save_settings()

    def show_about(self):
        """Show About dialog with license and donation info"""
        theme = THEMES[self.current_theme]
        popup = tk.Toplevel(self.root)
        popup.title("About Owl Editor")
        popup.geometry("500x620")
        popup.configure(bg=theme["bg"])
        popup.transient(self.root)
        popup.grab_set()
        popup.resizable(False, False)

        # Scrollable frame for content
        canvas = tk.Canvas(popup, bg=theme["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=theme["bg"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=480)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Owl icon
        tk.Label(scroll_frame, text="🦉", bg=theme["bg"], fg=theme["accent"],
                font=("Consolas", 72)).pack(pady=(10, 5))

        # Title
        tk.Label(scroll_frame, text="Owl Python Editor", bg=theme["bg"],
                fg=theme["accent"], font=("Consolas", 20, "bold")).pack()

        tk.Label(scroll_frame, text="v2.0", bg=theme["bg"],
                fg=theme["fg_dim"], font=("Consolas", 12)).pack()

        # Description
        tk.Label(scroll_frame, text="A lightweight, beautiful Python code editor\n"
                "built for coders who love speed and elegance.",
                bg=theme["bg"], fg=theme["fg"], font=("Consolas", 10),
                justify=tk.CENTER).pack(pady=10)

        # Developer
        dev_frame = tk.Frame(scroll_frame, bg=theme["bg"])
        dev_frame.pack(pady=5)
        tk.Label(dev_frame, text="Developer:", bg=theme["bg"], fg=theme["fg_dim"],
                font=("Consolas", 10)).pack()
        tk.Label(dev_frame, text="Husam Doughmosch", bg=theme["bg"], fg=theme["accent"],
                font=("Consolas", 14, "bold")).pack()

        # Links
        links_frame = tk.Frame(scroll_frame, bg=theme["bg"])
        links_frame.pack(pady=10)

        def open_link(url):
            import webbrowser
            webbrowser.open(url)

        tk.Button(links_frame, text="🐦 X (Twitter)", bg=theme["bg_sidebar"],
                 fg=theme["accent"], font=("Consolas", 10),
                 relief=tk.FLAT, cursor="hand2",
                 command=lambda: open_link("https://x.com/HDoughmosch")).pack(side=tk.LEFT, padx=5)

        tk.Button(links_frame, text="💼 LinkedIn", bg=theme["bg_sidebar"],
                 fg=theme["accent"], font=("Consolas", 10),
                 relief=tk.FLAT, cursor="hand2",
                 command=lambda: open_link("https://www.linkedin.com/in/husam-doughmosch-085568407")).pack(side=tk.LEFT, padx=5)

        # Separator
        tk.Frame(scroll_frame, height=2, bg=theme["accent"]).pack(fill=tk.X, padx=20, pady=15)

        # License section
        tk.Label(scroll_frame, text="📜 LICENSE", bg=theme["bg"], fg=theme["error"],
                font=("Consolas", 12, "bold")).pack()

        license_text = """FREE FOR PERSONAL USE ONLY

You may use this software for personal,
educational, and non-commercial purposes.

STRICTLY PROHIBITED:
  × Commercial use without permission
  × Redistribution on any website
  × Modification or derivative works
  × Removal of author credits
  × Selling or monetizing this software

NO WARRANTY
Provided "AS IS" without any warranty.
The author is not liable for any damages."""

        tk.Label(scroll_frame, text=license_text, bg=theme["bg_sidebar"],
                fg=theme["fg"], font=("Consolas", 9), justify=tk.LEFT,
                padx=15, pady=10).pack(fill=tk.X, padx=20, pady=5)

        # Donation section
        tk.Label(scroll_frame, text="❤️ SUPPORT THE PROJECT", bg=theme["bg"],
                fg=theme["success"], font=("Consolas", 12, "bold")).pack(pady=(10, 5))

        tk.Label(scroll_frame, text="This editor is free because of supporters like you.\n"
                "Your donation keeps updates coming forever!",
                bg=theme["bg"], fg=theme["fg"], font=("Consolas", 10),
                justify=tk.CENTER).pack()

        tk.Button(scroll_frame, text="💚 Support Owl Editor", bg=theme["success"],
                 fg="#ffffff", font=("Consolas", 11, "bold"),
                 relief=tk.FLAT, cursor="hand2",
                 command=lambda: open_link("https://x.com/HDoughmosch")).pack(pady=10)

        tk.Label(scroll_frame, text="Contact via X or LinkedIn for donations & sponsorship",
                bg=theme["bg"], fg=theme["fg_dim"], font=("Consolas", 9)).pack()

        # Close button
        tk.Button(scroll_frame, text="Close", bg=theme["accent"], fg=theme["sel_fg"],
                 font=("Consolas", 11, "bold"), relief=tk.FLAT,
                 command=popup.destroy, cursor="hand2", width=15).pack(pady=20)

    def toggle_zen_mode(self):
        """Toggle zen mode - hide everything except editor"""
        self.zen_mode = not self.zen_mode

        if self.zen_mode:
            self.toolbar.pack_forget()
            self.status_frame.pack_forget()
            self.tab_frame.pack_forget()
            if self.sidebar_visible:
                self.sidebar_frame.pack_forget()
            self.root.attributes("-fullscreen", True)
            self.status_left.config(text="  Zen Mode - Press F11 to exit")
        else:
            self.toolbar.pack(fill=tk.X, side=tk.TOP)
            self.tab_frame.pack(fill=tk.X, side=tk.TOP)
            self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
            if self.sidebar_visible:
                self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, before=self.paned)
            self.root.attributes("-fullscreen", False)
            self.status_left.config(text="  Zen mode: OFF")

    def _apply_sidebar_theme(self):
        """Apply current theme to sidebar widgets"""
        theme = THEMES[self.current_theme]
        self.sidebar_frame.config(bg=theme["bg_sidebar"])
        self.file_listbox.config(bg=theme["bg_sidebar"], fg=theme["fg"],
                                 selectbackground=theme["accent"],
                                 selectforeground=theme["sel_fg"])
        # Theme the header and path label children
        for child in self.sidebar_frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.config(bg=theme["bg_sidebar"])
                for sub in child.winfo_children():
                    if isinstance(sub, tk.Label):
                        sub.config(bg=theme["bg_sidebar"])
                    elif isinstance(sub, tk.Button):
                        sub.config(bg=theme["bg_sidebar"])

    def show_output(self):
        """Show output panel in PanedWindow"""
        if not self.output_visible:
            # Add output frame to paned window at bottom
            self.paned.add(self.output_frame, minsize=80)
            self.output_visible = True
            # Set sash position (editor gets ~70% of space)
            self.root.after(50, self._set_sash_position)
            self.root.update_idletasks()
            self._save_settings()

    def _set_sash_position(self):
        """Set paned window sash position after layout is calculated"""
        total_height = self.paned.winfo_height()
        if total_height > 250:
            self.paned.sash_place(0, 0, total_height - 200)

    def toggle_output(self):
        """Toggle output panel visibility"""
        if self.output_visible:
            # Remove from paned
            self.paned.remove(self.output_frame)
            self.output_visible = False
        else:
            self.show_output()
        self._save_settings()

    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

    def copy_output(self):
        """Copy all output text to clipboard"""
        text = self.output_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_left.config(text="  Output copied to clipboard")

    def append_output(self, text, tag_type="normal"):
        """Append text to output panel with clickable line numbers"""
        theme = THEMES[self.current_theme]

        # CRITICAL: Keep widget NORMAL so tag bindings work!
        # We prevent editing by binding keys to "break" instead of using DISABLED
        self.output_text.config(state=tk.NORMAL)

        import re

        # Check if this text contains clickable line numbers BEFORE inserting
        has_line_num = False
        line_num = None

        # Look for "File ... line X" pattern
        file_match = re.search(r'File "([^"]+)", line (\d+)', text)
        if file_match:
            has_line_num = True
            line_num = file_match.group(2)
        else:
            # Look for standalone "line X" pattern
            standalone_match = re.search(r'[Ll]ine (\d+)', text)
            if standalone_match:
                has_line_num = True
                line_num = standalone_match.group(1)

        if has_line_num and line_num:
            # Insert with a prominent prefix marker
            marker = "➤ "
            self.output_text.insert(tk.END, marker, "clickable_marker")
            self.output_text.tag_config("clickable_marker", foreground=theme["accent"])

            # Now insert the actual text
            start_idx = self.output_text.index(tk.END)
            if tag_type == "error":
                self.output_text.insert(tk.END, text, "error")
                self.output_text.tag_config("error", foreground=theme["error"])
            elif tag_type == "success":
                self.output_text.insert(tk.END, text, "success")
                self.output_text.tag_config("success", foreground=theme["success"])
            else:
                self.output_text.insert(tk.END, text)
            end_idx = self.output_text.index(tk.END)

            # Make the ENTIRE line clickable
            tag_name = f"goto_line_{line_num}_{hash(text) & 0xFFFF}"
            self.output_text.tag_add(tag_name, start_idx, end_idx)

            # Configure with VERY prominent styling
            self.output_text.tag_config(tag_name,
                                       foreground=theme["accent"],
                                       background=theme["bg_sidebar"],
                                       underline=True,
                                       font=(self.font_family, self.font_size, "bold"))

            # Raise tag priority to ensure it overrides "error" tag
            self.output_text.tag_raise(tag_name)

            # Bind click events - these ONLY work when widget is NORMAL!
            self.output_text.tag_bind(tag_name, "<Button-1>",
                                     lambda e, ln=line_num: self._goto_line_from_output(ln))
            self.output_text.tag_bind(tag_name, "<Enter>",
                                     lambda e: self.output_text.config(cursor="hand2"))
            self.output_text.tag_bind(tag_name, "<Leave>",
                                     lambda e: self.output_text.config(cursor=""))
        else:
            # No line number found - insert normally
            if tag_type == "error":
                self.output_text.insert(tk.END, text, "error")
                self.output_text.tag_config("error", foreground=theme["error"])
            elif tag_type == "success":
                self.output_text.insert(tk.END, text, "success")
                self.output_text.tag_config("success", foreground=theme["success"])
            else:
                self.output_text.insert(tk.END, text)

        # Keep widget NORMAL - tag bindings don't work in DISABLED state!
        # Instead we prevent editing by handling key events
        self.output_text.see(tk.END)

    def _setup_output_readonly(self):
        """Setup output panel to be read-only without using DISABLED state"""
        # Bind all editing keys to prevent modification
        self.output_text.bind("<Key>", lambda e: "break")
        self.output_text.bind("<Button-2>", lambda e: "break")  # Middle click paste
        self.output_text.bind("<Button-3>", lambda e: "break")  # Right click (we have custom menu)
        # Allow selection for copy
        self.output_text.config(exportselection=True)

    def _test_goto(self):
        """Test button to check if goto works"""
        import re
        output_text = self.output_text.get("1.0", tk.END)
        matches = list(re.finditer(r'[Ll]ine (\d+)', output_text))

        if matches:
            line_num = matches[-1].group(1)
            messagebox.showinfo("Test", f"Found line {line_num}!\nClick OK to jump...")
            self._goto_line_from_output(line_num)
        else:
            messagebox.showerror("Test", "No line numbers found in output!")

    def _goto_last_error(self):
        """Find the last error line in output and jump to it"""
        import re

        # Get all output text
        output_text = self.output_text.get("1.0", tk.END)

        # Find all line numbers in the output
        matches = list(re.finditer(r'[Ll]ine (\d+)', output_text))

        if matches:
            # Get the last match (most recent error)
            last_match = matches[-1]
            line_num = last_match.group(1)
            self._goto_line_from_output(line_num)
        else:
            self.status_left.config(text="  No error line found in output")

    def _goto_line_from_output(self, line_num):
        """Jump to a line number in the editor from output click"""
        try:
            line_num = int(line_num)
            total_lines = int(self.editor.index("end-1c").split(".")[0])
            if 1 <= line_num <= total_lines:
                self.editor.see(f"{line_num}.0")
                self.editor.mark_set(tk.INSERT, f"{line_num}.0")
                self.editor.focus()
                self.update_line_numbers()
                self.update_status()
                self.highlight_visible()
                self.highlight_matching_bracket()
                self.status_left.config(text=f"  ➤ Jumped to line {line_num}")
        except Exception as e:
            self.status_left.config(text=f"  Jump error: {e}")

    def _on_output_click(self, event):
        """Handle clicks on output panel - jump to error line"""
        # Get the line number where user clicked
        index = self.output_text.index(f"@{event.x},{event.y}")
        line = int(index.split(".")[0])

        # Get the full text of that line
        line_text = self.output_text.get(f"{line}.0", f"{line}.end")

        # DEBUG: Show what we found
        self.status_left.config(text=f"  Clicked line {line}: '{line_text[:50]}'")

        # Search for "line X" pattern in the line text
        import re
        match = re.search(r'[Ll]ine (\d+)', line_text)
        if match:
            line_num = match.group(1)
            self.status_left.config(text=f"  Found line {line_num}, jumping...")
            self._goto_line_from_output(line_num)
            return "break"

        # Also check previous line (in case click is on empty space after line)
        if line > 1:
            prev_text = self.output_text.get(f"{line-1}.0", f"{line-1}.end")
            match = re.search(r'[Ll]ine (\d+)', prev_text)
            if match:
                self.status_left.config(text=f"  Found line {match.group(1)} in prev, jumping...")
                self._goto_line_from_output(match.group(1))
                return "break"

        self.status_left.config(text=f"  No line number found on line {line}")

    def new_file(self):
        self.editor.delete("1.0", tk.END)
        self.file_path = None
        self.modified = False
        self.update_tab_title()
        self.status_left.config(text="  New file")
        if self.sidebar_visible:
            self._refresh_sidebar()

    def open_file(self):
        path = filedialog.askopenfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if path:
            self._load_file_and_track(path)

    def _add_recent_file(self, path):
        """Add file to recent files list"""
        if path in self.recent_files:
            self.recent_files.remove(path)
        self.recent_files.insert(0, path)
        self.recent_files = self.recent_files[:10]  # Keep last 10
        self._update_recent_menu()

    def _update_recent_menu(self):
        """Update the recent files submenu"""
        self.recent_menu.delete(0, tk.END)
        if not self.recent_files:
            self.recent_menu.add_command(label="  (no recent files)", state=tk.DISABLED)
            return
        for path in self.recent_files:
            name = os.path.basename(path)
            self.recent_menu.add_command(
                label=f"  {name}",
                command=lambda p=path: self._load_file_and_track(p)
            )
        self.recent_menu.add_separator()
        self.recent_menu.add_command(label="  Clear History", command=self._clear_recent)

    def _clear_recent(self):
        """Clear recent files list"""
        self.recent_files = []
        self._update_recent_menu()

    def _load_file_and_track(self, path):
        """Load a file and add to recent files"""
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", content)
            self.file_path = path
            self.modified = False
            self.update_tab_title()
            self.status_left.config(text=f"  Opened: {os.path.basename(path)}")
            self.highlight_visible()
            self.update_line_numbers()
            if self.sidebar_visible:
                self._refresh_sidebar()
            self._add_recent_file(path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    file.write(self.editor.get("1.0", tk.END))
                self.modified = False
                self.update_tab_title()
                self.status_left.config(text=f"  Saved: {os.path.basename(self.file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            self.save_as()

    def toggle_auto_save(self):
        """Toggle auto-save every 30 seconds"""
        if hasattr(self, '_auto_save_id'):
            self.root.after_cancel(self._auto_save_id)
            delattr(self, '_auto_save_id')
            self.status_left.config(text="  Auto-save: OFF")
        else:
            self._schedule_auto_save()
            self.status_left.config(text="  Auto-save: ON")

    def _schedule_auto_save(self):
        """Schedule next auto-save"""
        if self.modified and self.file_path:
            self.save_file()
        self._auto_save_id = self.root.after(30000, self._schedule_auto_save)

    def save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if path:
            self.file_path = path
            self.save_file()
            self._add_recent_file(path)

    def update_tab_title(self):
        name = os.path.basename(self.file_path) if self.file_path else "Untitled"
        prefix = "* " if self.modified else ""
        self.root.title(f"{prefix}{name} - Owl Editor 🦉")

    def undo(self):
        try:
            self.editor.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.editor.edit_redo()
        except tk.TclError:
            pass

    def cut(self):
        self.editor.event_generate("<<Cut>>")

    def copy(self):
        self.editor.event_generate("<<Copy>>")

    def paste(self):
        self.editor.event_generate("<<Paste>>")

    def select_all(self):
        self.editor.tag_add(tk.SEL, "1.0", tk.END)
        self.editor.mark_set(tk.INSERT, "1.0")

    def toggle_comment(self):
        try:
            sel_start = self.editor.index(tk.SEL_FIRST)
            sel_end = self.editor.index(tk.SEL_LAST)
            start_line = int(sel_start.split(".")[0])
            end_line = int(sel_end.split(".")[0])

            # Fix: if selection ends at column 0 of next line, don't include that line
            end_col = int(sel_end.split(".")[1])
            if end_col == 0 and end_line > start_line:
                end_line -= 1

            for line in range(start_line, end_line + 1):
                line_text = self.editor.get(f"{line}.0", f"{line}.end")

                # Skip truly empty lines - don't add # to them
                if not line_text.strip():
                    continue

                stripped = line_text.lstrip()
                indent = len(line_text) - len(stripped)

                if stripped.startswith("#"):
                    # Uncomment: remove # and optional space after it
                    if stripped.startswith("# "):
                        new_text = line_text[:indent] + stripped[2:]
                    else:
                        new_text = line_text[:indent] + stripped[1:]
                else:
                    # Comment: add # + space at the indentation level
                    new_text = line_text[:indent] + "# " + stripped

                self.editor.delete(f"{line}.0", f"{line}.end")
                self.editor.insert(f"{line}.0", new_text)
        except tk.TclError:
            pos = self.editor.index(tk.INSERT)
            line = int(pos.split(".")[0])
            line_text = self.editor.get(f"{line}.0", f"{line}.end")

            # Skip empty lines
            if not line_text.strip():
                return

            stripped = line_text.lstrip()
            indent = len(line_text) - len(stripped)

            if stripped.startswith("#"):
                if stripped.startswith("# "):
                    new_text = line_text[:indent] + stripped[2:]
                else:
                    new_text = line_text[:indent] + stripped[1:]
            else:
                new_text = line_text[:indent] + "# " + stripped

            self.editor.delete(f"{line}.0", f"{line}.end")
            self.editor.insert(f"{line}.0", new_text)

    def on_tab(self, event):
        try:
            sel_start = self.editor.index(tk.SEL_FIRST)
            sel_end = self.editor.index(tk.SEL_LAST)
            start_line = int(sel_start.split(".")[0])
            end_line = int(sel_end.split(".")[0])
            for line in range(start_line, end_line + 1):
                self.editor.insert(f"{line}.0", "    ")
            return "break"
        except tk.TclError:
            pass

        pos = self.editor.index(tk.INSERT)
        line = int(pos.split(".")[0])
        col = int(pos.split(".")[1])

        # Check for snippet expansion
        line_text = self.editor.get(f"{line}.0", pos)
        word = line_text.strip().split()[-1] if line_text.strip() else ""

        if word in SNIPPETS and col == len(line_text):
            self._expand_snippet(word, line, col)
            return "break"

        if col == 0:
            prev_line = self.editor.get(f"{line-1}.0", f"{line-1}.end")
            indent = len(prev_line) - len(prev_line.lstrip())
            stripped = prev_line.strip()
            if stripped.endswith(":") and any(stripped.startswith(k) for k in 
                ["def ", "class ", "if ", "elif ", "else:", "for ", "while ", 
                 "with ", "try:", "except", "finally:", "class"]):
                indent += 4
            self.editor.insert(pos, " " * indent)
            return "break"

        self.editor.insert(pos, "    ")
        return "break"

    def _expand_snippet(self, snippet_key, line, col):
        """Expand a code snippet"""
        snippet = SNIPPETS[snippet_key]

        # Remove the trigger word
        line_text = self.editor.get(f"{line}.0", f"{line}.{col}")
        trigger_start = f"{line}.{col - len(snippet_key)}"
        self.editor.delete(trigger_start, f"{line}.{col}")

        # Insert snippet with proper indentation
        current_indent = len(line_text) - len(line_text.lstrip())
        lines = snippet.split("\n")
        indented_lines = [lines[0]]
        for l in lines[1:]:
            indented_lines.append(" " * (current_indent + 4) + l)

        final_text = "\n".join(indented_lines)
        self.editor.insert(trigger_start, final_text)

        # Find first placeholder and select it
        start_idx = self.editor.search("${", trigger_start, tk.END)
        if start_idx:
            end_idx = self.editor.search("}", start_idx, tk.END)
            if end_idx:
                end_idx = f"{end_idx} + 1c"
                self.editor.tag_add(tk.SEL, start_idx, end_idx)
                self.editor.mark_set(tk.INSERT, end_idx)
                self.editor.see(start_idx)

        self.modified = True
        self.update_tab_title()
        self.on_key_release()

    def on_return(self, event):
        pos = self.editor.index(tk.INSERT)
        line = int(pos.split(".")[0])

        current_line = self.editor.get(f"{line}.0", f"{line}.end")
        indent = len(current_line) - len(current_line.lstrip())

        stripped = current_line.strip()
        if stripped.endswith(":"):
            indent += 4

        self.editor.insert(pos, "\n" + " " * indent)
        return "break"

    def on_backspace(self, event):
        pos = self.editor.index(tk.INSERT)
        line = int(pos.split(".")[0])
        col = int(pos.split(".")[1])

        if col > 0 and col % 4 == 0:
            prev_chars = self.editor.get(f"{line}.{col-4}", pos)
            if prev_chars == "    ":
                self.editor.delete(f"{line}.{col-4}", pos)
                return "break"

        return None

# ============================================================
#  MAIN ENTRY
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.iconbitmap("")
    except:
        pass

    try:
        from ctypes import windll
        from ctypes import c_int, byref, sizeof
        windll.dwmapi.DwmSetWindowAttribute(
            windll.user32.GetForegroundWindow(), 20, 
            byref(c_int(2)), sizeof(c_int)
        )
    except:
        pass

    app = OwlEditor(root)
    root.mainloop()
