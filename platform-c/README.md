# 数据结构实验插件平台（C 版）

不熟悉命令行？用 VSCode 打开这个文件夹，按 `F5` 即可自动编译并运行，详见 [`../docs/vscode_setup.md`](../docs/vscode_setup.md)。

命令行方式：
```bash
make run
```

依赖 `gcc`、`make`。Windows 装一个 MinGW-w64 编译器即可，不需要 WSL，三大平台编译命令完全一样。

插件和核心代码一起编译成一个可执行文件，没有动态库、没有运行时加载；新增或改动插件后重新 `make run` 一次就行。

## 操作步骤

1. 运行后会看到一个文本菜单，插件按实验编号连续排列，分类显示在插件名后面的括号里，如 `(E1)`（`E0` 是入门演示，不算正式实验）。
2. 输入插件前面的编号并回车进入该插件。
3. 按插件的提示输入一行文本，回车确认，可视化结果和文字结果都直接打印在终端里。
4. 回到菜单后输入 `0` 退出。

```
============ 数据结构实验插件平台（C） ============
  [1] 汉诺塔求解（示例） (E0)
  [2] 顺序表插入（示例） (E1)
  [0] 退出
请输入编号: 2

-- 顺序表插入（示例） --
依次输入原数组、插入位置和插入值，演示顺序表插入操作。

请输入原数组，用逗号分隔（例如 3,5,8,2,9）: 3,5,8,2,9
请输入插入位置和插入值，用逗号分隔（例如 2,100）: 2,100

插入后的数组：
   3    5  100    8    2    9
              ^^
 [ 0] [ 1] [ 2] [ 3] [ 4] [ 5]

做法：把下标 2 开始的元素都往后移一位，腾出的位置放 100。
```

插件接口规范、可视化工具用法、常见问题见 [`../docs/student_manual.md`](../docs/student_manual.md)。

新插件从空白模板开始：[`template/plugin_template.c`](template/plugin_template.c)，复制到 `plugins/` 下改个名字即可。
不知道代码该怎么写，先看完整示例：[`plugins/example_insert/insert_plugin.c`](plugins/example_insert/insert_plugin.c)（顺序表插入，含可视化）、[`plugins/example_recursion/recursion_plugin.c`](plugins/example_recursion/recursion_plugin.c)（汉诺塔，无需可视化）。
