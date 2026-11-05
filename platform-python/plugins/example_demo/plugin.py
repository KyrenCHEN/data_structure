"""插件模板：平台组件演示（新插件从这里开始）。

这是"万能模板"——把你以后各次实验可能用到的组件全部演示了一遍：
  - 怎么解析多行文本输入
  - 怎么画数组方格（vis.draw_array）
  - 怎么画柱状图（vis.draw_bars）
  - 怎么画图：节点 + 边（vis.draw_graph）
  - 怎么返回文字结果

写自己的插件时：
  1. 复制 plugins/example_demo/ 整个目录，改个名字（比如 plugins/sort_1234/）。
  2. 把下面用不到的部分删掉，只留你需要的那一种画法。
  3. 把 run() 里面的逻辑换成你自己的算法。
"""

from core.plugin_base import Plugin


class DemoPlugin(Plugin):
    name = "平台组件演示（新插件模板）"
    category = "E0 平台示例"
    description = (
        "第一行：一组用逗号分隔的数字，例如 5,3,8,1,9\n"
        "第二行（可选）：图的边，格式 A-B,B-C,C-A"
    )

    def example_input(self):
        return "5,3,8,1,9\nA-B,B-C,C-A,A-D"

    def run(self, text, vis):
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        if not lines:
            return "请至少输入一行：用逗号分隔的数字"

        # ---- 1. 解析第一行：一组数字 ----
        try:
            values = [int(x) for x in lines[0].split(",")]
        except ValueError:
            return "第一行格式不对，应为用逗号分隔的整数，例如 5,3,8,1"

        # ---- 2. 解析第二行（可选）：图的边 ----
        nodes, edges = [], []
        if len(lines) > 1:
            for pair in lines[1].split(","):
                a, b = pair.split("-")
                a, b = a.strip(), b.strip()
                edges.append((a, b))
                for v in (a, b):
                    if v not in nodes:
                        nodes.append(v)

        # ---- 3. 可视化：下面三种画法二选一/三选一，把不要的删掉或注释掉 ----
        vis.draw_array(values, highlight={0, len(values) - 1})      # 数组方格
        # vis.draw_bars(values, highlight={1})                      # 柱状图
        # if nodes:
        #     vis.draw_graph(nodes, edges)                          # 图（节点+边）

        # ---- 4. 文字结果：写清楚你的算法做了什么 ----
        result = [f"数组：{values}", f"最大值：{max(values)}，最小值：{min(values)}"]
        if nodes:
            result.append(f"图：{len(nodes)} 个节点，{len(edges)} 条边 -> {edges}")
        return "\n".join(result)
