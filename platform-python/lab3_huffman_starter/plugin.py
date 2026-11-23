"""实验三起始模板：哈夫曼树编码。

半成品，不是空白模板——权值解析这些骨架已经搭好，核心算法逻辑
（标 TODO 的地方）留给你自己实现。复制整个目录到 plugins/ 下改个名字，
照着 TODO 填完就行。

输入两行：第一行 字符:权值 用逗号分隔，比如 a:5,b:9,c:12；
第二行是要用生成的编码表编码的一个字符串，比如 abc。
"""

from plugin_base import Plugin


class HuffmanNode:
    def __init__(self, char=None, weight=0, left=None, right=None):
        self.char = char      # 叶子节点才有字符，内部节点是 None
        self.weight = weight
        self.left = left
        self.right = right


class HuffmanPlugin(Plugin):
    name = "哈夫曼编码（待完成）"   # TODO: 改成你自己的插件名
    category = "E3"
    description = (
        "第一行 字符:权值，逗号分隔，例如 a:5,b:9,c:12\n"
        "第二行是要编码的字符串，例如 abc"
    )

    def example_input(self):
        return "a:5,b:9,c:12\nabc"

    def run(self, text, vis):
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        if len(lines) != 2:
            return "需要两行：第一行字符:权值，第二行要编码的字符串"

        weights_line, text_to_encode = lines

        nodes = []
        for part in weights_line.split(","):
            ch, w = part.split(":")
            nodes.append(HuffmanNode(char=ch, weight=int(w)))

        # TODO: 构造哈夫曼树。思路：只要 nodes 里还剩不止一个节点，就找出
        # 权值最小的两个，合并成一个新节点（weight 是两者之和，char 留 None，
        # left/right 分别是那两个，建议权值小的放 left 对应编码 0，大的放
        # right 对应编码 1），把原来那两个从 nodes 里去掉、新节点加进去，
        # 重复直到 nodes 里只剩一个——那就是哈夫曼树的根。
        # 下面这行先占位，填完上面的逻辑后换成真正的根节点。
        root = nodes[0] if nodes else None

        codes = {}

        def collect(node, path):
            if node is None:
                return
            # TODO: node 是叶子节点（node.char 不是 None）就把 path 记进
            # codes[node.char]；不是叶子就递归处理左右孩子，往左孩子传
            # path + "0"，往右孩子传 path + "1"。
            pass

        collect(root, "")

        if not codes:
            return "哈夫曼树还没实现"

        lines_out = [f"{ch}: {code}" for ch, code in sorted(codes.items())]

        try:
            encoded = "".join(codes[ch] for ch in text_to_encode)
        except KeyError as exc:
            return f"字符串里有没见过的字符: {exc}"

        if vis:
            vis.draw_bars([len(c) for _, c in sorted(codes.items())])

        return "\n".join(lines_out) + f'\n编码 "{text_to_encode}" 的结果: {encoded}'
