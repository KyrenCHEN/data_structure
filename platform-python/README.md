# 数据结构实验插件平台（Python 版）

不熟悉命令行？用 VSCode 打开这个文件夹，打开 `main.py` 点右上角 ▶ 即可运行，详见 [`../docs/vscode_setup.md`](../docs/vscode_setup.md)。

命令行方式：
```bash
python3 main.py
```

依赖：Python ≥ 3.10，标准库 `tkinter`（无需 `pip install`）。若提示找不到 `tkinter`，Linux 下用包管理器安装 `python3-tk`。

## 操作步骤

1. **打开某次课的菜单**：顶部菜单栏按实验编号分组（`E1`、`E2`……），点开对应菜单能看到这次课所有已加载的插件。

   ![顶部菜单栏，点开 E1 菜单可以看到里面的插件](../docs/screenshots/python_ui_02_menu_open.png)

2. **选中一个插件**：点菜单里的插件名，左侧会出现这个插件的说明和一个纯文本输入框。

3. **准备输入**：可以直接在输入框里打字，也可以点"填入示例"一键填入插件自带的示例，或者点"加载文本文件..."从一个 `.txt` 文件读入。

4. **运行**：点"运行"，结果会显示在中间的大输出框里（纯文本）。

   ![运行汉诺塔示例插件后，中间输出框显示完整的移动步骤](../docs/screenshots/python_ui_03_result.png)

插件接口规范、如何新增插件、常见问题：见 [`../docs/student_manual.md`](../docs/student_manual.md)。
示例插件：[`plugins/example_recursion/plugin.py`](plugins/example_recursion/plugin.py)（E1 汉诺塔，附带示例输入文件 `plugins/example_recursion/sample_input.txt`）。
