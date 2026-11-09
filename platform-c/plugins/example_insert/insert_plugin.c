/*
 * 示例插件：顺序表（数组）插入与删除。
 *
 * 比较完整的示例，覆盖了插件平台大部分的能力：一行行读文本输入、
 * 可视化画布（数组方格 + 高亮）、文字结果输出，还演示了"一个插件里
 * 用输入第一行区分多个算法"这个约定的实际写法——这个约定以后每次
 * 实验都会用到。照着这个结构写自己的插件就行。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "plugin.h"
#include "visual.h"

#define MAX_N 64

static void do_insert(char *arr_line, char *pos_line) {
    int arr[MAX_N];
    int n = 0;
    char *tok = strtok(arr_line, ",\n");
    while (tok && n < MAX_N - 1) {   /* 留一个位置给插入的新值 */
        arr[n++] = atoi(tok);
        tok = strtok(NULL, ",\n");
    }

    int pos, val;
    if (sscanf(pos_line, "%d,%d", &pos, &val) != 2) {
        printf("格式不对，应该是“位置,插入值”\n");
        return;
    }
    if (pos < 0 || pos > n) {
        printf("插入位置 %d 超出范围，当前数组长度是 %d\n", pos, n);
        return;
    }

    /* 顺序表插入的核心逻辑：
     * 从数组末尾开始，把 pos 位置及其后面的元素依次往后挪一位，
     * 腾出 pos 这个位置，再把新值放进去。
     */
    n++;
    for (int i = n - 1; i > pos; i--) {
        arr[i] = arr[i - 1];
    }
    arr[pos] = val;

    printf("\n插入后的数组：\n");
    vis_draw_array(arr, n, pos);
    printf("\n做法：把下标 %d 开始的元素都往后移一位，腾出的位置放 %d。\n", pos, val);
}

static void do_delete(char *arr_line, char *pos_line) {
    int arr[MAX_N];
    int n = 0;
    char *tok = strtok(arr_line, ",\n");
    while (tok && n < MAX_N) {
        arr[n++] = atoi(tok);
        tok = strtok(NULL, ",\n");
    }

    int pos;
    if (sscanf(pos_line, "%d", &pos) != 1) {
        printf("格式不对，应该是一个下标\n");
        return;
    }
    if (pos < 0 || pos >= n) {
        printf("删除位置 %d 超出范围，当前数组长度是 %d\n", pos, n);
        return;
    }

    printf("\n删除前的数组：\n");
    vis_draw_array(arr, n, pos);
    int removed = arr[pos];

    /* 顺序表删除的核心逻辑：
     * 把 pos 后面的元素依次往前挪一位，覆盖掉 pos 这个位置，长度减一。
     */
    for (int i = pos; i < n - 1; i++) {
        arr[i] = arr[i + 1];
    }
    n--;

    printf("\n做法：把下标 %d 后面的元素都往前移一位，覆盖掉 %d，数组长度减一。\n", pos, removed);
    printf("删除后的数组：\n");
    vis_draw_array(arr, n, -1);
}

static void run(void) {
    char op[32];
    char arr_line[256];
    char pos_line[64];

    printf("请输入操作（insert 或 delete）: ");
    if (!fgets(op, sizeof(op), stdin)) {
        printf("读取失败\n");
        return;
    }
    op[strcspn(op, "\n")] = '\0';

    printf("请输入原数组，用逗号分隔（例如 3,5,8,2,9）: ");
    if (!fgets(arr_line, sizeof(arr_line), stdin)) {
        printf("读取失败\n");
        return;
    }

    if (strcmp(op, "insert") == 0) {
        printf("请输入插入位置和插入值，用逗号分隔（例如 2,100）: ");
        if (!fgets(pos_line, sizeof(pos_line), stdin)) {
            printf("读取失败\n");
            return;
        }
        do_insert(arr_line, pos_line);
    } else if (strcmp(op, "delete") == 0) {
        printf("请输入要删除的下标（例如 2）: ");
        if (!fgets(pos_line, sizeof(pos_line), stdin)) {
            printf("读取失败\n");
            return;
        }
        do_delete(arr_line, pos_line);
    } else {
        printf("不认识的操作：%s，只能输入 insert 或 delete\n", op);
    }
}

static const PluginInfo info = {
    .name = "顺序表插入与删除（示例）",
    .category = "E1",
    .description = "先输入 insert 或 delete 选择操作，再按提示输入数据。",
    .run = run,
};

static void __attribute__((constructor)) register_self(void) {
    plugin_register(&info);
}
