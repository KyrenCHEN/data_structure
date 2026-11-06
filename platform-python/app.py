"""基础图形界面（用 Python 自带的 tkinter，不需要额外安装任何东西）。

整体布局：
  顶部：菜单栏——一次课的插件放在同一个菜单里（按 category 分组）
  左侧：选中某个插件后出现的面板——插件说明 + 文本输入框 + 按钮
  中间上：可视化画布（数组方格 / 柱状图 / 图，插件可选使用）
  中间下：输出框，显示运行结果（纯文本）
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from visual import Visualizer

# 统一配色，照搬课程文档用的墨绿色系，不需要改这几个值。
BG = "#f4f5f7"
ACCENT = "#1a5632"
ACCENT_ACTIVE = "#154827"
BORDER = "#d4d7dc"
MUTED = "#5a6066"


class PlatformApp(tk.Tk):
    def __init__(self, plugins):
        super().__init__()
        self.plugins = plugins
        self.title("数据结构实验插件平台（Python）")
        self.geometry("1020x700")
        self.minsize(820, 560)
        self.current_plugin = None   # 当前选中的插件对象

        self._setup_style()
        self._build_menu()
        self._build_layout()

    def _setup_style(self):
        self.configure(bg=BG)
        style = ttk.Style(self)
        # clam 主题支持自定义颜色，换个主题能让控件看起来不那么“原始系统风格”。
        style.theme_use("clam")

        style.configure(".", background=BG)
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground="#1a1a1a")
        style.configure("Muted.TLabel", background=BG, foreground=MUTED)
        style.configure("Header.TLabel", background=BG, foreground=ACCENT, font=("", 13, "bold"))
        style.configure("Section.TLabel", background=BG, foreground="#1a1a1a", font=("", 11, "bold"))

        style.configure("TLabelframe", background=BG, bordercolor=BORDER, relief="solid", borderwidth=1)
        style.configure("TLabelframe.Label", background=BG, foreground="#1a1a1a", font=("", 11, "bold"))

        style.configure("TButton", padding=(12, 6))
        style.configure("Accent.TButton", padding=(14, 7), background=ACCENT, foreground="white")
        style.map(
            "Accent.TButton",
            background=[("disabled", "#b9c7bf"), ("active", ACCENT_ACTIVE)],
            foreground=[("disabled", "#f0f0f0")],
        )

    def _build_menu(self):
        # 菜单栏：每个 category（比如 "E1"）是一个菜单，里面是这次课的所有插件
        groups = {}
        for p in sorted(self.plugins, key=lambda p: (p.category, p.name)):
            groups.setdefault(p.category, []).append(p)

        menubar = tk.Menu(self)
        for category, plugins in groups.items():
            menu = tk.Menu(menubar, tearoff=0)
            for p in plugins:
                # plugin=p 是 Python 的一个小技巧：让每个菜单项"记住"自己对应的插件
                menu.add_command(label=p.name, command=lambda plugin=p: self._select_plugin(plugin))
            menubar.add_cascade(label=category, menu=menu)
        self.config(menu=menubar)

    def _build_layout(self):
        outer = ttk.Frame(self, padding=12)
        outer.pack(fill=tk.BOTH, expand=True)

        paned = ttk.PanedWindow(outer, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # ---------- 左侧：插件说明 + 输入框 ----------
        left = ttk.Frame(paned, width=300)
        paned.add(left, weight=1)

        self.title_label = ttk.Label(left, text="请从上方菜单选择一个插件", style="Header.TLabel", wraplength=280)
        self.title_label.pack(anchor="w", pady=(0, 4))

        self.desc_label = ttk.Label(left, text="", style="Muted.TLabel", wraplength=280, justify=tk.LEFT)
        self.desc_label.pack(anchor="w", pady=(0, 12))

        input_frame = ttk.Labelframe(left, text="输入（纯文本）", padding=8)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.input_box = tk.Text(
            input_frame, height=10, wrap="word", relief="flat",
            highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT,
            padx=6, pady=6,
        )
        self.input_box.pack(fill=tk.BOTH, expand=True)

        btn_row = ttk.Frame(left)
        btn_row.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(btn_row, text="加载文本文件...", command=self._on_load_file).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="填入示例", command=self._on_fill_example).pack(side=tk.LEFT, padx=(8, 0))

        self.run_btn = ttk.Button(left, text="运行", style="Accent.TButton", command=self._on_run, state=tk.DISABLED)
        self.run_btn.pack(anchor="w")

        # ---------- 右侧：画布（上）+ 输出框（下） ----------
        right = ttk.Frame(paned)
        paned.add(right, weight=3)

        vis_frame = ttk.Labelframe(right, text="可视化", padding=8)
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        self.canvas = tk.Canvas(vis_frame, height=250, bg="white", highlightthickness=1, highlightbackground=BORDER)
        self.canvas.pack(fill=tk.X)
        self.vis = Visualizer(self.canvas)

        output_frame = ttk.Labelframe(right, text="输出", padding=8)
        output_frame.pack(fill=tk.BOTH, expand=True)
        self.output = tk.Text(
            output_frame, wrap="word", relief="flat",
            highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT,
            padx=6, pady=6,
        )
        self.output.pack(fill=tk.BOTH, expand=True)

    def _select_plugin(self, plugin):
        # 从菜单里点了某个插件之后，刷新左侧面板
        self.current_plugin = plugin
        self.title_label.config(text=f"[{plugin.category}] {plugin.name}")
        self.desc_label.config(text=plugin.description or "（该插件没有填写说明）")
        self.run_btn.config(state=tk.NORMAL)
        self.input_box.delete("1.0", tk.END)
        self.output.delete("1.0", tk.END)
        self.vis.clear()

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
            result = self.current_plugin.run(text, self.vis)
        except Exception as exc:
            # 插件内部出错也不能让整个平台崩溃，把错误信息显示出来即可
            result = f"[运行出错] {exc!r}"

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, result)
