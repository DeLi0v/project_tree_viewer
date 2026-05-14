# 🌳 Project Tree Viewer

A lightweight CLI + GUI tool for visualizing project directory structure with filtering, sizes, colors, and export options.

---

## 🚀 Features

- CLI and GUI support
- Ignore system like `.gitignore`
- `.treeconfig` support
- File size display
- Colored output
- Extension filtering
- Markdown export
- Safe recursive traversal

---

## 📦 Installation

```bash
pip install -r requirements.txt
```
---

## ▶️ CLI Usage

```python
python main.py .
```

### Options

```bash
--sizes        Show file sizes
--color        Enable colored output
--only py,js   Filter extensions
--depth 3      Limit depth
--format md    Markdown output
```

---

## 🖥 GUI Usage

```python
python gui.py
```

---

## ⚙️ Config

### .treeconfig

```json
{
  "exclude_dirs": ["node_modules", ".git"],
  "exclude_files": [".env"]
}
```

### .treeignore

```json
*.log
__pycache__
dist/
```