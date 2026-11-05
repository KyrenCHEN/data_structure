/*
 * 插件模板：平台组件演示（新插件从这里开始）。
 *
 * 把以后各次实验可能用到的组件演示了一遍：解析逗号分隔的数字、
 * 数组方格画法、柱状图画法、图的邻接表画法、文字输出。
 *
 * 写自己的插件时：
 *   1. 复制 plugins/example_demo/ 整个目录，改个名字（比如 plugins/sort_1234/）。
 *   2. 把下面用不到的部分删掉，只留你需要的那一种画法。
 *   3. 把 run() 里面的逻辑换成你自己的算法。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "plugin.h"
#include "visual.h"

#define MAX_VALUES 32
#define MAX_EDGES 32

static void run(void) {
    char line[256];
    int values[MAX_VALUES];
    int n = 0;

    /* ---- 1. 读入一组数字 ---- */
    printf("请输入一组数字，用逗号分隔（例如 5,3,8,1,9）: ");
    if (!fgets(line, sizeof(line), stdin)) {
        printf("读取失败\n");
        return;
    }
    char *tok = strtok(line, ",\n");
    while (tok && n < MAX_VALUES) {
        values[n++] = atoi(tok);
        tok = strtok(NULL, ",\n");
    }
    if (n == 0) {
        printf("没有读到任何数字\n");
        return;
    }

    /* ---- 2. 可视化：下面两种画法都试一下，不需要的删掉 ---- */
    printf("\n数组方格画法：\n");
    vis_draw_array(values, n, 0);

    printf("\n柱状图画法：\n");
    vis_draw_bars(values, n);

    int max_v = values[0];
    int min_v = values[0];
    for (int i = 1; i < n; i++) {
        if (values[i] > max_v) max_v = values[i];
        if (values[i] < min_v) min_v = values[i];
    }
    printf("\n最大值: %d  最小值: %d\n", max_v, min_v);

    /* ---- 3.（可选）读入图的边，演示图的画法 ---- */
    printf("\n（可选）请输入图的边，格式 A-B,B-C，直接回车跳过: ");
    if (fgets(line, sizeof(line), stdin) && line[0] != '\n') {
        char *edges_a[MAX_EDGES];
        char *edges_b[MAX_EDGES];
        int ecount = 0;
        char *pair = strtok(line, ",\n");
        while (pair && ecount < MAX_EDGES) {
            char *dash = strchr(pair, '-');
            if (dash) {
                *dash = '\0';
                edges_a[ecount] = pair;
                edges_b[ecount] = dash + 1;
                ecount++;
            }
            pair = strtok(NULL, ",\n");
        }
        printf("\n图的邻接表画法：\n");
        vis_draw_graph_edges((const char *const *)edges_a, (const char *const *)edges_b, ecount);
    }
}

static const PluginInfo info = {
    .abi_version = PLUGIN_ABI_VERSION,
    .name = "平台组件演示（新插件模板）",
    .category = "E0",
    .description = "依次演示数组方格、柱状图、图的邻接表画法，复制本目录开始写自己的插件。",
    .run = run,
};

const PluginInfo *plugin_get_info(void) {
    return &info;
}
