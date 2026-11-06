/*
 * 插件接口规范（C 版）。
 *
 * 所有插件和核心程序一起编译成同一个可执行文件（没有 .so、没有 dlopen），
 * 新增插件后重新编译一次整个项目即可，Windows/Linux/macOS 做法完全一样。
 *
 * 插件靠 __attribute__((constructor)) 在 main() 之前自动把自己注册进平台，
 * 不需要改任何核心文件，写法照抄 template/plugin_template.c 即可。
 */
#ifndef DS_PLATFORM_PLUGIN_H
#define DS_PLATFORM_PLUGIN_H

typedef struct {
    const char *name;        /* 插件名称，菜单中显示 */
    const char *category;    /* 分类，如 "E1"、"E2"，同一类放进同一组 */
    const char *description; /* 一句话描述/用法提示 */
    void (*run)(void);       /* 交互式入口：自行 scanf/fgets 输入、printf 输出 */
} PluginInfo;

/* 把插件信息注册进平台，一般在 __attribute__((constructor)) 函数里调用一次。 */
void plugin_register(const PluginInfo *info);

#endif /* DS_PLATFORM_PLUGIN_H */
