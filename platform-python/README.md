# 数据结构实验插件平台（Python 版）

环境安装、第一次运行看 [`../docs/getting_started.md`](../docs/getting_started.md)。命令行方式：

```bash
cd platform-python
python3 main.py
```

依赖 Python 3.10 及以上、标准库 `tkinter`，不需要 `pip install`。

运行起来之后，顶部菜单栏按实验编号分组，点开菜单选一个插件，左侧填输入、点"运行"，结果和可视化显示在右侧：

![运行顺序表插入示例后，画布显示数组方格、输出框显示文字结果](../docs/screenshots/python_ui_04_demo_visual.png)

插件接口规范、怎么写自己的插件，看 [`../docs/student_manual.md`](../docs/student_manual.md)；平台内部原理看 [`../docs/architecture.md`](../docs/architecture.md)。

新插件从空白模板开始：[`template/plugin.py`](template/plugin.py)，复制到 `plugins/` 下改个名字即可。
不知道代码该怎么写，先看完整示例：[`plugins/example_insert/plugin.py`](plugins/example_insert/plugin.py)（顺序表插入，含可视化）。
