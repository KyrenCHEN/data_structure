"""实验三起始模板：二叉树遍历 + 哈夫曼树编码。

半成品，不是空白模板——输入解析、建树这些骨架已经搭好，核心算法逻辑
（标 TODO 的地方）留给你自己实现。复制整个目录到 plugins/ 下改个名字，
照着 TODO 填完就行。

两个算法封装在同一个插件里，用输入第一行区分：
  traverse -> 二叉树遍历，第二行是带 # 占位符的层序序列，比如 1,2,3,4,5,#,6
  huffman  -> 哈夫曼编码，第二行是 字符:权值 用逗号分隔，比如 a:5,b:9,c:12，
              第三行是要用生成的编码表编码的一个字符串，比如 abc
"""

from plugin_base import Plugin


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def build_tree(tokens):
    """按层序序列（带 # 占位符）建树，已经写好，不用改。
    tokens 是按逗号拆好的字符串列表，比如 ["1","2","3","4","5","#","6"]。
    用一个队列记录"还需要给它分配左右孩子"的节点，这是建树最标准的写法。
    """
    if not tokens or tokens[0] == "#":
        return None

    root = TreeNode(int(tokens[0]))
    queue = [root]
    i = 1
    while queue and i < len(tokens):
        node = queue.pop(0)

        if i < len(tokens):
            left_val = tokens[i]
            i += 1
            if left_val != "#":
                node.left = TreeNode(int(left_val))
                queue.append(node.left)

        if i < len(tokens):
            right_val = tokens[i]
            i += 1
            if right_val != "#":
                node.right = TreeNode(int(right_val))
                queue.append(node.right)

    return root


class HuffmanNode:
    def __init__(self, char=None, weight=0, left=None, right=None):
        self.char = char      # 叶子节点才有字符，内部节点是 None
        self.weight = weight
        self.left = left
        self.right = right


class TreeHuffmanPlugin(Plugin):
    name = "二叉树遍历与哈夫曼编码（待完成）"   # TODO: 改成你自己的插件名
    category = "E3"
    description = (
        "第一行写 traverse 或 huffman。\n"
        "traverse：第二行是带 # 占位符的层序序列，例如 1,2,3,4,5,#,6\n"
        "huffman：第二行是 字符:权值，逗号分隔，例如 a:5,b:9,c:12；"
        "第三行是要编码的字符串，例如 abc"
    )

    def example_input(self):
        return "traverse\n1,2,3,4,5,#,6"

    def run(self, text, vis):
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        if not lines:
            return "输入不能为空"

        op = lines[0].lower()
        if op == "traverse":
            if len(lines) != 2:
                return "traverse 需要两行：第一行 traverse，第二行是层序序列"
            return self._traverse(lines[1], vis)
        elif op == "huffman":
            if len(lines) != 3:
                return "huffman 需要三行：第一行 huffman，第二行字符:权值，第三行要编码的字符串"
            return self._huffman(lines[1], lines[2], vis)
        else:
            return f"不认识的操作：{lines[0]}，第一行只能写 traverse 或 huffman"

    # ---------- 二叉树遍历 ----------

    def _preorder(self, root, result):
        # TODO: 前序遍历——先访问根节点（把 root.val 加进 result），
        # 再递归处理左子树，再递归处理右子树。root 为 None 时直接返回。
        pass

    def _inorder(self, root, result):
        # TODO: 中序遍历——先递归处理左子树，再访问根节点，再递归处理右子树。
        pass

    def _levelorder(self, root):
        # TODO: 层序遍历——用一个队列，从根节点开始，每弹出一个节点就把它的
        # 值加进结果列表，再把它的左右孩子（存在的话）依次放进队列，直到
        # 队列空了为止。返回访问顺序的列表。
        return []

    def _traverse(self, seq_line, vis):
        tokens = seq_line.split(",")
        root = build_tree(tokens)
        if root is None:
            return "空树"

        pre, ino = [], []
        self._preorder(root, pre)
        self._inorder(root, ino)
        level = self._levelorder(root)

        if level and vis:
            vis.draw_array(level)

        return f"前序: {pre}\n中序: {ino}\n层序: {level}"

    # ---------- 哈夫曼编码 ----------

    def _huffman(self, weights_line, text_to_encode, vis):
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

        lines = [f"{ch}: {code}" for ch, code in sorted(codes.items())]

        try:
            encoded = "".join(codes[ch] for ch in text_to_encode)
        except KeyError as exc:
            return f"字符串里有没见过的字符: {exc}"

        if vis:
            vis.draw_bars([len(c) for _, c in sorted(codes.items())])

        return "\n".join(lines) + f'\n编码 "{text_to_encode}" 的结果: {encoded}'
