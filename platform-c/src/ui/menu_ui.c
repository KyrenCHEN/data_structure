#include "menu_ui.h"

#include <stdio.h>
#include <stdlib.h>

static void print_menu(const PluginManager *pm) {
    printf("\n============ 数据结构实验插件平台（C） ============\n");
    if (pm->count == 0) {
        printf("未发现任何插件，请检查 plugins_bin/ 目录。\n");
    }
    for (int i = 0; i < pm->count; i++) {
        const PluginInfo *info = pm->items[i].info;
        printf("  [%d] %-24s (%s)\n", i + 1, info->name, info->category);
    }
    printf("  [0] 退出\n");
    printf("请输入编号: ");
}

void menu_ui_run(PluginManager *pm) {
    char line[32];
    while (1) {
        print_menu(pm);
        if (!fgets(line, sizeof(line), stdin)) {
            break;
        }
        int choice = atoi(line);
        if (choice == 0) {
            break;
        }
        if (choice < 1 || choice > pm->count) {
            printf("无效选择。\n");
            continue;
        }
        const PluginInfo *info = pm->items[choice - 1].info;
        printf("\n-- %s --\n%s\n\n", info->name, info->description);
        info->run();
    }
    printf("已退出。\n");
}
