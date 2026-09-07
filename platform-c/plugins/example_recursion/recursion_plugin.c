/*
 * 示例插件：汉诺塔（递归）。作为 E1.3 的参考实现。
 * 学生完成 E1.3 时应新建 plugins/hanoi_myname/ 目录，不要直接修改本文件。
 */
#include <stdio.h>

#include "plugin.h"

static long move_count;

static void hanoi(int n, char src, char aux, char dst) {
    if (n == 0) {
        return;
    }
    hanoi(n - 1, src, dst, aux);
    move_count++;
    printf("  第 %ld 步: %c -> %c\n", move_count, src, dst);
    hanoi(n - 1, aux, src, dst);
}

static void run(void) {
    int n;
    printf("请输入盘子数量 n (建议 1~15): ");
    if (scanf("%d", &n) != 1 || n < 1) {
        printf("输入无效。\n");
        while (getchar() != '\n') { /* 清空输入缓冲 */ }
        return;
    }
    while (getchar() != '\n') { /* 清空残留换行 */ }

    move_count = 0;
    hanoi(n, 'A', 'B', 'C');
    printf("共 %ld 步（理论最少步数 2^n - 1）。\n", move_count);
}

static const PluginInfo info = {
    .abi_version = PLUGIN_ABI_VERSION,
    .name = "汉诺塔求解（示例）",
    .category = "E1.3 递归算法",
    .description = "输入盘子数量 n，输出递归求解的完整移动步骤。",
    .run = run,
};

const PluginInfo *plugin_get_info(void) {
    return &info;
}
