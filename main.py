import os
import argparse


def build_tree(
    root_path,
    exclude_dirs=None,
    exclude_files=None,
    max_depth=None,
    prefix="",
    current_depth=0
):
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
        filtered_items.append(item)

    for index, item in enumerate(filtered_items):
        path = os.path.join(root_path, item)
        is_last = index == len(filtered_items) - 1

        connector = "└── " if is_last else "├── "
        print(prefix + connector + item)

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            build_tree(
                path,
                exclude_dirs,
                exclude_files,
                max_depth,
                prefix + extension,
                current_depth + 1
            )


def parse_list(arg):
    if not arg:
        return set()
    return set(item.strip() for item in arg.split(","))


def main():
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

    args = parser.parse_args()

    exclude_dirs = parse_list(args.exclude_dirs) or {
        ".git",
        "node_modules",
        "__pycache__",
        "dist",
        "build",
        ".idea",
        ".vscode"
    }

    exclude_files = parse_list(args.exclude_files) or {
        ".DS_Store"
    }

    if args.output:
        import sys
        sys.stdout = open(args.output, "w", encoding="utf-8")

    print(args.path)
    build_tree(
        args.path,
        exclude_dirs,
        exclude_files,
        args.depth
    )


if __name__ == "__main__":
    main()