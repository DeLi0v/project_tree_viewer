import os
import argparse
import json
import fnmatch
from colorama import Fore, Style, init

# ============================
# CONFIG 
# ============================
def load_config(root_path):
    config_path = os.path.join(root_path, ".treeconfig")

    if not os.path.exists(config_path):
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
    
def load_ignore_patterns(root_path):
    ignore_path = os.path.join(root_path, ".treeignore")

    if not os.path.exists(ignore_path):
        return []

    patterns = []
    with open(ignore_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)

    return patterns

# ============================
# UTILS
# ============================

def is_ignored(name, relative_path, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(relative_path, pattern):
            return True
    return False

def format_size(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"

def colorize(name, is_dir, use_color):
    if not use_color:
        return name

    if is_dir:
        return Fore.BLUE + name + Style.RESET_ALL
    else:
        return name

def parse_extensions(arg):
    if not arg:
        return None
    return set(ext.strip().lower().lstrip(".") for ext in arg.split(","))

# ============================
# BUILD TREE
# ============================

def build_tree(
    root_path,
    exclude_dirs=None,
    exclude_files=None,
    ignore_patterns=None,
    base_path="",
    max_depth=None,
    prefix="",
    current_depth=0,
    show_sizes=False,
    use_color=False,
    only_ext=None,
    output_format="tree"
):
    relative = os.path.relpath(path, base_path) if base_path else item

    if max_depth is not None and current_depth > max_depth:
        return

    try:
        items = sorted(os.listdir(root_path))
    except PermissionError:
        print(prefix + "└── [ACCESS DENIED]")
        return

    filtered_items = []
    for item in items:
        if item in exclude_dirs or item in exclude_files:
            continue

        if ignore_patterns and is_ignored(item, relative, ignore_patterns):
            continue
        filtered_items.append(item)

    for index, item in enumerate(filtered_items):
        if only_ext and os.path.isfile(path):
            ext = os.path.splitext(item)[1].lstrip(".").lower()
            if ext not in only_ext:
                continue

        path = os.path.join(root_path, item)
        is_last = index == len(filtered_items) - 1

        connector = "└── " if is_last else "├── "
        display_name = item

        # Цвет
        display_name = colorize(display_name, os.path.isdir(path), use_color)

        # Размер
        if show_sizes and os.path.isfile(path):
            try:
                size = os.path.getsize(path)
                display_name += f" ({format_size(size)})"
            except Exception:
                display_name += " (?)"

        line = prefix + connector + display_name

        if output_format == "md":
            print(line)
        else:
            print(line)

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            build_tree(
                path,
                exclude_dirs,
                exclude_files,
                ignore_patterns,
                base_path,
                max_depth,
                prefix + extension,
                current_depth + 1,
                show_sizes,
                use_color
            )


def parse_list(arg):
    if not arg:
        return set()
    return set(item.strip() for item in arg.split(","))

# ============================
# MAIN CODE
# ============================


def main():
    init(autoreset=True)

    config = load_config(args.path)
    ignore_patterns = load_ignore_patterns(args.path)
    only_ext = parse_extensions(args.only)

    parser = argparse.ArgumentParser(
        description="Project structure viewer"
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root project directory"
    )

    parser.add_argument(
        "--exclude-dirs",
        help="Comma-separated directories to exclude"
    )

    parser.add_argument(
        "--exclude-files",
        help="Comma-separated files to exclude"
    )

    parser.add_argument(
        "--depth",
        type=int,
        help="Max depth of tree"
    )

    parser.add_argument(
        "--output",
        help="Save output to file"
    )

    parser.add_argument(
        "--sizes",
        action="store_true",
        help="Show file sizes"
    )

    parser.add_argument(
        "--color",
        action="store_true",
        help="Enable colored output"
    )

    parser.add_argument(
        "--only",
        help="Show only specific file extensions (e.g. py,js,ts)"
    )

    parser.add_argument(
        "--format",
        choices=["tree", "md"],
        default="tree",
        help="Output format"
    )

    args = parser.parse_args()

    exclude_dirs = parse_list(args.exclude_dirs) or set(config.get("exclude_dirs", [])) or {
        ".git",
        "node_modules",
        "__pycache__",
        "dist",
        "build",
        ".idea",
        ".vscode"
    }

    exclude_files = parse_list(args.exclude_files) or set(config.get("exclude_files", [])) or {
        ".DS_Store"
    }

    if args.output:
        import sys
        sys.stdout = open(args.output, "w", encoding="utf-8")

    if args.format == "md":
        print("```")

    root_name = os.path.basename(os.path.abspath(args.path))
    print(root_name if root_name else ".")
    
    build_tree(
        args.path,
        exclude_dirs,
        exclude_files,
        ignore_patterns,
        args.path,
        args.depth,
        show_sizes=args.sizes,
        use_color=args.color,
        only_ext=only_ext,
        output_format=args.format
    )

    if args.format == "md":
        print("```")


if __name__ == "__main__":
    main()