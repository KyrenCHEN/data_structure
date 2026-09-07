#ifndef DS_PLATFORM_PLUGIN_MANAGER_H
#define DS_PLATFORM_PLUGIN_MANAGER_H

#include "plugin.h"

#define MAX_PLUGINS 64

typedef struct {
    const PluginInfo *info;
    void *dl_handle;
} LoadedPlugin;

typedef struct {
    LoadedPlugin items[MAX_PLUGINS];
    int count;
} PluginManager;

/* 扫描 dir 目录下所有 .so 文件并尝试加载，返回成功加载的数量。 */
int pm_load_dir(PluginManager *pm, const char *dir);

/* 卸载全部插件、关闭 dlopen 句柄。 */
void pm_unload_all(PluginManager *pm);

#endif /* DS_PLATFORM_PLUGIN_MANAGER_H */
