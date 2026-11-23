"""实验三起始模板：二叉树遍历。

半成品，不是空白模板——输入解析、建树这些骨架已经搭好，核心算法逻辑
（标 TODO 的地方）留给你自己实现。复制整个目录到 plugins/ 下改个名字，
照着 TODO 填完就行。

输入是一行带 # 占位符的层序序列，比如 1,2,3,4,5,#,6。
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


class TreeTraversalPlugin(Plugin):
    name = "二叉树遍历（待完成）"   # TODO: 改成你自己的插件名
    category = "E3"
    description = "一行输入：带 # 占位符的层序序列，例如 1,2,3,4,5,#,6"

    def example_input(self):
        return "1,2,3,4,5,#,6"

    def run(self, text, vis):
        line = text.strip()
        if not line:
            return "输入不能为空"

        tokens = line.split(",")
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
