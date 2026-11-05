/*
 * 示例插件：汉诺塔（递归）。作为 E1.3 的参考实现。
 * 学生完成 E1.3 时应新建 plugins/hanoi_myname/ 目录，不要直接修改本文件。
 *
 * 约定：所有插件都用"整行文本"作为输入——先用 fgets 读一整行，
 * 再自己解析成需要的数据。这样比逐个用 scanf 读数字更简单、更不容易出 bug。
 */
#include <stdio.h>
#include <stdlib.h>

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
    char line[256];
    printf("请输入一段文本（盘子数量 n，例如 4）: ");
    if (!fgets(line, sizeof(line), stdin)) {
        printf("读取输入失败。\n");
        return;
    }

    int n = atoi(line);   /* atoi 遇到无法识别的内容会返回 0，正好用来判断输入是否合法 */
    if (n < 1) {
        printf("输入无效，请输入一个正整数。\n");
        return;
    }

    move_count = 0;
    hanoi(n, 'A', 'B', 'C');
    printf("共 %ld 步（理论最少步数 2^n - 1）。\n", move_count);
}

static const PluginInfo info = {
    .abi_version = PLUGIN_ABI_VERSION,
    .name = "汉诺塔求解（示例）",
    .category = "E1",
    .description = "输入一段文本形式的盘子数量 n，输出递归求解的完整移动步骤。",
    .run = run,
};

const PluginInfo *plugin_get_info(void) {
    return &info;
}
