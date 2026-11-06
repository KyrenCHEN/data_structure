# 数据结构实验插件平台（Python 版）

不熟悉命令行？用 VSCode 打开这个文件夹，打开 `main.py` 点右上角 ▶ 即可运行，详见 [`../docs/vscode_setup.md`](../docs/vscode_setup.md)。

命令行方式：
```bash
python3 main.py
```

依赖 Python 3.10 及以上，标准库 `tkinter`，不需要 `pip install`。提示找不到 `tkinter` 的话，Linux 下用包管理器装一下 `python3-tk`。

## 操作步骤

1. 打开某次课的菜单：顶部菜单栏按实验编号分组（`E1`、`E2`……），点开对应菜单能看到这次课所有已加载的插件。

   ![顶部菜单栏，点开菜单可以看到里面的插件](../docs/screenshots/python_ui_02_menu_open.png)

2. 选中一个插件：点菜单里的插件名，左侧出现这个插件的说明和一个纯文本输入框。

3. 准备输入：可以直接在输入框里打字，也可以点"填入示例"一键填入插件自带的示例，或者点"加载文本文件..."从一个 `.txt` 文件读入。

4. 运行：点"运行"，中间上方的画布显示可视化结果（如果插件调用了可视化工具），下方输出框显示文字结果。

   ![运行顺序表插入示例后，画布显示数组方格、输出框显示文字结果](../docs/screenshots/python_ui_04_demo_visual.png)

插件接口规范、可视化工具用法、常见问题见 [`../docs/student_manual.md`](../docs/student_manual.md)。

新插件从空白模板开始：[`template/plugin.py`](template/plugin.py)，复制到 `plugins/` 下改个名字即可。
不知道代码该怎么写，先看完整示例：[`plugins/example_insert/plugin.py`](plugins/example_insert/plugin.py)（顺序表插入，含可视化）、[`plugins/example_recursion/plugin.py`](plugins/example_recursion/plugin.py)（汉诺塔，无需可视化）。
