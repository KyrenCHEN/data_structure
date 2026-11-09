# 数据结构实验插件平台（C 版）

环境安装、第一次运行看 [`../docs/getting_started.md`](../docs/getting_started.md)。命令行方式：

```bash
cd platform-c
make run
```

依赖 `gcc`、`make`。插件和核心代码一起编译成一个可执行文件，没有动态库、没有运行时加载；新增或改动插件后重新 `make run` 一次就行。

运行起来之后是一个文字菜单，输入插件前面的编号进入，按提示输入一行文本，结果直接打印在终端里，`0` 退出：

```
============ 数据结构实验插件平台（C） ============
  [1] 顺序表插入与删除（示例） (E1)
  [0] 退出
请输入编号: 1

-- 顺序表插入与删除（示例） --
先输入 insert 或 delete 选择操作，再按提示输入数据。

请输入操作（insert 或 delete）: insert
请输入原数组，用逗号分隔（例如 3,5,8,2,9）: 3,5,8,2,9
请输入插入位置和插入值，用逗号分隔（例如 2,100）: 2,100

插入后的数组：
   3    5  100    8    2    9
              ^^
 [ 0] [ 1] [ 2] [ 3] [ 4] [ 5]

做法：把下标 2 开始的元素都往后移一位，腾出的位置放 100。
```

插件接口规范、怎么写自己的插件，看 [`../docs/student_manual.md`](../docs/student_manual.md)；平台内部原理看 [`../docs/architecture.md`](../docs/architecture.md)。

新插件从空白模板开始：[`template/plugin_template.c`](template/plugin_template.c)，复制到 `plugins/` 下改个名字即可。
不知道代码该怎么写，先看完整示例：[`plugins/example_insert/insert_plugin.c`](plugins/example_insert/insert_plugin.c)（顺序表插入与删除，含可视化）。
