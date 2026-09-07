"""基础 UI（Tkinter，标准库自带，无需额外依赖）。

布局：
  左侧：按 category 分组的插件列表
  右侧上：根据所选插件 params() 自动生成的输入表单
  右侧下：运行结果输出区
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from core.registry import registry, PluginRegistry
from core.plugin_base import Plugin


class PlatformApp(tk.Tk):
    def __init__(self, reg: PluginRegistry = registry) -> None:
        super().__init__()
        self.reg = reg
        self.title("数据结构实验插件平台（Python）")
        self.geometry("880x560")
        self.current_plugin: Plugin | None = None
        self.param_vars: dict[str, tk.StringVar] = {}

        self._build_layout()
        self._populate_plugin_list()

    def _build_layout(self) -> None:
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(paned, width=240)
        paned.add(left, weight=1)
        ttk.Label(left, text="插件列表", font=("", 11, "bold")).pack(anchor="w", padx=8, pady=(8, 0))
        self.tree = ttk.Treeview(left, show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        right = ttk.Frame(paned)
        paned.add(right, weight=3)

        self.desc_label = ttk.Label(right, text="请选择左侧插件", font=("", 12, "bold"))
        self.desc_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.form_frame = ttk.Frame(right)
        self.form_frame.pack(fill=tk.X, padx=10, pady=10)

        self.run_btn = ttk.Button(right, text="运行", command=self._on_run, state=tk.DISABLED)
        self.run_btn.pack(anchor="w", padx=10)

        ttk.Label(right, text="输出：").pack(anchor="w", padx=10, pady=(10, 0))
        self.output = tk.Text(right, height=20)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def _populate_plugin_list(self) -> None:
        self.tree.delete(*self.tree.get_children())
        self._node_to_plugin: dict[str, Plugin] = {}
        for category, plugins in self.reg.by_category().items():
            cat_node = self.tree.insert("", tk.END, text=category, open=True)
            for p in plugins:
                node = self.tree.insert(cat_node, tk.END, text=p.name)
                self._node_to_plugin[node] = p

    def _on_select(self, _event=None) -> None:
        sel = self.tree.selection()
        if not sel or sel[0] not in self._node_to_plugin:
            return
        plugin = self._node_to_plugin[sel[0]]
        self.current_plugin = plugin
        self.desc_label.config(text=plugin.describe())
        self.run_btn.config(state=tk.NORMAL)

        for child in self.form_frame.winfo_children():
            child.destroy()
        self.param_vars.clear()

        for i, spec in enumerate(plugin.params()):
            ttk.Label(self.form_frame, text=f"{spec.label}：").grid(row=i, column=0, sticky="w", pady=2)
            var = tk.StringVar(value=str(spec.default))
            entry = ttk.Entry(self.form_frame, textvariable=var, width=40)
            entry.grid(row=i, column=1, sticky="w", pady=2)
            if spec.help:
                ttk.Label(self.form_frame, text=spec.help, foreground="#888").grid(row=i, column=2, sticky="w", padx=6)
            self.param_vars[spec.name] = var

    def _on_run(self) -> None:
        if self.current_plugin is None:
            return
        kwargs = {}
        try:
            for spec in self.current_plugin.params():
                raw = self.param_vars[spec.name].get()
                if spec.type == "int":
                    kwargs[spec.name] = int(raw)
                elif spec.type == "float":
                    kwargs[spec.name] = float(raw)
                else:
                    kwargs[spec.name] = raw
        except ValueError as exc:
            messagebox.showerror("参数错误", str(exc))
            return

        try:
            result = self.current_plugin.run(**kwargs)
        except Exception as exc:  # noqa: BLE001 插件异常需在 UI 上可见，不应崩溃平台
            result = f"[运行出错] {exc!r}"

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, result)


def main() -> None:
    app = PlatformApp()
    app.mainloop()


if __name__ == "__main__":
    main()
