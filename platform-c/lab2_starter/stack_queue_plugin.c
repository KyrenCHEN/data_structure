/*
 * 实验二起始模板：表达式求值 + 循环队列。
 *
 * 半成品，不是空白模板——输入解析、数据结构骨架已经搭好，核心算法逻辑
 * （标 TODO 的地方）留给你自己实现。复制整个目录到 plugins/ 下改个
 * 名字，照着 TODO 填完就行。
 *
 * 两个算法封装在同一个插件里，用输入第一行区分：
 *   eval  -> 中缀表达式求值，第二行是表达式，比如 3+5*(2-1)
 *   queue -> 循环队列操作，第二行是容量，第三行是操作序列，
 *            用空格分隔，E<数字> 表示入队该数字，D 表示出队，
 *            比如 E1 E2 D E3 D D
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "plugin.h"
#include "visual.h"

#define MAX_TOKENS 128
#define MAX_QUEUE 64

/* ---------- 表达式求值 ---------- */

/* TODO: 返回运算符的优先级，+ - 低，* / 高，数字越大优先级越高。 */
static int precedence(char op) {
    (void)op;
    return 0;
}

/* TODO: 从 operator_stack 弹出一个运算符，从 operand_stack 弹出两个数字，
 * 算出结果后压回 operand_stack。注意顺序：先弹出的数字是右操作数，
 * 后弹出的是左操作数。*op_top 和 *opr_top 是栈里当前的元素个数，
 * 弹出元素记得对应减一，压入记得加一。
 */
static void apply_op(int *operand_stack, int *op_top, char *operator_stack, int *opr_top) {
    (void)operand_stack;
    (void)op_top;
    (void)operator_stack;
    (void)opr_top;
}

static void eval_expr(const char *expr) {
    int operand_stack[MAX_TOKENS];
    int op_top = 0;   /* 栈里当前有 op_top 个数字 */
    char operator_stack[MAX_TOKENS];
    int opr_top = 0;  /* 栈里当前有 opr_top 个运算符/括号 */

    int i = 0;
    int len = (int)strlen(expr);

    while (i < len) {
        char ch = expr[i];

        if (isspace((unsigned char)ch)) {
            i++;
            continue;
        }

        if (isdigit((unsigned char)ch)) {
            int val = 0;
            while (i < len && isdigit((unsigned char)expr[i])) {
                val = val * 10 + (expr[i] - '0');
                i++;
            }
            operand_stack[op_top++] = val;
            continue;
        }

        if (ch == '(') {
            operator_stack[opr_top++] = ch;
            i++;
            continue;
        }

        if (ch == ')') {
            /* TODO: 不断 apply_op()，直到弹出一个左括号 '(' 为止
             * （那个左括号弹出来之后就扔掉，不用压回去）。
             */
            i++;
            continue;
        }

        if (ch == '+' || ch == '-' || ch == '*' || ch == '/') {
            /* TODO: 只要 opr_top > 0、栈顶不是 '('、并且栈顶运算符的
             * 优先级 >= ch 的优先级，就先 apply_op()，直到不满足为止，
             * 再把 ch 压进 operator_stack（operator_stack[opr_top++] = ch）。
             */
            i++;
            continue;
        }

        printf("无法识别的字符: %c\n", ch);
        return;
    }

    /* TODO: 表达式扫描完了，operator_stack 里可能还剩运算符，
     * 不断 apply_op() 把它们都算完，最后 operand_stack 里剩的
     * 那一个数就是最终结果（operand_stack[0]）。
     */

    if (op_top > 0) {
        vis_draw_array(operand_stack, op_top, -1);  /* 把最终的操作数栈画出来 */
    }

    printf("结果: TODO\n");
}

/* ---------- 循环队列 ---------- */

static void run_queue(int capacity, char *ops) {
    if (capacity <= 0 || capacity > MAX_QUEUE) {
        printf("容量不对\n");
        return;
    }

    int queue[MAX_QUEUE];
    int front = 0;   /* 队头元素的下标 */
    int count = 0;   /* 当前队列里有几个元素，用它判断队空/队满最不容易出错 */

    char *tok = strtok(ops, " \n");
    while (tok) {
        if (tok[0] == 'E') {
            int value = atoi(tok + 1);
            /* TODO: 如果 count == capacity，说明队满，打印
             * "入队 %d 失败：队满\n" 然后跳过这个 token。没满的话，
             * 算出新元素应该放的下标（提示：(front + count) % capacity），
             * 放进 queue，count 加一，打印 "入队 %d\n"。
             */
            printf("入队 %d（还没实现）\n", value);
        } else if (tok[0] == 'D') {
            /* TODO: 如果 count == 0，说明队空，打印 "出队失败：队空\n"
             * 然后跳过。没空的话，取出 queue[front]，front 往前移一位
             * （提示：front = (front + 1) % capacity），count 减一，
             * 打印 "出队 %d\n" 和取出来的值。
             */
            printf("出队（还没实现）\n");
        } else {
            printf("看不懂的操作: %s\n", tok);
        }
        tok = strtok(NULL, " \n");
    }

    if (count > 0) {
        vis_draw_array(queue, capacity, front);
    }

    /* TODO: 把队列里剩下的 count 个元素，从 front 开始按顺序打印出来，
     * 替换掉下面这行。
     */
    printf("最终队列（从队头开始）: TODO\n");
}

/* ---------- 入口 ---------- */

static void run(void) {
    char op[32];
    printf("请输入操作（eval 或 queue）: ");
    if (!fgets(op, sizeof(op), stdin)) {
        printf("读取失败\n");
        return;
    }
    op[strcspn(op, "\n")] = '\0';

    if (strcmp(op, "eval") == 0) {
        char expr[256];
        printf("请输入中缀表达式（例如 3+5*(2-1)）: ");
        if (!fgets(expr, sizeof(expr), stdin)) {
            printf("读取失败\n");
            return;
        }
        expr[strcspn(expr, "\n")] = '\0';
        eval_expr(expr);
    } else if (strcmp(op, "queue") == 0) {
        char cap_line[32];
        char ops_line[256];
        printf("请输入队列容量: ");
        if (!fgets(cap_line, sizeof(cap_line), stdin)) {
            printf("读取失败\n");
            return;
        }
        printf("请输入操作序列，用空格分隔（例如 E1 E2 D E3）: ");
        if (!fgets(ops_line, sizeof(ops_line), stdin)) {
            printf("读取失败\n");
            return;
        }
        run_queue(atoi(cap_line), ops_line);
    } else {
        printf("不认识的操作：%s，只能输入 eval 或 queue\n", op);
    }
}

static const PluginInfo info = {
    .name = "表达式求值与循环队列（待完成）",   /* TODO: 改成你自己的插件名 */
    .category = "E2",
    .description = "第一行 eval 或 queue，eval 后面跟表达式，queue 后面跟容量和操作序列。",
    .run = run,
};

static void __attribute__((constructor)) register_self(void) {
    plugin_register(&info);
}
