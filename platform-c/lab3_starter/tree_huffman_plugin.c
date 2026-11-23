/*
 * 实验三起始模板：二叉树遍历 + 哈夫曼树编码。
 *
 * 半成品，不是空白模板——输入解析、建树这些骨架已经搭好，核心算法逻辑
 * （标 TODO 的地方）留给你自己实现。复制整个目录到 plugins/ 下改个
 * 名字，照着 TODO 填完就行。
 *
 * 两个算法封装在同一个插件里，用输入第一行区分：
 *   traverse -> 二叉树遍历，第二行是带 # 占位符的层序序列，
 *               比如 1,2,3,4,5,#,6
 *   huffman  -> 哈夫曼编码，第二行是 字符:权值 用逗号分隔，
 *               比如 a:5,b:9,c:12，第三行是要用生成的编码表
 *               编码的一个字符串，比如 abc
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "plugin.h"
#include "visual.h"

#define MAX_NODES 256

/* ---------- 二叉树 ---------- */

typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static TreeNode tree_arena[MAX_NODES];
static int tree_node_count;

static TreeNode *new_tree_node(int val) {
    TreeNode *n = &tree_arena[tree_node_count++];
    n->val = val;
    n->left = NULL;
    n->right = NULL;
    return n;
}

/* 按层序序列（带 # 占位符）建树，已经写好，不用改。
 * tokens 是按逗号拆出来的字符串数组，count 是元素个数。
 * 用一个队列记录"还需要给它分配左右孩子"的节点，这是建树最标准的写法。
 */
static TreeNode *build_tree(char **tokens, int count) {
    tree_node_count = 0;
    if (count == 0 || strcmp(tokens[0], "#") == 0) {
        return NULL;
    }

    TreeNode *root = new_tree_node(atoi(tokens[0]));
    TreeNode *queue[MAX_NODES];
    int qhead = 0, qtail = 0;
    queue[qtail++] = root;

    int i = 1;
    while (qhead < qtail && i < count) {
        TreeNode *node = queue[qhead++];

        if (i < count) {
            if (strcmp(tokens[i], "#") != 0) {
                node->left = new_tree_node(atoi(tokens[i]));
                queue[qtail++] = node->left;
            }
            i++;
        }

        if (i < count) {
            if (strcmp(tokens[i], "#") != 0) {
                node->right = new_tree_node(atoi(tokens[i]));
                queue[qtail++] = node->right;
            }
            i++;
        }
    }

    return root;
}

/* TODO: 前序遍历——先访问根节点（把 root->val 存进 out[(*n)++]），
 * 再递归处理左子树，再递归处理右子树。root 为 NULL 时直接返回。
 */
static void preorder(TreeNode *root, int *out, int *n) {
    (void)root;
    (void)out;
    (void)n;
}

/* TODO: 中序遍历——先递归处理左子树，再访问根节点，再递归处理右子树。 */
static void inorder(TreeNode *root, int *out, int *n) {
    (void)root;
    (void)out;
    (void)n;
}

/* TODO: 层序遍历——用一个数组当队列，从根节点开始，每取出一个节点就把
 * 它的值存进 out[(*n)++]，再把它的左右孩子（存在的话）依次放进队列，
 * 直到队列空了为止。
 */
static void levelorder(TreeNode *root, int *out, int *n) {
    (void)root;
    (void)out;
    (void)n;
}

static void run_traverse(char *seq_line) {
    char *tokens[MAX_NODES];
    int count = 0;
    char *tok = strtok(seq_line, ",\n");
    while (tok && count < MAX_NODES) {
        tokens[count++] = tok;
        tok = strtok(NULL, ",\n");
    }

    TreeNode *root = build_tree(tokens, count);
    if (!root) {
        printf("空树\n");
        return;
    }

    int pre[MAX_NODES], pre_n = 0;
    int ino[MAX_NODES], ino_n = 0;
    int level[MAX_NODES], level_n = 0;
    preorder(root, pre, &pre_n);
    inorder(root, ino, &ino_n);
    levelorder(root, level, &level_n);

    if (level_n > 0) {
        vis_draw_array(level, level_n, -1);
    }

    printf("前序: ");
    for (int i = 0; i < pre_n; i++) printf("%d ", pre[i]);
    printf("\n中序: ");
    for (int i = 0; i < ino_n; i++) printf("%d ", ino[i]);
    printf("\n层序: ");
    for (int i = 0; i < level_n; i++) printf("%d ", level[i]);
    printf("\n");
}

/* ---------- 哈夫曼编码 ---------- */

typedef struct HNode {
    char ch;        /* 叶子节点才有意义，内部节点存 '\0' */
    int weight;
    int is_leaf;
    struct HNode *left;
    struct HNode *right;
} HNode;

static HNode hnode_arena[MAX_NODES];
static int hnode_count;

static HNode *new_hnode(char ch, int weight, int is_leaf, HNode *left, HNode *right) {
    HNode *n = &hnode_arena[hnode_count++];
    n->ch = ch;
    n->weight = weight;
    n->is_leaf = is_leaf;
    n->left = left;
    n->right = right;
    return n;
}

static HNode *build_huffman(HNode **active, int active_count) {
    hnode_count = 0;

    /* TODO: 构造哈夫曼树。思路：只要 active_count 还不止 1，就从
     * active[0..active_count-1] 里找出权值最小的两个，用 new_hnode('\0',
     * 两者权值之和, 0, 较小的, 较大的) 合并成一个新节点（建议权值小的
     * 放 left 对应编码 0，大的放 right 对应编码 1），把这两个从 active
     * 数组里删掉、新节点加进去，active_count 减一，重复直到只剩一个——
     * 那就是哈夫曼树的根。
     * 下面这行先占位，填完上面的逻辑后换成真正的根节点。
     */
    return active_count > 0 ? active[0] : NULL;
}

typedef struct {
    char ch;
    char code[MAX_NODES];
} CodeEntry;

/* TODO: node 是叶子节点（node->is_leaf）就把 path 记进
 * codes[(*n)]（ch 设成 node->ch，code 拷贝 path），(*n) 加一；不是
 * 叶子就递归处理左右孩子，往左孩子传 path 后面接 '0'，往右孩子传
 * path 后面接 '1'（注意给新路径加上结尾的 '\0'）。
 */
static void collect_codes(HNode *node, char *path, int depth, CodeEntry *codes, int *n) {
    (void)node;
    (void)path;
    (void)depth;
    (void)codes;
    (void)n;
}

static int code_entry_cmp(const void *a, const void *b) {
    return ((const CodeEntry *)a)->ch - ((const CodeEntry *)b)->ch;
}

static void run_huffman(char *weights_line, char *text_line) {
    HNode *active[MAX_NODES];
    int active_count = 0;

    char *tok = strtok(weights_line, ",\n");
    while (tok) {
        char ch = tok[0];
        char *colon = strchr(tok, ':');
        if (!colon) {
            printf("格式不对：%s\n", tok);
            return;
        }
        int weight = atoi(colon + 1);
        active[active_count++] = new_hnode(ch, weight, 1, NULL, NULL);
        tok = strtok(NULL, ",\n");
    }

    HNode *root = build_huffman(active, active_count);

    CodeEntry codes[MAX_NODES];
    int code_count = 0;
    char path[MAX_NODES];
    collect_codes(root, path, 0, codes, &code_count);

    if (code_count == 0) {
        printf("哈夫曼树还没实现\n");
        return;
    }

    qsort(codes, code_count, sizeof(CodeEntry), code_entry_cmp);

    int lengths[MAX_NODES];
    for (int i = 0; i < code_count; i++) {
        printf("%c: %s\n", codes[i].ch, codes[i].code);
        lengths[i] = (int)strlen(codes[i].code);
    }
    vis_draw_array(lengths, code_count, -1);

    text_line[strcspn(text_line, "\n")] = '\0';
    printf("编码 \"%s\" 的结果: ", text_line);
    for (size_t i = 0; i < strlen(text_line); i++) {
        int found = 0;
        for (int j = 0; j < code_count; j++) {
            if (codes[j].ch == text_line[i]) {
                printf("%s", codes[j].code);
                found = 1;
                break;
            }
        }
        if (!found) {
            printf("\n字符串里有没见过的字符: %c\n", text_line[i]);
            return;
        }
    }
    printf("\n");
}

/* ---------- 入口 ---------- */

static void run(void) {
    char op[32];
    printf("请输入操作（traverse 或 huffman）: ");
    if (!fgets(op, sizeof(op), stdin)) {
        printf("读取失败\n");
        return;
    }
    op[strcspn(op, "\n")] = '\0';

    if (strcmp(op, "traverse") == 0) {
        char seq[1024];
        printf("请输入带 # 占位符的层序序列（例如 1,2,3,4,5,#,6）: ");
        if (!fgets(seq, sizeof(seq), stdin)) {
            printf("读取失败\n");
            return;
        }
        run_traverse(seq);
    } else if (strcmp(op, "huffman") == 0) {
        char weights[1024];
        char text[256];
        printf("请输入字符:权值，逗号分隔（例如 a:5,b:9,c:12）: ");
        if (!fgets(weights, sizeof(weights), stdin)) {
            printf("读取失败\n");
            return;
        }
        printf("请输入要编码的字符串: ");
        if (!fgets(text, sizeof(text), stdin)) {
            printf("读取失败\n");
            return;
        }
        run_huffman(weights, text);
    } else {
        printf("不认识的操作：%s，只能输入 traverse 或 huffman\n", op);
    }
}

static const PluginInfo info = {
    .name = "二叉树遍历与哈夫曼编码（待完成）",   /* TODO: 改成你自己的插件名 */
    .category = "E3",
    .description = "第一行 traverse 或 huffman。traverse 后面跟带 # 占位符的层序序列；"
                   "huffman 后面跟字符:权值表和要编码的字符串。",
    .run = run,
};

static void __attribute__((constructor)) register_self(void) {
    plugin_register(&info);
}
