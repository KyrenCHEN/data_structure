"""基础图形界面（用 Python 自带的 tkinter，不需要额外安装任何东西）。

整体布局：
  顶部：菜单栏——一次课的插件放在同一个菜单里（按 category 分组）
  左侧：选中某个插件后出现的面板——插件说明 + 文本输入框 + 按钮
  中间：一个大大的输出框，显示运行结果（纯文本）
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.registry import registry


class PlatformApp(tk.Tk):
    def __init__(self, reg=registry):
        super().__init__()
        self.reg = reg
        self.title("数据结构实验插件平台（Python）")
        self.geometry("980x600")
        self.current_plugin = None   # 当前选中的插件对象

        self._build_menu()
        self._build_layout()

    def _build_menu(self):
        # 菜单栏：每个 category（比如 "E1"）是一个菜单，里面是这次课的所有插件
        menubar = tk.Menu(self)
        for category, plugins in self.reg.by_category().items():
            menu = tk.Menu(menubar, tearoff=0)
            for p in plugins:
                # plugin=p 是 Python 的一个小技巧：让每个菜单项"记住"自己对应的插件
                menu.add_command(label=p.name, command=lambda plugin=p: self._select_plugin(plugin))
            menubar.add_cascade(label=category, menu=menu)
        self.config(menu=menubar)

    def _build_layout(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # ---------- 左侧：插件说明 + 输入框 ----------
        left = ttk.Frame(paned, width=280)
        paned.add(left, weight=1)

        self.title_label = ttk.Label(left, text="请从上方菜单选择一个插件", font=("", 12, "bold"), wraplength=260)
        self.title_label.pack(anchor="w", padx=10, pady=(10, 4))

        self.desc_label = ttk.Label(left, text="", foreground="#666", wraplength=260)
        self.desc_label.pack(anchor="w", padx=10, pady=(0, 10))

        ttk.Label(left, text="输入（纯文本）：").pack(anchor="w", padx=10)
        self.input_box = tk.Text(left, height=10)
        self.input_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))

        btn_row = ttk.Frame(left)
        btn_row.pack(fill=tk.X, padx=10, pady=(0, 8))
        ttk.Button(btn_row, text="加载文本文件...", command=self._on_load_file).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="填入示例", command=self._on_fill_example).pack(side=tk.LEFT, padx=6)

        self.run_btn = ttk.Button(left, text="运行", command=self._on_run, state=tk.DISABLED)
        self.run_btn.pack(anchor="w", padx=10, pady=(0, 10))

        # ---------- 中间：大输出框 ----------
        right = ttk.Frame(paned)
        paned.add(right, weight=3)
        ttk.Label(right, text="输出", font=("", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 4))
        self.output = tk.Text(right, wrap="word")
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def _select_plugin(self, plugin):
        # 从菜单里点了某个插件之后，刷新左侧面板
        self.current_plugin = plugin
        self.title_label.config(text=f"[{plugin.category}] {plugin.name}")
        self.desc_label.config(text=plugin.description or "（该插件没有填写说明）")
        self.run_btn.config(state=tk.NORMAL)
        self.input_box.delete("1.0", tk.END)
        self.output.delete("1.0", tk.END)

    def _on_load_file(self):
        # 弹出文件选择框，把选中的 .txt 文件内容读进输入框
        path = filedialog.askopenfilename(title="选择文本文件", filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as exc:
            messagebox.showerror("读取失败", str(exc))
            return
        self.input_box.delete("1.0", tk.END)
        self.input_box.insert(tk.END, content)

    def _on_fill_example(self):
        if self.current_plugin is None:
            return
        self.input_box.delete("1.0", tk.END)
        self.input_box.insert(tk.END, self.current_plugin.example_input())

    def _on_run(self):
        if self.current_plugin is None:
            return
        text = self.input_box.get("1.0", tk.END)

        try:
            result = self.current_plugin.run(text)
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
