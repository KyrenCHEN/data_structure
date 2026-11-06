/*
 * 插件空白模板。
 *
 * 用法：把整个 template/ 目录复制到 plugins/ 下面，改个文件夹名字，
 * 再把下面几处 TODO 换成你自己的内容，重新编译（make run）即可。
 *
 * 注意：这个目录本身不会被编译进插件——Makefile 只编译 plugins/ 目录下的
 * 文件夹，template/ 不在 plugins/ 里面，就是专门留给你复制用的。
 */
#include <stdio.h>
#include "plugin.h"
/* 需要可视化的话，取消下一行注释： */
/* #include "visual.h" */

static void run(void) {
    char line[256];
    printf("请输入: ");
    if (!fgets(line, sizeof(line), stdin)) {
        printf("读取失败\n");
        return;
    }
    /* TODO：解析 line，执行你的算法逻辑，用 printf 输出结果。
     * 需要可视化的话，三选一（不需要就不用调用）：
     *   vis_draw_array(values, n, highlight_index)         数组方格
     *   vis_draw_bars(values, n)                           柱状图
     *   vis_draw_graph_edges(edges_a, edges_b, edge_count)  图（邻接表）
     */
    printf("还没有实现\n");
}

static const PluginInfo info = {
    .name = "我的插件",                      /* TODO：改成你的插件名字，别和同学的重复 */
    .category = "E1",                        /* TODO：改成对应的实验编号 */
    .description = "TODO：写一句话说明输入格式",
    .run = run,
};

/* __attribute__((constructor)) 让这个函数在 main() 之前自动执行，
 * 把插件信息注册进平台——不需要手动调用，也不需要改任何核心文件。 */
static void __attribute__((constructor)) register_self(void) {
    plugin_register(&info);
}
