#include "plugin_manager.h"

#include <dirent.h>
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>

static int has_so_suffix(const char *filename) {
    size_t len = strlen(filename);
    return len > 3 && strcmp(filename + len - 3, ".so") == 0;
}

int pm_load_dir(PluginManager *pm, const char *dir) {
    DIR *d = opendir(dir);
    if (!d) {
        fprintf(stderr, "[plugin_manager] 无法打开插件目录: %s\n", dir);
        return 0;
    }

    struct dirent *entry;
    while ((entry = readdir(d)) != NULL) {
        if (!has_so_suffix(entry->d_name)) {
            continue;
        }
        if (pm->count >= MAX_PLUGINS) {
            fprintf(stderr, "[plugin_manager] 已达到插件数量上限 %d\n", MAX_PLUGINS);
            break;
        }

        char path[512];
        snprintf(path, sizeof(path), "%s/%s", dir, entry->d_name);

        void *handle = dlopen(path, RTLD_NOW);
        if (!handle) {
            fprintf(stderr, "[plugin_manager] 加载失败 %s: %s\n", path, dlerror());
            continue;
        }

        dlerror(); /* 清空历史错误 */
        plugin_get_info_fn get_info = (plugin_get_info_fn)dlsym(handle, "plugin_get_info");
        char *err = dlerror();
        if (err != NULL || get_info == NULL) {
            fprintf(stderr, "[plugin_manager] %s 未导出 plugin_get_info: %s\n", path, err);
            dlclose(handle);
            continue;
        }

        const PluginInfo *info = get_info();
        if (info == NULL || info->abi_version != PLUGIN_ABI_VERSION) {
            fprintf(stderr, "[plugin_manager] %s ABI 版本不匹配，跳过\n", path);
            dlclose(handle);
            continue;
        }

        pm->items[pm->count].info = info;
        pm->items[pm->count].dl_handle = handle;
        pm->count++;
    }

    closedir(d);
    return pm->count;
}

void pm_unload_all(PluginManager *pm) {
    for (int i = 0; i < pm->count; i++) {
        dlclose(pm->items[i].dl_handle);
    }
    pm->count = 0;
}
