"""极简可视化工具：基于 tkinter 自带的 Canvas，只覆盖数据结构课最常用的
三种画法——数组方格、柱状图、图（节点+边）。不依赖任何第三方绘图库。

插件在 run(text, vis) 里拿到的 vis 就是这个类的实例，直接调用即可：
    vis.draw_array([5, 3, 8, 1])
不需要可视化的插件可以完全不碰这个参数。
"""

import math


class Visualizer:
    def __init__(self, canvas):
        self.canvas = canvas

    def clear(self):
        self.canvas.delete("all")

    def draw_array(self, values, highlight=()):
        """画一排带数字的方格，适合数组/顺序表/栈/队列/排序中间状态。
        highlight：需要高亮的下标集合，比如当前比较到的位置。
        """
        self.clear()
        cell, x, y = 44, 20, 20
        for i, v in enumerate(values):
            x0 = x + i * cell
            fill = "#ffe08a" if i in highlight else "white"
            self.canvas.create_rectangle(x0, y, x0 + cell - 4, y + cell, fill=fill, outline="black")
            self.canvas.create_text(x0 + (cell - 4) / 2, y + cell / 2, text=str(v))
            self.canvas.create_text(x0 + (cell - 4) / 2, y + cell + 14, text=str(i), fill="#888")

    def draw_bars(self, values, highlight=()):
        """把一组数画成竖直柱状图，适合排序/查找过程演示。"""
        self.clear()
        x, base, width, gap, scale = 20, 220, 36, 8, 6
        for i, v in enumerate(values):
            x0 = x + i * (width + gap)
            h = max(2, v * scale)
            fill = "#ffe08a" if i in highlight else "#6fa8dc"
            self.canvas.create_rectangle(x0, base - h, x0 + width, base, fill=fill, outline="black")
            self.canvas.create_text(x0 + width / 2, base + 12, text=str(v))

    def draw_graph(self, nodes, edges, highlight_nodes=(), highlight_edges=()):
        """把节点和边画成圆圈+直线，节点自动均匀摆在一个圆周上。
        edges 里每条边是 (a, b) 这样的二元组（节点名字）。
        """
        self.clear()
        cx, cy, r = 220, 125, 90
        n = len(nodes)
        pos = {}
        for i, name in enumerate(nodes):
            angle = 2 * math.pi * i / max(n, 1)
            pos[name] = (cx + r * math.cos(angle), cy + r * math.sin(angle))

        for a, b in edges:
            if a not in pos or b not in pos:
                continue
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            lit = (a, b) in highlight_edges or (b, a) in highlight_edges
            self.canvas.create_line(x1, y1, x2, y2, fill="#e06666" if lit else "black", width=2)

        for name in nodes:
            x, y = pos[name]
            fill = "#ffe08a" if name in highlight_nodes else "white"
            self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill=fill, outline="black")
            self.canvas.create_text(x, y, text=str(name))
