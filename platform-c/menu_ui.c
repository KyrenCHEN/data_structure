#include "menu_ui.h"

#include <stdio.h>
#include <stdlib.h>

#include "plugin_registry.h"

static void print_menu(void) {
    int n = plugin_count();
    printf("\n============ 数据结构实验插件平台（C） ============\n");
    if (n == 0) {
        printf("没有发现任何插件。\n");
    }
    for (int i = 0; i < n; i++) {
        const PluginInfo *info = plugin_at(i);
        printf("  [%d] %-24s (%s)\n", i + 1, info->name, info->category);
    }
    printf("  [0] 退出\n");
    printf("请输入编号: ");
}

void menu_ui_run(void) {
    char line[32];
    while (1) {
        print_menu();
        if (!fgets(line, sizeof(line), stdin)) {
            break;
        }
        int choice = atoi(line);
        if (choice == 0) {
            break;
        }
        if (choice < 1 || choice > plugin_count()) {
            printf("无效选择。\n");
            continue;
        }
        const PluginInfo *info = plugin_at(choice - 1);
        printf("\n-- %s --\n%s\n\n", info->name, info->description);
        info->run();
    }
    printf("已退出。\n");
}
