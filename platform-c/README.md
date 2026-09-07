# 数据结构实验插件平台（C 版）

```bash
make run
```

依赖：`gcc`、`make`、`dlopen`（Linux/macOS 原生支持；Windows 建议用 WSL）。

插件为运行时动态加载的共享库（`.so`），核心程序改动无需重编译已有插件。
插件接口规范、如何新增插件、常见问题：见 [`../docs/student_manual.md`](../docs/student_manual.md)。
示例插件：[`plugins/example_recursion/recursion_plugin.c`](plugins/example_recursion/recursion_plugin.c)（E1.3 汉诺塔）。
