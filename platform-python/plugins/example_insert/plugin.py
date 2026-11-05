"""示例插件：顺序表（数组）插入。

这是一个完整实现的算法示例，用来演示插件应该写成什么样子——
照着这个结构写自己的插件就行。不知道从哪下手时先看这个文件，
比看 template/ 空模板更直观。
"""

from core.plugin_base import Plugin


class SeqListInsertPlugin(Plugin):
    name = "顺序表插入（示例）"
    category = "E2"
    description = (
        "第一行：原数组，用逗号分隔，例如 3,5,8,2,9\n"
        "第二行：插入位置和插入值，用逗号分隔，例如 2,100（表示在下标 2 处插入 100）"
    )

    def example_input(self):
        return "3,5,8,2,9\n2,100"

    def run(self, text, vis):
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        if len(lines) != 2:
            return "输入格式不对：需要两行，第一行是数组，第二行是“位置,插入值”"

        try:
            arr = [int(x) for x in lines[0].split(",")]
            pos, val = (int(x) for x in lines[1].split(","))
        except ValueError:
            return "数字格式不对，检查一下逗号和数字有没有打错"

        if not (0 <= pos <= len(arr)):
            return f"插入位置 {pos} 超出范围，当前数组长度是 {len(arr)}，位置应该在 0 到 {len(arr)} 之间"

        # 顺序表插入的核心逻辑：
        # 从数组末尾开始，把 pos 位置及其后面的元素依次往后挪一位，
        # 腾出 pos 这个位置，再把新值放进去。
        arr.append(0)  # 数组长度先加 1，占个位置
        for i in range(len(arr) - 1, pos, -1):
            arr[i] = arr[i - 1]
        arr[pos] = val

        vis.draw_array(arr, highlight={pos})  # 高亮刚插入的位置

        return (
            f"插入后的数组：{arr}\n"
            f"做法：把下标 {pos} 开始的元素都往后移一位，腾出的位置放 {val}。"
        )
