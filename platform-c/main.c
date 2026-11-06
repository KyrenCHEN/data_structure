#include <stdio.h>

#include "menu_ui.h"
#include "plugin_registry.h"

int main(void) {
    plugin_sort();
    printf("[main] 已加载 %d 个插件\n", plugin_count());

    menu_ui_run();
    return 0;
}
