"""示例插件：汉诺塔（递归）。

作为 E1.3 的参考实现，演示"文本输入 -> 文本输出"的最小写法。
学生完成 E1.3 时应在 plugins/ 下新建自己的目录（如 plugins/hanoi_myname/），
不要直接修改本文件。
"""

from core.plugin_base import Plugin


class HanoiPlugin(Plugin):
    name = "汉诺塔求解（示例）"
    category = "E1"
    description = "输入一个正整数 n（盘子数量），例如 4。也可以点“加载文本文件”读取 sample_input.txt。"

    def example_input(self):
        return "4"

    def run(self, text):
        text = text.strip()  # 去掉输入框里可能带的换行/空格
        if not text.isdigit():
            return "输入不合法：请输入一个正整数，例如 4"

        n = int(text)
        if n < 1:
            return "n 必须 >= 1"

        moves = []  # 用来记录每一步的移动，比如 "A -> C"

        # 递归函数：把 k 个盘子从 src 借助 aux 移动到 dst
        def hanoi(k, src, aux, dst):
            if k == 0:
                return
            hanoi(k - 1, src, dst, aux)      # 先把上面 k-1 个盘子移到辅助柱
            moves.append(f"{src} -> {dst}")  # 移动最底下这一个盘子
            hanoi(k - 1, aux, src, dst)      # 再把 k-1 个盘子从辅助柱移到目标柱

        hanoi(n, "A", "B", "C")

        lines = [f"共 {len(moves)} 步（理论最少步数 2^n - 1 = {2 ** n - 1}）："]
        lines.extend(moves)
        return "\n".join(lines)
