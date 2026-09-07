"""插件接口规范（Python 版）。

写一个插件，只需要：
1. 新建一个类，继承 Plugin；
2. 重写 params()：告诉平台这个插件需要哪些输入框；
3. 重写 run()：写你的算法逻辑，最后 return 一个字符串（会显示在界面上）。
"""


class Param:
    """描述一个输入参数。UI 会根据这个自动生成一个"标签 + 输入框"。"""

    def __init__(self, name, label, default="", param_type="str", help_text=""):
        self.name = name              # 内部名字，要和 run() 里用的 key 一致
        self.label = label            # 显示给用户看的中文名字
        self.default = default        # 输入框里默认填的内容
        self.type = param_type        # 取值范围："int"（整数）/"float"（小数）/"str"（文本）
        self.help_text = help_text    # 一句话提示，显示在输入框旁边


class Plugin:
    """所有插件的基类。写自己的插件时，继承它并重写下面两个方法即可。"""

    name = "未命名插件"       # 会显示在插件列表里，同一平台内不要和别人重名
    category = "未分类"       # 建议写实验编号，例如 "E1.3 递归算法"
    version = "1.0"

    def params(self):
        """返回一个 Param 列表。没有输入参数就返回空列表 []。"""
        return []

    def run(self, **kwargs):
        """执行插件的核心逻辑。kwargs 的 key 就是 params() 里每个 Param 的 name。"""
        return "这个插件还没有实现 run() 方法"

    def describe(self):
        return f"[{self.category}] {self.name} v{self.version}"
