/*
 * 实验三起始模板：哈夫曼树编码。
 *
 * 半成品，不是空白模板——权值解析这些骨架已经搭好，核心算法逻辑
 * （标 TODO 的地方）留给你自己实现。复制整个目录到 plugins/ 下改个
 * 名字，照着 TODO 填完就行。
 *
 * 输入两行：第一行 字符:权值 用逗号分隔，比如 a:5,b:9,c:12；
 * 第二行是要用生成的编码表编码的一个字符串，比如 abc。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "plugin.h"
#include "visual.h"

#define MAX_NODES 256

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

static void run(void) {
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

    HNode *active[MAX_NODES];
    int active_count = 0;

    char *tok = strtok(weights, ",\n");
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

    text[strcspn(text, "\n")] = '\0';
    printf("编码 \"%s\" 的结果: ", text);
    for (size_t i = 0; i < strlen(text); i++) {
        int found = 0;
        for (int j = 0; j < code_count; j++) {
            if (codes[j].ch == text[i]) {
                printf("%s", codes[j].code);
                found = 1;
                break;
            }
        }
        if (!found) {
            printf("\n字符串里有没见过的字符: %c\n", text[i]);
            return;
        }
    }
    printf("\n");
}

static const PluginInfo info = {
    .name = "哈夫曼编码（待完成）",   /* TODO: 改成你自己的插件名 */
    .category = "E3",
    .description = "第一行 字符:权值，逗号分隔；第二行要编码的字符串。",
    .run = run,
};

static void __attribute__((constructor)) register_self(void) {
    plugin_register(&info);
}
