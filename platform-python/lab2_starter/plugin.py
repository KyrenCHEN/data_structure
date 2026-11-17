"""实验二起始模板：表达式求值 + 循环队列。

半成品，不是空白模板——输入解析、数据结构骨架已经搭好，核心算法逻辑
（标 TODO 的地方）留给你自己实现。复制整个目录到 plugins/ 下改个名字，
照着 TODO 填完就行。

两个算法封装在同一个插件里，用输入第一行区分：
  eval  -> 中缀表达式求值，第二行是表达式，比如 3+5*(2-1)
  queue -> 循环队列操作，第二行是容量，第三行是操作序列，
           用空格分隔，E<数字> 表示入队该数字，D 表示出队，
           比如 E1 E2 D E3 D D
"""

from plugin_base import Plugin


class StackQueuePlugin(Plugin):
    name = "表达式求值与循环队列（待完成）"   # TODO: 改成你自己的插件名
    category = "E2"
    description = (
        "第一行写 eval 或 queue。\n"
        "eval：第二行是中缀表达式，支持 + - * / 和括号，例如 3+5*(2-1)\n"
        "queue：第二行是队列容量，第三行是操作序列（空格分隔），"
        "E<数字> 表示入队该数字，D 表示出队，例如 E1 E2 D E3 D D"
    )

    def example_input(self):
        return "eval\n3+5*(2-1)"

    def run(self, text, vis):
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        if not lines:
            return "输入不能为空"

        op = lines[0].lower()
        if op == "eval":
            if len(lines) != 2:
                return "eval 需要两行：第一行 eval，第二行是表达式"
            return self._eval(lines[1], vis)
        elif op == "queue":
            if len(lines) != 3:
                return "queue 需要三行：第一行 queue，第二行容量，第三行操作序列"
            return self._queue(lines[1], lines[2], vis)
        else:
            return f"不认识的操作：{lines[0]}，第一行只能写 eval 或 queue"

    # ---------- 表达式求值 ----------

    def _tokenize(self, expr):
        """把表达式字符串拆成 token 列表，数字、运算符、括号各自一个元素。
        这部分已经写好，不用改。
        """
        tokens = []
        i = 0
        while i < len(expr):
            ch = expr[i]
            if ch.isspace():
                i += 1
                continue
            if ch.isdigit():
                j = i
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                tokens.append(expr[i:j])
                i = j
            elif ch in "+-*/()":
                tokens.append(ch)
                i += 1
            else:
                raise ValueError(f"无法识别的字符: {ch}")
        return tokens

    def _eval(self, expr, vis):
        try:
            tokens = self._tokenize(expr)
        except ValueError as exc:
            return str(exc)

        operand_stack = []   # 存数字
        operator_stack = []  # 存运算符和左括号

        def precedence(op):
            # TODO: 返回运算符的优先级，+ - 低，* / 高，
            # 数字越大优先级越高。括号不会传进来，不用管。
            pass

        def apply_op():
            # TODO: 从 operator_stack 弹出一个运算符，从 operand_stack 弹出两个数字，
            # 算出结果后压回 operand_stack。注意顺序：先弹出的数字是右操作数，
            # 后弹出的是左操作数。
            pass

        for tok in tokens:
            if tok.isdigit():
                operand_stack.append(int(tok))
            elif tok == "(":
                operator_stack.append(tok)
            elif tok == ")":
                # TODO: 不断 apply_op()，直到弹出一个左括号 "(" 为止
                # （那个左括号弹出来之后就扔掉，不用压回去）
                pass
            else:
                # tok 是 + - * / 中的一个
                # TODO: 只要 operator_stack 不是空的、栈顶也不是 "("、
                # 并且栈顶运算符的优先级 >= tok 的优先级，就先 apply_op()，
                # 直到不满足为止，再把 tok 压进 operator_stack。
                pass

        # TODO: 表达式扫描完了，operator_stack 里可能还剩运算符，
        # 不断 apply_op() 把它们都算完，最后 operand_stack 里剩的
        # 那一个数就是最终结果。

        if operand_stack and vis:
            vis.draw_array(operand_stack)  # 把最终的操作数栈画出来

        return "结果: TODO"  # TODO: 换成 operand_stack 里最后剩下的那个数

    # ---------- 循环队列 ----------

    def _queue(self, cap_line, ops_line, vis):
        try:
            capacity = int(cap_line)
        except ValueError:
            return "容量必须是整数"

        queue = [0] * capacity
        front = 0   # 队头元素的下标
        count = 0   # 当前队列里有几个元素，用它判断队空/队满最不容易出错

        log = []

        for op in ops_line.split():
            if op.startswith("E"):
                try:
                    value = int(op[1:])
                except ValueError:
                    return f"看不懂的入队操作: {op}"
                # TODO: 如果 count == capacity，说明队满，记一条
                # "入队 {value} 失败：队满" 到 log，然后 continue。
                # 没满的话，算出新元素应该放的下标（提示：(front + count) % capacity），
                # 放进 queue，count 加一，记一条 "入队 {value}" 到 log。
                log.append(f"入队 {value}（还没实现）")
            elif op == "D":
                # TODO: 如果 count == 0，说明队空，记一条 "出队失败：队空" 到 log，
                # 然后 continue。没空的话，取出 queue[front]，front 往前移一位
                # （提示：front = (front + 1) % capacity），count 减一，
                # 记一条 "出队 {取出的值}" 到 log。
                log.append("出队（还没实现）")
            else:
                return f"看不懂的操作: {op}"

        if vis:
            vis.draw_array(queue, highlight={front})

        # TODO: 把队列里剩下的 count 个元素，从 front 开始按顺序列出来，
        # 替换掉下面这行的 "TODO"
        log.append("最终队列（从队头开始）: TODO")
        return "\n".join(log)
