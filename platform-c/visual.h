/*
 * 极简终端可视化工具（header-only，不用单独编译）。
 * 覆盖数据结构课最常用的三种"画法"，全部用字符画：
 *   vis_draw_array        数组方格，适合数组/栈/队列/排序中间状态
 *   vis_draw_bars         横向字符柱状图，适合排序/查找过程
 *   vis_draw_graph_edges  图的邻接表文字画法，适合图相关实验
 *
 * 用法：在插件的 .c 文件里 #include "visual.h" 直接调用，不需要额外链接。
 */
#ifndef DS_PLATFORM_VISUAL_H
#define DS_PLATFORM_VISUAL_H

#include <stdio.h>

static inline void vis_draw_array(const int *values, int n, int highlight) {
    for (int i = 0; i < n; i++) {
        printf(" %3d ", values[i]);
    }
    printf("\n");
    for (int i = 0; i < n; i++) {
        printf(i == highlight ? "  ^^  " : "      ");
    }
    printf("\n");
    for (int i = 0; i < n; i++) {
        printf(" [%2d]", i);
    }
    printf("\n");
}

static inline void vis_draw_bars(const int *values, int n) {
    for (int i = 0; i < n; i++) {
        printf("%3d | ", values[i]);
        for (int k = 0; k < values[i]; k++) {
            putchar('#');
        }
        printf("\n");
    }
}

static inline void vis_draw_graph_edges(const char *const *edges_a, const char *const *edges_b, int edge_count) {
    for (int i = 0; i < edge_count; i++) {
        printf("  %s -- %s\n", edges_a[i], edges_b[i]);
    }
}

#endif /* DS_PLATFORM_VISUAL_H */
