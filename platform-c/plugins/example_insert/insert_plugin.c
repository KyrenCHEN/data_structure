/*
 * 示例插件：顺序表（数组）插入。
 *
 * 这是一个完整实现的算法示例，用来演示插件应该写成什么样子——
 * 照着这个结构写自己的插件就行。不知道从哪下手时先看这个文件，
 * 比看 template/ 空模板更直观。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "plugin.h"
#include "visual.h"

#define MAX_N 64

static void run(void) {
    char line[256];
    int arr[MAX_N];
    int n = 0;

    printf("请输入原数组，用逗号分隔（例如 3,5,8,2,9）: ");
    if (!fgets(line, sizeof(line), stdin)) {
        printf("读取失败\n");
        return;
    }
    char *tok = strtok(line, ",\n");
    while (tok && n < MAX_N - 1) {   /* 留一个位置给插入的新值 */
        arr[n++] = atoi(tok);
        tok = strtok(NULL, ",\n");
    }

    printf("请输入插入位置和插入值，用逗号分隔（例如 2,100）: ");
    if (!fgets(line, sizeof(line), stdin)) {
        printf("读取失败\n");
        return;
    }
    int pos, val;
    if (sscanf(line, "%d,%d", &pos, &val) != 2) {
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

static const PluginInfo info = {
    .name = "顺序表插入（示例）",
    .category = "E2",
    .description = "依次输入原数组、插入位置和插入值，演示顺序表插入操作。",
    .run = run,
};

static void __attribute__((constructor)) register_self(void) {
    plugin_register(&info);
}
