# gui.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import sys
import io
import contextlib

# импорт твоей логики
import core


class TreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Tree Viewer")
        self.root.geometry("800x600")
        self.lock = threading.Lock()

        # ===== ПУТЬ =====
        path_frame = tk.Frame(root)
        path_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(path_frame, text="Project path:").pack(side="left")

        self.path_var = tk.StringVar(value=".")
        self.path_entry = tk.Entry(path_frame, textvariable=self.path_var)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=5)

        tk.Button(path_frame, text="Browse", command=self.browse).pack(side="left")

        # ===== ОПЦИИ =====
        options_frame = tk.Frame(root)
        options_frame.pack(fill="x", padx=10, pady=5)

        self.sizes_var = tk.BooleanVar()
        self.color_var = tk.BooleanVar()
        self.md_var = tk.BooleanVar()

        tk.Checkbutton(options_frame, text="Show sizes", variable=self.sizes_var).pack(side="left")
        tk.Checkbutton(options_frame, text="Color output", variable=self.color_var).pack(side="left")
        tk.Checkbutton(options_frame, text="Markdown", variable=self.md_var).pack(side="left")

        # ===== ФИЛЬТРЫ =====
        filter_frame = tk.Frame(root)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Only extensions:").pack(side="left")
        self.only_entry = tk.Entry(filter_frame)
        self.only_entry.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Depth:").pack(side="left")
        self.depth_entry = tk.Entry(filter_frame, width=5)
        self.depth_entry.pack(side="left", padx=5)

        # ===== КНОПКИ =====
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(btn_frame, text="Generate", command=self.run).pack(side="left")
        tk.Button(btn_frame, text="Save to file", command=self.save).pack(side="left")

        # ===== ВЫВОД =====
        self.text = tk.Text(root, wrap="none")
        self.text.pack(fill="both", expand=True, padx=10, pady=5)

    def browse(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def run(self):
        threading.Thread(target=self.generate_tree).start()

    def generate_tree(self):
        try:
            self.text.delete("1.0", tk.END)

            path = self.path_var.get()
            only = self.only_entry.get()
            depth = self.depth_entry.get()

            only_ext = core.parse_extensions(only.strip() if only else "")
            depth = int(depth) if depth else None

            config = core.load_config(path)
            ignore_patterns = core.load_ignore_patterns(path)

            exclude_dirs = set(config.get("exclude_dirs", []))
            exclude_files = set(config.get("exclude_files", []))

            buffer = io.StringIO()

            with self.lock:
                with contextlib.redirect_stdout(buffer):

                    root_name = os.path.basename(os.path.abspath(path))
                    print(root_name)

                    core.build_tree(
                        path,
                        exclude_dirs,
                        exclude_files,
                        ignore_patterns,
                        path,
                        depth,
                        show_sizes=self.sizes_var.get(),
                        use_color=self.color_var.get(),
                        only_ext=only_ext,
                        output_format="md" if self.md_var.get() else "tree"
                    )

            result = buffer.getvalue()
            self.text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save(self):
        content = self.text.get("1.0", tk.END)

        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Markdown", "*.md")]
        )

        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    root = tk.Tk()
    app = TreeApp(root)
    root.mainloop()