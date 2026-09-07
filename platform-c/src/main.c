#include <stdio.h>

#include "plugin_manager.h"
#include "menu_ui.h"

int main(int argc, char **argv) {
    const char *plugins_dir = (argc > 1) ? argv[1] : "plugins_bin";

    PluginManager pm = {0};
    int n = pm_load_dir(&pm, plugins_dir);
    printf("[main] 已从 %s 加载 %d 个插件\n", plugins_dir, n);

    menu_ui_run(&pm);

    pm_unload_all(&pm);
    return 0;
}
