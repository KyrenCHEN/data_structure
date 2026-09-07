# 数据结构实验插件平台（C 版）

不熟悉命令行？用 VSCode 打开这个文件夹，按 `F5` 即可自动编译并运行，详见 [`../docs/vscode_setup.md`](../docs/vscode_setup.md)。

命令行方式：
```bash
make run
```

依赖：`gcc`、`make`、`dlopen`（Linux/macOS 原生支持；Windows 必须用 WSL，原生 Windows 没有 `dlopen`）。

插件为运行时动态加载的共享库（`.so`），核心程序改动无需重编译已有插件。

## 操作步骤

1. 运行后会看到一个文本菜单，插件按实验编号连续排列（分类会显示在插件名后面的括号里，如 `(E1)`）。
2. 输入插件前面的编号并回车进入该插件。
3. 按插件的提示输入一行文本（例如 `请输入一段文本（盘子数量 n，例如 4）:`），回车确认。
4. 结果直接打印在终端里；回到菜单后可以输入 `0` 退出。

```
============ 数据结构实验插件平台（C） ============
  [1] 汉诺塔求解（示例） (E1)
  [0] 退出
请输入编号: 1

-- 汉诺塔求解（示例） --
输入一段文本形式的盘子数量 n，输出递归求解的完整移动步骤。

请输入一段文本（盘子数量 n，例如 4）: 4
  第 1 步: A -> B
  第 2 步: A -> C
  ...
共 15 步（理论最少步数 2^n - 1）。
```

插件接口规范、如何新增插件、常见问题：见 [`../docs/student_manual.md`](../docs/student_manual.md)。
示例插件：[`plugins/example_recursion/recursion_plugin.c`](plugins/example_recursion/recursion_plugin.c)（E1 汉诺塔）。
