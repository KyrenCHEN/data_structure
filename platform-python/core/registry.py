"""插件注册表：一个全局的"插件仓库"，保存所有已加载的插件实例。
一般不需要修改这个文件。
"""


class PluginRegistry:
    def __init__(self):
        self._plugins = {}   # key: 插件名字, value: 插件实例

    def register(self, plugin):
        key = plugin.name
        if key in self._plugins:
            raise ValueError(f"插件名重复: {key}")
        self._plugins[key] = plugin

    def get(self, name):
        return self._plugins[name]

    def all(self):
        return sorted(self._plugins.values(), key=lambda p: (p.category, p.name))

    def by_category(self):
        # 把插件按 category 分组，方便左侧列表按分类显示
        groups = {}
        for p in self.all():
            groups.setdefault(p.category, []).append(p)
        return groups


registry = PluginRegistry()
