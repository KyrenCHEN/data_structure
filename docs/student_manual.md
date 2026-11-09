# 数据结构实验插件平台 —— 学生操作手册

`platform-python`、`platform-c` 两版接口语义一致，任选其一完成作业，除非任务另有说明。

还没把平台跑起来的话，先看 [`getting_started.md`](getting_started.md)（环境安装 + 第一次运行）。这篇文档假设平台已经能跑了，讲的是怎么写插件。

## 0. 你到底要做什么

平台（菜单栏、加载插件、画布、输出框）已经搭好了，不需要看懂，也不需要改。你要做的只有三步：

1. 复制 `template/` 整个文件夹，粘贴到 `plugins/` 目录下，改个名字。
2. 打开复制出来的文件，把里面的 TODO 换成你自己的算法逻辑。
3. 重新打开平台，菜单里会自动出现你的插件，点开、输入测试数据、运行，看结果对不对。

平台里其余的文件（`main.py`、`app.py`、`plugin_base.py`、`visual.py`，C 版对应 `main.c`、`menu_ui.c`、`plugin_registry.c`、`plugin.h`、`visual.h`）不用打开。

不知道代码应该写成什么样子，可以先看 `plugins/example_insert/`，这是一个比较完整的例子（顺序表插入与删除），照着这个结构写就行。

每次实验的要求是固定的，不设选做题；每次实验对应一个新插件、菜单里的一个新按钮。如果一次实验要求实现 2~3 个算法，这几个算法都写进同一个插件里，用输入的第一行写算法名（比如 `insert`）来区分走哪个分支，具体要求见 `course_design.md`。

## 1. 目录结构

```
platform-python/
  main.py                         启动入口：扫描 plugins/，启动界面
  app.py                          图形界面：顶部菜单栏 + 左侧输入面板 + 中间画布/输出框
  plugin_base.py                  Plugin 基类
  visual.py                       可视化工具
  template/plugin.py              空白模板，复制它去 plugins/ 下新建自己的插件
  plugins/example_insert/plugin.py     完整示例：顺序表插入与删除
  plugins/<你的插件目录>/plugin.py

platform-c/
  main.c                          启动入口
  menu_ui.c                       文本菜单界面
  plugin_registry.c               插件注册表
  plugin.h                        插件接口定义
  visual.h                        可视化工具，直接 #include 使用
  template/plugin_template.c      空白模板，复制它去 plugins/ 下新建自己的插件
  plugins/example_insert/insert_plugin.c       完整示例：顺序表插入与删除
  plugins/<你的插件目录>/xxx.c
  Makefile
```

新增插件、改插件代码后，重新运行一次就行（Python 直接重新运行，C 重新 `make`）。平台是怎么自动发现新插件的，不需要知道也能完成作业；好奇内部原理的看 [`architecture.md`](architecture.md)。

`template/` 目录不会出现在插件菜单里，只有 `plugins/` 目录下的文件夹才会被自动加载——`template/` 专门留给你复制。

界面布局：
- 插件按 `category`（实验编号，如 `E1`、`E2`）分组。Python 版是顶部菜单栏的一个个菜单，C 版是文本菜单里按分类连续排列的一段。
- 选中一个插件后，Python 版左侧出现说明和输入框，中间上方是可视化画布，下方是文字输出；C 版直接在终端里继续输入，可视化和文字结果都打印在终端里。
- 可视化是可选的，不需要画图的插件可以完全不调用。

## 2. 插件接口

### 2.1 Python

平台统一用纯文本做输入：输入框里的一整段文本，可以手打，也可以点"加载文本文件"从 `.txt` 读入。输出是 `run()` 返回的一整段文本，再加上可选的可视化画布。

```python
from plugin_base import Plugin

class MyPlugin(Plugin):
    name = "我的插件名"      # 菜单里显示的名称，同一平台内不可重复
    category = "E2"          # 实验编号，同一次课的插件放进同一个菜单
    description = "输入一行整数，用逗号分隔，例如 3,1,2"   # 显示在左侧面板里

    def example_input(self):
        return "3,1,2"       # 点"填入示例"按钮时自动填到输入框，方便测试

    def run(self, text, vis):
        arr = [int(x) for x in text.strip().split(",")]
        vis.draw_array(arr)              # 可选：把数组画成方格
        # ... 你的算法逻辑 ...
        return "结果：" + str(sorted(arr))
```

要点：
- `text` 是输入框里的全部内容，格式自己定，写在 `description` 里说明清楚就行——数组用逗号分隔、矩阵用换行分隔行、树/图用什么记号都可以，由你决定。
- `vis` 是画布工具，不需要可视化的插件不用管这个参数。
- `run()` 必须返回字符串，不要用 `print()`，界面只显示返回值。
- 对非法输入做基本检查，返回一句说明就行。异常没接住平台也不会崩，会显示成 `[运行出错] ...`，但自己判断、给出清楚的提示更好。
- `example_input()` 建议每个插件都写一个，点"填入示例"就能一键测试。

#### 可视化工具（Python）

`visual.py` 里的 `Visualizer` 只有三个方法，覆盖数据结构课最常见的三种画法：

```python
vis.draw_array([5, 3, 8, 1])                        # 数组方格，适合数组/顺序表/栈/队列
vis.draw_array([5, 3, 8, 1], highlight={0, 2})       # highlight 传下标集合，高亮当前位置

vis.draw_bars([5, 3, 8, 1])                          # 柱状图，适合排序/查找过程

vis.draw_graph(["A", "B", "C"], [("A", "B"), ("B", "C")])   # 图：节点名字列表 + (a, b) 边列表
```

每次调用都会清空画布重画，想展示过程就在算法的关键步骤里多调用几次，比如排序每交换一次就画一次。

### 2.2 C

每个插件是一个独立的 `.c` 文件，和核心代码一起编译成同一个可执行文件：

```c
#include <stdio.h>
#include <stdlib.h>
#include "plugin.h"
#include "visual.h"      // 需要可视化时加上这一行

static void run(void) {
    char line[256];
    printf("请输入一行文本（例如 3,1,2）: ");
    if (!fgets(line, sizeof(line), stdin)) {
        printf("读取输入失败。\n");
        return;
    }
    int n = atoi(line);   // 简单场景直接转成整数，更复杂的输入自己写解析
    // ... 你的算法逻辑，用 printf 输出，vis_draw_* 画图 ...
}

static const PluginInfo info = {
    .name = "我的插件名",
    .category = "E2",
    .description = "一句话说明输入格式",
    .run = run,
};

// __attribute__((constructor)) 让这个函数在 main() 之前自动执行，
// 把插件信息注册进平台，不需要手动调用。
static void __attribute__((constructor)) register_self(void) {
    plugin_register(&info);
}
```

要点：
- 文件放在 `plugins/<你的目录名>/`，`Makefile` 会自动把该目录下所有 `.c` 一起编译进最终的可执行文件，不需要改 `Makefile`。
- 统一用 `fgets` 读一整行文本，再自己解析（转成整数用 `atoi`，转成多个数字配合 `strtok`）。不要用 `scanf("%d", ...)`——它读完数字会在输入缓冲区留一个换行符，容易导致后面的读取出问题。
- C 版 UI 是文本菜单，`run()` 里用 `fgets`/`printf` 和用户交互，不需要图形库。
- 不要在插件里调用 `exit()`，会导致整个平台退出，而不是当前插件返回。
- `register_self` 这个名字随便起，不同插件文件里重名没关系（都是 `static` 函数，只在各自文件内可见）；真正的插件名字是 `info.name`，这个不能和别人重复。

#### 可视化工具（C）

`visual.h` 是 header-only 的，`#include "visual.h"` 就能直接用，不用额外编译或链接：

```c
vis_draw_array(values, n, highlight_index);   // 数组方格；highlight_index 传 -1 表示不高亮
vis_draw_bars(values, n);                     // 横向字符柱状图
vis_draw_graph_edges(edges_a, edges_b, edge_count);  // 图的邻接表文字画法
```

这几个函数直接把结果 `printf` 到终端，用字符画图（方格、`#` 柱子、`--` 连线），不依赖任何图形库。具体用法照抄 `plugins/example_insert/insert_plugin.c` 就行。

## 3. 新增插件的步骤

1. 复制 `template/` 整个目录到 `plugins/` 下面，改个名字，建议带上算法名和学号后四位，例如 `plugins/kmp_1234/`。
2. 把文件里的 TODO 换成你自己的算法逻辑。
3. 重新启动平台（Python 直接 `python3 main.py`；C 重新 `make`），菜单里应该出现你的新插件。
4. 用至少两组测试数据自测，其中一组要是边界情况，比如空输入、单元素、最大规模。
5. 确认异常输入不会导致平台崩溃或卡死。

## 4. 常见问题

**Python：插件没有出现在列表里**
检查目录下文件名是否严格为 `plugin.py`，检查类是否直接继承 `Plugin`。再看终端启动时打印的 `[loader] 加载插件目录 ... 失败` 报错信息。

**Python：`name` 重复报错**
插件名冲突会抛异常，给自己的插件起一个和示例插件、和同学都不重复的名字。

**C：插件没有出现在菜单里**
先看 `make` 输出有没有编译错误（最常见的是结构体字段名拼错）；如果编译通过但菜单里没有，检查插件文件里是不是漏了 `__attribute__((constructor))` 那个注册函数，或者文件没有放在 `plugins/<目录>/` 下面（`template/` 目录本身不会被编译进去）。

**怎么表示数组、矩阵、树、图这类输入**
全部用纯文本表示，平台不强制格式，每次实验的任务说明会给建议格式，比如矩阵每行一行、数字用逗号分隔，树用带占位符的层序序列。全班统一格式，方便用同一份 `.txt` 测试文件验收，写插件时把格式写进 `description`。

**Python：想用一个 .txt 文件反复测试**
把测试数据存成 `.txt`，点左侧的"加载文本文件..."按钮读入，不用每次手动打字。

**我的算法要不要可视化**
不强制。结果是单个数值或一段文字的算法，比如递归求值，直接返回文字就够了；数组、排序、查找、图这类过程比结果更值得看的算法，建议调一次 `vis.draw_array`/`vis.draw_bars`。

**可视化要不要做成动画**
不需要。平台不提供自动播放，每次调用画的都是当前这一帧，想展示过程就在算法关键步骤里多调用几次。

## 5. 提交要求

提交 `plugins/<你的目录>/` 整个目录，不要提交没改过的平台核心文件。文件里保留简要说明，算法思路一两句话即可，复杂度分析写在 `description` 或注释里。
