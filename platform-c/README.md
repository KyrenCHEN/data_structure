# 数据结构实验插件平台（C 版）

不熟悉命令行？用 VSCode 打开这个文件夹，按 `F5` 即可自动编译并运行，详见 [`../docs/vscode_setup.md`](../docs/vscode_setup.md)。

命令行方式：
```bash
make run
```

依赖：`gcc`、`make`、`dlopen`（Linux/macOS 原生支持；Windows 必须用 WSL，原生 Windows 没有 `dlopen`）。

插件为运行时动态加载的共享库（`.so`），核心程序改动无需重编译已有插件。
插件接口规范、如何新增插件、常见问题：见 [`../docs/student_manual.md`](../docs/student_manual.md)。
示例插件：[`plugins/example_recursion/recursion_plugin.c`](plugins/example_recursion/recursion_plugin.c)（E1.3 汉诺塔）。
