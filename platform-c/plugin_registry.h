#ifndef DS_PLATFORM_PLUGIN_REGISTRY_H
#define DS_PLATFORM_PLUGIN_REGISTRY_H

#include "plugin.h"

/* 已注册插件的数量。 */
int plugin_count(void);

/* 第 index 个插件（0 开始），需要先调用过 plugin_sort()。 */
const PluginInfo *plugin_at(int index);

/* 按 category 再按 name 排序，让同一次课的插件排在一起。 */
void plugin_sort(void);

#endif /* DS_PLATFORM_PLUGIN_REGISTRY_H */
