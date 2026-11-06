# VSCode 环境配置指南（零命令行版）

面向不熟悉命令行的同学：全程只需要点击 VSCode 里的按钮，不需要自己敲编译/运行命令。
仓库里已经放好了 `.vscode/` 配置文件，负责把"编译""运行"这些步骤接到 VSCode 的按钮上。

## 0. 安装 VSCode

前往 https://code.visualstudio.com/ 下载安装（Windows / macOS 均可）。安装完成后打开。

---

## 1. Python 平台配置

### 1.1 安装 Python

- Windows：前往 https://www.python.org/downloads/ 下载安装包，**安装时务必勾选 "Add python.exe to PATH"**。
- macOS：系统自带的 Python 版本可能过旧，建议前往官网下载安装最新版（≥ 3.10）。

### 1.2 打开项目文件夹

在 VSCode 里：`文件（File）→ 打开文件夹（Open Folder）`，选中 `platform-python` 这个文件夹（**注意是这一个子文件夹，不是整个仓库根目录**）。

### 1.3 安装 Python 插件

打开文件夹后，VSCode 右下角通常会弹出提示"是否安装推荐的扩展"，点 **安装（Install）**。
如果没有弹出，手动安装：点击左侧竖排图标中的 **扩展（Extensions，图标像四个方块）**，搜索 `Python`（发布者 Microsoft），点击 **安装**。

### 1.4 选择 Python 解释器

按 `Ctrl+Shift+P`（macOS 是 `Cmd+Shift+P`）打开命令面板，输入 `Python: Select Interpreter`，回车后选择你安装的 Python 版本（版本号 ≥ 3.10）。

### 1.5 运行平台

打开 `main.py` 文件，用以下任意一种方式运行：

- **方式一（最简单）**：点击编辑器右上角的 **▶ 三角形按钮**（"运行 Python 文件"）。
- **方式二**：按 `F5`，如果弹出选择框，选择 **"运行插件平台 (Python)"**。

运行后会弹出一个图形界面窗口，左侧是插件列表，选中一个插件、填好参数、点"运行"即可看到结果。

**常见问题**：如果提示找不到 `tkinter`（Linux 用户较常见），说明系统 Python 没有自带图形库，需要额外安装（例如 Ubuntu 执行 `sudo apt install python3-tk`）。这是安装系统级依赖，不属于插件开发范畴，可以请助教协助。

---

## 2. C 平台配置

插件和核心代码一起编译成一个可执行文件，不涉及任何动态库，Windows / macOS / Linux 装好编译器之后操作完全一样，**不需要 WSL**。

### 2.1 安装编译器

- **Windows**：安装 MinGW-w64。最简单的方式是装 [MSYS2](https://www.msys2.org/)（跟着官网首页步骤装完），打开它自带的终端执行一次：
  ```
  pacman -S mingw-w64-ucrt-x86_64-gcc
  ```
  然后把安装路径下的 `ucrt64\bin` 目录加进系统环境变量 PATH（MSYS2 官网安装步骤最后一步会提示怎么做）。只需要做一次。
- **macOS**：打开终端执行一次 `xcode-select --install`（弹出的安装向导点安装即可）。
- **Linux**：执行一次 `sudo apt install build-essential gdb`（Ubuntu/Debian 系）。

### 2.2 打开项目、运行

1. VSCode 中 `文件 → 打开文件夹`，选中 `platform-c` 文件夹。
2. 安装推荐扩展：右下角提示安装，或手动搜索安装 **C/C++**（发布者 Microsoft）。
3. 按 `F5`：VSCode 会自动先执行"编译平台"任务（等价于 `make`），再启动程序，直接在下方的"终端"面板里看到文本菜单。

### 2.3 运行效果

按 `F5` 后，下方"终端"面板会显示：

```
[main] 已加载 1 个插件

============ 数据结构实验插件平台（C） ============
  [1] 顺序表插入（示例） (E1)
  [0] 退出
请输入编号:
```

在终端里直接输入数字并回车即可与程序交互。

---

## 3. 新增自己的插件后要做什么

两版都一样：写完插件代码后直接重新按 `F5`（或点▶）即可，不需要改任何配置文件。
- Python 版：重新运行时会自动扫描 `plugins/` 下的新目录。
- C 版：会自动重新编译（`Makefile` 会发现 `plugins/` 下新增的目录并一起编译进去），再运行。
