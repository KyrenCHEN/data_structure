#include "plugin_registry.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PLUGINS 64

static const PluginInfo *g_plugins[MAX_PLUGINS];
static int g_count = 0;

void plugin_register(const PluginInfo *info) {
    if (g_count >= MAX_PLUGINS) {
        fprintf(stderr, "[plugin] 插件数量超过上限 %d，“%s” 未注册\n", MAX_PLUGINS, info->name);
        return;
    }
    g_plugins[g_count++] = info;
}

int plugin_count(void) {
    return g_count;
}

const PluginInfo *plugin_at(int index) {
    return g_plugins[index];
}

static int compare_plugins(const void *a, const void *b) {
    const PluginInfo *pa = *(const PluginInfo *const *)a;
    const PluginInfo *pb = *(const PluginInfo *const *)b;
    int cmp = strcmp(pa->category, pb->category);
    return cmp != 0 ? cmp : strcmp(pa->name, pb->name);
}

void plugin_sort(void) {
    qsort(g_plugins, (size_t)g_count, sizeof(g_plugins[0]), compare_plugins);
}
