#ifndef DS_PLATFORM_MENU_UI_H
#define DS_PLATFORM_MENU_UI_H

#include "plugin_manager.h"

/* 基础文本菜单 UI：列出插件、接收选择、调用 run()，循环直至用户选择退出。 */
void menu_ui_run(PluginManager *pm);

#endif /* DS_PLATFORM_MENU_UI_H */
