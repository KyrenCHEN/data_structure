"""插件空白模板。

用法：把整个 template/ 目录复制到 plugins/ 下面，改个文件夹名字，
再把下面几处 TODO 换成你自己的内容。

注意：这个目录本身不会出现在插件菜单里——只有 plugins/ 目录下的
文件夹才会被自动加载，template/ 不在 plugins/ 里面，就是专门留给
你复制用的。
"""

from plugin_base import Plugin


class MyPlugin(Plugin):
    name = "我的插件"            # TODO：改成你的插件名字，别和同学的重复
    category = "E1"              # TODO：改成对应的实验编号，例如 "E1"
    description = "TODO：写一句话说明输入格式，例如“输入一行用逗号分隔的整数”"

    def example_input(self):
        # TODO：返回一个示例输入，点"填入示例"按钮时会自动填进输入框
        return ""

    def run(self, text, vis):
        # TODO：在这里解析 text、执行你的算法逻辑。
        #
        # 需要可视化的话，三选一（不需要就不用调用）：
        #   vis.draw_array([5, 3, 8, 1])                   数组方格
        #   vis.draw_bars([5, 3, 8, 1])                    柱状图
        #   vis.draw_graph(["A", "B"], [("A", "B")])       图（节点+边）
        #
        # 最后把结果拼成一段文字 return 出去，不要用 print()。
        return "还没有实现"
