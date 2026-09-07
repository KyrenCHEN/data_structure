/*
 * 插件接口规范（C 版）。
 * 每个插件编译为独立的共享库（.so），必须导出函数：
 *     const PluginInfo *plugin_get_info(void);
 * 平台通过 dlopen/dlsym 在运行时动态加载，核心程序无需重新编译。
 */
#ifndef DS_PLATFORM_PLUGIN_H
#define DS_PLATFORM_PLUGIN_H

#define PLUGIN_ABI_VERSION 1

typedef struct {
    int abi_version;        /* 必须等于 PLUGIN_ABI_VERSION */
    const char *name;       /* 插件名称，UI 中显示 */
    const char *category;   /* 分类，如 "E1.3 递归算法" */
    const char *description;/* 一句话描述/用法提示 */
    void (*run)(void);      /* 交互式入口：自行 scanf 输入、printf 输出 */
} PluginInfo;

typedef const PluginInfo *(*plugin_get_info_fn)(void);

#endif /* DS_PLATFORM_PLUGIN_H */
