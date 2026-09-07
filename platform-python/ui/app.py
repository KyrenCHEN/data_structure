"""基础图形界面（用 Python 自带的 tkinter，不需要额外安装任何东西）。

界面分三块：
  左边：插件列表（按 category 分组）
  右边上：根据当前选中插件的 params() 自动生成的输入框
  右边下：点击"运行"之后，算法的输出结果
"""

import tkinter as tk
from tkinter import ttk, messagebox

from core.registry import registry


class PlatformApp(tk.Tk):
    def __init__(self, reg=registry):
        super().__init__()
        self.reg = reg
        self.title("数据结构实验插件平台（Python）")
        self.geometry("880x560")
        self.current_plugin = None   # 当前选中的插件对象
        self.param_vars = {}         # 每个输入框对应一个 StringVar，方便读取用户输入

        self._build_layout()
        self._populate_plugin_list()

    def _build_layout(self):
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

    def _populate_plugin_list(self):
        # 把所有已加载的插件按 category 分组，画到左边的树状列表里
        self.tree.delete(*self.tree.get_children())
        self._node_to_plugin = {}
        for category, plugins in self.reg.by_category().items():
            cat_node = self.tree.insert("", tk.END, text=category, open=True)
            for p in plugins:
                node = self.tree.insert(cat_node, tk.END, text=p.name)
                self._node_to_plugin[node] = p

    def _on_select(self, _event=None):
        # 用户点了左边某个插件后，动态生成右边的输入表单
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

        for i, param in enumerate(plugin.params()):
            ttk.Label(self.form_frame, text=f"{param.label}：").grid(row=i, column=0, sticky="w", pady=2)
            var = tk.StringVar(value=str(param.default))
            entry = ttk.Entry(self.form_frame, textvariable=var, width=40)
            entry.grid(row=i, column=1, sticky="w", pady=2)
            if param.help_text:
                ttk.Label(self.form_frame, text=param.help_text, foreground="#888").grid(row=i, column=2, sticky="w", padx=6)
            self.param_vars[param.name] = var

    def _on_run(self):
        # 点击"运行"：把每个输入框的文本转换成对应类型，再调用插件的 run()
        if self.current_plugin is None:
            return
        kwargs = {}
        try:
            for param in self.current_plugin.params():
                raw = self.param_vars[param.name].get()
                if param.type == "int":
                    kwargs[param.name] = int(raw)
                elif param.type == "float":
                    kwargs[param.name] = float(raw)
                else:
                    kwargs[param.name] = raw
        except ValueError as exc:
            messagebox.showerror("参数错误", str(exc))
            return

        try:
            result = self.current_plugin.run(**kwargs)
        except Exception as exc:
            # 插件内部出错也不能让整个平台崩溃，把错误信息显示出来即可
            result = f"[运行出错] {exc!r}"

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, result)


def main():
    app = PlatformApp()
    app.mainloop()


if __name__ == "__main__":
    main()
