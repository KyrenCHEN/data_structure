/*
 * 实验三起始模板：二叉树遍历。
 *
 * 半成品，不是空白模板——输入解析、建树这些骨架已经搭好，核心算法逻辑
 * （标 TODO 的地方）留给你自己实现。复制整个目录到 plugins/ 下改个
 * 名字，照着 TODO 填完就行。
 *
 * 输入是一行带 # 占位符的层序序列，比如 1,2,3,4,5,#,6。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "plugin.h"
#include "visual.h"

#define MAX_NODES 256

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

static void run(void) {
    char line[1024];
    printf("请输入带 # 占位符的层序序列（例如 1,2,3,4,5,#,6）: ");
    if (!fgets(line, sizeof(line), stdin)) {
        printf("读取失败\n");
        return;
    }

    char *tokens[MAX_NODES];
    int count = 0;
    char *tok = strtok(line, ",\n");
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

static const PluginInfo info = {
    .name = "二叉树遍历（待完成）",   /* TODO: 改成你自己的插件名 */
    .category = "E3",
    .description = "一行输入：带 # 占位符的层序序列，例如 1,2,3,4,5,#,6",
    .run = run,
};

static void __attribute__((constructor)) register_self(void) {
    plugin_register(&info);
}
