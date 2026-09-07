# 数据结构实验插件平台 —— 学生操作手册

版本对应：`platform-python`、`platform-c`（两版接口语义一致，任选其一完成作业，除非任务另有说明）。

## 1. 目录结构

```
platform-python/
  core/plugin_base.py   插件基类 Plugin、参数描述 ParamSpec
  core/registry.py      插件注册表（一般无需修改）
  core/loader.py        插件自动发现与加载（一般无需修改）
  ui/app.py             Tkinter 图形界面
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

## 2. 运行平台

### Python 版
```bash
cd platform-python
python3 main.py
```
要求 Python ≥ 3.10（用到了 `list[int]` 等语法）。仅依赖标准库（`tkinter`），无需 `pip install`。若 `tkinter` 缺失，Linux 下用包管理器安装 `python3-tk`。

### C 版
```bash
cd platform-c
make        # 编译核心程序 + 编译 plugins/ 下所有插件为 .so
make run    # 编译并直接运行
```
依赖：`gcc`、`make`，Linux/macOS 下 `dlopen` 为 glibc/libSystem 自带。Windows 建议使用 WSL。

## 3. 插件接口规范

### 3.1 Python

```python
from core.plugin_base import Plugin, ParamSpec

class MyPlugin(Plugin):
    name = "我的插件名"              # UI 中显示的名称，同一平台内不可重复
    category = "E2.1 线性表"          # 建议填实验编号，UI 按此分组
    version = "1.0"

    def params(self) -> list[ParamSpec]:
        return [
            ParamSpec(name="arr", label="整数序列（逗号分隔）", type="str", default="3,1,2"),
        ]

    def run(self, **kwargs) -> str:
        arr = [int(x) for x in kwargs["arr"].split(",")]
        # ... 你的算法逻辑 ...
        return "结果：" + str(sorted(arr))
```

要点：
- `params()` 返回的每一项会在 UI 里自动生成一个输入框，`name` 必须与 `run()` 里读取的 key 一致。
- `type` 目前支持 `"int"`、`"float"`、`"str"`；复杂结构（数组、树、图）一律用 `"str"`，自行在 `run()` 内解析，解析格式由你在插件里约定并写清楚 `help` 字段。
- `run()` **必须返回字符串**；不要在插件内部调用 `print()` 展示结果——UI 只显示返回值。
- `run()` 内部要对非法输入做基本校验并返回可读的错误信息，**不要让异常直接抛出到平台**（未捕获的异常会被 `ui/app.py` 兜底转成 `[运行出错] ...` 显示，但更好的做法是插件自己判断并给出有意义的提示）。

### 3.2 C

每个插件是一个独立的编译单元，导出一个函数：

```c
#include "plugin.h"

static void run(void) {
    int n;
    printf("请输入 n: ");
    if (scanf("%d", &n) != 1) {
        printf("输入无效\n");
        return;
    }
    // ... 你的算法逻辑，用 printf 输出 ...
}

static const PluginInfo info = {
    .abi_version = PLUGIN_ABI_VERSION,
    .name = "我的插件名",
    .category = "E2.1 线性表",
    .description = "一句话说明用法",
    .run = run,
};

const PluginInfo *plugin_get_info(void) {
    return &info;
}
```

要点：
- 文件放在 `plugins/<你的目录名>/`，`make` 会自动把该目录下所有 `.c` 一起编译为一个 `.so`。
- C 版 UI 是文本菜单，`run()` 里用标准输入输出（`scanf`/`printf`）与用户交互即可，不需要也不应该调用图形库。
- `scanf` 后如果后面还有 `getchar()`/`fgets` 混用，注意清空输入缓冲区（参考 `plugins/example_recursion/recursion_plugin.c` 的写法），否则残留换行符会导致下一次读取异常。
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
- **两版通用：如何表示数组/矩阵/树/图这类结构化输入** —— 平台不强制格式，但每次实验的任务说明会给出建议格式（如矩阵用分号分隔行、逗号分隔列；树用带 `#` 占位空节点的层序序列）。同一次实验全班使用统一格式，便于助教用同一组测试数据批量验收。

## 6. 提交要求

- 提交内容：`plugins/<你的目录>/` 整个目录（不要提交你未修改的 `core/`、`ui/`、`src/` 等平台文件）。
- 文件内保留简要说明（算法思路 1~2 句即可，不要求完整设计文档），复杂度分析（时间/空间）写在插件的 `description`/注释中或单独一行文字说明。
