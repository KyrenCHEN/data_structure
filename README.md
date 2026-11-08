# 数据结构实验课程 —— 插件式集成平台

学生第一次打开这个仓库，按顺序看：

1. [`docs/getting_started.md`](docs/getting_started.md) —— 环境安装、第一次把平台跑起来，跟着做就行
2. [`docs/student_manual.md`](docs/student_manual.md) —— 插件接口规范、怎么写自己的插件、常见问题
3. [`docs/architecture.md`](docs/architecture.md) —— 平台内部原理，选读，写插件不需要看这篇

其他文档：
- 课程设计（每次课讲什么、布置什么任务、验收标准，给老师看的）：[`docs/course_design.md`](docs/course_design.md)
- 图文讲解页（架构图 + 快速上手 + 课程时间线，一页纸总览）：[`docs/plugin_platform_guide.html`](docs/plugin_platform_guide.html)（下载后用浏览器打开，GitHub 网页只会显示源码不会渲染）
- Python 平台代码：[`platform-python/`](platform-python/)
- C 平台代码：[`platform-c/`](platform-c/)

两版平台都带一个空白模板（`template/`，复制去写自己的插件）和一个完整示例：`plugins/example_insert`（顺序表插入，含可视化）。

## 界面预览（Python 版）

| 顶部菜单栏（按实验分组） | 运行结果（含可视化画布） |
| --- | --- |
| ![菜单栏截图](docs/screenshots/python_ui_02_menu_open.png) | ![运行结果截图](docs/screenshots/python_ui_04_demo_visual.png) |

更多截图和详细操作步骤见 [`platform-python/README.md`](platform-python/README.md)。
