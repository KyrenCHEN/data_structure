# 数据结构实验插件平台 —— 学生操作手册

版本对应：`platform-python`、`platform-c`（两版接口语义一致，任选其一完成作业，除非任务另有说明）。

> **不熟悉命令行？** 直接看 [`vscode_setup.md`](vscode_setup.md)——全程只需要点 VSCode 里的按钮（▶ 或 F5），本手册后面的 `python3 main.py` / `make run` 命令都有对应的按钮可以代替手动输入。

## 1. 目录结构

```
platform-python/
  core/plugin_base.py   插件基类 Plugin（一般无需修改）
  core/registry.py      插件注册表（一般无需修改）
  core/loader.py        插件自动发现与加载（一般无需修改）
  ui/app.py             Tkinter 图形界面：顶部菜单栏 + 左侧输入面板 + 中间输出框
  plugins/<你的插件目录>/plugin.py
  main.py               启动入口

platform-c/
  include/plugin.h            插件 ABI 定义
  src/core/plugin_manager.c   dlopen 动态加载核心（一般无需修改）
  src/ui/menu_ui.c            文本菜单 UI
  plugins/<你的插件目录>/xxx.c
  plugins_bin/                编译产物 .so 存放处（自动生成）
  Makefile
```

**你只需要在 `plugins/` 下新建自己的子目录，不要修改 `core/`、`src/core/`、`ui/`、`src/ui/` 中的文件。**

**平台的界面布局（两版都遵循这个思路）：**
- 插件按 `category`（实验编号，如 `E1`、`E2`）分组——Python 版是顶部菜单栏的一个个菜单，C 版是文本菜单里按分类连续排列的一段。
- 选中一个插件后，Python 版左侧会出现说明 + 输入框 + "运行"按钮；C 版直接在终端里继续输入。
- 中间/终端里的输出统一是**纯文本**——平台不解析你的输出格式，你 `return`/`printf` 什么，用户就看到什么。

## 2. 运行平台

> 下面给的是命令行方式。用 VSCode 的同学可以直接跳过命令行，看 [`vscode_setup.md`](vscode_setup.md)：Python 版点▶按钮，C 版按 F5，效果完全一样。

### Python 版
```bash
cd platform-python
python3 main.py
```
要求 Python ≥ 3.10。仅依赖标准库（`tkinter`），无需 `pip install`。若 `tkinter` 缺失，Linux 下用包管理器安装 `python3-tk`。

### C 版
```bash
cd platform-c
make        # 编译核心程序 + 编译 plugins/ 下所有插件为 .so
make run    # 编译并直接运行
```
依赖：`gcc`、`make`，Linux/macOS 下 `dlopen` 为 glibc/libSystem 自带。Windows 必须用 WSL（原生 Windows 没有 `dlopen`）。

## 3. 插件接口规范

### 3.1 Python

平台统一用**纯文本**做输入输出：输入是左侧输入框里的一整段文本（可以手打，也可以点"加载文本文件"从 `.txt` 读入）；输出是 `run()` 返回的一整段文本。

```python
from core.plugin_base import Plugin

class MyPlugin(Plugin):
    name = "我的插件名"      # 菜单里显示的名称，同一平台内不可重复
    category = "E2"          # 实验编号，同一次课的插件放进同一个菜单
    description = "输入一行整数，用逗号分隔，例如 3,1,2"   # 显示在左侧面板里

    def example_input(self):
        return "3,1,2"       # 点"填入示例"按钮时自动填到输入框，方便测试

    def run(self, text):
        arr = [int(x) for x in text.strip().split(",")]
        # ... 你的算法逻辑 ...
        return "结果：" + str(sorted(arr))
```

要点：
- `run(text)` 的 `text` 就是输入框里的全部内容（一个字符串），格式由你自己约定并写在 `description` 里——数组用逗号分隔、矩阵用换行分隔行、树/图用什么记号，都是你说了算，写清楚就行。
- `run()` **必须返回字符串**；不要在插件内部调用 `print()` 展示结果——界面只显示返回值。
- `run()` 内部要对非法输入做基本校验并返回可读的错误信息，**不要让异常直接抛出到平台**（未捕获的异常会被 `ui/app.py` 兜底转成 `[运行出错] ...` 显示，但更好的做法是插件自己判断并给出有意义的提示）。
- `example_input()` 是可选的，写了的话点"填入示例"按钮就能一键测试，强烈建议每个插件都写一个。

### 3.2 C

每个插件是一个独立的编译单元，导出一个函数：

```c
#include <stdio.h>
#include <stdlib.h>
#include "plugin.h"

static void run(void) {
    char line[256];
    printf("请输入一行文本（例如 3,1,2）: ");
    if (!fgets(line, sizeof(line), stdin)) {
        printf("读取输入失败。\n");
        return;
    }
    int n = atoi(line);   // 简单场景下直接转成整数；更复杂的输入自己写解析
    // ... 你的算法逻辑，用 printf 输出 ...
}

static const PluginInfo info = {
    .abi_version = PLUGIN_ABI_VERSION,
    .name = "我的插件名",
    .category = "E2",
    .description = "一句话说明输入格式",
    .run = run,
};

const PluginInfo *plugin_get_info(void) {
    return &info;
}
```

要点：
- 文件放在 `plugins/<你的目录名>/`，`make` 会自动把该目录下所有 `.c` 一起编译为一个 `.so`。
- **统一约定：用 `fgets` 读一整行文本，再自己解析**（转成整数用 `atoi`，转成多个数字可以配合 `strtok`）。不要用 `scanf("%d", ...)`——它读完数字会在输入缓冲区里留一个换行符，容易导致后面的 `getchar`/`fgets` 读到意外内容，对初学者很不友好。
- C 版 UI 是文本菜单，`run()` 里用标准输入输出（`fgets`/`printf`）与用户交互即可，不需要也不应该调用图形库。
- 不要在插件里调用 `exit()`：这会导致整个平台退出，而不仅是当前插件返回。

## 4. 新增插件的步骤（两版通用流程）

1. 在 `plugins/` 下新建目录，命名建议：`算法名_你的学号后四位`，例如 `plugins/kmp_1234/`。
2. Python 版：新建 `plugin.py`，写一个继承 `Plugin` 的类。C 版：新建一个或多个 `.c` 文件，其中之一导出 `plugin_get_info`。
3. 重新启动平台（Python 直接 `python3 main.py`；C 重新 `make`），左侧/菜单应出现你的新插件，无需修改任何核心文件。
4. 用至少 2 组测试数据（含一组边界情况，如空输入、单元素、最大规模）自测。
5. 确认异常输入不会导致平台整体崩溃或卡死。

## 5. 常见问题

- **Python：插件没有出现在列表里** —— 检查目录下文件名是否严格为 `plugin.py`；检查类是否直接继承 `Plugin`（不是继承你自己的中间类）；查看终端启动时打印的 `[loader] 加载插件目录 ... 失败` 报错信息。
- **Python：`name` 重复报错** —— `PluginRegistry.register` 会在插件名冲突时抛异常，给你的插件起一个和示例插件、和同学不会重复的名字。
- **C：`make` 报 `undefined reference to dlopen`** —— 确认 `Makefile` 中 `LDFLAGS = -ldl` 未被删除。
- **C：插件没有出现在菜单里** —— 先看 `make` 输出中是否有编译错误；再看运行时 `[plugin_manager] 加载失败 ...` 的具体报错（多数是 `abi_version` 未设置或 `plugin_get_info` 拼写错误、未加 `extern "C"`风格的正确签名）。
- **两版通用：如何表示数组/矩阵/树/图这类结构化输入** —— 全部用纯文本表示，平台不强制具体格式，但每次实验的任务说明会给出建议格式（如矩阵每行一行、行内数字用逗号分隔；树用带 `#` 占位空节点的层序序列）。同一次实验全班使用统一格式，便于助教用同一份 `.txt` 测试文件批量验收——写插件时把格式约定写进 `description`。
- **Python：想用一个 .txt 文件反复测试怎么办** —— 把测试数据存成 `.txt` 文件（可以参考 `plugins/example_recursion/sample_input.txt`），点左侧的"加载文本文件..."按钮读入，不用每次都手动打字。

## 6. 提交要求

- 提交内容：`plugins/<你的目录>/` 整个目录（不要提交你未修改的 `core/`、`ui/`、`src/` 等平台文件）。
- 文件内保留简要说明（算法思路 1~2 句即可，不要求完整设计文档），复杂度分析（时间/空间）写在插件的 `description`/注释中或单独一行文字说明。
