"""示例插件：顺序表（数组）插入与删除。

这是一个比较完整的示例，覆盖了插件平台大部分的界面能力：纯文本输入、
"填入示例"按钮、可视化画布（数组方格 + 高亮）、文字结果输出，还演示了
"一个插件里用输入第一行区分多个算法"这个约定的实际写法——这个约定以后
每次实验都会用到。不知道从哪下手时先看这个文件，比看 template/ 空模板
更直观。
"""

from plugin_base import Plugin


class SeqListPlugin(Plugin):
    name = "顺序表插入与删除（示例）"
    category = "E1"
    description = (
        "第一行写操作名：insert 或 delete。\n"
        "insert 后面两行：原数组（逗号分隔）、插入位置和插入值（逗号分隔），例如 2,100 表示在下标 2 处插入 100。\n"
        "delete 后面两行：原数组（逗号分隔）、要删除的下标，例如 2 表示删除下标 2 处的元素。"
    )

    def example_input(self):
        return "insert\n3,5,8,2,9\n2,100"

    def run(self, text, vis):
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        if len(lines) != 3:
            return "输入格式不对：需要三行，第一行是 insert 或 delete，后两行是数据"

        op = lines[0].lower()
        if op == "insert":
            return self._insert(lines[1], lines[2], vis)
        elif op == "delete":
            return self._delete(lines[1], lines[2], vis)
        else:
            return f"不认识的操作：{lines[0]}，第一行只能写 insert 或 delete"

    def _insert(self, arr_line, pos_line, vis):
        try:
            arr = [int(x) for x in arr_line.split(",")]
            pos, val = (int(x) for x in pos_line.split(","))
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

    def _delete(self, arr_line, pos_line, vis):
        try:
            arr = [int(x) for x in arr_line.split(",")]
            pos = int(pos_line)
        except ValueError:
            return "数字格式不对，检查一下逗号和数字有没有打错"

        if not (0 <= pos < len(arr)):
            return f"删除位置 {pos} 超出范围，当前数组长度是 {len(arr)}，位置应该在 0 到 {len(arr) - 1} 之间"

        vis.draw_array(arr, highlight={pos})  # 删除前先高亮要删的位置
        removed = arr[pos]

        # 顺序表删除的核心逻辑：
        # 把 pos 后面的元素依次往前挪一位，覆盖掉 pos 这个位置，长度减一。
        for i in range(pos, len(arr) - 1):
            arr[i] = arr[i + 1]
        arr.pop()

        return (
            f"删除后的数组：{arr}\n"
            f"做法：把下标 {pos} 后面的元素都往前移一位，覆盖掉 {removed}，数组长度减一。"
        )
